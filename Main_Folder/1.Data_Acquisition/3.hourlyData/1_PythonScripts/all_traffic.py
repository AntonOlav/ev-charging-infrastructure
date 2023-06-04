import os
import json
import requests
import time
import random
from tqdm import tqdm  


# define the base path where the file should be saved
base_path = r"C:\Users\anton\Desktop\Master-Oppgave\Anton\Kode\All_Roads\JSON"

# define the file name
file_name = "all_IDs.json"

# combine the base path and file name to create a valid file path
file_path = os.path.join(base_path, file_name)

# define the endpoint of the API
endpoint = "https://www.vegvesen.no/trafikkdata/api/?query=%0A%20%20%20%20query%7B%0A%20%20%20%20%20%20trafficRegistrationPoints(searchQuery%3A%20%7BroadCategoryIds%3A%20%5BE%5D%20%7D)%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20location%20%7B%0A%20%20%20%20%20%20%20%20%20%20coordinates%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20latLon%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20lat%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20lon%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%0A%20"

# define the GraphQL query for fetching ID's of registration points (only Europe roads)
query = """
{
  trafficRegistrationPoints(searchQuery: {roadCategoryIds: [E ,R, F], registrationFrequency: CONTINUOUS}) {
    id
  }
}
"""

# make a POST request to the API
response = requests.post(endpoint, json={"query": query})

# check the status code of the response
if response.status_code == 200:
    # if the request was successful, get the data from the response
    data = response.json()

    # open the file for writing
    with open(file_path, "w") as file:
        # write the data to the file in JSON format
        json.dump(data, file)



# define the file path of the JSON file
file_path = r"C:\Users\anton\Desktop\Master-Oppgave\Anton\Kode\All_Roads\JSON\all_IDs.json"

# open the file for reading
with open(file_path, "r") as file:
    # load the data from the file into a Python object
    data = json.load(file)

# create an empty list for the registration point ID's
registration_point_ids = []

# iterate over the data returned by the GraphQL query
for item in data["data"]["trafficRegistrationPoints"]:
    # get the ID of the current registration point
    id = item["id"]

    # add the ID to the list of registration point ID's
    registration_point_ids.append(id)

# print the list of registration point ID's to the console
#print(registration_point_ids)


# define the endpoint of the API
endpoint = """https://www.vegvesen.no/trafikkdata/api/?query=%7B%0A%20%20trafficData(trafficRegistrationPointId%3A%20%'DISTINCT_ID'%22)%20%7B%0A%20%20%20%20volume%20%7B%0A%20%20%20%20%20%20byHour(%0A%20%20%20%20%20%20%20%20from%3A%20%222019-10-24T12%3A00%3A00%2B02%3A00%22%0A%20%20%20%20%20%20%20%20to%3A%20%222019-10-24T14%3A00%3A00%2B02%3A00%22%0A%20%20%20%20%20%20)%20%7B%0A%20%20%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20from%0A%20%20%20%20%20%20%20%20%20%20%20%20to%0A%20%20%20%20%20%20%20%20%20%20%20%20total%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20volumeNumbers%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20volume%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20coverage%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20percentage%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A"""

# define the list of registration point ID's

#registration_point_ids = ["73166V180782", "73007V249534", "03614V1740869"]

data = []
with tqdm(total=len(registration_point_ids)) as pbar:
  for registration_point_id in registration_point_ids:
    time.sleep(random.uniform(1, 3))
    #print("ID:", registration_point_id)
  # define the GraphQL query, (add "%s" in ID for all )
    query = """
{
      trafficData(trafficRegistrationPointId: "%s") {
        trafficRegistrationPoint {
          id
          name
          location {
            coordinates {
              latLon {
                lat
                lon
              }
            }
          }
        }
        volume {
          average{
            daily{
              byMonth(year: 2018, dayType: ALL) {
                from
                to
                dayType
                total{
                  volume {
                  	average
                }
                }
              }
              }
            }
        	}
  			}
}
    """ % registration_point_id
    # make a POST request to the API
    response = requests.post(endpoint, json={"query": query})
    # check the status code of the response
    if response.status_code == 200:
      # if the request was successful, get the volume data from the response
      volume_data = response.json()

      # # check if the volume data is not empty
      # if volume_data["data"]["trafficData"]["volume"]["average"]:

        # associate the volume data with the corresponding traffic registration point
        #for item in data["data"]["trafficRegistrationPoints"]:
        #  if item["id"] == registration_point_id:
        #    item["volume_data"] = volume_data

      data.append(volume_data)
      
      # update the progress bar
      pbar.update(1)

# define the path and filename for the JSON file
filename1 = r"C:\Users\anton\Desktop\Master-Oppgave\Anton\Kode\All_Roads\JSON\volume_all.json"

# write the data to the JSON file
with open(filename1, "w") as f:
    json.dump(data, f, indent=2)