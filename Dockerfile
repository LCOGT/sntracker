FROM python:3.7-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN apk --no-cache add ffmpeg imagemagick postgresql-libs \
        && apk --no-cache add --virtual .build-deps gcc musl-dev postgresql-dev \
        && pip --no-cache-dir install -r requirements.txt \
        && apk --no-cache del .build-deps

# Install application
COPY app/ .
