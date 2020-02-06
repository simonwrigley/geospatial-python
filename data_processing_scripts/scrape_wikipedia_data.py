#!/usr/bin/env python3
import wikipedia
import geopandas as gpd
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

# Set up command line arguments
parser = argparse.ArgumentParser(
    description='A script to gather popup and geometry information from Wikipedia for an input .csv list of assets')
parser.add_argument("input_file", default=None, type=str,
                    help="Input file with full path")
parser.add_argument("place_name", default=None, type=str,
                    help="The name of the city in which the assets are situated")

args = parser.parse_args()
input_file = args.input_file
place_name = args.place_name




# Define function to obtain coordinates for each asset. Handle exceptions for
# articles which do not have coordinate information should they arise.
# (Thanks to @AdamP for this one)
def getCoords(x):
    coords = ""
    try:
        coords = [wikipedia.WikipediaPage(title=x).coordinates]
    except:
        coords = np.nan
    return coords


# place_name = 'Bath'
# First read the csv of assets to a dataframe
df = pd.read_csv(input_file,
                 header=None, names=['assets'])

# Ensure data is type = string
df.assets = df.assets.astype(str)

# Pre-process the asset names for search. Append the place name to any asset
# that doesn't already have it to aid search.

df.loc[df['assets'].str.contains(place_name), 'append_place_name'] = df['assets']

df.loc[~df['assets'].str.contains(
    place_name), 'append_place_name'] = df['assets'] + ', ' + place_name

# Run a fuzzy search to return the actual Wikipedia article titles that should be searched against
df['suggested_article_title'] = [wikipedia.search(
    x, results=1, suggestion=False) for x in df['append_place_name']]

# Remove sqare brackets from results
df['suggested_article_title'] = df['suggested_article_title'].str.get(0)

# Re-construct the overall article URL and a hyperlink to be inserted at the end of the summary:
df['article_url'] = "https://en.wikipedia.org/wiki/" + \
    df['suggested_article_title'].astype(str).replace(' ', '_', regex=True)
df['article_hyperlink'] = "<a href=\"" + df['article_url'] + "\">Read More</a>"

# Obtain the summary paragraph for each article
df['summary'] = [wikipedia.summary(x) for x in df['suggested_article_title']]

# Append a read more link with the article URL to the end of the summary:
df['summary'] = df['summary'] + "\n\n" + df['article_hyperlink']


# Obtain the main image URL
df['image_url'] = [wikipedia.WikipediaPage(
    title=x).images[1] for x in df['suggested_article_title']]

# Obtain the coordinates of the asset
df['coordinates'] = [getCoords(x) for x in df['suggested_article_title']]

df['lat'] = df['coordinates'][0][0][0]
df['lon'] = df['coordinates'][0][0][1]

df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)

# Convert the dataframe to a geodataframe
gdf = gpd.GeoDataFrame(df[['assets', 'suggested_article_title', 'summary',
                           'image_url', 'lat', 'lon']], geometry=gpd.points_from_xy(df.lon, df.lat))


export_to_csv = gdf.to_csv(r'./data/export.csv')
