#!/bin/bash

backend=false
frontend=false
build=false
test=false

while getopts ":bfct" opt; do
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
    t )
      test=true
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
else
    echo "$build"
fi

echo "Starting services..."
docker-compose -f development.yml up -d

if [ "$test" = true ]; then
    echo "Running tests..."
    docker-compose -f development.yml exec backend python manage.py test
else
    echo "-------------------------------------"
    echo "Following logs..."
    echo "Press CTRL + C to stop all containers"
    echo "-------------------------------------"

    if [ "$backend" = true ] && [ "$frontend" = true ]; then
        docker-compose -f development.yml logs --follow --tail 50 backend frontend
    elif [ "$frontend" = true ]; then
        docker-compose -f development.yml logs --follow --tail 50 frontend
    else
        docker-compose -f development.yml logs --follow --tail 50 backend
    fi
fi

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."
