#!/bin/bash

backend=false
frontend=false
build=false
seed=false
data=""

# Arguments parsing
while getopts ":bfcsd:" opt; do
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
    s )
      seed=true
      ;;
    d )
      case "$OPTARG" in
        small|medium|large|real)
          if [ "$OPTARG" = "real" ]; then
            data="realistic"
          else
            data="$OPTARG"
          fi
          echo "$data"
          ;;
        * )
          echo "Invalid data size provided. Size must be 'small', 'medium', 'large' or 'real."
          exit 1
          ;;
      esac
      ;;
    : )
      echo "Usage: $0 [-b] [-f] [-c] [-s <size>] [-d <size>]" 1>&2
      exit 1
      ;;
    \? )
      echo "Usage: $0 [-b] [-f] [-c] [-s <size>] [-d <size>]" 1>&2
      exit 1
      ;;
  esac
done

echo "Checking environment file..."

# If clean build, remove .env and db.sqlite3
if [ "$build" = true ]; then
  rm .env > /dev/null 2>&1
  rm -f backend/db.sqlite3 > /dev/null 2>&1
fi

# Create environment file if it doesn't exist
if ! [ -f .env ]; then
  cp .dev.env .env
  sed -i "s/^DJANGO_SECRET_KEY=.*/DJANGO_SECRET_KEY=totally_random_key_string/" .env
  sed -i "s,^DJANGO_ROOT_DIR=.*,DJANGO_ROOT_DIR=$PWD/backend," .env
  echo "Created environment file"
fi

# Generate SSL certificates if they don't exist
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

# Build Docker images
if [ "$build" = true ]; then
  echo "Building Docker images..."
  echo "This can take a while..."
  docker-compose -f development.yml build --no-cache
fi

# Create new database fixtures if flag is set
if [ "$seed" = true ]; then
  # Cleanup function
  cleanup() {
      echo "Ctrl+C detected. Cleaning up..."
      docker-compose -f development.yml down
      exit 1
  }

  # Call cleanup function on SIGINT
  trap cleanup SIGINT

  echo "-------------------------------------"
  echo "Creating database fixtures."
  echo "This can take a long time..."
  echo "Go do something else in the meantime!"
  echo "-------------------------------------"

  docker-compose -f development.yml up -d backend > /dev/null 2>&1
  docker exec backend sh -c "python manage.py migrate" > /dev/null 2>&1

  sizes=("small" "medium" "large")
  for size in "${sizes[@]}"; do
    echo "Seeding $size database..."
    docker exec backend sh -c "python manage.py seed_db $size"

    echo "Dumping $size fixtures..."
    docker exec backend sh -c "python manage.py dumpdata api --output=api/fixtures/$size/$size.json"
    docker exec backend sh -c "python manage.py dumpdata authentication --output=authentication/fixtures/$size/$size.json"
    docker exec backend sh -c "python manage.py dumpdata notifications --output=notifications/fixtures/$size/$size.json"
  done

  echo "Cleaning up..."
  docker-compose -f development.yml down
  echo "Done."
  exit 0
fi

# Seed database if data size is provided
if [ "$data" != "" ]; then
  echo "--------------------------"
  echo "Filling the database."
  echo "This can take some time..."
  echo "--------------------------"

  echo "Starting the required services"
  docker-compose -f development.yml up -d backend redis celery

  echo "Clearing, Migrating & Populating the database"
  # We have nog fixtures for notification yet.
  docker-compose -f development.yml run backend sh -c "python manage.py flush --no-input; python manage.py migrate; python manage.py loaddata authentication/fixtures/$data/*; python manage.py loaddata api/fixtures/$data/*;"

  echo "Stopping the services"
  docker-compose -f development.yml down

  echo "Database filled."
fi

# Start services
echo "Starting services..."
docker-compose -f development.yml up -d

echo "-------------------------------------"
echo "Following logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

# Follow logs based on flags
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
