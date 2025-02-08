from unittest.mock import patch, MagicMock
from dubai_land_department import rent_contracts_downloader

@patch('lib.extract.dubai_land_department.RentContractsDownloader.run')
@patch('lib.extract.dubai_land_department.subprocess.run')
@patch('lib.extract.dubai_land_department.os.getenv')
def test_rent_contracts_downloader(mock_getenv, mock_subprocess_run, mock_rent_contracts_downloader_run):
    # Mock environment variable
    mock_getenv.return_value = 'http://example.com/data.csv'

    # Mock subprocess.run for file size check and git commands
    mock_subprocess_run.side_effect = [
        MagicMock(stdout='10M\trent_contracts_2023-10-10.csv\n'),  # Mock du command output
        MagicMock(),  # Mock git lfs track
        MagicMock(),  # Mock git add
        MagicMock(),  # Mock git commit
        MagicMock()   # Mock git push
    ]

    # Call the function
    rent_contracts_downloader()

    # Assertions
    mock_getenv.assert_called_once_with('DLD_URL')
    mock_rent_contracts_downloader_run.assert_called_once_with('http://example.com/data.csv', 'rent_contracts_2023-10-10.csv')
    assert mock_subprocess_run.call_count == 5
    mock_subprocess_run.assert_any_call(['du', '-h', 'rent_contracts_2023-10-10.csv'], capture_output=True, text=True)
    mock_subprocess_run.assert_any_call(['git', 'lfs', 'track', 'rent_contracts_2023-10-10.csv'])
    mock_subprocess_run.assert_any_call(['git', 'add', 'rent_contracts_2023-10-10.csv'])
    mock_subprocess_run.assert_any_call(['git', 'commit', '-m', 'Add rent_contracts_2023-10-10.csv'])
    mock_subprocess_run.assert_any_call(['git', 'push'])