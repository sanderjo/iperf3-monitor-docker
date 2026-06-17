FROM alpine:3.19

RUN apk add --no-cache iperf3 python3 busybox-suid tzdata

COPY scripts/ /scripts/
COPY web/ /web/
COPY crontab /etc/crontabs/root

RUN chmod +x /scripts/*.sh

VOLUME /data
EXPOSE 8080

ENTRYPOINT ["/scripts/entrypoint.sh"]
