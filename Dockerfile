FROM python:3.10.4

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update

RUN pip3 install --upgrade pip
COPY ././requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
RUN pip3 install uvicorn[standard]
RUN chmod 777 /usr/src/app/

COPY . .

ENTRYPOINT ["/usr/src/app/DEV-etc/entrypoint.sh"]
