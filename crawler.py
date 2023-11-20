import requests
import json
import csv
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class DataCrawler:
    def __init__(self, url):
        self.url = url
        self.data = self.get_data()
        self.extracted_data = self.extract_data()

    def get_data(self):
        json_data = json.JSONEncoder().encode(requests.get(url=self.url).json())
        return json.loads(json_data)

    def extract_data(self):
        extracted_data = []
        for listing in self.data["listings"]:
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
        return extracted_data

    def write_json_data(self, filename):
        with open(filename, 'w') as jsonfile:
            json.dump(self.data, jsonfile)

class CSVDataWriter:
    def __init__(self, filename, fieldnames):
        self.filename = filename
        self.fieldnames = fieldnames

    def write_to_csv(self, data):
        with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

class DataFactory:
    @staticmethod
    def create_crawler(url):
        return DataCrawler(url)

    @staticmethod
    def create_csv_writer(filename, fieldnames):
        return CSVDataWriter(filename, fieldnames)

url = os.getenv('URL')

# filename should have current date and time
filename_json = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_crawled_data.json"
filename_csv = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_extracted_data.csv"
fieldnames = ["title", "price", "area_square_meters", "area_square_feet", "bedrooms", "bathrooms", "latitude", "longitude", "property_type"]

data_crawler = DataFactory.create_crawler(url)
csv_data_writer = DataFactory.create_csv_writer(filename_csv, fieldnames)

data_crawler.write_json_data(filename_json)
csv_data_writer.write_to_csv(data_crawler.extracted_data)