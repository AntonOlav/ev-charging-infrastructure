import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 
import numpy as np
import requests
import geopandas as gpd
import shapely
from shapely.geometry import Point, Polygon, LineString 
from shapely.ops import nearest_points
from functools import partial
import geopandas as gpd
import pyproj
from shapely.ops import transform

# Load environment variables from .env 

GOOGLE_API = ("AIzaSyB_PsG0h91CTn9wNe2MrGB35HSerZN-dnM")

from funcs import * 


# Read GeoJson package from Vegvesen
max_roadclass = 3

ruttger_link_geom = gpd.read_file(r"C:\Users\anton\Documents\Master-Oppgave\Kode\geo\ruttger_link_03.geojson")
crs_name = 'epsg:4326'

# Add "length" column
ruttger_link_geom['length'] = ruttger_link_geom['geometry'].length

# Transform project into lat-long coordinate system (ESPG:4326)
project = pyproj.Transformer.from_proj(
    pyproj.Proj(init='epsg:8687'), # source coordinate system
    pyproj.Proj(init='epsg:4326')) # destination coordinate system

# Apply transformation
ruttger_link_geom['geometry'] = ruttger_link_geom['geometry'].apply(lambda x: transform(project.transform, x))

def build_network_data(GeoData):    
    """
    Returns node-dict and edge-dict which is networkx compatible network from Vegvesenets routable data available at https://kartkatalog.geonorge.no/metadata/statens-vegvesen/nvdb-ruteplan-nettverksdatasett/8d0f9066-34f9-4423-be12-8e8523089313 
    """

    # Get unique nodes
    nodes = {}

    print("Beginning tonodes...")
    for i in GeoData.drop_duplicates('tonode').index:

        # Get node ID for filtering duplicates
        _id          = GeoData.iloc[i]['tonode']

        # Only keep unique observations
        if _id not in nodes:
            # Get attributes if applicable, else get centroid coordinate in linestring (error usually indicate roundabout as one edge)
            try:
                x        = GeoData.iloc[i]['geometry'].boundary[-1].x
                y        = GeoData.iloc[i]['geometry'].boundary[-1].y
                roadclass = int(GeoData.iloc[i]['funcroadclass'])
                isBridge = int(GeoData.iloc[i]['isbridge'])
                isTunnel = int(GeoData.iloc[i]['istunnel'])
                geometry = Point(x,y)
            except Exception as e:
                x        = GeoData.iloc[i]['geometry'].centroid.x
                y        = GeoData.iloc[i]['geometry'].centroid.y
                roadclass = int(GeoData.iloc[i]['funcroadclass'])
                isBridge = int(GeoData.iloc[i]['isbridge'])
                isTunnel = int(GeoData.iloc[i]['istunnel'])
                geometry = Point(x,y)

            # Save and append
            content = {'x':x,'y':y,'osmid':_id, 'roadclass': roadclass, 'isBridge': isBridge, 'isTunnel': isTunnel, 'geometry':geometry}
            nodes[_id] = content
        else:
            pass

    # DO SIMILAR FOR FROMNODE:
    print("Beginning fromnodes...")
    for i in GeoData.drop_duplicates('fromnode').index:
            # Get node ID for filtering duplicates
        _id         = GeoData.iloc[i]['fromnode']

        # Only keep unique observations
        if _id not in nodes:
            # Get attributes if applicable, else get random coordinate in linestring (error usually indicate roundabout as one edge)
            try:
                x        = GeoData.iloc[i]['geometry'].boundary[-1].x
                y        = GeoData.iloc[i]['geometry'].boundary[-1].y
                roadclass = int(GeoData.iloc[i]['funcroadclass'])
                # isBridge = int(GeoData.iloc[i]['isbridge'])
                # isTunnel = int(GeoData.iloc[i]['istunnel'])
                geometry = Point(x,y)
            except Exception as e:
                x        = GeoData.iloc[i]['geometry'].centroid.x
                y        = GeoData.iloc[i]['geometry'].centroid.y
                roadclass = int(GeoData.iloc[i]['funcroadclass'])
                isBridge = int(GeoData.iloc[i]['isbridge'])
                isTunnel = int(GeoData.iloc[i]['istunnel'])
                geometry = Point(x,y)

            # Save and append
            content = {'x':x,'y':y,'osmid':_id, 'roadclass': roadclass, 'isBridge': isBridge, 'isTunnel': isTunnel, 'geometry':geometry}
            nodes[_id] = content
        else:
            pass


    # Get edges into networkx format
    edges = {}
    print("Beginning edges...")
    for i in GeoData.index:
        # Lets keep edges undirected for now (not one way)
        # Get edge ID for filtering duplicates:
        _id                 = GeoData.iloc[i]['linkid']

        # Get only data of edges not already retrieved
        if _id not in edges:
            ref                 = GeoData.iloc[i]['streetname'] 
            funcroadclass       = GeoData.iloc[i]['funcroadclass']
            roadclass           = GeoData.iloc[i]['roadclass']
            isFerry             = GeoData.iloc[i]['isferry']
            isBridge            = GeoData.iloc[i]['isbridge']
            isTunnel            = GeoData.iloc[i]['istunnel']
            speedlim            = GeoData.iloc[i]['speedfw']
            drivetime           = GeoData.iloc[i]['drivetime_fw']
            oneway              = False if GeoData.iloc[i]['oneway'] == "B" else False
            geometry            = GeoData.iloc[i]['geometry']
            u                   = GeoData.iloc[i]['fromnode']
            v                   = GeoData.iloc[i]['tonode']
            key                 = 0

            # linestring_trans = transform(project, GeoData.iloc[i]['geometry'])
            length = GeoData.iloc[i]['length'] - isFerry * GeoData.iloc[i]['length']
            length_weight = length.copy()

            # Estimate length based on speedlimit and drivetime
            # length_estimated = speedlim*drivetime*1000/60

            # Create dictionary of node data:
            content = {'id':_id, 'oneway':oneway, 'ref':ref, 'name':ref, 'funcroadclass':funcroadclass, 'roadclass':roadclass, 'isFerry':isFerry, 'isBridge':isBridge, 'isTunnel':isTunnel, 'speedlim':speedlim, 'drivetime':drivetime, 'length':length, 'length_weight':length_weight, 'geometry':geometry,'u':u, 'v':v, "key": key}

            edges[(u,v,0)] = content
        else:
            pass 

    # Set crs system
    crs = {'init': crs_name}

    # Create for nodes
    nodes_df = gpd.GeoDataFrame(nodes).T
    nodes_df = gpd.GeoDataFrame(
        nodes_df, geometry=nodes_df['geometry'])

    # Create for edges
    edges_df = gpd.GeoDataFrame(edges).T
    edges_df = gpd.GeoDataFrame(
        edges_df, geometry=edges_df['geometry'])


    return nodes_df, edges_df

# Use function created above to construct data
nodes, edges = build_network_data(ruttger_link_geom)

# Create graph from geodataframes
graph_attrs = {'crs': 'epsg:4326', 'simplified': False}
G = ox.graph_from_gdfs(nodes, edges.drop('key', axis = 1), graph_attrs = graph_attrs)

# Only keep mainland (or reachable islands)
start_node = ox.get_nearest_node(G, (59.9098, 10.7146))
F = G.subgraph(nx.shortest_path(G.to_undirected(), start_node))


# Retrieve elevation of each node and grade of edges (You'll need your own Google Cloud Console API for this)
H_elev = ox.elevation.add_node_elevations(F, api_key=GOOGLE_API)
H_elev = ox.elevation.add_edge_grades(H_elev)

# Copy H_elev
H = H_elev.copy()

# Remove inf and -inf values 
for i in H.edges:
    grade = H.edges[i]['grade']
    if grade == float('inf'):
        # print("grade is inf")
        H.edges[i]['grade'] = 0
    if grade == float('-inf'):
        # print("grade is -inf")
        H.edges[i]['grade'] = 0
    if np.isnan(grade):
        # print("grade is nan")
        H.edges[i]['grade'] = 0

# Remove geometry because it is unhashable and not compatible with ox.simplify_graph

# Apparently it is not unhashable anymore...
att_list = ['geometry']
for n1, n2, d in H.edges(data=True):
    for att in att_list:
        d.pop(att, None)

# Convert roadclass to int, because simplification appends it to list
for i in H.edges:
    data = H.edges[i]
    roadclass = data['funcroadclass']
    if type(roadclass) == list:
        # Keep minimum roadclass
        roadclass = min(roadclass)
    data['funcroadclass'] = roadclass

# Simplify graph, intersections along highways are kept intact. 
# BUT FIRST MANUALLY CHANGE A LINE OF CODE IN THE ORIGINAL OSMNX 1.01 LIBRARY
# Line 273 n osmnx/simplification.py should be changed to:
# edge_attributes[key] = list(edge_attributes[key])

print("Remember to change OSMNX source code to fit our purpose, see comment above this print statement...")
H = ox.simplify_graph(H)

# Shorten edges by cutoff value of 10kwh (adjust this value if you want to have vertices closer together)
# Takes a while
shorten_edges_by_cutoff(H, 10)


# Compute weighted (of length) average grade for each edge that has been simplified
# OSMNX source code is changed for this purpose
for i in H.edges:
    if type(H.edges[i]['grade']) == list:
        grades = H.edges[i]['grade']
        length_weight = H.edges[i]['length_weight']
        # numpy average function for calculating averages with weights
        if len(grades) == len(length_weight):
            wa = np.average(grades, weights=length_weight, axis=0) #I included axis=0 to this argument
            H.edges[i]['wa_grade'] = wa
        else:
            print("Error: length_weight and grades must have the same length")

        
    else:
        grade = H.edges[i]['grade']
        H.edges[i]['wa_grade'] = grade

# Convert faulty converted oneway attribute 
for i in H.edges:
    if type(H.edges[i]['oneway']) == list:
        H.edges[i]['oneway'] = False 

# Save as pickle object
path = 'pickle/BaseGraph0{}_NOR_wagrades.pickle'.format(max_roadclass)
nx.write_gpickle(H.to_undirected(), path)

print("Data transformation completed. Output saved at {}".format(path))