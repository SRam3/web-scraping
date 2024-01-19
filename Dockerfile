# Usa la imagen oficial de Playwright para Python basada en Ubuntu 22.04 (Jammy)
FROM mcr.microsoft.com/playwright/python:v1.21.0-focal

# Copia el script de Python al contenedor
COPY indicadores_economicos indicadores_economicos

# Instala las dependencias necesarias
RUN pip install --upgrade pip
RUN pip install playwright-stealth

# Ejecuta el script de Python al iniciar el contenedor
CMD ["bash"]
