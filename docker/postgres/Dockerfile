FROM postgres:15.3

RUN apt-get update && apt-get  install -y postgis

RUN echo "CREATE EXTENSION postgis;" >> /docker-entrypoint-initdb.d/init.sql

CMD ["/usr/local/bin/docker-entrypoint.sh","postgres"]