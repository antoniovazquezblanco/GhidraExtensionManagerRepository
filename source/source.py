#!/usr/bin/env python
# SPDX-License-Identifier: GPL-2.0-or-later

from abc import ABC
from model.extension import Extension


class Source(ABC):
    def list_extensions(self) -> list[Extension]:
        raise NotImplementedError()

    @staticmethod
    def list_sources(github_token=None):
        import source
        for c in Source.__subclasses__():
            for s in c.list_sources(github_token):
                yield s
