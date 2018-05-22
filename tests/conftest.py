# coding=utf-8

import pytest
import requests
import tarfile

def download_file_from_google_drive(_id, destination):
    """
    Download a file from Google Drive using it's ID

    :param _id: File id on google drive
    :param destination: Location to save file

    This function is adapted from https://stackoverflow.com/a/39225039
    """
    def get_confirm_token(_response):
        for key, value in _response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(_response, _destination):
        chunk_size = 32768

        with open(_destination, "wb") as f:
            for chunk in _response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(url, params={'id': _id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': _id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)


@pytest.fixture(scope="session")
def ref_data(tmpdir_factory):
    ref_dir = tmpdir_factory.mktemp('ref_data')
    ref_tar = ref_dir.join('ref_data.tgz')

    download_file_from_google_drive('1OHgxbnn4PRp5xMS3EqtjwLENEtvMfzNJ', ref_tar)

    with tarfile.open(ref_tar) as tar:
        tar.extractall(path=ref_dir)

    return ref_dir.join('cism-2.0.0-tests')


@pytest.fixture(scope="session")
def test_data(tmpdir_factory):
    ref_dir = tmpdir_factory.mktemp('test_data')
    ref_tar = ref_dir.join('test_data.tgz')

    download_file_from_google_drive('1mZeDSs4rmdKFX2bgpYkZcNuc1wx18BLq', ref_tar)

    with tarfile.open(ref_tar) as tar:
        tar.extractall(path=ref_dir)

    return ref_dir.join('cism-2.0.6-tests')