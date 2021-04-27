from mic._utils import upload_code, download
from pathlib import Path
from filecmp import cmp

RESOURCES = "resources"

def test_upload_code(tmp_path):
    file_name = "mic_full.yaml"
    file_test = Path(__file__).parent / RESOURCES / file_name
    response = upload_code(file_test)
    assert response.status_code == 200
    url = response.text
    response_get = download(url)
    assert response_get.status_code == 200
    file_test_downloaded = tmp_path / file_name
    with open(file_test_downloaded, 'wb') as f:
        f.write(response_get.content)
    assert cmp(file_test, file_test_downloaded)
