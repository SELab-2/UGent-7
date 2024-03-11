if ! [ -f .env ]; then
    echo "Error: .env file does not exist."
    exit 1
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

echo "Starting services..."
docker-compose -f development.yml up -d

echo "-------------------------------------"
echo "Following backend logs..."
echo "Press CTRL + C to stop all containers"
echo "-------------------------------------"

docker-compose -f development.yml logs --follow --tail 50 backend

echo "Cleaning up..."

docker-compose -f development.yml down

echo "Done."
