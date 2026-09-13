#!/bin/bash
set -euo pipefail

mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" <<EOSQL
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE:-egor_db}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE_DJANGO:-django_db}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE:-egor_db}\`.* TO '${MYSQL_USER}'@'%';
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE_DJANGO:-django_db}\`.* TO '${MYSQL_USER}'@'%';
FLUSH PRIVILEGES;
EOSQL

# Optional SQL dumps mounted at /docker-entrypoint-initdb.d/dumps/
DUMP_DIR="/docker-entrypoint-initdb.d/dumps"
if [ -d "${DUMP_DIR}" ]; then
  for f in "${DUMP_DIR}"/*.sql "${DUMP_DIR}"/*.sql.gz; do
    [ -e "$f" ] || continue
    echo "[mysql-init] Importing $f ..."
    case "$f" in
      *.sql.gz) gunzip -c "$f" | mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" ;;
      *.sql) mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < "$f" ;;
    esac
  done
fi
