import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import datetime


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
            db = client[self.database_name]
            collection = db[self.collection_name]
            collection.insert_many(self.get_data())
            print(f"Raw Data successfully dumped to MongoDB!")
        except Exception as e:
            print(e)
        

class DataFactory:
    @staticmethod
    def create_crawler(url, database_name, collection_name, uri):
        return DataCrawler(url, database_name, collection_name, uri)


url = os.environ.get('URL')
mongo_database_uri = os.environ.get('MONGO_DATABASE_URI')
mongo_database_name = os.environ.get('MONGO_DATABASE_NAME')
mongodb_collection_name = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"


data_crawler = DataFactory.create_crawler(url=url, database_name=mongo_database_name, collection_name=mongodb_collection_name, uri=mongo_database_uri)
data_crawler.dump_to_mongodb()
