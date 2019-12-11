# coding=utf-8

import os
import pytest
import requests
import tarfile
from hashlib import md5


def md5sum(filename):
    """
    Get a md5 checksum of a file

    :param filename:
    :return:

    THis function is adapted from https://stackoverflow.com/a/24847608
    """
    _hash = md5()
    with open(str(filename), "rb") as f:
        for chunk in iter(lambda: f.read(128 * _hash.block_size), b""):
            _hash.update(chunk)
    return _hash.hexdigest()


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

        with open(str(_destination), "wb") as f:
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
    tar_name = 'cism-2.0.0-tests.20160728.tgz'
    drive_id = '1OHgxbnn4PRp5xMS3EqtjwLENEtvMfzNJ'

    data_dir = os.getenv('LIVVKIT_TEST_DATA', '')
    data_tar = os.path.join(data_dir, tar_name)
    ref_dir = tmpdir_factory.mktemp('ref_data')

    if os.path.isfile(data_tar):
        ref_tar = data_tar
    else:
        print('Downloading test data...')
        ref_tar = ref_dir.join(tar_name)
        download_file_from_google_drive(drive_id, ref_tar)

    with tarfile.open(str(ref_tar)) as tar:
        tar.extractall(path=str(ref_dir))

    return ref_dir.join('cism-2.0.0-tests')


@pytest.fixture(scope="session")
def test_data(tmpdir_factory):
    tar_name = 'cism-2.0.6-tests.20160728.tgz'
    drive_id = '1mZeDSs4rmdKFX2bgpYkZcNuc1wx18BLq'

    data_dir = os.getenv('LIVVKIT_TEST_DATA', '')
    data_tar = os.path.join(data_dir, tar_name)
    ref_dir = tmpdir_factory.mktemp('test_data')

    if os.path.isfile(data_tar):
        ref_tar = data_tar
    else:
        ref_tar = ref_dir.join(tar_name)
        download_file_from_google_drive(drive_id, str(ref_tar))

    with tarfile.open(ref_tar) as tar:
        tar.extractall(path=ref_dir)

    return ref_dir.join('cism-2.0.6-tests')


@pytest.fixture(scope='session')
def diff_data(tmpdir_factory):
    content_template = '[DOME-TEST]\n\n' \
                       '[grid]\n' \
                       'upn = 10\n' \
                       'ewn = 31\n' \
                       'nsn = 31\n' \
                       'dew = {}\n' \
                       'dns = 2000.0\n\n' \
                       '[time]\n' \
                       'tstart = 0.\n' \
                       'tend = 10.\n' \
                       'dt = 1.\n' \
                       'dt_diag = 1.\n' \
                       'idiag = 10\n' \
                       'jdiag = 10\n'

    diff_dir = tmpdir_factory.mktemp('diff')
    from_file = diff_dir.join('from.cfg')
    to_file = diff_dir.join('to.cfg')

    with open(from_file, 'w') as from_, open(to_file, 'w') as to_:
        from_.write(content_template.format(2000.0))
        to_.write(content_template.format(200.0))

    return from_file, to_file
