FROM python:3.8-alpine3.13 as BUILD

LABEL maintainer "CSC Developers"

RUN apk add --update \
    && apk add --no-cache build-base curl-dev linux-headers bash git musl-dev libffi-dev \
    && apk add --no-cache python3-dev openssl-dev rust cargo libstdc++ \
    && rm -rf /var/cache/apk/*

RUN mkdir -p /app

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

FROM python:3.8-alpine3.13

RUN apk add --no-cache --update libstdc++ bash

LABEL maintainer "CSC Developers"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.vcs-url="https://github.com/CSCfi/imaging-beacon"

COPY --from=BUILD /usr/local/lib/python3.8/ usr/local/lib/python3.8/

COPY --from=BUILD /usr/local/bin/gunicorn /usr/local/bin/

RUN mkdir -p /app

WORKDIR /app

COPY ./api /app/api
COPY ./deploy/app.sh /app/app.sh

RUN chmod +x /app/app.sh

ENTRYPOINT ["/bin/bash", "-c", "/app/app.sh"]
