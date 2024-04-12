#!/bin/bash

backend=false
frontend=false
build=false
data="small"
sleep_duration=7

while getopts ":bfcd:" opt; do
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
    d )
      data="$OPTARG"
      if [[ ! $data =~ ^("small"|"medium"|"large")$ ]]; then
        echo "Invalid size provided. Size must be 'small', 'medium', or 'large'."
        exit 1
      fi
      ;;
    \? )
      echo "Usage: $0 [-b] [-f] [-c] [-d <size>] "
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

echo "-------------------------------------"
echo "starting wait"
if [ "$data" = "medium" ] || [ "$data" = "large" ]; then
    sleep "$sleep_duration"
    echo "starting data"
    docker exec backend sh -c "python manage.py migrate"
    echo "migrated db"
fi
if [ "$data" = "medium" ]; then
    docker exec backend sh -c "python manage.py loaddata */fixtures/medium/*"
elif [ "$data" = "large" ]; then
    docker exec backend sh -c "python manage.py loaddata */fixtures/large/*"
fi
echo "$data data is ready"
echo "-------------------------------------"
echo ""
echo "-------------------------------------"
echo "Following logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

if [ "$backend" = true ]; then
    docker-compose -f development.yml logs --follow --tail 50 backend
elif [ "$frontend" = true ]; then
    docker-compose -f development.yml logs --follow --tail 50 frontend
else
    docker-compose -f development.yml logs --follow --tail 50 backend frontend
fi

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."
