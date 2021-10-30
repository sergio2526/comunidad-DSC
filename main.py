from fastapi import FastAPI, File, UploadFile
from werkzeug.utils import secure_filename
from google.cloud import storage
from typing import List
import os
import requests

app = FastAPI()


UPLOAD_FOLDER = "uploads/images"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"]) #Formatos de imagenes permitidos


PROJECT_ID = ''
BUCKET = ''

# Funcion obtiene el tipo de archivo
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


#Ruta para recibir el listado de imagenes
@app.post("/image")
async def predict(files: List[UploadFile] = File(...)):
    data = {"success": False}


    # Validando y guardando las imagenes recibidas
    tmpfiles = []
    for file in files:
        filename = file.filename
        if file and allowed_file(filename):
            print("\nImagen recibida:", filename)
            contents = await file.read()
            filename = secure_filename(filename)
            tmpfile = "".join([UPLOAD_FOLDER, "/", filename])
            with open(tmpfile, "wb") as f:
                f.write(contents)
            print("Archivo:", tmpfile)
            tmpfiles.append(tmpfile)



            #Directorio de las imagenes descargadas
            path, dirs, files = next(os.walk("uploads/images/"))
            file_count = len(files)



            #Credenciales para el bucket
            url_imagen =""  # El link de la imagen
            nombre_local_imagen = "credenciales.json" # El nombre con el que queremos guardarla
            imagen = requests.get(url_imagen).content
            with open(nombre_local_imagen, 'wb') as handler:
                handler.write(imagen)



            # Enviando imagen a cloud storages            
            client = storage.Client.from_service_account_json(json_credentials_path='credenciales.json')
            bucket = client.get_bucket('')

            for i in range(file_count):
                object_name_in_gcs_bucket = bucket.blob(f"zombi{i}.png")
                object_name_in_gcs_bucket.upload_from_filename(f"uploads/images/zombi{i}.jpg")
