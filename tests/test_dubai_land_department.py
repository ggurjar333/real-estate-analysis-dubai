from datetime import date
import os
import pytest
import sys
import requests
import polars as pl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.workspace.zenodo_client import Zenodo

@pytest.fixture
def zenodo_repo():
    return Zenodo(access_token=os.getenv("ZENODO_TOKEN"))

def get_filtered_deposition(depositions, title):
    return next((deposition for deposition in depositions if deposition['title'] == title), None)

def test_list_depositions(zenodo_repo):
    title = f'DLD - Rent Contracts - {date.today()}'
    depositions = zenodo_repo.list_depositions()
    filtered_deposition = get_filtered_deposition(depositions, title)
    
    assert filtered_deposition is not None
    assert filtered_deposition['title'] == title
    assert len(filtered_deposition['files']) > 0
    assert filtered_deposition['files'][0]['filename'] == f'rent_contracts_{date.today()}.parquet'

def test_parquet(zenodo_repo):
    title = f'DLD - Rent Contracts - {date.today()}'
    depositions = zenodo_repo.list_depositions()
    filtered_deposition = get_filtered_deposition(depositions, title)
    
    assert filtered_deposition is not None
    assert filtered_deposition["links"]["files"] is not None
    assert filtered_deposition['title'] == title
    
    file_url = f"{list(filtered_deposition['links'].values())[0]}/files/rent_contracts_{date.today()}.parquet/content"
    response = requests.get(file_url, stream=True)
    
    with open('temp.parquet', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    
    df = pl.read_parquet('temp.parquet')
    print(df.head(5))
    assert len(df) > 0