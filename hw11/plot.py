import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from networkx.drawing import nx_agraph

BAY_AREA_COUNTY_NAMES = {"Alameda", "Contra Costa", "Marin", "Napa", "San Francisco", "San Mateo", "Santa Clara", "Solano", "Sonoma"}
CALIFORNIA_POPULATION = 39809693

def get_counties():
    counties = pd.read_excel("../data/2018-ca-pop.xls", sheet_name="E-1 CountyState2018", names=["Name", "2017Population", "2018Population", "PercentChange"], skiprows=8)
    counties = counties.dropna()
    counties = counties.set_index("Name")
    counties = counties.sort_values("2018Population", ascending=False)
    return counties

def get_cities(counties):
    cities = pd.read_excel("../data/2018-ca-pop.xls", sheet_name="E-1 CityCounty2018", names=["Name", "2017Population", "2018Population", "PercentChange"], skiprows=8)
    cities = cities.dropna()
    cities = cities[cities.Name != "Balance of County"]
    cities.insert(len(cities.columns), "County", value="")

    # Fill new County column
    current_county = ""
    for row in cities.itertuples():
        if row.Name in counties.index:
            current_county = row.Name

        cities.at[row.Index, "County"] = current_county


    # Remove header of each group except for cities that are also counties
    cities = cities.groupby(by="County")
    cities = cities.apply(lambda x: x.head(1) if len(x) == 1 else x.tail(len(x) - 1))
    cities.index = cities.index.droplevel()
    cities = cities.set_index("Name")
    return cities


def main():
    counties = get_counties()
    cities = get_cities(counties)

    graph = nx.DiGraph()
    graph.add_node("California", label="California", left_pos=[30 , 0], right_pos=[0, 0])

    bay_area_counties = [county for county in counties.itertuples() if county.Index in BAY_AREA_COUNTY_NAMES]
    bay_area_cities = []

    # Add counties to graph
    for county in bay_area_counties:
        graph.add_node(county, label=county.Index, left_pos=[0, 0], right_pos=[40, 0])
        graph.add_edge("California", county, label=str(round(county[2] * 100 / CALIFORNIA_POPULATION, 3)) + "%")

        # Add largest cities from those counties to the graph
        largest_cities = cities[cities.County == county.Index].nlargest(n=3, columns="2018Population")
        for city in largest_cities.itertuples():
            bay_area_cities.append(city)
            graph.add_node(city, label=city.Index, left_pos=[0, 0], right_pos=[0, 0])
            graph.add_edge(county, city, label=str(round(city[2] * 100 / county[2], 3)) + "%")


    # https://stackoverflow.com/a/11484144
    # https://github.com/pygraphviz/pygraphviz/issues/40
    # Gsplines=ortho is unfortunately ignored
    # Get positions of nodes as tree layout
    pos = nx_agraph.graphviz_layout(graph, prog="dot", args="-Grankdir=LR")

    # Prevent edges from drawing on labels by specifying positions
    for node in pos:
        x, y = pos[node]
        l = graph.nodes[node]["left_pos"]
        l[0] += x
        l[1] += y

        l = graph.nodes[node]["right_pos"]
        l[0] += x
        l[1] += y

    # Split the graph into two to specify separate edge positions
    left_subgraph = graph.subgraph(bay_area_counties + ["California"])
    right_subgraph = graph.subgraph(bay_area_counties + bay_area_cities)

    labels = nx.get_node_attributes(graph, "label")
    left_pos = nx.get_node_attributes(left_subgraph, "left_pos")
    right_pos = nx.get_node_attributes(right_subgraph, "right_pos")
    left_edge_labels = nx.get_edge_attributes(left_subgraph, "label")
    right_edge_labels = nx.get_edge_attributes(right_subgraph, "label")

    # Draw edges and labels
    print(left_pos)
    nx.draw_networkx_edges(left_subgraph, left_pos, alpha=0.3)
    nx.draw_networkx_edges(right_subgraph, right_pos, alpha=0.3)
    nx.draw_networkx_edge_labels(left_subgraph, left_pos, left_edge_labels, label_pos=0.3)
    nx.draw_networkx_edge_labels(right_subgraph, right_pos, right_edge_labels, label_pos=0.3)
    nx.draw_networkx_labels(graph, pos, labels=labels, horizontalalignment="left", font_weight="bold")

    # Open up the plot maximized
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    ax = plt.gca()
    ax.set_axis_off()
    plt.title("Most Populous Cities in Bay Area, Sorted by 2018 County Population", fontsize=24)
    plt.xlim(0, 550)
    plt.show()



if __name__ == "__main__":
    main()