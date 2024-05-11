FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN ["pip", "install", "--force-reinstall", "-r", "requirements.txt"]

COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.api.app:app"]