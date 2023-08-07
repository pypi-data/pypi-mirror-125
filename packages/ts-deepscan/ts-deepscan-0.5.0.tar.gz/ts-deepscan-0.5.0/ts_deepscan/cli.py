# SPDX-FileCopyrightText: 2020 EACG GmbH
#
# SPDX-License-Identifier: Apache-2.0


import json
import time
import argparse
import requests
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from typing import List

from .scanner.Scan import Scan
from .scanner.Scanner import *

from .analyser.Dataset import Dataset
from .analyser.SourcesAnalyser import SourcesAnalyser
from .analyser.LicenseAnalyser import LicenseAnalyser

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("path", help="File or directory to be scanned", nargs='+')

    parser.add_argument("-o", "--output", help="Store results to the OUTPUT in JSON format")

    parser.add_argument("--includeCopyright",
                        help="Enables searching for copyright information in files",
                        action="store_true")

    parser.add_argument("--filterFiles",
                        help="Only scan files based on commonly used names (LICENSE, README, etc.) and extensions (source code files)",
                        action="store_true")

    parser.add_argument("--upload",
                        help="Upload to the TrustSource service",
                        action="store_true")

    parser.add_argument("--moduleName", help="Module name of the scan")

    parser.add_argument("--apiKey", help="Upload to the TrustSource service")

    parser.add_argument("--baseUrl", help="TrustSource service base URL", )

    args = parser.parse_args()
    options = AnalyserOptions(includeCopyright=args.includeCopyright,
                              filterFiles=args.filterFiles)


    result, stats = execute([Path(p) for p in args.path], options)

    print()

    # Output result
    if not result:
        print('Nothing found')
        return

    if args.upload:
        scan = Scan(options=options)

        scan.result = result
        scan.stats = stats

        upload(scan, args.moduleName, args.apiKey, args.baseUrl)

    elif args.output:
        with open(args.output, 'w') as fp:
            fp.write(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2), )



def execute(paths: List[Path], options):
    scanner = FSScanner(paths, get_analysers(), options)
    scan_finished = False

    def print_progress(final=False):
        print('\rScanning... [{}\{}]'.format(scanner.finishedTasks, scanner.totalTasks), end='')
        if final: print()

    def update_progress():
        while not scan_finished:
            print_progress()
            time.sleep(2)

    progress = threading.Thread(target=update_progress)
    progress.start()

    result = scanner.run()

    scan_finished = True
    progress.join()

    print_progress(final=True)

    return result, {
        'total': scanner.totalTasks,
        'finished': scanner.finishedTasks
    }


def upload(scan, moduleName, apiKey, baseUrl):
    if not baseUrl:
        baseUrl = 'https://api.prod.trustsource.io/deepscan'

    if not moduleName or not apiKey:
        print('Module name and API key must be provided')
        exit(2)

    url = '{}/upload-results?module={}'.format(baseUrl, moduleName)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'ts-deepscan/1.0.0',
        'x-api-key': apiKey
    }
    print('Uploading results...')
    response = requests.post(url, json=scan.__dict__, headers=headers)

    print(json.dumps(response.text, indent=2))

    if response.status_code not in range(200, 300):
        exit(2)


def get_analysers():
    import spacy

    path = config.get_datasetdir()
    dataset = Dataset(path)

    if not spacy.util.is_package('en_core_web_sm'):
        spacy.cli.download('en_core_web_sm')
        print()

    if not spacy.util.is_package('en_core_web_sm'):
        print('Cannot download language model')
        exit(2)

    print('Loading dataset...')
    dataset.load()

    return [LicenseAnalyser(dataset), SourcesAnalyser(dataset)]



