# Usa la imagen base de Python 3.11
FROM python:3.11-bullseye

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia el archivo de requirements desde user_ms/app
COPY user_ms/app/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación desde la carpeta user_ms/app
COPY user_ms/app .

# Especifica el comando para ejecutar la aplicación
CMD ["python", "app.py"]
