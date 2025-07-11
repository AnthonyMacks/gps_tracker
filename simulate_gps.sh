#!/bin/bash

URL="https://gps-tracker-69gb.onrender.com/gps"

declare -a LATLONS=(
  "-33.8700,151.2100"
  "-33.8710,151.2110"
  "-33.8720,151.2120"
  "-33.8730,151.2130"
  "-33.9100,151.2100"
  "-33.9050,151.2110"
  "-33.9050,151.2150"
  "-33.9050,151.2180"
)

for coord in "${LATLONS[@]}"
do
  LAT="${coord%%,*}"
  LON="${coord##*,}"
  curl -X POST $URL \
  -H "Content-Type: application/json" \
  -d "{
    \"latitude\": \"$LAT\",
    \"longitude\": \"$LON\",
    \"timestamp\": \"$(date -u +%Y%m%dT%H%M%S)\",
    \"speed\": \"0.00\",
    \"satellites\": \"7\"
  }"
  echo "🛰️ Sent: $LAT, $LON"
  sleep 3
done
