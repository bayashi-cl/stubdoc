"""stubdoc

Sphinx extension for read docstrings from stub files.

Intervene in the Python import system and change it to load modules
from a ``.pyi`` file.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import os
import sys
from typing import Any, Optional

import sphinx
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging

logger = logging.getLogger(__name__)


def _get_filename_pyi(path: str) -> str:
    """change source file suffix to ``.pyi``."""
    for suffix in importlib.machinery.all_suffixes():
        if path.endswith(suffix):
            return path[: -len(suffix)] + ".pyi"
    else:
        raise ImportError(f"{path} has invalid suffix.")


class PyiLoader(importlib.abc.FileLoader):
    """PyiLoader

    Load modules from ``.pyi`` file.
    """

    def get_source(self, fullname: str) -> str:
        filename_pyi = _get_filename_pyi(self.get_filename(fullname))
        try:
            source_bytes = self.get_data(filename_pyi)
        except OSError:
            raise ImportError
        return importlib.util.decode_source(source_bytes)


class PyiFinder(importlib.machinery.PathFinder):
    """PyiFinder

    Change ``spec.loader`` to ``PyiLoader`` for modules that start with
    ``module_names`` and have ``.pyi`` files in the same directory.
    """

    module_names: list[str] = []

    @classmethod
    def find_spec(
        cls, fullname, path=None, target=None
    ) -> Optional[importlib.machinery.ModuleSpec]:
        if any(fullname.startswith(module) for module in cls.module_names):
            spec = super().find_spec(fullname, path, target)

            if spec is not None:
                assert spec.loader is not None
                assert hasattr(spec.loader, "path")
                assert hasattr(spec.loader, "name")
                assert isinstance(spec.loader.path, str)

                if os.path.exists(_get_filename_pyi(spec.loader.path)):
                    logger.debug(f"Found stub file of {fullname}")
                    spec.loader = PyiLoader(spec.loader.name, spec.loader.path)

            return spec
        else:
            return None


def _add_finder(app: Sphinx, config: Config) -> None:
    PyiFinder.module_names = config.module_names
    sys.meta_path.insert(0, PyiFinder)
    logger.debug("add PyiFinder to sys.meta_path")


def setup(app: Sphinx) -> dict[str, Any]:
    app.add_config_value("module_names", [], "html")
    app.connect("config-inited", _add_finder)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
