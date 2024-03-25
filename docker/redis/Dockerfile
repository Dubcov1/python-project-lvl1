FROM debian:latest

RUN apt-get update && apt-get install -y redis-server

RUN apt-get clean

EXPOSE 6379

CMD ["redis-server"]
