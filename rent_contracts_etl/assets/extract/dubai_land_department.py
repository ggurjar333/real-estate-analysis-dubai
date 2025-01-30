from rent_contracts_etl.classes.rent_contracts_downloader import RentContractsDownloader

from datetime import date
import subprocess

from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset

@asset(group_name="DubaiLandDepartment", compute_kind="WebScraping")
def rent_contracts_downloader(context: AssetExecutionContext) -> MaterializeResult:
    URL = "https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open"
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
    
    return MaterializeResult(
        metadata={
            "file_size": MetadataValue.str(file_size),
        }
    )