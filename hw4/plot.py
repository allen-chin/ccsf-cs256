import folium
import geopandas as gpd
import pandas as pd


def main():
    sf_gdf = gpd.read_file("san-francisco.geojson")
    sf_gdf['pop10_sqmi'] = pd.to_numeric(sf_gdf['pop10_sqmi'], downcast='integer')

    sf_map = folium.Map([37.7556, -122.4399], zoom_start = 13)

    folium.GeoJson(
        'san-francisco.geojson',
        name='geojson'
    ).add_to(sf_map)

    sf_map.choropleth(sf_gdf, data=sf_gdf, columns=['zip_code', 'pop10_sqmi'], key_on='feature.properties.zip_code', fill_color='OrRd', fill_opacity=0.7, legend_name='Population per Square Mile')
    sf_map.save('index.html')

if __name__ == "__main__":
    main()
