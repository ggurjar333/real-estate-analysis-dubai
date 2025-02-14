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

def upload_to_zenodo(file):
    logger.debug(f"Upload {file} to Zenodo ")
    logger.addFilter(MaskSensitiveDataFilter())
    try:
        uploader = ZenodoUploader(access_token=os.getenv("ZENODO_TOKEN"))
        title = f"DLD - Rent Contracts"
        description = "Acquired from Dubai Land Department Website"
        creators = [{'name': 'Gaurav Gurjar'}]

        # Check if deposition with the same title already exists
        depositions = uploader.list_depositions()
        for deposition in depositions:
            if not deposition['title'] == title:
                logger.info(f"{title} - Deposition created")
                deposition = uploader.create_deposition(title, description, creators)
                deposition_id = deposition['id']

            if deposition['title'] == title:
                logger.info(f"Deposition - {title} already exists. Skipping upload.")
                deposition_id = deposition['id']

            logger.info(f"{title} and id: {deposition['id']}")
            uploader.save_to_drafts(deposition_id=deposition_id, file_path=file)
            uploader.publish_deposition(deposition_id)
            return
    except (Exception, FileNotFoundError) as e:
        logger.error(f"Error uploading to Zenodo: {e}")


def main():
    url = os.getenv("DLD_URL")
    if not url:
        logger.error("DLD_URL environment variable not set.")
        return

    csv_filename = f'rent_contracts_{date.today()}.csv'
    parquet_filename = f'output/rent_contracts_{date.today()}.parquet'

    try:
        download_rent_contracts(url, csv_filename)
        transform_rent_contracts(csv_filename, parquet_filename)
        upload_to_zenodo(parquet_filename)
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()
