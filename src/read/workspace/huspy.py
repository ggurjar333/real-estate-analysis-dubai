import os
import datetime
from typing import Any, Self

import requests
from pydantic import HttpUrl
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import read

logger = read.logging_helpers.get_logger(__name__)

class DataCrawler:
    # def __init__(self, url, database_name, collection_name, uri):
    #     self.url = url
    #     self.database_name = database_name
    #     self.collection_name = collection_name
    #     self.uri = uri

    timeout: float
    http: requests.Session

    def __init__(self: Self, timeout: float = 15.0):
        self.timeout = timeout
        retries = Retry(
            backoff_max=2, total=3, status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.http = requests.Session()

    def _fetch_from_url(self: Self, url: HttpUrl) -> requests.Response:
        logger.info(f'Retrieving {url} from Huspy')
        response = self.http.get(url=url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded {url}")
            return response
        raise ValueError(f"Could not download {url}: {response.text}")


    def get_descriptor(self: Self, dataset:str):

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

# url = os.environ.get('URL')
# mongo_database_uri = os.environ.get('MONGO_DATABASE_URI')
# mongo_database_name = os.environ.get('MONGO_DATABASE_NAME')
# mongodb_collection_name = f"{datetime.datetime.now().strftime('%Y-%m-%d')}"
#
#
# data_crawler = DataFactory.create_crawler(url=url, database_name=mongo_database_name, collection_name=mongodb_collection_name, uri=mongo_database_uri)
# data_crawler.dump_to_mongodb()
