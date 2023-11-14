# NavigationServer   
Server for https://github.com/Svovoniks/Navigation.git

# How to start
1. Fill in all .template files and remove '.tempalate' from their names
2. Get a .pbf file from https://download.geofabrik.de/russia/central-fed-district.html, put it in graphhopper folder and rename it to map.pbf
3. Start the server with command: docker compose --env-file .env up --build
