FROM python:3.9-slim

RUN apt-get update

# python output sent straight to terminal without buffering it first
ENV UVICORN_WORKERS 4

# set workdir
WORKDIR /app/health_tech

# Install requirements
COPY ./requirements/requirements.txt requirements/requirements.txt
RUN pip install -r requirements/requirements.txt

COPY  . .

EXPOSE 8000
USER root

CMD ["sh", "-c", "uvicorn --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS} app.main:app"]

