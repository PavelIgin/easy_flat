import datetime

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=60 * 60 * 24 * 365),
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(seconds=60 * 60 * 24 * 365),
}
