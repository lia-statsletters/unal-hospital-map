# Codigo constructor de COVID19 Map para UNAL-Hospital Dash/ Map making code COVID19 UNAL-Hospital Dash 

Este codigo hace parte de un MVP para crear un Dash+app que ayude a los servicios de respuesta de emergencia a manejar la epidemia de COVID19 en Bogota. Mas info [aqui](https://github.com/UNAL-Hospital-project/unal-hospital-front). 

** VERY VERY EARLY PROTOTYPE **

This repo is aimed at making things as easy as possible to any spanish-speaking dev in Bogota
that wants to hack this around and build things, so feel free to copy-paste the docs here in google translate and I'm sure its simple enough spanish. Otherwise please feel free to contact me :).



# FAQ

## Como genero el mapa? / How do I generate the map?

Pasos:
1. Consigue una api key en Mapbox (gratis, free tier 50000 llamadas).
2. Crea una estructura de folders ".to_ignore/keys/" en la raiz de este proyecto.
3. Copy-Paste tu api key en un archivo dentro del folder keys que create, llamalo "mapbox.key"
4. Corre "mapbox_out" desde el directorio raiz de este proyecto (todos los path son relativos a esta)
5. El mapa estara en .to_ignore.

El resultado es un html que contiene las capas y una interfaz sencilla para visualizarlas.


## Como funciona mapbox_out por debajo? / How does mapbox_out work underneath?

* Templates guarda un folder con configuraciones de capa y ciudad, y una plantilla del html de salida (fancy_geojson_mapbox.html). Codigo de interaccion (tooltips) es more or less "hardcoded" en la template del mapa (fancy_geojson_mapbox.html)

* En Layers cada capa a visualizar se expresa con un json que connecta una fuente en geojson dentro de /data con codigo que describe como esos datos han de ser visualizados por MapBox.


## De donde salieron los datos? / Where is this data coming from?

* bogota_hospitales.geojson : 
	* Poligonos, nombre: Overpass/Nominatim, query hospitales/amenidades (ver pull_hospitals.py en data_utils). 
	* Numero de camas: mock, creado en massage_geodata.py in data_utils.

* Pacientes, gps coords: Creado en massage_geodata.py, risk_fake_dots como puntos dentro de cada poligono de riesgo. Los poligonos de riesgo se crearon a mano alzada en MyMap en google, y las formas convertidas de kml a geojson. 

* Localidades de Bogota: Tomadas de https://datosabiertos.bogota.gov.co/. Luego hicimos spatial join de los pacientes con los poligonos de cada localidad para obtener la cuenta de "mock" pacientes por localidad. El spatial join esta en spatial_join_points_localities en massage_geodata.py

## Pero estos son geojsons estaticos! podemos conectar esto con datos en tiempo real? / But those geojsons are static! can we connect this to real time data?

Si, es posible conectar el mapa con streaming data y tambien podemos hacer "fake" real time conectando el mapa a datos en un S3 bucket o algo asi. Tambien para hacer enriquecimientos como numero de pacientes por localidad, densidad, camas por hospital y otros podemos configurar un pipeline que haga eso junto con backend.


## Tengo mas preguntas! / I have more questions!

Comments/Issues github 



