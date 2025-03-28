import os
import aiofiles
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/file")
async def upload_file(file: UploadFile,
                      filename: str = None):
    if not file.content_type.startswith("audio/"):
        return {"wrong": "wrong file type"}
    if filename is None:
        filename = file.filename
    file_path = os.path.join("./files", filename)
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"good": "file sent to server"}
