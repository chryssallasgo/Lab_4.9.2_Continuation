#Team name: TEAMPOORAH
#Member names: Iway, Mark Jorland
#Allasgo, Chryssdale Heart
#Marte, Ares Daniel
#Lumapas, Nina Regene

import requests
import urllib.parse
import folium
import webbrowser
import os

route_url = "https://graphhopper.com/api/1/route?"
key = "211c0ffb-2f42-4a89-a32f-a3cabaf536bd"  # Replace with your actual API key

def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    response = requests.get(url)
    json_status = response.status_code
    json_data = response.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        country = hit.get("country", "")
        state = hit.get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"Geocoding API URL for {new_loc}\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Geocode API status: {json_status}\nError message: {json_data.get('message', 'No message')}")
    return json_status, lat, lng, new_loc

#Feature 1, Map Visualization
def create_map(start_coords, end_coords, start_label, end_label):
    # Center the map between the two points
    map_center = [(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2]
    my_map = folium.Map(location=map_center, zoom_start=13)

    # Add markers
    folium.Marker(start_coords, popup=f"Start: {start_label}", icon=folium.Icon(color='green')).add_to(my_map)
    folium.Marker(end_coords, popup=f"End: {end_label}", icon=folium.Icon(color='red')).add_to(my_map)

    # Draw a line (route)
    folium.PolyLine([start_coords, end_coords], color="blue", weight=5, opacity=0.8).add_to(my_map)

    # Save to HTML and open
    map_filename = "route_map.html"
    my_map.save(map_filename)
    webbrowser.open('file://' + os.path.realpath(map_filename))


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")
    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)


    loc2 = input ("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print("==============================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" +
        paths_url)
        print("=================================================")
        create_map((orig[1], orig[2]), (dest[1], dest[2]), orig[3], dest[3])
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000,
distance/1000/1.61))
            print("=============================================")
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")


