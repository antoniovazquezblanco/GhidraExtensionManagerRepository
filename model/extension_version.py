#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import json


class ExtensionVersion:
    def __init__(self, version, url):
        # Internal format version to keep readers compatible whenever the format changes.
        # If a field of this class changes, changing the encoder, it should be bumped.
        self._fmt_version = 0
        self._ext_version = version
        self._url = url

    def __eq__(self, other):
        if not isinstance(other, ExtensionVersion):
            return False
        return self._ext_version == other._ext_version

    def __hash__(self):
        return hash(self._ext_version)

    def __lt__(self, other):
        if not isinstance(other, ExtensionVersion):
            raise NotImplementedError()
        return self._ext_version < other._ext_version


class ExtensionVersionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ExtensionVersion):
            return {"version": o._ext_version, "url": o._url}
        return super().default(o)
