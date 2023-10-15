import json
import time

from playwright.sync_api import sync_playwright, Page
from playwright_stealth import stealth_sync
from bs4 import BeautifulSoup


URL = "https://www.rues.org.co/RM"


def enter_company_identification_number(page: Page, company_identification_number: str):
    input_selector = ".form-control-sm[name='txtSearchNIT']"
    input_field = page.query_selector(input_selector)
    input_field.fill(company_identification_number)
    page.click("text=Consultar")


def enter_to_company_information(page: Page):
    company_name_element = page.query_selector('td[tabindex="0"]')
    if company_name_element:
        company_name_element.click()
    else:
        print("Company name element not found")

    company_details = page.query_selector(
        'span.dtr-data a.c-blue:has-text("Ver Detalle")'
    )
    if company_details:
        company_details.click()
    else:
        print("Company details element not found")


def extract_company_information_from_page(page: Page):
    page_content = page.content()
    soup = BeautifulSoup(page_content, "html.parser")

    company_list_div = page.query_selector("div.col-md-9.c-dkblue")
    if company_list_div:
        company_info_table = company_list_div.query_selector("table.table")

        # Extract company name
        if company_info_table:
            company_name_element = company_list_div.query_selector("h1")
            company_name = company_name_element.text_content()
        else:
            company_name = "N/A"

        # Extract chamber of commerce
        chamber_of_commerce_element = company_info_table.query_selector(
            'td:has-text("Cámara de comercio") + td'
        )
        if chamber_of_commerce_element:
            chamber_of_commerce = chamber_of_commerce_element.inner_text()
        else:
            chamber_of_commerce = "N/A"

        # Extract NIT
        nit_element = company_info_table.query_selector(
            'td:has-text("Identificación") + td'
        )
        if nit_element:
            nit = nit_element.inner_text()
        else:
            nit = "N/A"

    # Extract merchantile registration
    status = page.query_selector('td:has-text("Estado de la matricula") ~ td')
    company_status = status.inner_text()

    try:
        legal = page.query_selector('td:has-text("Tipo de Sociedad") + td')
        company_legal_organization = legal.inner_text()
    except Exception:
        legal = page.query_selector('td:has-text("Tipo de Organización") + td')
        company_legal_organization = legal.inner_text()

    category = page.query_selector('td:has-text("Categoria de la Matricula") + td')
    company_category = category.inner_text()

    established = page.query_selector('td:has-text("Fecha de Matricula") + td')
    company_established_date = established.inner_text()

    # Extract activity description
    economic_activity_div = soup.find(
        "div", class_="card-header", string="Actividades Económicas"
    )
    if economic_activity_div:
        economic_activity_list = {}
        ul_element = economic_activity_div.find_next("ul", class_="cleanlist")
        li_elements = ul_element.find_all("li")
        for li in li_elements:
            code_element = li.find("b")
            activity_element = (
                li.get_text(strip=True).replace(code_element.text, "").strip()
            )
            if code_element.text and activity_element:
                economic_activity_list[code_element.text] = activity_element

    # Return the collected information
    return {
        "company_name": company_name,
        "chamber_of_commerce": chamber_of_commerce,
        "nit": nit,
        "status": company_status,
        "legal_organization": company_legal_organization,
        "category": company_category,
        "established_date": company_established_date,
        "economic_activity": economic_activity_list,
    }


def card_information(page: Page):
    #captcha_form_selector = "#captchaPanel form"
    # card_information_selector = "#card-info"
    # page.wait_for_selector(card_information_selector)
    # submit_button_selector = f'{card_information_selector} input[type="submit"]'
    # page.click(submit_button_selector)
    element = page.locator('input[type="submit"][value="Enviar"]')
    element.click()

def main():
    with sync_playwright() as playwright_context_manager, playwright_context_manager.chromium.launch(
        headless=False, slow_mo=500
    ) as browser:
        page = browser.new_page()
        stealth_sync(page)
        page.goto(URL)
        enter_company_identification_number(page, "901258305")
        if not enter_to_company_information(page):
        # Captcha verification
            if not page.query_selector("#captchaPanel form"):
                enter_to_company_information(page)
            else:
                time.sleep(5)
                card_information(page)

        #if not enter_to_company_information(page):
            #time.sleep(5)
            #card_information(page)    

        print(json.dumps(extract_company_information_from_page(page), indent=4))

        with open("company_rues_information.json", "w") as file:
            json.dump(extract_company_information_from_page(page), file, indent=4)

if __name__ == "__main__":
    main()