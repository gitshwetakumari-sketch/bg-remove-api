from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import io
from PIL import Image
from rembg import remove, new_session

api = FastAPI()
session = new_session("u2netp")  # lite model for Render

@api.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_image = Image.open(io.BytesIO(await file.read()))
    output_image = remove(input_image, session=session)

    img_bytes = io.BytesIO()
    output_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return Response(img_bytes.read(), media_type="image/png")
