import requests

import csv
import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import datetime


load_dotenv()

class DataCrawler:
    def __init__(self, url, database_name, collection_name, uri):
        self.url = url
        self.database_name = database_name
        self.collection_name = collection_name
        self.uri = uri

    def get_data(self):
        response = requests.get(url=self.url).json()
        return response["listings"]

    def dump_to_mongodb(self):
        client = MongoClient(self.uri, server_api=ServerApi('1'))
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        db = client[self.database_name]
        collection = db[self.collection_name]
        collection.insert_many(self.get_data())
        print(f"Raw Data successfully dumped to MongoDB!")
    

class CSVDataWriter:
    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = fieldnames

    def write_to_csv(self, data):
        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)


class DataFactory:
    @staticmethod
    def create_crawler(url, database_name, collection_name, uri):
        return DataCrawler(url, database_name, collection_name, uri)

    @staticmethod
    def create_csv_writer(filename, fieldnames):
        return CSVDataWriter(filename, fieldnames)

url = os.getenv('URL')
mongo_database_uri = os.getenv('MONGO_DATABASE_URI')
mongo_database_name = os.getenv('MONGO_DATABASE_NAME')
mongodb_collection_name = f"{mongo_database_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}"

filename_csv = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_extracted_data.csv"
fieldnames = ["title", "price", "area_square_meters", "area_square_feet", "bedrooms", "bathrooms", "latitude", "longitude", "property_type"]

data_crawler = DataFactory.create_crawler(url=url, database_name=mongo_database_name, collection_name=mongodb_collection_name, uri=mongo_database_uri)
data_crawler.dump_to_mongodb()

# Connect to MongoDB and extract data from mongodb_collection_name
client = MongoClient(mongo_database_uri)
db = client[mongo_database_name]
collection = db[mongodb_collection_name]
extracted_data = list(collection.find())

# Print element from extracted_data
# for i in range(len(extracted_data)):
#     print(extracted_data[i]['title'])
#     print(extracted_data[i]['price'])


# csv_data_writer = DataFactory.create_csv_writer(filename_csv, fieldnames)
# csv_data_writer.write_to_csv(extracted_data)

# csv_data_writer.write_to_csv(data_crawler.extract_data())
