#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

import importlib
from pathlib import Path

__all__ = [file.stem for file in Path(__file__).parent.glob(
    "*.py") if file.stem != "__init__"]

for m in __all__:
    importlib.import_module(f"{Path(__file__).parent.stem}.{m}")
