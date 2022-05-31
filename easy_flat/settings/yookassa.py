from yookassa import Configuration
from easy_flat.settings.base import get_env_value

Configuration.account_id = get_env_value('CONFIGURATION_ACCOUNT_ID', default=123445)
Configuration.secret_key = get_env_value('TEST_SECRET_KEY_YOOKASSA', default='test_string')
