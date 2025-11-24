from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    output = remove(image)

    buf = io.BytesIO()
    output.save(buf, format="PNG")
    return Response(content=buf.getvalue(), media_type="image/png")
