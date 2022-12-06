FROM alpine:latest

EXPOSE 9050

RUN apk update && apk add tor

COPY torrc.default /etc/tor/torrc.default

ENTRYPOINT [ "tor" ]

CMD [ "-f", "/etc/tor/torrc.default" ]