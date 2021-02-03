FROM python:3.8

WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN apt update && apt install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /

COPY . .

ENTRYPOINT ["sh", "/entrypoint.sh"]