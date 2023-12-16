"""Datastore manages data retrieval for READ datasets."""
import json

import read
import os
from typing import Annotated, Any, Self
import re

import requests
from pydantic import HttpUrl, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import datapackage

from read.workspace.huspy import DataFactory
from read.workspace.resource_cache import ReadResourceKey

logger = read.logging_helpers.get_logger(__name__)

HuspyDoi = Annotated[
    str,
    StringConstraints(
        strict=True, min_length=16, pattern=r"search"
    ),
]

class DatapackageDescriptor:
    """A simple wrapper providing access to datapackage.json contents."""

    def __init__(self, datapackage_json:dict, dataset:str, doi: HuspyDoi):
        """Constructs DatapackageDescriptor.

        Args:
            datapackage_json: parsed datapackage.json describing this datapackage.
            dataset: The name (an identifying string) of the dataset.
            doi: A versioned Digital Object Identifier for the dataset.
        """
        self.datapackage_json = datapackage_json
        self.dataset = dataset
        self.doi = doi
        self._validate_datapackage(datapackage_json)

    # def get_resource_path(self, name: str) -> str:
    #     """Returns Huspy URL that holds contents of given named resource."""
    #     res = self._get_resource_metadata(name)
    #     return res


    def _get_resource_metadata(self, name: str) -> dict:
        for res in self.datapackage_json['total']:
            if res['listings'] == name:
                return res
        raise KeyError(f"Resource {name} not found for {self.dataset}/{self.doi}")

    def _validate_datapackage(self, datapackage_json: dict):
        """Checks the correctness of datapackage.json metadata.

        Throws ValueError if invalid.
        """
        dp = datapackage.Package(datapackage_json)
        if not dp.valid:
            msg = f"Found {len(dp.errors)} datapackage validation errors:\n"
            for e in dp.errors:
                msg = msg + f"  * {e}\n"
            raise ValueError(msg)


class HuspyDoiSettings(BaseSettings):
    """Digital Object Identifiers pointing to currently used Huspy API. """
    LIMIT_5000: HuspyDoi = '?limit=5000'
    GEO_LIMIT_5000: HuspyDoi = 'geo?limit=5000'
    API_ROOT: str = 'https://huspy.com/api/v1/search'

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
        self._descriptor_cache = {}
    
    def get_doi(self: Self, dataset: str) -> HuspyDoi:
        """Returns DOI for given dataset."""
        try:
            doi = self.huspy_dois.__getattribute__(dataset)
        except AttributeError:
            raise AttributeError(f"No Huspy DOI found for dataset {dataset}.")
        return doi

    def get_known_datasets(self: Self) -> list[str]:
        """Returns list of supported datasets."""
        return [name for name, doi in sorted(self.huspy_dois)]

    def _get_url(self: Self, doi: HuspyDoi) -> HttpUrl:
        """Create a Huspy deposition URL based on its Huspy DOI"""
        match = re.search(r"(search(?:/geo)?)\?limit=5000", doi)

        if match is None:
            raise ValueError(f"Invalid Huspy DOI: {doi}")

        doi_prefix = match.group()[1]
        base_url = self._construct_base_url(doi_prefix)
        return f"{base_url}{doi_prefix}"

    def _construct_base_url(self, doi_prefix: str) -> str:
        """Construct the base URL based on the Huspy DOI prefix"""
        return f"{self.huspy_dois.API_ROOT}/search" if doi_prefix == 'search/geo' else self.huspy_dois.API_ROOT

    def _fetch_from_url(self: Self, url: HttpUrl) -> requests.Response:
        logger.info(f"Retrieving {url} from Huspy")
        response = self.http.get(url = url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded {url}")
            return response
        raise ValueError(f"Could not download {url}: {response.text}")
    
    def get_descriptor(self: Self, dataset: str) -> DatapackageDescriptor:
        """Returns class: `DatapackageDescriptor` for given dataset."""
        doi = self.get_doi(dataset)
        if doi not in self._descriptor_cache:
            dpkg = self._fetch_from_url(self._get_url(doi))
            self._descriptor_cache['doi'] = DatapackageDescriptor(dpkg.json(), dataset=dataset, doi=doi)
        else:
            raise RuntimeError(
                f"Huspy datapackage for {dataset}/{doi} does not contain valid doi"
            )
        return self._descriptor_cache[doi]


class DataStore:
    """Handle connections and downloading of Huspy Source"""
    def __init__(self, timeout: float = 15.0):
        self._datapackage_descriptors: dict[str, DatapackageDescriptor] = {}
        self._huspy_fetcher = HuspyFetcher(timeout=timeout)

    def get_known_datasets(self) -> list[str]:
        """Return list of supported datasets."""
        return self._huspy_fetcher.get_known_datasets()

    def get_datapackage_descriptor(self, dataset: str) -> DatapackageDescriptor:
        """Fetch datapackage descriptor for dataset either from Huspy."""
        doi = self._huspy_fetcher.get_doi(dataset)
        if doi not in self._datapackage_descriptors:
            res = ReadResourceKey(dataset, doi, 'datapackage.json')
            self._datapackage_descriptors[doi] = DatapackageDescriptor(
                json.loads(res)
            )


 #   def _fetch_from_url(self, collection_name):
 #       data_crawler = DataFactory.create_crawler(url=self.url, database_name=self.mongodb_name, collection_name=collection_name, uri=self.mongodb_uri)
 #       data_crawler.dump_to_mongodb()
