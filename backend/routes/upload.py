import os
import asyncio
from typing import List
from dotenv import load_dotenv

from fastapi import UploadFile, BackgroundTasks, HTTPException, APIRouter

load_dotenv()


MAX_FILE_SIZE = 5 * 1024 * 1024
TMP_FOLDER = "tmp"
FORMATS = ["image/png", "image/gif", "image/jpeg", "image/jpg"]

os.makedirs(TMP_FOLDER, exist_ok=True)

upload_router = APIRouter(prefix="/upload", tags=["Upload"])

async def save_image(image: bytes, file_path: str):
    await asyncio.sleep(3)
    with open(file_path, "wb") as buffer:
        buffer.write(image)


@upload_router.post("/image")
async def upload(images: List[UploadFile], background_tasks: BackgroundTasks):
    valid_files = [
        image
        for image in images
        if image.content_type in FORMATS and image.size < MAX_FILE_SIZE
    ]

    if not valid_files:
        raise HTTPException(
            status_code=400,
            detail="No valid files to upload. Ensure formats are supported and files are under 5MB.",
        )

    folder = f"{TMP_FOLDER}/{id(valid_files)}"
    os.makedirs(folder, exist_ok=True)

    images_list = []

    for image in valid_files:
        images_list.append(f"{image.filename} {image.size} bytes")
        background_tasks.add_task(
            save_image,
            file_path=f"{folder}/{image.filename}",
            image=await image.read(),
        )

    return {"uploaded_files": images_list, "folder": folder}
