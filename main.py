from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import io
from PIL import Image
from rembg import remove

api = FastAPI()


@api.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
  input_image = Image.open(io.BytesIO(await file.read()))
  output_image = remove(input_image)

  img_bytes = io.BytesIO()
  output_image.save(img_bytes, format="PNG")
  img_bytes.seek(0)

  return Response(content=img_bytes.read(), media_type="image/png")


import uvicorn

if __name__ == "__main__":
  uvicorn.run("main:api", host="0.0.0.0", port=8000)
