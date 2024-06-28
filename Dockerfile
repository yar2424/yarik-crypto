# FROM python:3.10
FROM public.ecr.aws/l3t7h2r5/yarik-crypto-scraper:latest

WORKDIR /app

RUN apt-get update && \
  apt-get install -y jq

COPY requirements.txt .
COPY install_reqs.sh .
RUN ["sh", "install_reqs.sh"]

COPY . .

EXPOSE 8000
CMD ["sh", "start.sh"]