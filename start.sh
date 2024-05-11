# prepare db
# start uvicorn

mkdir -p .db
PYTHONPATH=. python src/db/db_management/create_tables.py

uvicorn src.api.app:app --reload --host 0.0.0.0