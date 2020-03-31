from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from shapely.geometry import Point, Polygon, MultiPolygon

import pandas as pd, geopandas as gpd

if __name__ == "__main__":
	nominatim = Nominatim()
	areaId = nominatim.query('Bogota, Colombia').areaId()
	overpass = Overpass()
	query = overpassQueryBuilder(area=areaId,
								 elementType=['way'],
								 selector='"amenity"="hospital"',
								 includeGeometry=True)
	result = overpass.query(query)
	result = [{'tags': x.tags(), 'geometry': x.geometry()}
										 for x in result.elements()]
	#to pandas for cleaning tags
	df_hosps= pd.io.json.json_normalize(result)
	#to geopandas
	gdf_hosps = gpd.GeoDataFrame(df_hosps)
	#
	#gdf_hosps['geometry']=gdf_hosps['geometry.coordinates'].apply(lambda x: Polygon(x[0]))
	gdf_hosps['geometry.point']=gdf_hosps['geometry.coordinates'].apply(lambda x: x[0][0]).apply(Point)
	gdf_hosps=gdf_hosps.set_geometry(col='geometry.point')
	#gdf_hosps.plot().get_figure().savefig('hospitals_points.png')
	gdf_hosps.drop(columns=['geometry.coordinates']).to_file(driver='GeoJSON', filename="bogota_hospitales.geojson")
	print('foo')