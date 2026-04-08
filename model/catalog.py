#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import json
import datetime
from pathlib import Path
from model.extension import Extension, ExtensionEncoder


class Catalog:
    def __init__(self, date=datetime.datetime.now()):
        # Internal format version to keep readers compatible whenever the format changes.
        # If a field of this class changes, changing the encoder, it should be bumped.
        self._fmt_version = 0
        self._date = date
        self._extensions = []

    def add_extension(self, extension: Extension):
        if self._fmt_version != extension._fmt_version:
            raise Exception(
                "Extension fmt version does not match catalog fmt version. Please bump catalog fmt version if needed."
            )
        self._extensions.append(extension)

    def write_to_file(self, path: Path):
        with path.open(mode="w") as f:
            json.dump(self, f, cls=CatalogEncoder)


class CatalogEncoder(ExtensionEncoder):
    def default(self, o):
        if isinstance(o, Catalog):
            return {
                "version": o._fmt_version,
                "date": o._date.isoformat(),
                "extensions": o._extensions,
            }
        return super().default(o)
