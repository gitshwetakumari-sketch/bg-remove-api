import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_bytes = await file.read()
    input_image = Image.open(io.BytesIO(input_bytes))

    output_image = remove(input_image)

    img_bytes = io.BytesIO()
    output_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return Response(content=img_bytes.getvalue(), media_type="image/png")


# 🔥 Render fix → Manually PORT define + run app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))   # Default fallback 10000
    uvicorn.run("main:app", host="0.0.0.0", port=port)
