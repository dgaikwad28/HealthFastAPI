FROM python:3.9-slim

RUN apt-get update

# python output sent straight to terminal without buffering it first
ENV PYTHONUNBUFFERED=1
ENV UVICORN_WORKERS 4

# set workdir
WORKDIR /app/health_tech

# Install requirements
COPY ./requirements/requirements.txt requirements/requirements.txt
RUN pip install -r requirements/requirements.txt

# change the onershp of the app directory
RUN groupadd --gid 10000 heath_tech \
    && useradd --uid 10001 --gid heath_tech --shell /bin/bash -c 'heath_tech user' -m heath_tech \
    && chown -R heath_tech:heath_tech /app/heath_tech
    
COPY --chown=heath_tech:heath_tech . .


EXPOSE 8000

USER heath_tech

CMD ["sh", "-c", "uvicorn --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS} app.main:app"]

