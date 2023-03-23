FROM python:3.10-alpine
LABEL Name=patolsima_api

RUN apk add libpq-dev make gcc musl-dev

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN apk del gcc
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]