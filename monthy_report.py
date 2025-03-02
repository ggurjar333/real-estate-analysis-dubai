from datetime import date

from lib.logging_helpers import get_logger, configure_root_logger
from lib.workspace.github_client import GitHubRelease

from lib.classes.property_usage import PropertyUsage

configure_root_logger(logfile="property_usage.log", loglevel="DEBUG")

logger = get_logger("ETL")

def main():
    logger.info("Running monthly report")
    property_usage = PropertyUsage(
        output=f"property_usage_report_{date.today()}.csv",
        github_release=GitHubRelease(repo='ggurjar333/real-estate-analysis-dubai', 
                                     tag_name=f"property-usage-{date.today()}", 
                                     release_name=f"Property Usage Report {date.today()}")
    )
    property_usage.generate_monthly_report(
        input_file=f"dld_rent_contracts_{date.today()}.parquet"
    )
    property_usage.publish_to_github_release(
        tag_name=f"property-usage-{date.today()}",
        release_name=f"Property Usage Report {date.today()}"
    )
    logger.info("Monthly report completed")

if __name__ == "__main__":
    main()