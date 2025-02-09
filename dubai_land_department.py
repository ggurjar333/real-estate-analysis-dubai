import os

from lib.extract.rent_contracts_downloader import RentContractsDownloader
from lib.logging_helpers import get_logger, configure_root_logger
from datetime import date
import subprocess

configure_root_logger(logfile="extract.log", loglevel="DEBUG")
logger = get_logger(__name__)
try:
    logger.info("Downloading rent contracts")
    URL = os.getenv("DLD_URL")
    filename = f'rent_contracts_{date.today()}.csv'
    rcd = RentContractsDownloader()
    rcd.run(URL, filename)

except Exception as e:
    logger.info("Error downloading rent contracts")