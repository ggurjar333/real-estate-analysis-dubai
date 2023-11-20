import requests
import json
# json_data= requests.get(url='https://huspy.com/api/v1/search?lastItemId=').json()

json_data = json.JSONEncoder().encode(requests.get(url='https://huspy.com/api/v1/search?lastItemId=').json())
# Parse the JSON data
data = json.loads(json_data)

# Extract required elements from each listing
extracted_data = []
for listing in data["listings"]:
    extracted_listing = {
        "title": listing["title"],
        "price": listing["price"],
        "area-squareMeters": listing["area"]["squareMeters"],
        "area-squareFeet": listing["area"]["squareFeet"],
        "bedrooms": listing["bedrooms"],
        "bathrooms": listing["bathrooms"],
        "floor": listing["floor"],
        "latitude": listing["latitude"],
        "longitude": listing["longitude"],
        "propertyType": listing["propertyType"]
    }
    extracted_data.append(extracted_listing)

# Print the extracted data
for item in extracted_data:
    print(item)