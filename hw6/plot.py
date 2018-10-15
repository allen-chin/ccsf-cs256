import tkinter
import tkinter.font

import folium
import geopandas as gpd
import pandas as pd

POINT_RADIUS = 3
LINE_WEIGHT = 3

def get_centroid(row):
    return (row['geometry'].centroid.y, row['geometry'].centroid.x)


def get_text_size(text, font_size):
    tkinter.Frame().destroy()
    font = tkinter.font.Font(family='Helvetica Neue', size=font_size)
    return (font.measure(text) + 10, font.metrics('linespace'))

def add_label(map_object, location, text, font_size=18, icon_anchor=None):
    # icon_anchor is left-aligned so need to shift
    length, width = get_text_size(text, font_size)

    if not icon_anchor:
        icon_anchor = (length // 2, width // 2 + 30)

    folium.map.Marker(location,
                      icon=folium.DivIcon(
                          icon_size=None,
                          icon_anchor=icon_anchor,
                          html='<div style="font-size: {0}pt"><span style="background-color: rgba(255, 255, 255, 0.6); padding: 0px 5px; white-space: nowrap">'.format(font_size) + text + '</div>'
                      )
                      ).add_to(map_object)

def style(feature):
    return {
        'fillColor': '#e7bc9a',
        'fillOpacity': 0.7,
        'color': 'black',
        'weight': 1
    }

def main():
    sf_gdf = gpd.read_file("san-francisco.geojson")
    sf_gdf['pop2010'] = pd.to_numeric(sf_gdf['pop2010'], downcast='integer')

    sf_map = folium.Map([37.7556, -122.4399], zoom_start=13)

    folium.GeoJson(
        'san-francisco.geojson',
        name='geojson'
    ).add_to(sf_map)

    folium.GeoJson(
        data='san-francisco.geojson',
        name='geojson',
        style_function=style
    ).add_to(sf_map)

    # Add labels
    manual_label = {5, 8, 9, 12, 15, 26, 27}

    for index, row in sf_gdf.iterrows():
        if index not in manual_label:
            folium.CircleMarker(get_centroid(row), radius=POINT_RADIUS, color='black', fill=True, fill_opacity=1).add_to(sf_map)
            add_label(sf_map, get_centroid(row), row['zip_code'])


    # 94104
    row = sf_gdf.iloc[12]
    add_label(sf_map, (37.794, -122.363705), row['zip_code'], icon_anchor=(0, 13))
    centroid = get_centroid(row)
    folium.CircleMarker(centroid, radius=POINT_RADIUS, color='black', fill=True, fill_opacity=1).add_to(sf_map)
    folium.PolyLine(locations=[centroid, (37.794, centroid[1])], color='black', weight=LINE_WEIGHT).add_to(sf_map)
    folium.PolyLine(locations=[(37.794, centroid[1]), (37.794, -122.363705)], color='black', weight=LINE_WEIGHT).add_to(sf_map)


    # 94108
    row = sf_gdf.iloc[15]
    add_label(sf_map, (37.797, -122.363705), row['zip_code'], icon_anchor=(0, 25))
    centroid = get_centroid(row)
    folium.CircleMarker(centroid, radius=POINT_RADIUS, color='black', fill=True, fill_opacity=1).add_to(sf_map)
    folium.PolyLine(locations=[centroid, (37.797, centroid[1])], color='black', weight=LINE_WEIGHT).add_to(sf_map)
    folium.PolyLine(locations=[(37.797, centroid[1]), (37.797, -122.363705)], color='black', weight=LINE_WEIGHT).add_to(sf_map)

    sf_map.save('index.html')

if __name__ == "__main__":
    main()
