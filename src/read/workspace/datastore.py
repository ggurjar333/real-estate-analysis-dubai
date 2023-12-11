"""Datastore manages data retrieval for READ datasets."""
import read
import os
from read.workspace.huspy import DataFactory

logger = read.logging_helpers.get_logger(__name__)


class HuspyFetcher:
    """API for fetching contents from Huspy."""

    def __init__(self, url, mongodb_uri, mongodb_name):
        self.url = url
        self.mongodb_uri = mongodb_uri
        self.mongodb_name = mongodb_name

    def _fetch_from_url(self, collection_name):
        data_crawler = DataFactory.create_crawler(url=self.url, database_name=self.mongodb_name, collection_name=collection_name, uri=self.mongodb_uri)
        data_crawler.dump_to_mongodb()