import fiona
import os
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import geojson

os.chdir(r"D:\Github\GovTechHackathon2024-Schneereserven\tol")


data = gpd.read_file("stauanlagen-bundesaufsicht_2056.gpkg")

data.to_csv("D:/Github/GovTechHackathon2024-Schneereserven/tol/standorte.csv", index=False)

# Einlesen der Rasterdaten
with rasterio.open('2023-11-11+000_alps_SWE_product.tif') as src:
    schneemengen = src.read(1, masked=True)


import urllib
import geojson
import geopandas as gpd
from shapely.geometry import shape, Polygon
import requests

x = "2664782.608032227"
y = "1096804.3518066406"

api_url = "https://api3.geo.admin.ch/rest/services/all/MapServer/identify?geometry="+ x + ","+y+"&geometryFormat=geojson&geometryType=esriGeometryPoint&imageDisplay=430,932,96&lang=de&layers=all:ch.bafu.wasser-teileinzugsgebiete_2&limit=10&mapExtent=2552500.000001527,956999.9998479064,2767500.000001527,1422999.9998479064&returnGeometry=true&sr=2056&tolerance=10"
#api_url = "https://api3.geo.admin.ch/rest/services/all/MapServer/identify?geometry=2664782.608032227,1096804.3518066406&geometryFormat=geojson&geometryType=esriGeometryPoint&imageDisplay=430,932,96&lang=de&layers=all:ch.bafu.wasser-teileinzugsgebiete_2&limit=10&mapExtent=2552500.000001527,956999.9998479064,2767500.000001527,1422999.9998479064&returnGeometry=true&sr=2056&tolerance=10"

#gj = geojson.load(api_url)


r = requests.get(api_url)
data = r.json()

data.keys()
data = data["results"][0]


# Annahme: Ihr 'data' Dictionary enthält eine Geometry Collection unter dem Schlüssel "geometry"
geometry_data = data["geometry"]

# Konvertierung der Geometry Collection in eine Liste von unterstützten Geometrietypen
geometries = []
for geom in geometry_data['geometries']:
    # Überprüfen Sie den Typ jeder Geometrie und konvertieren Sie sie in einen unterstützten Typ, z.B. Polygon
    if geom['type'] == 'Polygon':
        geometries.append(shape(geom))
    # Fügen Sie weitere Bedingungen für andere unterstützte Geometrietypen hinzu, falls erforderlich

# Erstellen eines GeoDataFrames aus den unterstützten Geometrien
gdf = gpd.GeoDataFrame(geometry=geometries)

# Speichern des GeoDataFrames als Shapefile
gdf.to_file("einzugsgebiet.shp")



