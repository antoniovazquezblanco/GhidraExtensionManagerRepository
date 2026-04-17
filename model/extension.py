#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

from model.extension_version import ExtensionVersion, ExtensionVersionEncoder


class Extension:
    def __init__(self, name, description=None, author=None, created_on=None):
        # Internal format version to keep readers compatible whenever the format changes.
        # If a field of this class changes, changing the encoder, it should be bumped.
        self._fmt_version = 0
        self._name = name
        self._description = description
        self._author = author
        self._created_on = created_on
        self._versions = []

    def add_version(self, version: ExtensionVersion):
        if self._fmt_version != version._fmt_version:
            raise Exception(
                "ExtensionVersion fmt version does not match Extension fmt version. Please bump Extension fmt version if needed."
            )
        if version not in self._versions:
            self._versions.append(version)

    def __eq__(self, other):
        if not isinstance(other, Extension):
            raise NotImplementedError()
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)

    def __lt__(self, other):
        if not isinstance(other, Extension):
            raise NotImplementedError()
        return self._name < other._name


class ExtensionEncoder(ExtensionVersionEncoder):
    def default(self, o):
        if isinstance(o, Extension):
            return {
                "name": o._name,
                "description": o._description,
                "author": o._author,
                "created_on": o._created_on,
                "versions": o._versions,
            }
        return super().default(o)
