echo "Checking for existing SSL certificates..."

if [ ! -f "data/nginx/ssl/private.key" ] || [ ! -f "data/nginx/ssl/certificate.crt" ]; then
echo "Generating SSL certificates..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout data/nginx/ssl/private.key \
    -out data/nginx/ssl/certificate.crt \
    -subj "/C=BE/ST=/L=/O=/OU=/CN="
else
    echo "SSL certificates already exist, skipping generation."
fi

echo "Starting services..."
docker-compose -f development.yml up -d

echo "Following logs..."
docker-compose -f development.yml logs --follow --tail 50 backend