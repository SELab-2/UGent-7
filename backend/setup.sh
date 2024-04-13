echo "Installing dependencies..."
pip install poetry > /dev/null 2>&1
poetry install > /dev/null

if [ "$FIXTURE" != "" ]; then
    echo "Clearing database..."
    rm -f db.sqlite3
fi

echo "Migrating database..."
python manage.py migrate > /dev/null
python manage.py migrate django_celery_results > /dev/null

if [ "$FIXTURE" != "" ]; then
    echo "Populating $FIXTURE database..."
    python manage.py loaddata */fixtures/$FIXTURE/* > /dev/null
fi

echo "Compiling translations..."
django-admin compilemessages > /dev/null

echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null

echo "Done"
