FROM alpine:latest

EXPOSE 8080

RUN apk update

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

RUN apk add firefox

RUN apk add font-noto

RUN apk add terminus-font

RUN python3 -m ensurepip

RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install Flask requests requests[socks] requests[security] cryptography selenium

COPY ./files/geckodriver /usr/local/bin/

RUN chmod +x /usr/local/bin/geckodriver

ENTRYPOINT [ "python3", "/home/script.py" ]