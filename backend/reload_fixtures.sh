#!/bin/bash
docker-compose -f development.yml up -d backend 

# migrate database
# docker exec backend sh -c "python manage.py makemigrations"
docker exec backend sh -c "python manage.py migrate"

# seed small data
docker exec backend sh -c "python manage.py seed_db_new small"
docker exec backend sh -c "python manage.py seed_db small"

# create fixtures for small data
docker exec backend sh -c "python manage.py dumpdata api --output=api/fixtures/small/small.json"
docker exec backend sh -c "python manage.py dumpdata authentication --output=authentication/fixtures/small/small.json"
docker exec backend sh -c "python manage.py dumpdata notifications --output=notifications/fixtures/small/small.json"

# seed medium data
docker exec backend sh -c "python manage.py seed_db_new medium"
docker exec backend sh -c "python manage.py seed_db medium"

# create fixtures for medium data
docker exec backend sh -c "python manage.py dumpdata api --output=api/fixtures/medium/medium.json"
docker exec backend sh -c "python manage.py dumpdata authentication --output=authentication/fixtures/medium/medium.json"
docker exec backend sh -c "python manage.py dumpdata notifications --output=notifications/fixtures/medium/medium.json"

# seed large data
docker exec backend sh -c "python manage.py seed_db_new large"
docker exec backend sh -c "python manage.py seed_db large"

# create fixtures for large data
docker exec backend sh -c "python manage.py dumpdata api --output=api/fixtures/large/large.json"
docker exec backend sh -c "python manage.py dumpdata authentication --output=authentication/fixtures/large/large.json"
docker exec backend sh -c "python manage.py dumpdata notifications --output=notifications/fixtures/large/large.json"


echo "-----------------"
echo "Cleaning up..."
docker-compose -f development.yml down backend
echo "Done."

exit $exit_code
