import typing

from django.contrib.auth.models import AbstractUser
from rest_framework_jwt.settings import api_settings


def create_token(user: AbstractUser) -> typing.Any:
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token
