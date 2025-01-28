from rent_contracts_downloader import RentContractsDownloader
from zenodo_client import ZenodoClient, ZenodoAPIError  # Add this import

import logging
from datetime import date

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    URL = "https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open"
    # downloader = RentContractsDownloader(URL)
    filename = f'rent_contracts_{date.today()}.csv'
    # downloader.run(filename=filename)
    try:
        # Initialize client (uses sandbox by default)
        client = ZenodoClient()
        
        # Create new deposition
        deposition = client.create_deposition()
        deposition_id = deposition["id"]
        logger.info("Created deposition ID: %s", deposition_id)
        
        # Upload file
        upload_response = client.upload_file(deposition_id, filename)
        logger.info("Uploaded file: %s", upload_response["filename"])
        
        # Publish deposition
        published = client.publish_deposition(deposition_id)
        record_id = published["id"]
        logger.info("Published record ID: %s", record_id)
        
        # Download file
        # client.download_file(record_id, "example.csv", "downloaded.csv")
    
    except ZenodoAPIError as e:
        logger.error("Zenodo operation failed: %s", e)
    except Exception as e:
        logger.error("Unexpected error: %s", e)



if __name__ == "__main__":
    main()
