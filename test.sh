#!/bin/bash

backend=false
frontend=false
build=false

while getopts ":bfc" opt; do
  case ${opt} in
    b )
      backend=true
      ;;
    f )
      frontend=true
      ;;
    c )
      build=true
      ;;
    \? )
      echo "Usage: $0 [-b] [-f] [-c]"
      exit 1
      ;;
  esac
done

echo "Checking environment file..."

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
    docker-compose -f testing.yml build --no-cache
else
    echo "$build"
fi

echo "Starting services..."
docker-compose -f testing.yml up -d

if [ "$frontend" = true ]; then
    echo "Running frontend tests..."
    echo "Not implemented yet"
fi

if [ "$backend" = true ]; then
    echo "Running backend tests..."
    docker-compose -f testing.yml exec backend python manage.py test
fi

echo "Cleaning up..."

docker-compose -f testing.yml down

echo "Done."
