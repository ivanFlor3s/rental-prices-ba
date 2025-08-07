# Scripts para Docker

## Construir la imagen

docker build -t rental-prices-api .

## Ejecutar solo la API

docker run -p 8000:8000 rental-prices-api

## Ejecutar con docker-compose

docker-compose up -d

## Ver logs de la API

docker-compose logs -f rental-api

## Parar los servicios

docker-compose down

## Reconstruir y ejecutar

docker-compose up --build -d

## Ejecutar en modo desarrollo (con logs)

docker-compose up

## Verificar que la API está funcionando

curl http://localhost:8000/health
