import os
import subprocess
from datetime import date
from dotenv import load_dotenv
import logging

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import MaskSensitiveDataFilter, get_logger, configure_root_logger
from lib.transform.rent_contracts_transformer import RentContractsTransformer
from lib.workspace.zenodo_client import ZenodoUploader

load_dotenv()

configure_root_logger(logfile="etl.log", loglevel="DEBUG")
logger = get_logger("ETL")


def download_rent_contracts(url, filename):
    logger.info("Downloading rent contracts")
    if os.path.isfile(filename):
        logger.info(f"{filename} already exists. Skipping download.")
        return

    logger.info(f"{filename} not found. Running RentContractsDownloader.")
    try:
        downloader = RentContractsDownloader(url)
        downloader.run(filename)
    except Exception as e:
        logger.error(f"Error downloading rent contracts: {e}")
        raise

def transform_rent_contracts(input_file, output_file):
    if not os.path.isfile(input_file):
        logger.error(f"{input_file} not found. Cannot transform.")
        return
    if not os.path.isfile(output_file):
        logger.info(f"Transforming {input_file} to {output_file}.")
        try:
            transformer = RentContractsTransformer(input_file, output_file)
            transformer.transform()
        except Exception as e:
            logger.error(f"Error transforming rent contracts: {e}")
            raise
    else:
        logger.info(f"{output_file} exists")

def upload_to_zenodo(files):
    logger.debug(f"Uploading to Zenodo... ")
    logger.addFilter(MaskSensitiveDataFilter())
    try:
        uploader = ZenodoUploader(access_token=os.getenv("ZENODO_TOKEN"))
        title = f"DLD - Rent Contracts - {date.today()}"
        description = "Acquired from Dubai Land Department Website"
        creators = [{'name': 'Gaurav Gurjar'}]

        # Create a new deposition if one does not exist
        deposition = uploader.create_deposition(title, description, creators)
        deposition_id = deposition['id']
        logger.info(f"Created new deposition with ID {deposition_id}")
        # Upload each file to the deposition
        for file in files:
            uploader.save_to_drafts(deposition_id=deposition_id, file_path=file)
            logger.info(f"Uploaded {file} to deposition {deposition_id}")
        # Publish the deposition
        uploader.publish_deposition(deposition_id)
        logger.info(f"Published deposition {deposition_id}")
    except (Exception, FileNotFoundError) as e:
        logger.error(f"Error uploading to Zenodo: {e}")


def main():
    url = os.getenv("DLD_URL")
    if not url:
        logger.error("DLD_URL environment variable not set.")
        return

    csv_filename = f'output/rent_contracts_{date.today()}.csv'
    parquet_filename = f'output/rent_contracts_{date.today()}.parquet'

    try:
        download_rent_contracts(url, csv_filename)
        transform_rent_contracts(csv_filename, parquet_filename)
        upload_to_zenodo([parquet_filename, csv_filename])
    except Exception as e:
        logger.error(f"An error occurred in the ETL process: {e}")

if __name__ == "__main__":
    main()
