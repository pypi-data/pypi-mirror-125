#!/bin/bash
set -euo pipefail

set -x
cd vendor/
wget -q --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.css
wget -q --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css
wget -q --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css
wget -q --continue https://unpkg.com/luxon@2.0.2/build/global/luxon.min.js
wget -q --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.js
wget -q --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.js.map
wget -q --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster-src.js
wget -q --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster-src.js.map
