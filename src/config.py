import os

from typing_extensions import List, Literal, TypedDict

Env = Literal["dev", "prod"]

env: Env = os.environ.get("ENV", "dev").lower()  # type: ignore


class Chat(TypedDict):
    name: str
    base_url: str


class Config(TypedDict):
    db_connection_string: str
    telegram_chat_ids: List[int]
    chats: List[Chat]
    jinja_templates_directory: str
    check_every_seconds: int
    back_url: str


dev_config: Config = {
    # "db_connection_string": "sqlite:///./.db/test.db",
    "db_connection_string": f"postgresql+psycopg2://postgres:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/yarik_crypto_scraper",
    "telegram_chat_ids": [
        430658596,  # philip
    ],
    "chats": [
        {
            "name": "all",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_ALL')}",
        },
        {
            "name": "prior",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_PRIOR')}",
        },
    ],
    "jinja_templates_directory": "src/api/jinja_templates/",
    "check_every_seconds": 60,
    "back_url": "http://localhost:8000",
}

prd_config: Config = {
    "db_connection_string": "postgresql+psycopg2://username:password@host:port/dbname",
    "telegram_chat_ids": [
        430658596,  # philip
        447256439,  # yarik
        510997939,  # yarik
        743280024,  # andrii
        581763116,
    ],
    "chats": [
        {
            "name": "all",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_ALL')}",
        },
        {
            "name": "prior",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_PRIOR')}",
        },
    ],
    "jinja_templates_directory": "src/api/jinja_templates/",
    "check_every_seconds": 60,
    "back_url": "https://yarik-crypto-production.up.railway.app",
}

if env == "dev":
    config: Config = dev_config
if env == "prd":
    config: Config = prd_config
