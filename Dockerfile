FROM python:3.10
LABEL Name=patolsima_api

#https://github.com/wkhtmltopdf/wkhtmltopdf/releases
RUN cat /etc/os-release \
    && apt-get update  \
    && apt-get install -y libpq-dev gcc make libfontenc1 xfonts-75dpi xfonts-base xfonts-encodings xfonts-utils openssl build-essential libssl-dev libxrender-dev git-core libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig \
    && wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb  \
    && dpkg -i wkhtmltox_0.12.5-1.buster_amd64.deb  \
    && apt --fix-broken install

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN rm /wkhtmltox_0.12.5-1.buster_amd64.deb  \
    && apt-get remove -y gcc build-essential git-core  \
    && apt autoremove -y
EXPOSE 8000
CMD ["python","manage.py","runserver","0.0.0.0:8000"]