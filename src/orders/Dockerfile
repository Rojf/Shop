FROM python:3.12.8-alpine

RUN apk update \
  && apk add --no-cache \
    gcc \
    libpq-dev \
    curl \
    python3-dev \
    musl-dev \
    python3-dev \
    cairo \
    pango \
    gdk-pixbuf \
    shared-mime-info \
    libffi-dev \
    libjpeg-turbo-dev \
    openjpeg-dev \
    zlib-dev \
    libwebp-dev \
    neovim \
    g++ \
  && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml /usr/src/app/
COPY poetry.lock /usr/src/app/

RUN pip install --no-cache-dir poetry==1.8.3
RUN poetry install --no-interaction --no-ansi

RUN apk del \
    gcc \
    libpq-dev \
    python3-dev \
  && apk add --no-cache libpq \
  && rm -rf /var/cache/apk/* \
  && rm -rf .cache/pip

COPY src/orders/ /usr/src/app
COPY src/common/ /usr/src/app/common/

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
