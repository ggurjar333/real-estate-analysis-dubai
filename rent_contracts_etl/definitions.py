from .assets.extract.dubai_land_department import rent_contracts_downloader
from dagster import Definitions

my_assets = [rent_contracts_downloader]


defs = Definitions(assets=my_assets)
