import logging
import polars as pl
from datetime import date

from lib.workspace.github_client import GitHubRelease

# Configure logging
logging.basicConfig(level=logging.INFO)

class PropertyUsage:
    """
    Processes property usage data and publishes a report.
    """
    def __init__(self, output: str, github_release: GitHubRelease):
        self.output = output
        self.github_release = github_release

    def transform(self, input_file: str):
        lf = pl.scan_parquet(input_file)
        property_usage_count = lf.group_by("property_usage_en").agg(pl.len().alias("no_of_contracts"))
        # add today's data as a column
        property_usage_count = property_usage_count.with_columns(
            pl.lit(date.today()).cast(pl.Date).alias("report_date")
        )
        logging.info(f"Property usage count: {property_usage_count.collect()}")
        property_usage_count.sink_csv(self.output)

    def generate_monthly_report(self, input_file: str):
        self.transform(input_file)
        logging.info("Monthly report generated")

    def publish_to_github_release(self, tag_name: str, release_name: str):
        self.github_release.create_release(tag_name=tag_name, release_name=release_name)
        self.github_release.publish(files=[self.output])
        