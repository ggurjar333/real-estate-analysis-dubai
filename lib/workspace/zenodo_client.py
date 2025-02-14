"""
Zenodo API Client with clean code practices
"""
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

class Zenodo:
    def __init__(self, access_token: str, sandbox: bool = False):
        self.access_token = access_token
        self.base_url = 'https://sandbox.zenodo.org/api' if sandbox else 'https://zenodo.org/api'
    
    def _get_headers(self):
        return {'Content-Type': 'application/json'}

    def _get_params(self):
        return {'access_token': self.access_token}

    def list_depositions(self):
        url = f"{self.base_url}/deposit/depositions"
        response = requests.get(url, params=self._get_params())
        response.raise_for_status()
        return response.json()

class ZenodoUploader(Zenodo):
    def create_deposition(self, title: str, description: str, creators: list):
        url = f"{self.base_url}/deposit/depositions"
        data = {
            'metadata': {
                'title': title,
                'upload_type': 'dataset',
                'description': description,
                'creators': creators
            }
        }
        response = requests.post(url, params=self._get_params(), headers=self._get_headers(), json=data)
        response.raise_for_status()
        return response.json()

    def save_to_drafts(self, deposition_id, file_path: str):
        self.upload_file(deposition_id, file_path)

    def upload_file(self, deposition_id: str, file_path: str):
        logger.debug(f"Uploading {file_path} to Zenodo")
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/files"
        with open(file_path, 'rb') as fp:
            files = {'file': (file_path.split('/')[-1], fp)}
            response = requests.post(url, params=self._get_params(), files=files)
            response.raise_for_status()
            return response.json()

    def publish_deposition(self, deposition_id: str):
        url = f"{self.base_url}/deposit/depositions/{deposition_id}/actions/publish"
        response = requests.post(url, params=self._get_params())
        response.raise_for_status()
        return response.json()

class ZenodoDeleter(Zenodo):
    def delete_deposition(self, deposition_id: str):
        url = f"{self.base_url}/deposit/depositions/{deposition_id}"
        response = requests.get(url, params=self._get_params())
        deposition = response.json()

        if deposition.get('submitted'):
            raise ValueError(f"Deposition {deposition_id} is already published and cannot be deleted via API.")

        response = requests.delete(url, params=self._get_params())
        response.raise_for_status()
        return response.status_code == 204
