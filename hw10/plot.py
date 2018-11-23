from math import radians, cos, sin, asin, sqrt
from itertools import combinations

import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx


# Unfortunately this did not get the correct result so unused
# https://gis.stackexchange.com/questions/279109/calculate-distance-between-a-coordinate-and-a-county-in-geopandas
# Calculates distance between 2 GPS coordinates
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def get_length(geometry):
    if geometry.geom_type == "MultiLineString":
        for line in geometry:
            numCoords = len(line.coords) - 1
            distance = 0

            for i in range(0, numCoords):
                point1 = line.coords[i]
                point2 = line.coords[i + 1]
                distance += haversine(point1[0], point1[1], point2[0], point2[1])

    elif geometry.geom_type == "LineString":
        line = geometry
        numCoords = len(line.coords) - 1
        distance = 0

        for i in range(0, numCoords):
            point1 = line.coords[i]
            point2 = line.coords[i + 1]
            distance += haversine(point1[0], point1[1], point2[0], point2[1])

    return distance


def get_df():
    df = gpd.read_file("../data/bay-area-counties.geojson")
    counties = df["county"]
    geometries = df["geometry"]

    intersections = []

    for i, j in combinations(df.index, 2):
        intersection = geometries[i].intersection(geometries[j])

        if not intersection.is_empty:
            intersections.append([counties[i], counties[j], intersection])


    intersections = gpd.GeoDataFrame(data=intersections, columns=["county1", "county2", "geometry"])
    return df, intersections


def draw(df, intersections):
    # Draw graphs
    G = nx.Graph()
    pos = {}
    pos_labels = {}

    # Add nodes with position to draw
    for index, row in df.iterrows():
        centroid = row["geometry"].centroid
        pos[row["county"]] = [centroid.x, centroid.y]
        pos_labels[row["county"]] = [centroid.x + 0.05, centroid.y + 0.05]

    # Manual offsets
    pos_labels["San Francisco"][0] -= 0.25
    pos_labels["San Francisco"][1] -= 0.05
    pos_labels["San Mateo"][0] += 0.05
    pos_labels["Santa Clara"][0] += 0.05
    pos_labels["Alameda"][0] += 0.05
    pos_labels["Contra Costa"][0] += 0.1

    # Add edges
    for index, row in intersections.iterrows():
        weight = 1
        if row["geometry"].geom_type == "MultiLineString":
            weight = len(row["geometry"])
        G.add_edge(row.loc["county1"], row.loc["county2"], weight=weight)
        print(row.loc["county1"], row.loc["county2"], weight)

    weights = nx.get_edge_attributes(G, "weight")
    pos_weight = {}


    df.plot(color="#e7bc9a", edgecolor="gray", alpha=1)
    nx.draw(G, pos=pos, node_color="black")
    nx.draw_networkx_labels(G, pos=pos_labels)

    plt.title("Network Graph of Adjacent Bay Area Counties", fontsize=40)
    plt.show()

def main():
    df, intersections = get_df()
    draw(df, intersections)

if __name__ == "__main__":
    main()