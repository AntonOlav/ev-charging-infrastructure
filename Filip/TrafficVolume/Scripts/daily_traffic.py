import os
import json
import requests
import time



# define the base path where the file should be saved
base_path = r"TVolume_data"

# define the file name
file_name = "point_data_test.json"

# combine the base path and file name to create a valid file path
file_path = os.path.join(base_path, file_name)

# define the endpoint of the API
endpoint = "https://www.vegvesen.no/trafikkdata/api/?query=%0A%20%20%20%20query%7B%0A%20%20%20%20%20%20trafficRegistrationPoints(searchQuery%3A%20%7BroadCategoryIds%3A%20%5BE%5D%20%7D)%20%7B%0A%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20location%20%7B%0A%20%20%20%20%20%20%20%20%20%20coordinates%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20latLon%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20lat%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20lon%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%0A%20"


query_2 = """
{
  trafficRegistrationPoints(searchQuery: {roadCategoryIds: [E]}) {
    id
  }
}
"""


# make a POST request to the API
response = requests.post(endpoint, json={"query": query_2})

# check the status code of the response
if response.status_code == 200:
    data = response.json()

    # open the file for writing
    with open(file_path, "w") as file:
        json.dump(data, file)


#####


# define the file path of the JSON file
file_path = r"TVolume_data/point_data_test.json"

# open the file for reading
with open(file_path, "r") as file:
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
print(registration_point_ids)


# define the endpoint of the API
endpoint = """https://www.vegvesen.no/trafikkdata/api/?query=%7B%0A%20%20trafficData(trafficRegistrationPointId%3A%20%'DISTINCT_ID'%22)%20%7B%0A%20%20%20%20volume%20%7B%0A%20%20%20%20%20%20byHour(%0A%20%20%20%20%20%20%20%20from%3A%20%222019-10-24T12%3A00%3A00%2B02%3A00%22%0A%20%20%20%20%20%20%20%20to%3A%20%222019-10-24T14%3A00%3A00%2B02%3A00%22%0A%20%20%20%20%20%20)%20%7B%0A%20%20%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20from%0A%20%20%20%20%20%20%20%20%20%20%20%20to%0A%20%20%20%20%20%20%20%20%20%20%20%20total%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20volumeNumbers%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20volume%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20coverage%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20percentage%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A"""

# define the list of registration point ID's

data = []

for i in range(len(registration_point_ids)):
    if i % 20 == 19:
        time.sleep(2)
        for id_ in registration_point_ids:
            print("ID:", id_)
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
            byMonth(year: 2022, dayType: ALL){
              year
              month
              from
              dayType
              total{
                volume{
                  average
                 } 
                }
              byDirection{
                heading
                total{
                  volume{
                    average
                  }
                  coverage{
                    percentage
                  }
                }
              }
              }
            }
          }
        }
      }
  }
  """ % id_
        # make a POST request to the API
        response = requests.post(endpoint, json={"query": query})
        # check the status code of the response
        if response.status_code == 200:
        # if the request was successful, get the volume data from the response
            volume_data = response.json()
            data.append(volume_data)

        else: 
            pass


# define the path and filename for the JSON file
filename1 = r"TVolume_data/Monthly_Volume_data"

# write the data to the JSON file
with open(filename1, "w") as f:
    json.dump(data, f, indent=2)






