from dotenv import load_dotenv
import requests
from datetime import date
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"

class GitHubRelease:
    """
    A class to handle publishing releases to a GitHub repository.

    Attributes:
        repo (str): The GitHub repository in the format 'owner/repo'.
        token (str): The GitHub token for authentication.
        headers (dict): The headers for GitHub API requests.

    Methods:
        create_release():
            Creates a new release in the specified GitHub repository.
        
        upload_files(release, files):
            Uploads files to the specified GitHub release.
        
        publish(files):
            Creates a new release and uploads the specified files to it.

    Usage:
        publisher = GitHubReleasePublisher(repo="owner/repo")
        publisher.publish(files=["file1.txt", "file2.zip"])
    """
    def __init__(self, repo):
        self.repo = repo
        self.token = os.getenv("GH_TOKEN")
        if not self.token:
            logger.error("GH_TOKEN not found in environment variables")
            raise ValueError("GH_TOKEN not set")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_release(self):
        tag_name = f"release-{date.today()}"
        release_name = f"Release {date.today()}"

        release_data = {
            "tag_name": tag_name,
            "name": release_name,
            "body": "Automated release",
            "draft": False,
            "prerelease": False
        }

        try:
            response = requests.post(f"{GITHUB_API_URL}/repos/{self.repo}/releases", headers=self.headers, json=release_data)
            response.raise_for_status()
            release = response.json()
            logger.info(f"Created GitHub release {release_name}")
            return release
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {e}")
            raise

    def upload_files(self, release, files):
        for file in files:
            try:
                with open(file, 'rb') as f:
                    upload_url = release['upload_url'].split('{')[0] + f"?name={file}"
                    upload_headers = self.headers.copy()
                    upload_headers["Content-Type"] = "application/octet-stream"

                    upload_response = requests.post(upload_url, headers=upload_headers, data=f)
                    upload_response.raise_for_status()
                    logger.info(f"Uploaded {file} to GitHub release {release['name']}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to upload {file}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error uploading {file}: {e}")

    def publish(self, files):
        try:
            release = self.create_release()
            self.upload_files(release, files)
        except Exception as e:
            logger.error(f"Failed to publish release: {e}")
    

    def release_exists(self, tag_name):
        """
        Checks if a release with the specified tag name already exists.

        Args:
            tag_name (str): The tag name of the release to check.

        Returns:
            bool: True if the release exists, False otherwise.
        """
        try:
            response = requests.get(f"{GITHUB_API_URL}/repos/{self.repo}/releases/tags/{tag_name}", headers=self.headers)
            if response.status_code == 200:
                logger.info(f"Release with tag {tag_name} already exists.")
                return True
            elif response.status_code == 404:
                logger.info(f"Release with tag {tag_name} does not exist.")
                return False
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {e}")
            raise
