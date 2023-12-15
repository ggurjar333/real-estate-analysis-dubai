"""Datastore manages data retrieval for READ datasets."""
import read
import os
from typing import Annotated, Any, Self
import re

import requests
from pydantic import HttpUrl, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


from read.workspace.huspy import DataFactory

logger = read.logging_helpers.get_logger(__name__)

HuspyDoi = Annotated[
    str,
    StringConstraints(
        strict=True, min_length=16, pattern=r"search"
    ),
]


class HuspyDoiSettings(BaseSettings):
    """Digital Object Identifiers pointing to currently used Huspy API. """
    LIMIT_5000: HuspyDoi = '?limit=5000'
    GEO_LIMIT_5000: HuspyDoi = 'geo?limit=5000'

    model_config = SettingsConfigDict(env_prefix="read_huspy_doi_", env_file=".env")


class HuspyFetcher:
    """API for fetching contents from Huspy."""
    huspy_dois: HuspyDoiSettings()
    timeout: float
    http: requests.Session()

    def __init__(self: Self, huspy_dois: HuspyDoiSettings | None= None, timeout: float = 15.0):
        """Constructs HuspyFetcher instance."""
        self.huspy_dois = HuspyDoiSettings() or huspy_dois
        self.timeout = timeout

        retries = Retry(backoff_max=2, total=3, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.http = requests.Session()
        self.http.mount("https://", adapter)
    
    def get_doi(self: Self, dataset: str) -> HuspyDoi:
        """Returns DOI for given dataset."""
        try:
            doi = self.huspy_dois.__getattribute__(dataset)
        except AttributeError:
            raise AttributeError(f"No Huspy DOI found for dataset {dataset}.")
        return doi

    def get_known_resources(self: Self) -> list[str]:
        """Returns list of supported datasets."""
        return [name for name, doi in sorted(self.huspy_dois)]

    def _get_url(self: Self, doi: HuspyDoi) -> HttpUrl:
        """Create a Huspy deposition URL based on its Huspy DOI"""
        match = re.search(r"search", doi)

        if match is None:
            raise ValueError(f"Invalid Huspy DOI: {doi}")

        doi_prefix = match.groups()[0]
        huspy_id = match.groups()[1]
        if doi_prefix == 'limit=5000':
            api_root = "https://huspy.com/api/search?"
        elif doi_prefix == 'geo?limit=5000':
            api_root = "https://huspy.com/api/search/"
        else:
            raise ValueError(f"Invalid Huspy DOI: {doi}")
        return f"{api_root}{huspy_id}"

    def _fetch_from_url(self: Self, url: HttpUrl) -> requests.Response:
        logger.info(f"Retrieving {url} from Huspy")
        response = self.http.get(url = url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded {url}")
            return response
        raise ValueError(f"Could not download {url}: {response.text}")
    
    def get_descriptor(self: Self, dataset: str)


 #   def _fetch_from_url(self, collection_name):
 #       data_crawler = DataFactory.create_crawler(url=self.url, database_name=self.mongodb_name, collection_name=collection_name, uri=self.mongodb_uri)
 #       data_crawler.dump_to_mongodb()
