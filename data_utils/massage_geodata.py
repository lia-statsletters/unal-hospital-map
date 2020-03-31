import pandas as pd, numpy as np
import geopandas as gpd
import fiona
import shapely
from shapely.geometry import Point, Polygon, MultiPolygon

import random

from fiona.crs import from_epsg
#import logging
#logging.basicConfig(level=logging.DEBUG)

from pyproj import Proj, transform


def maquillaje_risk():
	fl = './.to_ignore/data/bogota/mock_risk.geojson'
	gdf_div = gpd.read_file(fl)
	LUT = {'medio': '#ffa41b', 'alto': '#d63447', 'bajo': '#216353'}
	gdf_div['color'] = np.array([LUT[x] for x in gdf_div.Name])
	
	gdf_div = gpd.read_file(fl)


def risk_fake_dots():
	#creates dots inside the shapes of mock risk.
	#use those dots to create heatmaps in mapbox :)
	#https://docs.mapbox.com/mapbox-gl-js/example/heatmap-layer/
	def random_points_within(poly, num_points,label):
		min_x, min_y, max_x, max_y = poly.bounds
		points = []
		while len(points) < num_points:
			random_point = Point([LUT_distr[label](min_x, max_x), LUT_distr[label](min_y, max_y)])
			if (poly.contains(random_point)):
				points.append(random_point)
		return points
	
	fl = './.to_ignore/data/bogota/mock_risk.geojson'
	gdf_div = gpd.read_file(fl)
	gdf_div.set_index(keys='Name',inplace=True)
	LUT = {'medio': '#ffa41b', 'alto': '#d63447', 'bajo': '#216353'}
	LUT_distr = {'medio': lambda a,b: random.triangular(a,b),
				 'alto': lambda a,b: random.triangular(a,b),
				 'bajo': lambda a,b: random.uniform(a,b)}
	LUT_ndots = {'medio': 80, 'alto':30, 'bajo':300 }
	#modified sin verguenza:
	#https://codereview.stackexchange.com/questions/69833/generate-sample-coordinates-inside-a-polygon

	for label in gdf_div.index: #create one geojson per point set
		pts=random_points_within(gdf_div.geometry[label],LUT_ndots[label],label)
		gdf_out=gpd.GeoDataFrame({'color':np.full(LUT_ndots[label],LUT[label]), 'geometry':pts},
								 geometry='geometry',crs={'init':'EPSG:4326'})
		gdf_out.plot().get_figure().savefig(f'{label}.png')
		gdf_out.to_file(f'./.to_ignore/data/bogota/mock_risk_points_{label}.geojson',
						driver='GeoJSON')
		
	print('pff')
	
def spatial_join_points_localities():
	gdf_localities = gpd.read_file('./.to_ignore/data/bogota/localidades.geojson')
	for label in ('medio','alto','bajo'):
		fl=f'./.to_ignore/data/bogota/mock_risk_points_{label}.geojson'
		gdf_div=gpd.read_file(fl)
		gdf_sjoined=gpd.sjoin(gdf_div, gdf_localities) #spatial join localities on points
		# count patients per locality
		patients_loc=gdf_sjoined.groupby(by='LocNombre').agg({'geometry':'count'}).reset_index()
		#gdf_localities.join(pat)
		out=gdf_localities.merge(patients_loc, on='LocNombre', suffixes=('','_count'))
		out['densidad_pacientes_km2']=(out.geometry_count/out.LocArea).apply(lambda x: np.round(10**(6)*x,2))
		out[['LocNombre','geometry','geometry_count','densidad_pacientes_km2']].to_file(f'./.to_ignore/data/bogota/locality_count_{label}.geojson', driver='GeoJSON')
		print('ff')
	
def crs_conv(fl, from_epsg='EPSG:3116'): #bogota crs 3116 EPSG:21897
	gdf_div = gpd.read_file(fl)
	#gdf_div.crs={'init':from_epsg}
	gdf_div = gdf_div.to_crs('EPSG:4326') #mapbox tiles
	gdf_div.to_file(fl, driver='GeoJSON')
	
def add_mock_beds_to_hospital():
	fl='./.to_ignore/data/bogota/bogota_hospitales.geojson'
	gdf_div = gpd.read_file(fl)
	fake_beds=[int(np.ceil(random.betavariate(2,5)*20)) for x in range(gdf_div.shape[0])] # beta distributed, alpha 2 beta 5
	gdf_div['avail_icu']=np.array(fake_beds)
	gdf_div.to_file(fl, driver='GeoJSON')


if __name__ == "__main__":
	#transform_catastro()
	#maquillaje_risk()
	#risk_fake_dots()
	#fl = './.to_ignore/data/bogota/localidades.geojson'
	#gdf_div = gpd.read_file(fl)
	
	#gdf_div.plot().get_figure().savefig('barrios.png')
	#crs_conv('./.to_ignore/data/bogota/localidades.geojson') #crs_conv barrios
	#spatial_join_points_localities()
	add_mock_beds_to_hospital()
