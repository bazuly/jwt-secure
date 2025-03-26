#!/bin/bash

echo "Останавливаем контейнеры и удаляем вольюмы..."
clear
docker-compose down --volumes

echo "Запускаем контейнеры..."
docker-compose up --build

echo "Проверяем статус контейнеров..."
docker-compose ps 