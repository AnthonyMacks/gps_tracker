#!/bin/bash

URL="https://gps-tracker-69gb.onrender.com/gps"

declare -A DEVICE_COORDS=(
  ["I"]="-33.8700,151.2100"
  ["II"]="-33.8710,151.2110"
  ["III"]="-33.8720,151.2120"
  ["IV"]="-33.8730,151.2130"
  ["V"]="-33.9100,151.2100"
  ["VI"]="-33.9050,151.2110"
  ["VII"]="-33.9050,151.2150"
  ["VIII"]="-33.9050,151.2180"
  ["IX"]="-33.8990,151.2200"
  ["X"]="-33.8980,151.2220"
)

for ID in "${!DEVICE_COORDS[@]}"
do
  LAT="${DEVICE_COORDS[$ID]%%,*}"
  LON="${DEVICE_COORDS[$ID]##*,}"
  TIMESTAMP="$(date -u +%Y%m%dT%H%M%S)"

  JSON="{
    \"latitude\": \"$LAT\",
    \"longitude\": \"$LON\",
    \"timestamp\": \"$TIMESTAMP\",
    \"speed\": \"0.00\",
    \"satellites\": \"7\",
    \"device_id\": \"$ID\"
  }"

  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST $URL \
    -H "Content-Type: application/json" \
    -d "$JSON")

  if [ "$RESPONSE" -eq 200 ]; then
    echo -e "\033[32m✅ Device $ID sent: $LAT, $LON\033[0m"
  else
    echo -e "\033[31m❌ Device $ID failed: $RESPONSE\033[0m"
  fi

  sleep 1
done