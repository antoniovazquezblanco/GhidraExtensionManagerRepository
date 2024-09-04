#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import io
import zipfile
import requests
from github import Auth, Github
from source.source import Source
from source.extension_parser import parse_info, InvalidExtensionZip
from model.extension import Extension
from model.extension_version import ExtensionVersion


class GithubSource(Source):
    GH_SOURCES = [
        "0ffffffffh/dragondance",
        "al3xtjames/ghidra-firmware-utils",
        "antoniovazquezblanco/GhidraDeviceTreeBlob",
        "antoniovazquezblanco/GhidraExtensionManager",
        "antoniovazquezblanco/GhidraFindcrypt",
        "antoniovazquezblanco/GhidraSVD",
        "antoniovazquezblanco/GhidraSystemmap",
        "BartmanAbyss/ghidra-amiga",
        "boricj/ghidra-delinker-extension",
        "chaoticgd/ghidra-emotionengine-reloaded",
        "Coder-256/IntcodeGhidra",
        "CreepNT/VitaLoaderRedux",
        "desrdev/ghidra-fr60",
        "fmagin/ghidra-minesweeper",
        "Gekkio/GhidraBoy",
        "hazzaaclark/gdiGhidra",
        "KeenSecurityLab/BinAbsInspector",
        "kotcrab/ghidra-allegrex",
        "kotcrab/ghidra-rest-api",
        "kylewlacy/GhidraNes",
        "lab313ru/ghidra_psx_ldr",
        "likvidera/GhidraChatGPT",
        "nccgroup/Cartographer",
        "nccgroup/ghidra-nanomips",
        "nccgroup/ghostrings",
        "nicodex/ghidra_motorolaffp",
        "nneonneo/ghidra-wasm-plugin",
        "mooncat-greenpy/Ghidra_GolangAnalyzerExtension",
        "pedro-javierf/NTRGhidra",
        "rafalh/ghidra-dwarf1",
        "Random06457/Ghidra-RSP",
        "RobertLarsen/GhidraFirmwareToolkit",
        "roysmeding/ghidra-os9",
        "oshogbo/ghidra-lx-loader",
        "sigurasg/GhidraTek2465",
        "ubfx/BinDiffHelper",
        "VDOO-Connected-Trust/KotlinScriptProvider",
        "westfox-5/GhidraMetrics",
        "XboxDev/ghidra-xbe",
        "XYFC128/GhidraLookup",
    ]

    def __init__(self, repo, token=None):
        auth = Auth.Token(token=token) if token else None
        self._gh = Github(auth=auth)
        self._repo = repo
        self._regex = r'ghidra_(?P<version>.+)_PUBLIC_.+_(?P<name>.+)\.zip'

    def _get_latest_release_assets(self):
        repo = self._gh.get_repo(self._repo)
        release = repo.get_latest_release()
        # Filter out the non-zip assets...abs
        assets = [
            asset for asset in release.assets if asset.name.endswith('.zip')]
        return release.assets

    def _get_props_from_asset(self, asset):
        r = requests.get(asset.browser_download_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        props = parse_info(z)
        return props

    def _get_extension_from_asset(self, asset):
        props = self._get_props_from_asset(asset)

    def list_extensions(self) -> list[Extension]:
        assets = self._get_latest_release_assets()
        extension = None
        for asset in assets:
            try:
                props = self._get_props_from_asset(asset)
                if not extension:
                    extension = Extension(
                        name=props['name'], description=props['description'], author=props['author'], created_on=props['createdOn'])
                if extension:
                    extension.add_version(ExtensionVersion(
                        version=props['version'], url=asset.browser_download_url))
            except InvalidExtensionZip as e:
                pass
        if not extension:
            print("Could not locate a valid asset for this extension...")
        return extension

    def __str__(self):
        return f"GithubSource@{self._repo}"

    @staticmethod
    def list_sources(github_token=None):
        for n in GithubSource.GH_SOURCES:
            yield GithubSource(n, github_token)
