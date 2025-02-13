import os
import subprocess
from datetime import date

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import get_logger, configure_root_logger
from lib.transform.rent_contracts_transformer import RentContractsTransformer

configure_root_logger(logfile="extract.log", loglevel="DEBUG")
logger = get_logger("Main")

def download_rent_contracts(url, filename):
    logger.info("Downloading rent contracts")
    if not os.path.isfile(filename):
        logger.info(f"{filename} not found in the root directory. Running RentContractsDownloader.")
        try:
            rcd = RentContractsDownloader(url)
            rcd.run(filename)
        except Exception as e:
            logger.error(f"Error downloading rent contracts: {e}")
            raise

def transform_rent_contracts(input_file, output_file, n_threads):
    logger.info(f"{input_file} found in the root directory. Running RentContractsTransformer.")
    if os.path.isfile(input_file):    
        try:
            rct = RentContractsTransformer(input_file, output_file)
            rct.transform()
        except Exception as e:
            logger.error(f"Error transforming rent contracts: {e}")
            raise

def commit_transformed_file(file):
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
    csv_filename = f'rent_contracts_{date.today()}.csv'
    parquet_filename = f'rent_contracts_{date.today()}.parquet'

    try:
        download_rent_contracts(url, csv_filename)
        transform_rent_contracts(csv_filename, parquet_filename, n_threads=2)
        commit_transformed_file(parquet_filename)
    except Exception as e:
        logger.error(f"An error occurred in the main process: {e}")

if __name__ == "__main__":
    main()
