FROM python:3.9.1-alpine3.13
LABEL maintainer="ravetam"

RUN mkdir src
WORKDIR /src
COPY . /src

RUN pip3 install --no-cache-dir --upgrade paho-mqtt pyyaml

EXPOSE 15002

CMD [ "python", "./AlarmServer.py" ]