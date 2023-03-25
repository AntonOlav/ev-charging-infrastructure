import numpy as np
import pandas as pd
import json

raw_data = json.load(open(r"C:\Users\anton\Desktop\Master-Oppgave\Kode\New_Traffic\JSON\volume_w_id.json"))

def flatten(item):
    return [
        {
            "id": item["data"]["trafficData"]["trafficRegistrationPoint"]["id"],
            "name": item["data"]["trafficData"]["trafficRegistrationPoint"]["name"],
            "date_from": edge["node"]["from"],
            "date_to": edge["node"]["to"],
            "volume": edge["node"]["total"]["volumeNumbers"]["volume"] if edge["node"]["total"]["volumeNumbers"] else np.nan,
        }
        for edge in item["data"]["trafficData"]["volume"]["byHour"]["edges"]
        if edge
    ]

data = []
for item in raw_data:
    data.extend(flatten(item))


df = pd.DataFrame(data)
df.head()
