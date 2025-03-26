#!/bin/bash

echo "Останавливаем контейнеры..."
clear
docker-compose down

echo "Запускаем контейнеры..."
docker-compose up --build

echo "Проверяем статус контейнеров..."
docker-compose ps 