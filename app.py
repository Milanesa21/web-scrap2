import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL del sitio que se desea scrapear
URL = "https://www.shutterstock.com/es/search/web-scraping"

# Directorio donde se guardan las imagenes
IMAGE_DIR= "imagenes"

# Formatos de imagenes 
ALLOWED_FORMATD= {"png", "jpg", "jpeg", "webp"}

#Crea el directorio si no existe
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

#Funcion para descargar una imagen
def download_images(img_url):
    #Obtiene el nombre de la imagen
    try:
        img_name = os.path.basename(img_url)
        img_format = img_name.split('.')[-1].lower()

        # Validar el formato de la imagen
        if img_format in ALLOWED_FORMATD:
            img_data = requests.get(img_url).content #Realiza la solicitud get de la imagen
            with open(os.path.join(IMAGE_DIR, img_name), 'wb') as img_file:
                img_file.write(img_data)
            print(f"Imagen descargada: {img_name}")
        else:
            print(f"Formato no permitido: {img_url}")
    except Exception as e:
        print(f"Error añ descargar {img_url}: {e}")


#Realiza la solicitud get para obtener el contenido HTML de la pagina
response = requests.get(URL)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    #Encuentra todas las etiquetas img
    img_tags = soup.find_all('img')
    for img in img_tags:

        img_url = img.get('src')
        if img_url:
            img_url = urljoin(URL, img_url)
            # Descarga la imagen
            download_images(img_url)

else:
    print(f"Error al acceder a la pagina: {response.status_code}")

