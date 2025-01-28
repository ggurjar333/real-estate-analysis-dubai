import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import date

class RentContractsDownloader:
    def __init__(self, url):
        self.url = url

    def fetch_rent_contracts(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.content

    def parse_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        a_tag = soup.find('a', class_='action-icon-anchor')
        return a_tag['href'] if a_tag else None

    def download_file(self, href):
        filename = f'rent_contracts_{date.today()}.csv'
        subprocess.run(['wget', '-c', '-O', filename, href])

    def run(self):
        html_content = self.fetch_rent_contracts()
        href = self.parse_html(html_content)
        if href:
            self.download_file(href)


def main():
    URL = "https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open"
    downloader = RentContractsDownloader(URL)
    downloader.run()


if __name__ == "__main__":
    main()
