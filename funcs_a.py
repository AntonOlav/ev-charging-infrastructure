import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt 
import matplotlib as mpl
import seaborn as sns 
import geopandas as gpd
import pandas as pd 
import numpy as np
import requests
import shapely
import pickle
import progressbar
import geopy.distance
from shapely.geometry import Point, Polygon, LineString 
from shapely.ops import nearest_points
from shapely.ops import transform
from shapely import geometry, ops
from functools import partial
from itertools import combinations
import geopandas as gpd
import pyproj
import os
import matplotlib.cm as cm
import matplotlib.colors as colors
from scipy.sparse import lil_matrix
import itertools
import warnings
warnings.simplefilter('ignore')
import random
from random import choice, randint
import timeit
import time
import threading
from multiprocessing import Pool
from joblib import Parallel, delayed

crs_name = 'epsg:4326'

def build_network_data(GeoData):    
    """
    Returns node-dict and edge-dict which is networkx compatible network from Vegvesenets routable data available at 
    https://kartkatalog.geonorge.no/metadata/statens-vegvesen/nvdb-ruteplan-nettverksdatasett/8d0f9066-34f9-4423-be12-8e8523089313 
    
    Created by Samuel Berntzen: https://github.com/samuelberntzen
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
            roadclass           = GeoData.iloc[i]['roadClass']
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
    nodes_df = gpd.GeoDataFrame(nodes, crs = crs).T
    nodes_df = gpd.GeoDataFrame(
        nodes_df, geometry=nodes_df['geometry'])

    # Create for edges
    edges_df = gpd.GeoDataFrame(edges, crs = crs).T
    edges_df = gpd.GeoDataFrame(
        edges_df, geometry=edges_df['geometry'])


    return nodes_df, 