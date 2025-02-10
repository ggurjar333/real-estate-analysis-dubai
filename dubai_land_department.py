import os

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import get_logger, configure_root_logger
from datetime import date
import subprocess

from lib.transform.rent_contracts_transformer import RentContractsTransformer

configure_root_logger(logfile="extract.log", loglevel="DEBUG")
logger = get_logger(__name__)
try:
    logger.info("Downloading rent contracts")
    URL = os.getenv("DLD_URL")
    filename = f'rent_contracts_{date.today()}.csv'
    
    # if not filename in the root directory then run RentContractsDownloader
    if not os.path.isfile(filename):
        logger.info(f"{filename} not found in the root directory. Running RentContractsDownloader.")
        try:
            rcd = RentContractsDownloader(URL)
            rcd.run(filename)
        except Exception as e:
            logger.info("Error downloading rent contracts")
        finally:
            pass
    else:
        logger.info(f"{filename} found in the root directory. Running RentContractsTransformer.")
        transformed_file = f'rent_contracts_{date.today()}.parquet'
        rct = RentContractsTransformer(filename, transformed_file)
        rct.transform()
        # add the transformed_file to git
        try:
            subprocess.run(['git', 'add', transformed_file], check=True)
            subprocess.run(['git', 'commit', '-m', f'Add transformed file {transformed_file}'], check=True)
            subprocess.run(['git', 'push'], check=True)
            print(f'{transformed_file} has been added, committed, and pushed to Git LFS.')
        except subprocess.CalledProcessError as e:
            print(f'An error occurred: {e}')

finally:
    print("Nothing is working.")