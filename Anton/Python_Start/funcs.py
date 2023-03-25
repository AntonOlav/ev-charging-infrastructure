import networkx as nx
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 
import numpy as np
import scipy.special
import shapely
from shapely.geometry import Point, Polygon, LineString 
from shapely.ops import nearest_points
from scipy import sparse
import grinpy
import time








def calculate_batterycost_single(grade, length):
# Coefficients indiciate consumption in kWh per KILOMETER
# Numbers from https://www.sciencedirect.com/science/article/pii/S1361920917303887 
    coefficients = [-0.332, -0.217, -0.148, -0.121, -0.073, 0.085, 0.152, 0.203, 0.306, 0.358, 0.552]
    gradients = [-0.09, -0.07, -0.05, -0.03, -0.01, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11]
    const = 0.372
    coeffs = {}
    for i in enumerate(gradients):
        _index = i[0]
        value = i[1]
        coeffs[value] = coefficients[_index]

    cost = None
    # If not ferry:
    if length != 0:
    
        # Messy...
        kwh_cost = None

        if grade == 0:
            kwh_cost = 0

        kwh_cost = None
        if grade < gradients[0]:                    # Up to -9%
            kwh_cost = coefficients[0]      
        if gradients[0] <= grade < gradients[1]:    # -9 to -7%
            kwh_cost = coefficients[1]  
        if gradients[1] <= grade < gradients[2]:     # -7 to -5%
            kwh_cost = coefficients[2]
        if gradients[2] <= grade < gradients[3]:     # -5 to -3% 
            kwh_cost = coefficients[3]
        if gradients[3] <= grade < gradients[4]:     # -3 to -1%
            kwh_cost = coefficients[4]
        if gradients[4] <= grade < gradients[5]:     # 1 to 3% 
            kwh_cost = coefficients[5]
        if gradients[5] <= grade < gradients[6]:    # 3 to 5%
            kwh_cost = coefficients[6]
        if gradients[6] <= grade < gradients[7]:     # 5 to 7%
            kwh_cost = coefficients[7]
        if gradients[7] <= grade < gradients[8]:    # 7 to 9%
            kwh_cost = coefficients[8]
        if gradients[8] <= grade <= gradients[9]:   # 9 to 11%
            kwh_cost = coefficients[9]
        if grade > gradients[9]:                    # More than 11%
            kwh_cost = coefficients[10]

            # print(kwh_cost)
        cost = (const + kwh_cost)/1000 * length
    if length == 0:
        cost = 0
    # print("Gradient is {} and length is {}. Cost is {}".format(grade, length, cost))
    return cost




def shorten_edges_by_cutoff(G: nx.graph, cutoff:float):
    """
    Function for shortening edges to a specific cutoff threshold. Guarantees that any node can be reached with any range. Divides every edge > cutoff by 2 until no edge surpasses the cutoff value. 
    """

    edges = [e for e in G.edges]
    edges_length = len(edges)
    counter = 0
    new_nodes = []
    edges_shortened = 0

    for e in edges:
        counter += 1
        max_index = max(G.nodes)
        # print("Progess:\t {}".format(counter/edges_length))
        try:
            edge_data = G.edges[e]
            geometry = edge_data['geometry']

            # BEGIN Calculate cost iteratively ================================= 
            source = e[0]
            target = e[1]
            s_elevation = G.nodes[source]['elevation']
            n_elevation = G.nodes[target]['elevation']
            length = edge_data['length']
            if length == 0:
                continue 

            if s_elevation > n_elevation:
                rise = n_elevation - s_elevation
                grade = rise/length
                # print("Edge goes downwards:{}".format(grade))
            # If source elevation is lower than neighbor's, grade is positive
            if s_elevation < n_elevation:
                rise = n_elevation - s_elevation
                grade = rise/length
                # print("Edge goes upwards:{}".format(grade))
            if s_elevation == n_elevation:
                rise = 0 
                grade = 0 

            cost = calculate_batterycost_single(grade, length)
            # END Calculate cost iteratively ================================= 

            # TESTING WITH LOWER CUTOFF VALUE!!! 
            if cost > cutoff:
                # print(cost)
                max_index += 1
                # print("Edge {} surpasses cutoff threshold with edge cost {}".format(e, cost))

                # Retrieve start and end node
                start_node = e[0]
                end_node = e[1]

                # Get coordinates of nodes
                start_node_x = G.nodes[start_node]['x']
                start_node_y = G.nodes[start_node]['y']
                end_node_x = G.nodes[end_node]['x']
                end_node_y = G.nodes[end_node]['y']
                
                # Get roadclass, tunnel and bridge (assuming same as start node)
                roadclass = G.nodes[start_node]['roadclass']
                isbridge = 0
                istunnel = 0
                elevation = G.nodes[start_node]['elevation']

                # Get middle-point between nodes (for new node)
                new_x = (start_node_x + end_node_x)/2
                new_y =  (start_node_y + end_node_y)/2

                # Create Point object
                newpoint = Point([new_x, new_y])

                # Get nearest point along original edge geometry
                np = nearest_points(geometry, newpoint)[0]

                # Add node between start_node and end_node
                # set artificial = True so we know which nodes are inserted into the network
                G.add_node(max_index, x = np.x, y = np.y, osmid = max_index, elevation = elevation, isBridge = isbridge, isTunnel = istunnel, roadclass = roadclass,  geometry = np, artificial = True)
                # Create new geometry between nodes
                first_half = LineString([Point(start_node_x, start_node_y), np])
                second_half = LineString([np, Point(end_node_x, end_node_y)])

                # Create edge between old nodes and new node, delete previous unfeasible edge
                G.add_edge(start_node, max_index,
                id = None, oneway = edge_data['oneway'], ref = edge_data['ref'], 
                name = edge_data['name'], funcroadclass = edge_data['funcroadclass'],
                roadclass = edge_data['roadclass'], isFerry = edge_data['isFerry'], isBridge = isbridge, isTunnel = istunnel, 
                speedlim = edge_data['speedlim'], length = length/2, geometry = first_half, grade = 0, grade_abs = 0)

                G.add_edge(max_index, end_node,
                id = None, oneway = edge_data['oneway'], ref = edge_data['ref'], 
                name = edge_data['name'], funcroadclass = edge_data['funcroadclass'],
                roadclass = edge_data['roadclass'], isFerry = edge_data['isFerry'], isBridge = isbridge, isTunnel = istunnel, 
                speedlim = edge_data['speedlim'], length = length/2, geometry = second_half, grade = 0, grade_abs = 0)

                # print("Edge added...")

                G.remove_edge(e[0], e[1])
                new_nodes.append(max_index)
                edges_shortened += 1

        except KeyError as KE:
            # print("ERROR:\t{}".format(e))
            pass

    if edges_shortened > 0:
        print("Performing recursion...")
        shorten_edges_by_cutoff(G = G, cutoff = cutoff)
    else:
        print("No condition satisfied. Recursion ended and function completed.")
        pass  


