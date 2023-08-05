#!/bin/bash
set -euo pipefail

cd vendor/
wget --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.css
wget --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css
wget --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css
wget --continue https://unpkg.com/luxon@2.0.2/build/global/luxon.min.js
wget --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.js
wget --continue https://unpkg.com/leaflet@1.7.1/dist/leaflet.js.map
wget --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster-src.js
wget --continue https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster-src.js.map
