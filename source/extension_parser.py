#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

from zipfile import ZipFile


class InvalidExtensionZip(Exception):
    pass


def _get_props_file(filenames):
    for file in filenames:
        if file.endswith('extension.properties'):
            return file
    return None


def _property_parse(content: str):
    props = {
        "name": None,
        "description": None,
        "author": None,
        "createdOn": None,
        "version": None
    }
    for line in content.splitlines():
        if line.startswith("#"):
            continue
        key, value = line.split("=")
        if value == "":
            value = None
        props[key] = value
    return props


def parse_info(zipfile: ZipFile):
    props_file = _get_props_file(zipfile.namelist())
    if not props_file:
        raise InvalidExtensionZip("Could not find props file")
    with zipfile.open(props_file, 'r') as props_f:
        return _property_parse(props_f.read().decode("utf-8"))
