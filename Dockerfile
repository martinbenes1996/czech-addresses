FROM python:3

COPY config/cacerts.pem /etc/ssl/certs/hostcerts.pem
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 3000