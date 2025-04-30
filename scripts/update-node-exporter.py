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

NODE_EXPORTER_INSTALLED_PATH = '/usr/local/bin/'
NODE_EXPORTER_SERVICE_NAME = 'node_exporter.service'
NODE_EXPORTER_USER_GROUP = 'node_exporter:node_exporter'
UNKNOWN_VERSION = 'unknown'

GITHUB_REST_API_URL = 'https://api.github.com'
GITHUB_API_VERSION = 'application/vnd.github.v3+json'

NODE_EXPORTER_LATEST_RELEASE = '/repos/prometheus/node_exporter/releases/latest'

def get_current_node_exporter_version():
    version = UNKNOWN_VERSION

    try:
        process_result = subprocess.run([
            NODE_EXPORTER_INSTALLED_PATH + 'node_exporter', '--version'
            ], capture_output=True, text=True)

        process_output = process_result.stdout + '\n' + process_result.stderr
        result = re.search(r'version (?P<version>[^ ]+)', process_output)
        if result:
            version = result.group('version')

    except FileNotFoundError:
        return False

    return version

def get_latest_node_exporter_version():
    version = UNKNOWN_VERSION
    release_data = {}

    url = GITHUB_REST_API_URL + NODE_EXPORTER_LATEST_RELEASE
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
            result = re.search(r'(?P<version>[^ ]+)', response_json['name'])
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

def update_node_exporter(release_data):
    print('Updating Node Exporter...')
    print(f'Downloading latest release archive {release_data["asset_name"]} ...')

    with urlopen(release_data['download_url']) as response:
        if response.status == 200:
            with TemporaryDirectory() as tmpdir:
                download_target = str(tmpdir) + '/' + release_data["asset_name"]
                with open(download_target, 'wb') as output_target:
                    shutil.copyfileobj(response, output_target)

                print(f'Extracting archive {release_data["asset_name"]} ...')
                subprocess.run(['tar', 'xvf', release_data["asset_name"]], cwd=str(tmpdir))

                extracted_directory = str(tmpdir) + '/' + release_data["asset_name"][:-7]

                print('Stopping Node Exporter service...')
                subprocess.run(['sudo', 'systemctl', 'stop', NODE_EXPORTER_SERVICE_NAME])

                print('Updating installed Node Exporter binary...')
                extracted_node_exporter_path = extracted_directory + '/' + 'node_exporter'
                installed_node_exporter_path = NODE_EXPORTER_INSTALLED_PATH + 'node_exporter'
                subprocess.run(['sudo', 'cp', extracted_node_exporter_path, NODE_EXPORTER_INSTALLED_PATH])
                subprocess.run(['sudo', 'chown', '-R', NODE_EXPORTER_USER_GROUP, installed_node_exporter_path])

                print('Restarting Node Exporter service...')
                subprocess.run(['sudo', 'systemctl', 'start', NODE_EXPORTER_SERVICE_NAME])
        else:
            print(f'Unexpected response status from Github: {response.status}')
            return False
    
    return True

def main():
    current_version = get_current_node_exporter_version()

    if not current_version:
        print(f'Unable to find current Node Exporter version. Is Node Exporter installed in '
            f'{NODE_EXPORTER_INSTALLED_PATH}?')
        quit()
    if current_version == UNKNOWN_VERSION:
        print('Unable to find current Node Exporter version. Cannot parse version output.')
        quit()

    latest_version, release_data = get_latest_node_exporter_version()

    if not latest_version:
        print('Unable to find latest Node Exporter version. Is your internet working?')
        quit()
    if latest_version == UNKNOWN_VERSION:
        print('Unable to find latest Node Exporter version. Issue with parsing or connecting to '
            'Github.')
        quit()
    if 'asset_name' not in release_data or 'download_url' not in release_data:
        print('Unable to find downloadable asset in Github response.')
        quit()

    loose_current_version = parse_version(current_version)
    loose_latest_version = parse_version(latest_version)

    if loose_current_version == loose_latest_version:
        print(f'Node Exporter is up-to-date. (Installed: {current_version}, '
            f'Latest: {latest_version})')
    elif loose_current_version > loose_latest_version:
        print(f'Node Exporter is ahead of the latest version. (Installed: {current_version}, '
            f'Latest: {latest_version})')
    else:
        print(f'Node Exporter can be updated to the latest version: {latest_version} '
            f'(Installed: {current_version})')
        answer = input('Would you like to update Node Exporter? [Y\\n]: ')
        answer = answer.strip().lower()
        if answer in ('', 'y', 'yes'):
            if update_node_exporter(release_data):
                print(f'Node Exporter updated to the latest version: {latest_version}')
                print('')
                print('You can make sure Node Exporter is working properly by checking out your '
                    'logs with this command:')
                print(f'sudo journalctl -ru {NODE_EXPORTER_SERVICE_NAME}')
            else:
                print('Failed to update Node Exporter.')

if __name__ == "__main__":
    main()