#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for database..."
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

python manage.py collectstatic --noinput

# Start Gunicorn
exec "$@"
