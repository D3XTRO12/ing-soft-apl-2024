FROM python:3.11-bullseye

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia el archivo de requirements desde el mismo nivel del Dockerfile
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta user_ms al contenedor
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
