FROM debian:buster

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libncurses5-dev \
    libssl-dev \
    libxml2-dev \
    libsqlite3-dev \
    uuid-dev \
    libedit-dev

RUN wget -O /tmp/asterisk.tar.gz https://github.com/asterisk/asterisk/archive/refs/tags/16.20.0.tar.gz \
    && tar -zxvf /tmp/asterisk.tar.gz -C /tmp \
    && cd /tmp/asterisk-* \
    && ./configure \
    && make \
    && make install \
    && make samples \
    && rm -rf /tmp/asterisk*

COPY sip.conf /docker/asterisk/sip.conf
COPY extensions.conf /docker/asterisk/extensions.conf

CMD ["/usr/sbin/asterisk", "-f"]
