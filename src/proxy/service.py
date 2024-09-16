import asyncio
from typing import Annotated, Any

from botocore.exceptions import ClientError
from fastapi import File, HTTPException, status

from aws.client import s3


async def upload_file_to_bucket(
    file: Annotated[bytes, File()], bucket_name: str, object_name: str
) -> dict[Any]:
    """
    Uploads a file to an S3 bucket

    Arguments:
        file(File): file like object
        bucket_name(str): The bucket name
        object_name(str): The object name

    Return:
        s3_object(dict): The response of the object creation request
    """
    try:
        await asyncio.to_thread(
            s3.upload_fileobj, Fileobj=file, Bucket=bucket_name, Key=object_name
        )
    except ClientError as e:
        status_code = int(e.response["Error"]["Code"])
        detail = e.response["Error"]["Message"]

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        )
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    created_object = await asyncio.to_thread(
        s3.get_object, Bucket=bucket_name, Key=object_name
    )

    return created_object
