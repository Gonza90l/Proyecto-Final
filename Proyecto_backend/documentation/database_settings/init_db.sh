#!/bin/bash
set -e

# Wait for MariaDB to be ready
until mysqladmin ping -h mariadb --silent; do
  >&2 echo "MariaDB is unavailable - sleeping"
  sleep 5
done

>&2 echo "MariaDB is up - executing command"

# Run the SQL scripts
mariadb -h mariadb -u root -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/create_db.sql
mariadb -h mariadb -u root -p"$MYSQL_ROOT_PASSWORD" "$MYSQL_DATABASE" < /docker-entrypoint-initdb.d/create_tables.sql

exec "$@"