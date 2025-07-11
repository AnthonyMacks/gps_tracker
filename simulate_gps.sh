#!/bin/bash

URL="https://gps-tracker-69gb.onrender.com/gps"

declare -a LATLONS=(
  "-33.8700,151.2100"
  "-33.8710,151.2110"
  "-33.8720,151.2120"
  "-33.8730,151.2130"
  "-33.9100,151.2100"
  "-33.9050,151.2110"
  "-33.8050,151.1150"
  "-33.7050,151.0180"
)

for coord in "${LATLONS[@]}"
do
  LAT="${coord%%,*}"
  LON="${coord##*,}"

  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $URL \
    -H "Content-Type: application/json" \
    -d "{
      \"latitude\": \"$LAT\",
      \"longitude\": \"$LON\",
      \"timestamp\": \"$(date -u +%Y%m%dT%H%M%S)\",
      \"speed\": \"0.00\",
      \"satellites\": \"7\"
    }")

  if [ "$RESPONSE" -eq 200 ]; then
    echo -e "\033[32m🛰️ Success: $LAT, $LON ($RESPONSE)\033[0m"
  else
    echo -e "\033[31m⚠️ Failed: $LAT, $LON ($RESPONSE)\033[0m"
  fi

  sleep 3
done