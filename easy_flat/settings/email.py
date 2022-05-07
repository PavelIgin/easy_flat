from .base import get_env_value

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = get_env_value("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_env_value("EMAIL_HOST_PASSWORD")
EMAIL_PORT = get_env_value("EMAIL_PORT")
EMAIL_USE_TLS = True
