import os
import requests
from unittest.mock import patch
from assignment2.assignment2 import download_pdf

# New URL for the test case
NEW_PDF_URL = "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-02_daily_incident_summary.pdf"


def test_download_pdf_success():
    # Content you expect to receive from a successful get request
    mock_content = b'%PDF-1.4 sample PDF content'

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_content

        test_filename = 'test_download.pdf'

        result_filename = download_pdf(NEW_PDF_URL, test_filename)

        assert os.path.isfile(result_filename)

        with open(result_filename, 'rb') as f:
            file_content = f.read()
            assert file_content == mock_content

        if os.path.exists(test_filename):
            os.remove(test_filename)


def test_download_pdf_failure():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404

        test_filename = 'test_download.pdf'

        result_filename = download_pdf(NEW_PDF_URL, test_filename)

        assert not os.path.isfile(result_filename)

# Additional tests can be included here if needed.
