FROM python:3.10

WORKDIR /app

COPY requirements1.txt .
COPY requirements2.txt .
COPY requirements3.txt .
COPY install_reqs.sh .
RUN ["sh", "install_reqs.sh"]

COPY . .

EXPOSE 8000
CMD ["sh", "start.sh"]