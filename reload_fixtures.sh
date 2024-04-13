#!/bin/bash

backend=true
frontend=true
build=false

while getopts ":c" opt; do
  case ${opt} in
    c )
      build=true
      ;;
    \? )
      echo "Usage: $0 [-c]"
      exit 1
      ;;
  esac
done

echo "Checking environment file..."
if [ "$build" = true ]; then
    rm .env > /dev/null 2>&1
fi

if ! [ -f .env ]; then
    cp .dev.env .env
    sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=totally_random_key_string/" .env
    echo "Created environment file"
fi

echo "Checking for existing SSL certificates..."

if [ ! -f "data/nginx/ssl/private.key" ] || [ ! -f "data/nginx/ssl/certificate.crt" ]; then
    echo "Generating SSL certificates..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout data/nginx/ssl/private.key \
    -out data/nginx/ssl/certificate.crt \
    -subj "/C=BE/ST=/L=/O=/OU=/CN=" > /dev/null
    echo "SSL certificates generated."
else
    echo "SSL certificates already exist, skipping generation."
fi

if [ "$build" = true ]; then
    echo "Building Docker images..."
    echo "This can take a while..."
    docker-compose -f development.yml build --no-cache
fi

echo "Starting services..."
docker-compose -f development.yml up -d

# seed small data
docker exec backend sh -c "python manage.py seed_db_new small"
docker exec backend sh -c "python manage.py seed_db small"

# create fixtures for small data
python manage.py dumpdata api --output=api/fixtures/small/small.json
python manage.py dumpdata authentication --output=authentication/fixtures/small/small.json
python manage.py dumpdata notifications --output=notifications/fixtures/small/small.json


# docker exec backend sh -c "python manage.py seed_db_new medium"
# docker exec backend sh -c "python manage.py seed_db medium"

# docker exec backend sh -c "python manage.py seed_db_new large"
# docker exec backend sh -c "python manage.py seed_db large"


echo "-----------------"

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."

exit $exit_code
