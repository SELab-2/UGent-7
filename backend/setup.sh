echo "Installing requirements..."
pip install -r requirements.txt > /dev/null

echo "Migrating database..."
python manage.py migrate > /dev/null

echo "Populating database..."
python manage.py loaddata */fixtures/* > /dev/null

echo "Compiling translations..."
django-admin compilemessages > /dev/null

echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null

echo "Done"