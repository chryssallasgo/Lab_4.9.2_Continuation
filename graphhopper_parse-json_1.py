import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Roma, Italia"
loc2 = "Baltimore, Maryland"
key = "211c0ffb-2f42-4a89-a32f-a3cabaf536bd"

url = geocode_url + urllib.parse.urlencode({"q":loc1, "limit": "1", "key":key})

replydata = requests.get(url)
json_data = replydata.json()
json_status = replydata.status_code

json_status = replydata.status_code

if json_status == 200:
    print("Geocoding API URL for " + loc1 + ":\n" + url)