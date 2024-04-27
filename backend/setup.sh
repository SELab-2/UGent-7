echo "Migrating database..."
python manage.py migrate > /dev/null 2>&1
echo "Compiling translations..."
django-admin compilemessages > /dev/null 2>&1
echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null 2>&1
echo "Setup complete"
