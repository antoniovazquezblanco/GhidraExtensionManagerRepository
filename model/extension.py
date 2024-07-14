#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import json
from model.extension_version import ExtensionVersion, ExtensionVersionEncoder


class Extension:
    def __init__(self, name, description=None, author=None, created_on=None):
        self._version = 0
        self._name = name
        self._description = description
        self._author = author
        self._created_on = created_on
        self._versions = []

    def add_version(self, version: ExtensionVersion):
        if self._version != version._version:
            raise Exception(
                "ExtensionVersion version does not match Extension version. Please bump Extension version if needed.")
        self._versions.append(version)


class ExtensionEncoder(ExtensionVersionEncoder):
    def default(self, obj):
        if isinstance(obj, Extension):
            return {
                "name": obj._name,
                "description": obj._description,
                "author": obj._author,
                "created_on": obj._created_on,
                "versions": obj._versions
            }
        return super().default(obj)
