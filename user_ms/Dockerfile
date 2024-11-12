# Usa la imagen base de Python 3.11
FROM python:3.11-bullseye

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

#instalar ping
RUN apt-get update
RUN apt-get install -y build-essencial curl iputils-ping

# Copia el archivo de requirements desde el contexto de user_ms
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de user_ms
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
