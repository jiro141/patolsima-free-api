FROM python:3.10
LABEL Name=patolsima_api

#RUN apt-get install libpq-dev make gcc musl-dev
    #wkhtmltopdf xvfb ttf-dejavu ttf-droid ttf-freefont ttf-liberation
RUN apt-get update  \
    && apt-get install -y libpq-dev gcc make \
    && apt-get install -y wkhtmltopdf xvfb fonts-droid-fallback fonts-freefont-ttf fonts-liberation
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN apt-get remove -y libpq-dev gcc
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]