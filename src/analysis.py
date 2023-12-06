from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
import pandas as pd


class RealEstateAnalyzer:
    def __init__(self, mongo_database_uri, mongo_database_name):
        self.mongo_database_uri = mongo_database_uri
        self.mongo_database_name = mongo_database_name

    def connect_to_mongodb(self):
        client = MongoClient(self.mongo_database_uri)
        self.db = client[self.mongo_database_name]

    def extract_data(self):
        collection_name = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
        collection = self.db[collection_name]
        raw_data = list(collection.find())
        return raw_data

    def transform(self, raw_data):
        extracted_data = []
        for listing in raw_data:
            extracted_listing = {
                "title": listing["title"],
                "price": listing["price"],
                "area_square_meters": listing["area"]["squareMeters"],
                "area_square_feet": listing["area"]["squareFeet"],
                "bedrooms": listing["bedrooms"],
                "bathrooms": listing["bathrooms"],
                "latitude": listing["latitude"],
                "longitude": listing["longitude"],
                "property_type": listing["propertyType"]
            }
            extracted_data.append(extracted_listing)
        
        transformed_data = pd.DataFrame(extracted_data)
        transformed_data['bedrooms'] = transformed_data['bedrooms'].astype(float)
        transformed_data['bathrooms'] = transformed_data['bathrooms'].astype(float)
        transformed_data['bed_bath_ratio'] = transformed_data['bedrooms'] / transformed_data['bathrooms']

        return transformed_data
    
    def feature_engineering(self, transformed_data):
        transformed_data['price_range'] = pd.cut(transformed_data['price'], bins=[0, 100000, 200000, 300000, float('inf')], labels=['0-100k', '100k-200k', '200k-300k', '300k+'])
        transformed_data['price_per_sqft'] = transformed_data['price'] / transformed_data['area_square_feet']
        transformed_data['bed_bath_ratio'] = transformed_data['bedrooms'] / transformed_data['bathrooms']
        transformed_data['total_rooms'] = transformed_data['bedrooms'] + transformed_data['bathrooms']


# Create an instance of the RealEstateAnalyzer class
analyzer = RealEstateAnalyzer(os.getenv('MONGO_DATABASE_URI'), os.getenv('MONGO_DATABASE_NAME'))

# Connect to MongoDB
analyzer.connect_to_mongodb()

# Extract raw data
raw_data = analyzer.extract_data()

# Perform data transformation
transformed_data = analyzer.transform(raw_data)
print(transformed_data)
# Perform feature engineering
featured_data = analyzer.feature_engineering(transformed_data)
# print(featured_data)
# Save the DataFrame to JSON
# featured_data = pd.DataFrame(extracted_data)
# featured_data.to_json('featured_data.json', orient='records')
