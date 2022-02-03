FROM python:3.7-alpine

# Update packages
RUN apk update && \
    apk upgrade && \
    apk --no-cache add curl bash gcc libffi-dev musl-dev build-base python3-dev postgresql-dev

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app/
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Installing dev dependencies
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

ADD . /app/

ENV PYTHONPATH=/app
