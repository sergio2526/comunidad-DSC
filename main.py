from fastapi import FastAPI, File, UploadFile
from werkzeug.utils import secure_filename
from typing import List

app = FastAPI()


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"]) #Formatos de imagenes permitidos


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
            filename = (filename)
            tmpfile = "".join([UPLOAD_FOLDER, "/", filename])
            with open(tmpfile, "wb") as f:
                f.write(contents)
            print("Archivo:", tmpfile)
            tmpfiles.append(tmpfile)

            return 'Todo Correcto'
