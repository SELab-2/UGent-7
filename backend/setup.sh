echo "Installing dependencies..."
pip install poetry > /dev/null 2>&1
poetry install > /dev/null
echo "Migrating database..."
python manage.py migrate > /dev/null
echo "Compiling translations..."
django-admin compilemessages > /dev/null
echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null
echo "Done"
