import os
import argparse

from src.classes.rent_contracts_downloader import RentContractsDownloader

from datetime import date
import subprocess

def rent_contracts_downloader():
    URL = os.getenv("DLD_URL")
    downloader = RentContractsDownloader(URL)
    filename = f'rent_contracts_{date.today()}.csv'
    downloader.run(filename=filename)
    # Check the file size with bash command and echo the result to metadata
    file_size = subprocess.run(['du', '-h', filename], capture_output=True, text=True).stdout

    # Save the file to Git LFS
    subprocess.run(['git', 'lfs', 'track', filename])
    subprocess.run(['git', 'add', filename])
    subprocess.run(['git', 'commit', '-m', f'Add {filename}'])
    subprocess.run(['git', 'push'])

if __name__ == "__main__":
    rent_contracts_downloader()