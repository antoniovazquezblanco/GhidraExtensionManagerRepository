#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import io
import zipfile
import requests
from typing import Generator
from github import Auth, Github
from github.GitReleaseAsset import GitReleaseAsset
from source.source import Source
from source.extension_parser import parse_info, InvalidExtensionZip
from model.extension import Extension
from model.extension_version import ExtensionVersion


class GithubSource(Source):
    GH_SOURCES = [
        "al3xtjames/ghidra-firmware-utils",
        "Adubbz/Ghidra-Switch-Loader",
        "antoniovazquezblanco/GhidraDeviceTreeBlob",
        "antoniovazquezblanco/GhidraExtendedSourceParser",
        "antoniovazquezblanco/GhidraExtensionManager",
        "antoniovazquezblanco/GhidraFindcrypt",
        "antoniovazquezblanco/GhidraInvalidMemoryRefs",
        "antoniovazquezblanco/GhidraLinkerScript",
        "antoniovazquezblanco/GhidraSVD",
        "antoniovazquezblanco/GhidraSystemmap",
        "antoniovazquezblanco/GhidraTopSM",
        "astrelsky/GhidraOrbis",
        "astrelsky/GhidraProspero",
        "Baldanos/ghidra-bflt-loader",
        "BartmanAbyss/ghidra-amiga",
        "boricj/ghidra-delinker-extension",
        "chaoticgd/ghidra-emotionengine-reloaded",
        "clienthax/Ps3GhidraScripts",
        "Coder-256/IntcodeGhidra",
        "CreepNT/VitaLoaderRedux",
        "CUB3D/ghidra-hexagon-sleigh",
        "Cuyler36/Ghidra-GameCube-Loader",
        "cyberkaida/reverse-engineering-assistant",
        "desrdev/ghidra-fr60",
        "diommsantos/Gx64Sync",
        "domenukk/dragondance",
        "edmcman/ghidra-scala-loader",
        "fmagin/ghidra-minesweeper",
        "Gekkio/GhidraBoy",
        "goatshriek/ruby-dragon",
        "hazzaclark/gdiGhidra",
        "hippietrail/RetroGhidra",
        "ilyakharlamov/Ghidra-Nes-Rom-Decompiler-Plugin",
        "imxeno/ghidracord",
        "jtang613/GhidrAssist",
        "KeenSecurityLab/BinAbsInspector",
        "kotcrab/ghidra-allegrex",
        "kotcrab/ghidra-rest-api",
        "kylewlacy/GhidraNes",
        "lab313ru/ghidra_psx_ldr",
        "LAC-Japan/Ghidra_AntiDebugSeeker",
        "likvidera/GhidraChatGPT",
        "Nalen98/AngryGhidra",
        "Nalen98/GhidraEmu",
        "nccgroup/Cartographer",
        "nccgroup/ghidra-nanomips",
        "nccgroup/ghostrings",
        "nicodex/ghidra_motorolaffp",
        "nneonneo/ghidra-wasm-plugin",
        "marysaka/ghidra_falcon",
        "mobilemutex/GhidraCalculator",
        "mooncat-greenpy/Ghidra_GolangAnalyzerExtension",
        "oshogbo/ghidra-lx-loader",
        "pedro-javierf/NTRGhidra",
        "radareorg/ghidra-r2web",
        "rafalh/ghidra-dwarf1",
        "Random06457/Ghidra-RSP",
        "RevEngAI/reai-ghidra",
        "ReverseApple/GhidraApple",
        "RobertLarsen/GhidraFirmwareToolkit",
        "roysmeding/ghidra-os9",
        "sigurasg/GhidraMC6800",
        "sigurasg/GhidraTek2465",
        "subreption/ghidra_yara",
        "symgraph/GhidrAssist",
        "ubfx/BinDiffHelper",
        "VDOO-Connected-Trust/KotlinScriptProvider",
        "Washi1337/ghidra-nativeaot",
        "westfox-5/GhidraMetrics",
        "XboxDev/ghidra-xbe",
        "XYFC128/GhidraLookup",
        "zeroKilo/XEXLoaderWV",
        "Ziemas/ghidra_irx",
    ]

    def __init__(self, repo, token=None):
        auth = Auth.Token(token=token) if token else None
        self._gh = Github(auth=auth)
        self._repo = repo
        self._asset_name_suffix = ".zip"

    def _get_latest_release_assets(self) -> GitReleaseAsset:
        repo = self._gh.get_repo(self._repo)
        release = repo.get_latest_release()
        print(f"[+] Found release with title '{release.title}'")
        # Filter out the non-zip assets...
        assets = [
            asset
            for asset in release.assets
            if asset.name.endswith(self._asset_name_suffix)
        ]
        return assets

    def _get_props_from_asset(self, asset) -> dict:
        r = requests.get(asset.browser_download_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        props = parse_info(z)
        return props

    def _get_extension_version_from_asset(
        self, asset: GitReleaseAsset
    ) -> Extension | None:
        print(f"[+] Processing asset '{asset.name}'")
        props = self._get_props_from_asset(asset)
        # Parse extension info
        extension = Extension(
            name=props["name"],
            description=props["description"],
            author=props["author"],
            created_on=props["createdOn"],
        )
        # Add found version
        extension.add_version(
            ExtensionVersion(version=props["version"], url=asset.browser_download_url)
        )
        print(f"[+] Found version for Ghidra {props['version']}")
        return extension

    def list_extensions(self) -> list[Extension]:
        extensions = []
        assets = self._get_latest_release_assets()
        for asset in assets:
            extensions.append(self._get_extension_version_from_asset(asset))
        if not extensions or len(extensions) == 0:
            print("[!] Could not locate a valid asset for this extension...")
        return extensions

    def name(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"GithubSource@{self._repo}"

    @staticmethod
    def list_sources(github_token=None) -> Generator[Source]:
        for n in GithubSource.GH_SOURCES:
            yield GithubSource(n, github_token)
