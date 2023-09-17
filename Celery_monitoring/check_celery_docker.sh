#!/bin/bash

# Pobieranie ID kontenera za pomocą polecenia
CONTAINER_ID=$(docker ps | grep ':5555' | awk '{print $1}')

# Sprawdzenie, czy zmienna CONTAINER_ID nie jest pusta
if [[ -z "$CONTAINER_ID" ]]; then
    echo "0" # Kontener nie jest uruchomiony
else
    echo "1" # Kontener jest uruchomiony
fi
