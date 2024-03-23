#!/bin/bash

backend=false
frontend=false
windows_hmr=false
build=false

while getopts ":bfcw" opt; do
  case ${opt} in
    b )
      backend=true
      ;;
    f )
      frontend=true
      ;;
    w )
      windows_hmr=true
      ;;
    c )
      build=true
      ;;
    \? )
      echo "Usage: $0 [-b] [-f] [-w] [-c]"
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

if [ "$windows_hmr" = true ]; then
    sed -i "s/^FRONTEND_CMD=.*/FRONTEND_CMD=\"npm run watch\"/" .env
else
    sed -i "s/^FRONTEND_CMD=.*/FRONTEND_CMD=\"npm run host\"/" .env
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

echo "-------------------------------------"
echo "Following logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

if [ "$backend" = true ] && [ "$frontend" = true ]; then
    docker-compose -f development.yml logs --follow --tail 50 backend frontend
elif [ "$frontend" = true ]; then
    docker-compose -f development.yml logs --follow --tail 50 frontend
else
    docker-compose -f development.yml logs --follow --tail 50 frontend
fi

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."
