import networkx as nx
import matplotlib.pyplot as plt
import json


# Define the graph as a dictionary
graph_dict = {
    "A": {"B": {"volume": "?"}, "C": {"volume": 3}, "D": {"volume": 2}},
    "B": {"A": {"volume": "?"}, "E": {"volume": 3}, "F": {"volume": 6}},
    "C": {"A": {"volume": 4}, "G": {"volume": "?"}, "H": {"volume": 3}},
    "D": {"A": {"volume": 3}, "I": {"volume": 6}, "J": {"volume": 8}},
    "E": {"B": {"volume": 5}, "K": {"volume": 7}},
    "F": {"B": {"volume": 7}, "L": {"volume": 4}},
    "G": {"C": {"volume": "?"}, "M": {"volume": 6}},
    "H": {"C": {"volume": 3}, "N": {"volume": 5}},
    "I": {"D": {"volume": 7}, "O": {"volume": 5}},
    "J": {"D": {"volume": 7}, "P": {"volume": 8}},
    "K": {"E": {"volume": 8}},
    "L": {"F": {"volume": 3}},
    "M": {"G": {"volume": 7}},
    "N": {"H": {"volume": 2}},
    "O": {"I": {"volume": 10}},
    "P": {"J": {"volume": 8}},
}

# Save graph_dict as json for further usage
with open("graphJson.json", "w") as f:
    json.dump(graph_dict, f, indent=4)

# Create an empty directed graph
G = nx.DiGraph()

# Iterate through the dictionary and add edges along with their attributes
for node, neighbors in graph_dict.items():
    for neighbor, attributes in neighbors.items():
        G.add_edge(node, neighbor, **attributes)

H=G.to_undirected()

# Merge parallel edges and sum their volumes
edges=list(H.edges(data=True))
for u, v, data in edges:
    if H.has_edge(v, u):
        data["volume"] += H[v][u]["volume"]
        #H.remove_edge(v, u)

def fill_missing_volumes(H):
    for u, v, data in H.edges(data=True):
        if "volume" not in data:
            # Check edges before and after
            neighbors = list(H.neighbors(u)) + list(H.neighbors(v))
            volumes = [H[u][n].get("volume", 0) for n in neighbors]
            volumes += [H[v][n].get("volume", 0) for n in neighbors]
            volumes = [v for v in volumes if v is not None]
            if len(volumes) > 0:
                avg_volume = sum(volumes) / len(volumes)
                data["volume"] = avg_volume
    return H

H= fill_missing_volumes(H)

pos = nx.spring_layout(H, seed=2)
labels = {(u, v): data["volume"] for u, v, data in H.edges(data=True)}

plt.figure(figsize=(10, 10))
nx.draw(H, pos=pos, with_labels=True)
nx.draw_networkx_edge_labels(
    H, pos, labels, label_pos=0.3, bbox=dict(alpha=0), font_size=10
)
nx.draw_networkx_edges(H, pos, arrows=True)
plt.savefig("undirected_digraphFromDict.png", dpi=400)
plt.show()