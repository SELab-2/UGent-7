echo "Migrating database..."
python manage.py migrate > /dev/null 2>&1
echo "Compiling translations..."
django-admin compilemessages > /dev/null 2>&1
echo "Generating Swagger documentation..."
<<<<<<< HEAD
echo "yes" | python manage.py collectstatic > /dev/null 2>&1
=======
echo "yes" | python manage.py collectstatic > /dev/null
>>>>>>> 50c8072 (chore: networking)
echo "Setup complete"
