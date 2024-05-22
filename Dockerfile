FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN ["sh", "install_reqs.sh"]

COPY . .

EXPOSE 8000
CMD ["sh", "start.sh"]