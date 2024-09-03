#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import re
from github import Auth, Github
from source.source import Source
from model.extension import Extension
from model.extension_version import ExtensionVersion


class GithubSource(Source):
    GH_SOURCES = [
        "0ffffffffh/dragondance",
        "al3xtjames/ghidra-firmware-utils",
        "antoniovazquezblanco/GhidraDeviceTreeBlob",
        "antoniovazquezblanco/GhidraFindcrypt",
        "antoniovazquezblanco/GhidraSVD",
        "antoniovazquezblanco/GhidraSystemmap",
        "BartmanAbyss/ghidra-amiga",
        "boricj/ghidra-delinker-extension",
        "chaoticgd/ghidra-emotionengine-reloaded",
        "Coder-256/IntcodeGhidra",
        "CreepNT/VitaLoaderRedux",
        "fmagin/ghidra-minesweeper",
        "Gekkio/GhidraBoy",
        "hazzaaclark/gdiGhidra",
        "KeenSecurityLab/BinAbsInspector",
        "kotcrab/ghidra-allegrex",
        "kotcrab/ghidra-rest-api",
        "lab313ru/ghidra_psx_ldr",
        "likvidera/GhidraChatGPT",
        "nccgroup/ghidra-nanomips",
        "nccgroup/ghostrings",
        "nicodex/ghidra_motorolaffp",
        "nneonneo/ghidra-wasm-plugin",
        "mooncat-greenpy/Ghidra_GolangAnalyzerExtension",
        "pedro-javierf/NTRGhidra",
        "rafalh/ghidra-dwarf1",
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
        return release.assets

    def _get_extension_from_asset(self, asset):
        name = re.search(self._regex, asset.name).group('name')
        return Extension(name)

    def _get_extension_version_from_asset(self, asset):
        version = re.search(self._regex, asset.name).group('version')
        url = asset.browser_download_url
        return ExtensionVersion(version, url)

    def list_extensions(self) -> list[Extension]:
        assets = self._get_latest_release_assets()
        extension = self._get_extension_from_asset(assets[0])
        for asset in assets:
            extension.add_version(
                self._get_extension_version_from_asset(asset))
        return extension

    def __str__(self):
        return f"GithubSource@{self._repo}"

    @staticmethod
    def list_sources(github_token=None):
        for n in GithubSource.GH_SOURCES:
            yield GithubSource(n, github_token)
