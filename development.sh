#!/bin/bash

build=false

while getopts ":b" opt; do
  case ${opt} in
    b ) build=true ;;
    \? ) echo "Usage: $0 [-b]" >&2
         exit 1 ;;
  esac
done

echo "Checking environment file..."

if ! [ -f .env ]; then
    cp .dev.env .env
    read -s -p "Enter a random string for the django secret (just smash keyboard): " new_secret
    sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=$new_secret/" .env
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

echo "-------------------------------------"
echo "Following backend logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

docker-compose -f development.yml logs --follow --tail 50 backend

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."
