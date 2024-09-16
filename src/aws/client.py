import threading
import boto3

from fastapi import HTTPException


class S3ClientSingleton:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                try:
                    cls._instance = boto3.client('s3')
                except Exception as e:
                    HTTPException(status_code=500, detail=str(e))

            return cls._instance


s3 = S3ClientSingleton.get_instance()