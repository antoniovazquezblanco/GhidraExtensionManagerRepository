#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
from pathlib import Path
from model.catalog import Catalog
from source.source import Source


def create_catalog(gh_token=None):
    # If a previous catalog file exists, delete it...
    catalog_file = Path('catalog.json')
    if catalog_file.exists():
        catalog_file.unlink()

    catalog = Catalog()

    for s in Source.list_sources(gh_token):
        try:
            print(f"Retrieving extensions from {s}...")
            catalog.add_extension(s.list_extensions())
        except Exception as e:
            print(f"Could not retrieve extensions for {s}")
            print(e)

    catalog.write_to_file(catalog_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gh-token", help="Github API token to avoid rate limiting")
    args = parser.parse_args()
    create_catalog(args.gh_token)


if __name__ == "__main__":
    main()
