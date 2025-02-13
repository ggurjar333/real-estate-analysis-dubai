import os
import subprocess
from datetime import date
from dotenv import load_dotenv

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import get_logger, configure_root_logger
from lib.transform.rent_contracts_transformer import RentContractsTransformer

load_dotenv()

configure_root_logger(logfile="dld.log", loglevel="DEBUG")
logger = get_logger("DLD")

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

    logger.info(f"Transforming {input_file} to {output_file}.")
    try:
        transformer = RentContractsTransformer(input_file, output_file)
        transformer.transform()
    except Exception as e:
        logger.error(f"Error transforming rent contracts: {e}")
        raise

def commit_transformed_file(file):
    logger.info(f"Committing {file} to Git LFS.")
    try:
        subprocess.run(['git', 'add', file], check=True)
        subprocess.run(['git', 'commit', '-m', f'Add transformed file {file}'], check=True)
        subprocess.run(['git', 'push'], check=True)
        logger.info(f'{file} has been added, committed, and pushed to Git LFS.')
    except subprocess.CalledProcessError as e:
        logger.error(f'An error occurred while committing the file: {e}')
        raise

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
        commit_transformed_file(parquet_filename)
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()