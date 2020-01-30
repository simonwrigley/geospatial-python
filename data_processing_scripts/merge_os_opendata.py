# Import relevant modules
import pandas
import geopandas as gpd
from pathlib import Path

# Provide the full path to the directory containing the shape files to be merged
folder = Path("/full/path/to/data")

# Replace the section of the name that is common to all .shp files
shapefiles = folder.glob("*_RoadLink.shp")
gdf = pandas.concat([
    gpd.read_file(shp)
    for shp in shapefiles
]).pipe(gpd.GeoDataFrame)

# To write the results to a .shp file
# gdf.to_file(folder / 'name_of_merged_file.shp')

# To write the results to a .geojson file
gdf.to_file("name_of_merged_file.geojson", driver='GeoJSON')

# To write the results to a geopackage file
#gdf.to_file("name_of_merged_file.gpkg", driver="GPKG")

