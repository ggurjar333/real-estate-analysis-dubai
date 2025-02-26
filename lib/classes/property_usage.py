import logging
import polars as pl
from datetime import date

# Configure logging
logging.basicConfig(level=logging.INFO)

class PropertyUsage:
    """
    This module contains classes and methods related to property_usage
    """
    def __init__(self, input_file: str, output_file: str):
        self.input = input_file
        self.output = output_file

    def transform(self):
        lf = pl.scan_parquet(self.input)
        print(lf.head(5).collect())
        property_usage_count = lf.group_by("property_usage_en").agg(pl.len().alias("no_of_contracts"))
        logging.info(f"Property usage count: {property_usage_count.collect()}")
        property_usage_count.sink_csv(self.output) 

# Usage
parquet_filename = '/home/datageek01/home/real-estate-analysis-dubai/dld_rent_contracts_2025-02-17.parquet'

propery_usage_en = PropertyUsage(parquet_filename, f'/home/datageek01/home/real-estate-analysis-dubai/property_usage_counts.csv')
propery_usage_en.transform()
