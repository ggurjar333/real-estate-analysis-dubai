"""
Zenodo API Client with clean code practices
"""
import os
import json
import logging
from typing import Dict, Any, Optional
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

class ZenodoClient:
    """Client for interacting with Zenodo API"""
    
    def __init__(
        self,
        base_url: str = "https://sandbox.zenodo.org/api",
        access_token: Optional[str] = None
    ):
        """
        Initialize Zenodo client
        
        Args:
            base_url: Zenodo API base URL
            access_token: Zenodo access token (default: read from ZENODO_PAT environment variable)
        """
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token or os.getenv("ZENODO_PAT")
        
        if not self.access_token:
            raise ValueError("Zenodo access token not provided and ZENODO_PAT environment variable not set")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Internal method to handle HTTP requests with proper error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., "/deposit/depositions")
            **kwargs: Additional arguments for requests.request
            
        Returns:
            JSON response data
            
        Raises:
            ZenodoAPIError: For API communication failures
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, "response") and e.response is not None:
                error_msg += f" | Status: {e.response.status_code} | Response: {e.response.text}"
            logger.error(error_msg)
            raise ZenodoAPIError(error_msg) from e

    def create_deposition(self) -> Dict[str, Any]:
        """Create a new empty deposition"""
        return self._request("POST", "/deposit/depositions")

    def upload_file(
        self,
        deposition_id: str,
        file_path: str,
        file_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to an existing deposition
        
        Args:
            deposition_id: Zenodo deposition ID
            file_path: Path to local file to upload
            file_name: Optional custom filename for upload
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_name = file_name or os.path.basename(file_path)
        endpoint = f"/deposit/depositions/{deposition_id}/files"
        
        with open(file_path, "rb") as file:
            files = {"file": (file_name, file)}
            return self._request("POST", endpoint, files=files)

    def publish_deposition(self, deposition_id: str) -> Dict[str, Any]:
        """Publish a deposition"""
        endpoint = f"/deposit/depositions/{deposition_id}/actions/publish"
        return self._request("POST", endpoint)

    def download_file(
        self,
        record_id: str,
        file_name: str,
        save_path: str
    ) -> None:
        """
        Download a file from a published record
        
        Args:
            record_id: Zenodo record ID
            file_name: Name of the file to download
            save_path: Path to save downloaded file
        """
        endpoint = f"/records/{record_id}/files/{file_name}/content"
        
        try:
            response = self.session.get(f"{self.base_url}{endpoint}", stream=True)
            response.raise_for_status()
            
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info("File downloaded successfully to %s", save_path)
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Download failed: {str(e)}"
            logger.error(error_msg)
            raise ZenodoAPIError(error_msg) from e

class ZenodoAPIError(Exception):
    """Custom exception for Zenodo API errors"""

