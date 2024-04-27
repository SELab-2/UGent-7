echo "Migrating database..."
python manage.py migrate > /dev/null
echo "Compiling translations..."
django-admin compilemessages > /dev/null
echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null
echo "Setup complete"
