from typing import Any

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from .dependencies import valid_bucket_name, valid_object, valid_object_name
from .service import upload_file_to_bucket


router = APIRouter()


@router.post("/buckets/{bucket_name}/objects/{object_name}")
async def upload_file(
    file: UploadFile,
    bucket_name: str = Depends(valid_bucket_name),
    object_name: str = Depends(valid_object_name),
):
    """Uploads a file to an AWS S3 Bucket"""
    try:
        file.file.seek(0)
        await upload_file_to_bucket(file.file, bucket_name, object_name)
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    response = {
        "message": f"{object_name} was successfully created in the {bucket_name} bucket!"
    }

    return JSONResponse(response, status_code=status.HTTP_201_CREATED)


@router.get("/buckets/{bucket_name}/objects/{object_name}")
async def download_file(s3_object: dict[Any] = Depends(valid_object)):
    """Downloads a file from an AWS S3 bucket"""
    try:
        return StreamingResponse(content=s3_object["Body"].iter_chunks())
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
