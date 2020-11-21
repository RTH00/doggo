FROM postgres:12.2

ENV POSTGRES_PASSWORD=doggosecretpassword

COPY init.sql /docker-entrypoint-initdb.d/init.sql
