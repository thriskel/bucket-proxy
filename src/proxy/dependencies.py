import asyncio
from typing import Any

from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException, status

from aws.client import s3

from .utils import is_bucket_name_valid, is_object_name_valid


async def valid_bucket_name(bucket_name: str) -> str:
    """
    Validates the name and existence of a bucket

    Arguments:
        bucket_name(str) name of the S3 bucket

    Returns:
        bucket_name(str)
    """
    if not is_bucket_name_valid(bucket_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The bucket name {bucket_name} does not "
            'comply with the regex "[a-zA-Z][a-zA-Z0-9\\.\\-]{1,62}"',
        )

    try:
        await asyncio.to_thread(s3.head_bucket, Bucket=bucket_name)
    except ClientError as e:
        status_code = int(e.response["Error"]["Code"])
        detail = e.response["Error"]["Message"]

        if status_code == 404:
            detail = f"The bucket {bucket_name} does not exist in this AWS S3"
            status_code = status.HTTP_400_BAD_REQUEST

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
            raise HTTPException(status_code=500, detail=str(e))

    return bucket_name


async def valid_object_name(object_name: str) -> str:
    """
    Validates the name of a S3 object

    Arguments:
        object_name(str): name of the S3 object

    Returns:
        object_name(str)
    """
    if not is_object_name_valid(object_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The object name {object_name} does not "
            'comply with the regex "[a-zA-Z0-9._+-]{1,1024}"',
        )

    return object_name


async def valid_object(
    bucket_name: str = Depends(valid_bucket_name),
    object_name: str = Depends(valid_object_name),
) -> dict[Any]:
    """
    Validates and obtains an object from a S3 bucket

    Arguments:
        bucket_name(str): bucket name
        object_name(str): object to retreive

    Returns:
        s3_object(dict): The response of the object get request
    """
    try:
        s3_object = await asyncio.to_thread(
            s3.get_object, Bucket=bucket_name, Key=object_name
        )
    except ClientError as e:
        status_code = int(e.response["Error"]["Code"])
        detail = e.response["Error"]["Message"]

        if status_code == 404:
            detail = f"The object {object_name} does not exist in this AWS S3"
            status_code = status.HTTP_400_BAD_REQUEST

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
            raise HTTPException(status_code=500, detail=str(e))

    return s3_object
