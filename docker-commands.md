# Scripts para Docker

## Construir la imagen

docker build -t rental-prices-scraper .

## Ejecutar el scrapper sobre todos los barrios

docker run --rm rental-prices-scraper

## Ejecutar barrios específicos

docker run --rm rental-prices-scraper Palermo Recoleta

## Exportar a CSV

docker run --rm rental-prices-scraper --export-csv departments.csv

## Ejecutar con docker-compose (PostgreSQL)

docker-compose up -d

## Ver logs de PostgreSQL

docker-compose logs -f postgres

## Parar los servicios

docker-compose down
