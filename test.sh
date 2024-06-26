#!/bin/bash

backend=false
frontend=false
build=false
keep=false

while getopts ":bfck" opt; do
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
    k )
      keep=true
      ;;
    \? )
      echo "Usage: $0 [-b] [-f] [-c]"
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
    docker-compose -f test.yml build --no-cache
fi

echo "Starting services..."
docker-compose -f test.yml up -d --scale cypress=0

cypress_exit=0
vitest_exit=0
django_exit=0

echo "Filling up database with test data"
docker exec backend sh -c "python manage.py flush --no-input; python manage.py migrate;
    python manage.py loaddata authentication/fixtures/realistic/*;
    python manage.py loaddata notifications/fixtures/realistic/*;
    python manage.py loaddata api/fixtures/realistic/*;"

if [ "$frontend" = true ]; then
    echo "Running frontend tests..."
    echo "Running Cypress tests..."
    docker-compose -f test.yml up --exit-code-from cypress --abort-on-container-exit  cypress
    cypress_exit=$?
    echo "Running Vitest tests..."
    docker exec frontend npm run test
    vitest_exit=$?
elif [ "$backend" = true ]; then
    echo "Running backend tests..."
    docker exec backend python manage.py test
    django_exit=$?
else
    echo "Running backend tests..."
    docker exec backend python manage.py test
    django_exit=$?
    echo "Running frontend_test tests..."
    echo "Running Cypress tests..."
    docker-compose -f test.yml up --exit-code-from cypress --abort-on-container-exit  cypress
    cypress_exit=$?
    echo "Running Vitest tests..."
    docker exec frontend npm run test
    vitest_exit=$?
fi

exit_code=0

echo "-----------------"
if [ $cypress_exit -ne 0 ] || [ $vitest_exit -ne 0 ] || [ $django_exit -ne 0 ]; then
    echo "Tests failed:"
    if [ $cypress_exit -ne 0 ]; then
        echo "  - Cypress"
    fi
    if [ $vitest_exit -ne 0 ]; then
        echo "  - Vitest"
    fi
    if [ $django_exit -ne 0 ]; then
        echo "  - Django"
    fi
    exit_code=1
else
    echo "All tests passed!"
fi
echo "-----------------"

echo "Cleaning up..."

if [ "$keep" = false ]; then
    docker-compose -f test.yml down --rmi all
else
    docker-compose -f test.yml down
fi

echo "Done."

exit $exit_code
