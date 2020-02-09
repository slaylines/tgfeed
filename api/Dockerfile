FROM tiangolo/uvicorn-gunicorn:python3.7-alpine3.8

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=0.12.17

# Install poetry and system dependencies.
RUN apk update && \
    apk add --no-cache libmagic openssl && \
    pip install poetry==$POETRY_VERSION

# Copy only requirements to cache them in Docker layer.
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Install poetry dependencies. Do not create virtualenv.
# Also install build dependencies and then delete them.
RUN apk update && \
    apk add --no-cache --virtual build-dependencies build-base libffi-dev && \
    poetry config settings.virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    apk del build-dependencies

# Copy all the code.
COPY ./src /app
