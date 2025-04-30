#!/usr/bin/env python3

import re
import subprocess
import json
import shutil

from urllib.request import Request, urlopen
from urllib.error import URLError

from tempfile import TemporaryDirectory

try:
    from packaging.version import parse as parse_version
except ModuleNotFoundError:
    print('Cannot find the packaging module. Try installing it with: '
        'sudo apt install python3-packaging')
    quit()

ETHDO_INSTALLED_PATH = '/usr/local/bin/'
UNKNOWN_VERSION = 'unknown'

GITHUB_REST_API_URL = 'https://api.github.com'
GITHUB_API_VERSION = 'application/vnd.github.v3+json'

ETHDO_LATEST_RELEASE = '/repos/wealdtech/ethdo/releases/latest'

def get_current_ethdo_version():
    version = UNKNOWN_VERSION

    try:
        process_result = subprocess.run([
            ETHDO_INSTALLED_PATH + 'ethdo', 'version'
            ], capture_output=True, text=True)

        process_output = process_result.stdout + '\n' + process_result.stderr
        version = process_output.strip()

    except FileNotFoundError:
        return False

    return version

def get_latest_ethdo_version():
    version = UNKNOWN_VERSION
    release_data = {}

    url = GITHUB_REST_API_URL + ETHDO_LATEST_RELEASE
    headers = {
        'Accept': GITHUB_API_VERSION
    }

    try:
        response_json = {}
        with urlopen(Request(url, headers=headers)) as response:
            if response.status == 200:
                response_content = response.read().decode('utf8')
                response_json = json.loads(response_content)
            else:
                print(f'Unexpected response status from Github: {response.status}')
                return version, release_data

        if not response_json:
            return version, release_data

        if 'name' in response_json:
            result = re.search(r'Release (?P<version>[^ ]+)', response_json['name'])
            if result:
                version = result.group('version')

        data_fields = ('created_at', 'published_at')
        for field in data_fields:
            if field in response_json:
                release_data[field] = response_json[field]

        if 'assets' in response_json and isinstance(response_json['assets'], list):
            for asset in response_json['assets']:
                if 'name' not in asset:
                    continue
                if not asset['name'].endswith('linux-amd64.tar.gz'):
                    continue

                if 'browser_download_url' in asset:
                    release_data['download_url'] = asset['browser_download_url']
                    release_data['asset_name'] = asset['name']
                    break

    except URLError as e:
        print(f'Error while trying to connect to Github: {e}')
        return False, False

    return version, release_data

def update_ethdo(release_data):
    print('Updating ethdo...')
    print(f'Downloading latest release archive {release_data["asset_name"]} ...')

    with urlopen(release_data['download_url']) as response:
        if response.status == 200:
            with TemporaryDirectory() as tmpdir:
                download_target = str(tmpdir) + '/' + release_data["asset_name"]
                with open(download_target, 'wb') as output_target:
                    shutil.copyfileobj(response, output_target)

                print(f'Extracting archive {release_data["asset_name"]} ...')
                subprocess.run(['tar', 'xvf', release_data["asset_name"]], cwd=str(tmpdir))

                extracted_directory = str(tmpdir)

                print('Updating installed ethdo binary...')
                extracted_ethdo_path = extracted_directory + '/' + 'ethdo'
                subprocess.run(['sudo', 'cp', extracted_ethdo_path, ETHDO_INSTALLED_PATH])
        else:
            print(f'Unexpected response status from Github: {response.status}')
            return False
    
    return True

def main():
    current_version = get_current_ethdo_version()

    if not current_version:
        print(f'Unable to find current ethdo version. Is ethdo installed in '
            f'{ETHDO_INSTALLED_PATH}?')
        quit()
    if current_version == UNKNOWN_VERSION:
        print('Unable to find current ethdo version. Cannot parse version output.')
        quit()

    latest_version, release_data = get_latest_ethdo_version()

    if not latest_version:
        print('Unable to find latest ethdo version. Is your internet working?')
        quit()
    if latest_version == UNKNOWN_VERSION:
        print('Unable to find latest ethdo version. Issue with parsing or connecting to '
            'Github.')
        quit()
    if 'asset_name' not in release_data or 'download_url' not in release_data:
        print('Unable to find downloadable asset in Github response.')
        quit()

    loose_current_version = parse_version(current_version)
    loose_latest_version = parse_version(latest_version)

    if loose_current_version == loose_latest_version:
        print(f'ethdo is up-to-date. (Installed: {current_version}, '
            f'Latest: {latest_version})')
    elif loose_current_version > loose_latest_version:
        print(f'ethdo is ahead of the latest version. (Installed: {current_version}, '
            f'Latest: {latest_version})')
    else:
        print(f'ethdo can be updated to the latest version: {latest_version} '
            f'(Installed: {current_version})')
        answer = input('Would you like to update ethdo? [Y\\n]: ')
        answer = answer.strip().lower()
        if answer in ('', 'y', 'yes'):
            if update_ethdo(release_data):
                print(f'ethdo updated to the latest version: {latest_version}')
            else:
                print('Failed to update ethdo.')

if __name__ == "__main__":
    main()