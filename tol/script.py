import fiona
import os
import geopandas as gpd

os.chdir(r"D:\Github\GovTechHackathon2024-Schneereserven\tol")


data = gpd.read_file("stauanlagen-bundesaufsicht_2056.gpkg")

