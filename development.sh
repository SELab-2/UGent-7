docker-compose -f development.yml up -d

docker-compose -f development.yml logs --follow --tail 50 backend