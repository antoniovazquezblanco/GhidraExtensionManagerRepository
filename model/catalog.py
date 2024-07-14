#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import json
import datetime
from pathlib import Path
from model.extension import Extension, ExtensionEncoder


class Catalog:
    def __init__(self, date=datetime.datetime.now()):
        # The version field is to keep readers compatible whenever the format changes. If a field of this class changes, it should be bumped.
        self._version = 0
        self._date = date
        self._extensions = []

    def add_extension(self, extension: Extension):
        if self._version != extension._version:
            raise Exception(
                "Extension version does not match catalog version. Please bump catalog version if needed.")
        self._extensions.append(extension)

    def write_to_file(self, path: Path):
        with path.open(mode='w') as f:
            json.dump(self, f, cls=CatalogEncoder)


class CatalogEncoder(ExtensionEncoder):
    def default(self, obj):
        if isinstance(obj, Catalog):
            return {
                "version": obj._version,
                "date": obj._date.isoformat(),
                "extensions": obj._extensions
            }
        return super().default(obj)
