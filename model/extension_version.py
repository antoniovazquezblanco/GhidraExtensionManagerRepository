#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import json


class ExtensionVersion:
    def __init__(self, version, url):
        self._version = 0
        self._ext_version = version
        self._url = url


class ExtensionVersionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExtensionVersion):
            return {
                "version": obj._ext_version,
                "url": obj._url
            }
        return super().default(obj)
