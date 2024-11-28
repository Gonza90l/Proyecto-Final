FROM mariadb:latest

ENV MYSQL_ROOT_PASSWORD=your_password
ENV MYSQL_DATABASE=proyecto_informatico

COPY ./Proyecto_backend/documentation/database_settings /docker-entrypoint-initdb.d

CMD ["--bind-address=0.0.0.0"]