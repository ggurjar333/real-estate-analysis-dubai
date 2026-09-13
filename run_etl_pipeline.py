"""
ETL Pipeline for Dubai Ejari Rent Transactions.

Stages:
1. Download: POST EJARI_URL rents endpoint -> raw CSV
2. Transform: CSV -> Parquet (canonical aliases for downstream)
3. Analyze: property usage report
4. Publish: (Optional) GitHub Release

Usage:
    EJARI_URL=<endpoint> python run_etl_pipeline.py
"""

from pathlib import Path
import os
from datetime import date
from dotenv import load_dotenv

from lib.extract.ejari_rents_downloader import EjariRentsDownloader
from lib.transform.rents_transformer import RentsTransformer
from lib.classes.property_usage import PropertyUsage
from lib.workspace import GitHubRelease
from lib.logging_helpers import get_logger, configure_root_logger

load_dotenv()

configure_root_logger(logfile="etl.log", loglevel="DEBUG")
logger = get_logger("ETL")


def download_rents(url: str, filename: str) -> bool:
    """Download Ejari rents; skip if file already exists."""
    logger.info("=== PHASE 1: DOWNLOAD ===")

    if os.path.isfile(filename):
        logger.info(f"File already exists: {filename}. Skipping download.")
        return True

    logger.info(f"Downloading rents from {url} to {filename}")
    try:
        if EjariRentsDownloader(url).run(filename):
            logger.info(f"Download complete: {filename}")
            return True
        logger.error("Download failed.")
        return False
    except Exception as e:
        logger.error(f"Download failed with exception: {e}")
        raise


def transform_rents(input_csv: str, output_parquet: str) -> bool:
    """Transform rents CSV to Parquet."""
    logger.info("=== PHASE 2: TRANSFORM ===")
    try:
        if RentsTransformer(input_csv, output_parquet).transform():
            logger.info(f"Transformation complete: {output_parquet}")
            return True
        logger.error("Transformation failed.")
        return False
    except Exception as e:
        logger.error(f"Transformation failed with exception: {e}")
        raise


def analyze_property_usage(input_parquet: str, output_report: str) -> bool:
    """Generate property usage analysis report."""
    logger.info("=== PHASE 3: ANALYZE ===")
    try:
        PropertyUsage(output_report).transform(input_parquet)
        logger.info(f"Analysis complete: {output_report}")
        return True
    except Exception as e:
        logger.error(f"Analysis failed with exception: {e}")
        raise


def publish_artifacts_to_github(files: list, release_notes: str = "RELEASE_NOTES.md") -> None:
    """Publish data artifacts to GitHub Release."""
    logger.info("=== PHASE 4: PUBLISH ===")

    if not os.getenv("GH_TOKEN"):
        logger.warning("GH_TOKEN not set. Skipping GitHub publication.")
        return

    existing_files = [f for f in files if os.path.exists(f)]
    if not existing_files:
        logger.error("No files to publish!")
        return

    for f in existing_files:
        logger.info(f"  - {f} ({os.path.getsize(f) / (1024 * 1024):.1f} MB)")

    try:
        GitHubRelease('dataengineergaurav/rental-market-dynamics-dubai').publish(files=existing_files)
        logger.info("GitHub publication complete!")
    except Exception as e:
        logger.error(f"GitHub publication failed: {e}")
        raise


def main():
    """Main ETL pipeline entry point (rents only)."""
    logger.info("=" * 60)
    logger.info("DUBAI EJARI RENTS ETL PIPELINE")
    logger.info("Workflow: Download -> Transform -> Analyze -> Publish")
    logger.info("=" * 60)

    url = os.getenv("EJARI_URL")
    if not url:
        logger.error("EJARI_URL environment variable not set. Please set it in .env file.")
        return False

    date_str = date.today().strftime('%Y%m%d')
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    csv_filename = output_dir / f'rents_{date.today()}.csv'
    parquet_filename = str(output_dir / f'rents_{date_str}.parquet')
    property_usage_report = str(output_dir / f'property_usage_{date_str}.csv')

    try:
        if not download_rents(url, str(csv_filename)):
            logger.error("Pipeline stopped at Download phase.")
            return False

        if not transform_rents(str(csv_filename), parquet_filename):
            logger.error("Pipeline stopped at Transform phase.")
            return False

        if not analyze_property_usage(parquet_filename, property_usage_report):
            logger.error("Pipeline stopped at Analysis phase.")
            return False

        if os.getenv("GH_TOKEN"):
            publish_artifacts_to_github([parquet_filename, property_usage_report])
        else:
            logger.info("Skipping GitHub publication (GH_TOKEN not set)")

        logger.info("=" * 60)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"  - Parquet: {parquet_filename}")
        logger.info(f"  - Report:  {property_usage_report}")
        logger.info("=" * 60)
        return True

    except Exception as e:
        logger.critical(f"Pipeline failed with unhandled exception: {e}")
        raise


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
