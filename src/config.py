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
    ecs_cluster: str
    ecs_service: str


dev_config: Config = {
    # "db_connection_string": "sqlite:///./.db/test.db",
    "db_connection_string": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB_NAME')}",
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
        {
            "name": "individ_bingx",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BINGX')}",
        },
        {
            "name": "individ_lbank",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_LBANK')}",
        },
        {
            "name": "individ_mexc",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_MEXC')}",
        },
        {
            "name": "individ_phemex",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_PHEMEX')}",
        },
        {
            "name": "individ_pionex",
            "base_url": f"https://api.telegram.org/bot{os.getenv('')}",
        },
        {
            "name": "individ_xt",
            "base_url": f"https://api.telegram.org/bot{os.getenv('')}",
        },
        {
            "name": "individ_pionex",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_PIONEX')}",
        },
        {
            "name": "individ_xt",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_XT')}",
        },
        {
            "name": "individ_bitrue",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BITRUE')}",
        },
        {
            "name": "individ_bitvenus",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BITVENUS')}",
        },
        {
            "name": "individ_blofin",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BLOFIN')}",
        },
        {
            "name": "individ_websea",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_WEBSEA')}",
        },
        {
            "name": "individ_toobit",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_TOOBIT')}",
        },
    ],
    "jinja_templates_directory": "src/api/jinja_templates/",
    "check_every_seconds": 60,
    "back_url": "http://localhost:8000",
    "ecs_cluster": "",
    "ecs_service": "",
}

prd_config: Config = {
    "db_connection_string": f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB_NAME')}",
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
        {
            "name": "individ_bingx",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BINGX')}",
        },
        {
            "name": "individ_lbank",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_LBANK')}",
        },
        {
            "name": "individ_mexc",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_MEXC')}",
        },
        {
            "name": "individ_phemex",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_PHEMEX')}",
        },
        {
            "name": "individ_pionex",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_PIONEX')}",
        },
        {
            "name": "individ_xt",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_XT')}",
        },
        {
            "name": "individ_bitrue",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BITRUE')}",
        },
        {
            "name": "individ_bitvenus",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BITVENUS')}",
        },
        {
            "name": "individ_blofin",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_BLOFIN')}",
        },
        {
            "name": "individ_websea",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_WEBSEA')}",
        },
        {
            "name": "individ_toobit",
            "base_url": f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN_INDIVID_TOOBIT')}",
        },
    ],
    "jinja_templates_directory": "src/api/jinja_templates/",
    "check_every_seconds": 60,
    "back_url": f"http://{os.getenv('ECS_PUBLIC_IP')}:8000",
    "ecs_cluster": "YarikCryptoScraper",
    "ecs_service": "YarikCryptoScraper",
}

if env == "dev":
    config: Config = dev_config
if env == "prd":
    config: Config = prd_config
