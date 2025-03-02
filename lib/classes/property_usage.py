import logging
import polars as pl
from datetime import date


# Configure logging
logging.basicConfig(level=logging.INFO)

class PropertyUsage:
    """
    Processes property usage data and publishes a report.
    """
    def __init__(self, output: str):
        self.output = output

    def transform(self, input_file: str):
        lf = pl.scan_parquet(input_file)
        property_usage_count = lf.group_by("property_usage_en").agg(pl.len().alias("no_of_contracts"))
        # add today's data as a column
        property_usage_count = property_usage_count.with_columns(
            pl.lit(date.today()).cast(pl.Date).alias("report_date")
        )
        property_usage_count.sink_csv(self.output)
        