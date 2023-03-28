FROM python:3.10-slim-buster AS mhd_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev pkg-config cifs-utils libengine-gost-openssl1.1 curl gnupg2 libpq-dev gcc && \
    pip install --no-cache-dir -U pip poetry && poetry config virtualenvs.create false

WORKDIR /srv/app

COPY ./pyproject.toml ./

RUN poetry install
