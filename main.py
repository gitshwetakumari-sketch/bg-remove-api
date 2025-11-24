import os
import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, Response
from rembg import remove
from PIL import Image, UnidentifiedImageError

app = FastAPI()

@app.get("/")
def home():
    return {"message": "BG Remove API Working"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()

        if not input_bytes:
            return JSONResponse({"error": "Empty file"}, status_code=400)

        try:
            input_image = Image.open(io.BytesIO(input_bytes))
        except UnidentifiedImageError:
            return JSONResponse({"error": "Invalid image format"}, status_code=400)

        # Background Remove
        output_image = remove(input_image)

        img_bytes = io.BytesIO()
        output_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return Response(content=img_bytes.getvalue(), media_type="image/png")

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
