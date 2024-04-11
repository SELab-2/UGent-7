small=false
medium=false
large=false

while getopts "sml" opt; do
  case ${opt} in
    s )
      small=true
      ;;
    m )
      medium=true
      ;;
    l )
      large=true
      ;;
    \? )
      echo "Usage: $0 [-s] [-m] [-l]"
      exit 1
      ;;
  esac
done



echo "Installing dependencies..."
pip install poetry > /dev/null 2>&1
poetry install > /dev/null

echo "Migrating database..."
python manage.py migrate > /dev/null
python manage.py migrate django_celery_results > /dev/null

echo "Populating database..."
if [ "$large" = true ]; then
    python manage.py loaddata */fixtures/large/* > /dev/null
elif [ "$medium" = true ]; then
    python manage.py loaddata */fixtures/medium/* > /dev/null
else
    python manage.py loaddata */fixtures/small/* > /dev/null
fi

echo "Compiling translations..."
django-admin compilemessages > /dev/null

echo "Generating Swagger documentation..."
echo "yes" | python manage.py collectstatic > /dev/null

echo "Done"
