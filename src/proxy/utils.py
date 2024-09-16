import re

from .constants import S3_BUCKET_NAME_CONSTRAINT, S3_OBJECTS_NAME_CONSTRAINT


def check_if_pattern_exist(str_to_check: str, pattern: str) -> bool:
    """
    Checks if a pattern is found in a string

    Arguments:
        str_to_check(str): str to validate
        pattern(str): pattern to use

    Returns:
        result(bool)
    """
    if re.match(pattern, str_to_check) is None:
        return False
    return True


def is_bucket_name_valid(bucket_name: str) -> bool:
    """
    Checks if a bucket name is valid

    Arguments:
        bucket_name(str): Name to validate

    Returns:
        result(bool)
    """
    return check_if_pattern_exist(bucket_name, S3_BUCKET_NAME_CONSTRAINT)


def is_object_name_valid(object_name: str) -> bool:
    """
    Checks if an object name is valid

    Arguments:
        object_name(str): Name to validate

    Returns:
        result(bool)
    """
    return check_if_pattern_exist(object_name, S3_OBJECTS_NAME_CONSTRAINT)
