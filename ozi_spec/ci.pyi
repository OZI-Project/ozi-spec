# ozi/spec/ci.py
# Part of the OZI Project.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Unlicense
"""Continuous integration specification."""
from __future__ import annotations

from collections.abc import Mapping  # noqa: TCH003,TC003,RUF100
from dataclasses import dataclass
from dataclasses import field

from ozi_spec.base import Default


@dataclass(slots=True, frozen=True, eq=True)
class Publish(Default):
    """Publishing patterns for packaged project."""

    include: tuple[str, ...] = ('*.tar.gz', '*.whl', 'sig/*')
    version: str = '1.x.x'


@dataclass(slots=True, frozen=True, eq=True)
class Draft(Default):
    """Draft release patterns for packaged project."""

    version: str = '1.x.x'


@dataclass(slots=True, frozen=True, eq=True)
class Release(Default):
    """Release patterns for packaged project."""

    version: str = '1.x.x'


@dataclass(slots=True, frozen=True, eq=True)
class Checkpoint(Default):
    """Checkpoint suites to run."""

    suites: tuple[str, ...] = ('dist', 'lint', 'test')
    version: str = '1.x.x'


@dataclass(slots=True, frozen=True, eq=True)
class CheckpointSuite(Default):
    """OZI checkpoint base class."""

    exclude: tuple[str, ...] = field(default_factory=tuple)
    module: tuple[str, ...] = field(default_factory=tuple)
    plugin: Mapping[str, str] = field(default_factory=dict)
    utility: Mapping[str, str] = field(default_factory=dict)
    ignore: tuple[str, ...] = field(default_factory=tuple)


@dataclass(slots=True, frozen=True, eq=True)
class RuffLint(CheckpointSuite):
    """OZI experimental linting and formatting with ruff.
    The goal is parity with the classic lint suite.
    """

    ignore: tuple[str, ...] = (
        'A003',
        'ARG',
        'ANN401',
        'TRY003',
        'B028',
        'B905',
        'D1',
        'D2',
        'D101',
        'D4',
        'FLY',
        'FBT',
        'PGH003',
        'PLR',
        'RET',
        'EM',
        'PLW',
        'PTH',
        'RUF009',
        'RUF012',
        'RUF015',
        'RUF200',
        'SIM',
        'T201',
        'TCH002',
        'TCH004',
        'UP',
        'PERF203',
    )
    module: tuple[str, ...] = ('ruff', 'mypy', 'pyright')
    exclude: tuple[str, ...] = ('meson-private',)
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'ruff': 'ruff>=0.1.6',
            'mypy': 'mypy',
            'pyright': 'pyright',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicLint(CheckpointSuite):
    """OZI standard linting and formatting suite."""

    ignore: tuple[str, ...] = ('E203', 'E501', 'TC007', 'TC008')
    module: tuple[str, ...] = ('bandit', 'black', 'flake8', 'isort', 'mypy', 'pyright')
    exclude: tuple[str, ...] = ('venv', 'meson-private', 'subprojects')
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'bandit': 'bandit[toml]',
            'black': 'black>=24.3',
            'flake8': 'flake8',
            'isort': 'isort',
            'mypy': 'mypy',
            'pyright': 'pyright',
            'readme-renderer': 'readme-renderer[md]',
        },
    )
    plugin: Mapping[str, str] = field(
        default_factory=lambda: {
            'Flake8-pyproject': 'Flake8-pyproject',
            'flake8-annotations': 'flake8-annotations',
            'flake8-broken-line': 'flake8-broken-line',
            'flake8-bugbear': 'flake8-bugbear',
            'flake8-comprehensions': 'flake8-comprehensions',
            'flake8-datetimez': 'flake8-datetimez',
            'flake8-docstring-checker': 'flake8-docstring-checker',
            'flake8-eradicate': 'flake8-eradicate',
            'flake8-fixme': 'flake8-fixme',
            'flake8-leading-blank-lines': 'flake8-leading-blank-lines',
            'flake8-no-pep420': 'flake8-no-pep420',
            'flake8-pyi': 'flake8-pyi',
            'flake8-pytest-style': 'flake8-pytest-style',
            'flake8-quotes': 'flake8-quotes',
            'flake8-tidy-imports': 'flake8-tidy-imports',
            'flake8-type-checking': 'flake8-type-checking',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicTest(CheckpointSuite):
    """OZI standard testing and coverage."""

    module: tuple[str, ...] = ('coverage', 'pytest')
    plugin: Mapping[str, str] = field(
        default_factory=lambda: {
            'hypothesis': 'hypothesis[all]',
            'pytest-asyncio': 'pytest-asyncio',
            'pytest-cov': 'pytest-cov',
            'pytest-randomly': 'pytest-randomly',
            'pytest-tcpclient': 'pytest-tcpclient',
            'pytest-xdist': 'pytest-xdist',
        },
    )
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'coverage': 'coverage[toml]',
            'pytest': 'pytest',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class ClassicDist(CheckpointSuite):
    """OZI standard publishing and distribution.

    .. versionchanged:: 0.6
        Added ``cibuildwheel`` and ``twine`` as plugins.

    .. versionchanged:: 0.10
        Moved ``cibuildwheel`` and ``twine`` to utility.
    """

    module: tuple[str, ...] = ('python-semantic-release', 'sigstore')
    utility: Mapping[str, str] = field(
        default_factory=lambda: {
            'python-semantic-release': 'python-semantic-release',
            'sigstore': 'sigstore',
            'twine': 'twine',
            'cibuildwheel': 'cibuildwheel',
        },
    )
    plugin: Mapping[str, str] = field(
        default_factory=lambda: {},
    )


@dataclass(slots=True, frozen=True, eq=True)
class Build(Default):
    """Build backend and required packages for OZI.

    .. versionchanged:: 0.7
       Invoke added to build-system dependencies.

    .. versionchanged:: 0.8
       All build-system requires moved to OZI.build 1.2 as extra optional_dependencies.
    """

    backend: str = 'ozi_build.buildapi'
    requires: Mapping[str, str] = field(
        default_factory=lambda: {
            'OZI.build': 'OZI.build[core]~=1.5.0',
        },
    )


@dataclass(slots=True, frozen=True, eq=True)
class CI(Default):
    """Provider-agnostic CI information."""

    backend: Mapping[str, str] = field(
        default_factory=lambda: {
            'tox': 'tox~=4.18',
            'tox-gh': 'tox-gh~=1.3',
        },
    )
    checkpoint: Checkpoint = Checkpoint()
    draft: Draft = Draft()
    release: Release = Release()
    publish: Publish = Publish()
    providers: tuple[str, ...] = ('github',)