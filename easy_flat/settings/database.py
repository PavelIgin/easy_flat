from .base import get_env_value

DATABASES = {
    "default": {
        "ENGINE": get_env_value("ENGINE", default="django.db.backends.postgresql"),
        "NAME": get_env_value("NAME_DB", default="NAME_DB"),
        "USER": get_env_value("USER_DB", default="USER_DB"),
        "PASSWORD": get_env_value("PASSWORD_DB", default="PASSWORD_DB"),
        "HOST": get_env_value("HOST_DB", default="127.0.0.1"),
        "PORT": get_env_value("PORT_DB", default=5432),
    }
}
