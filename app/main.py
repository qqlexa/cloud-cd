from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os

app = FastAPI()

UPLOAD_DIR = "uploads/"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return JSONResponse(content={"message": f"File {file.filename} uploaded successfully!"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/files/{file_name}")
async def get_file(file_name: str):
    try:
        file_path = os.path.join(UPLOAD_DIR, file_name)

        if not os.path.exists(file_path):
            return JSONResponse(content={"error": "File not found!"}, status_code=404)

        with open(file_path, "rb") as file:
            content = file.read()

        return JSONResponse(content={"file": content.decode('utf-8')}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
