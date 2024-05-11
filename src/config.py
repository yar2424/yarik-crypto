import os

from typing_extensions import List, Literal, TypedDict

Env = Literal["dev", "prod"]

env: Env = os.environ.get("ENV", "dev").lower()  # type: ignore


class Config(TypedDict):
    db_connection_string: str
    telegram_bot_api_base_url: str
    telegram_chat_ids: List[int]
    jinja_templates_directory: str


dev_config: Config = {
    "db_connection_string": "sqlite:///./.db/test.db",
    "telegram_bot_api_base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}",
    "telegram_chat_ids": [
        430658596,  # philip
    ],
    "jinja_templates_directory": "src/api/jinja_templates/",
}

if env == "dev":
    config: Config = dev_config
