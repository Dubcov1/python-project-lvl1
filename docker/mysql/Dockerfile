FROM debian:buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg lsb-release && \
    echo "deb http://repo.mysql.com/apt/debian/ $(lsb_release -sc) mysql-8.0" > /etc/apt/sources.list.d/mysql.list && \
    apt-get update && \
    apt-get install -y mysql-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY my.cnf /etc/mysql/my.cnf

EXPOSE 3306

CMD ["mysqld_safe"]
