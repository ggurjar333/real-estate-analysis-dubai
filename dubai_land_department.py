import os

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import get_logger, configure_root_logger
from datetime import date
import subprocess

def rent_contracts_downloader():
    # Example usage in your script
    URL = os.getenv("DLD_URL")
    filename = f'rent_contracts_{date.today()}.csv'
    RentContractsDownloader.run(URL, filename)

    # Check the file size with bash command and echo the result to metadata
    file_size = subprocess.run(['du', '-h', filename], capture_output=True, text=True).stdout

    # Save the file to Git LFS
    subprocess.run(['git', 'lfs', 'track', filename])
    subprocess.run(['git', 'add', filename])
    subprocess.run(['git', 'commit', '-m', f'Add {filename}'])
    subprocess.run(['git', 'push'])

if __name__ == "__main__":
    configure_root_logger(logfile="extract.log", loglevel="DEBUG")
    logger = get_logger(__name__)
    try:
        logger.info("Downloading rent contracts")
        rent_contracts_downloader()
    except Exception as e:
        logger.info("Error downloading rent contracts")