import requests
from bs4 import BeautifulSoup


class RentContractsDownloader:
    def __init__(self, url):
        """
        Initialize with the URL to fetch rent contracts from.
        """
        self.url = url

    def fetch_rent_contracts(self):
        """
        Fetch the rent contracts HTML content from the URL.
        """
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content

    def parse_html(self, html_content):
        """
        Parse the HTML content to find the download link.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        a_tag = soup.find('a', class_='action-icon-anchor')
        return a_tag['href'] if a_tag else None

    def download_file(self, href, filename):
        """
        Download the file from the given href and save it as filename.
        """
        response = requests.get(href, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def run(self, filename):
        """
        Run the downloader to fetch, parse, and download the rent contract file.
        """
        html_content = self.fetch_rent_contracts()
        href = self.parse_html(html_content)
        if href:
            self.download_file(href, filename)
        else:
            print("No download link found.")