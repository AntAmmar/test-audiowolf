FROM amd64/ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV DJANGO_SETTINGS_MODULE audiowolf.settings

#RUN apk update && apk add --no-cache git gcc python3-dev musl-dev libffi-dev make build-base py-pip jpeg-dev zlib-dev
RUN apt clean
RUN apt -y update && apt-get -y install git gcc python3-pip python3-dev

WORKDIR /app
COPY . .

# install latest pip version that welcomes version conflicts between packages
RUN pip install --upgrade pip
RUN pip install .
