# ozi/spec/python.py
# Part of the OZI Project.
# See LICENSE.txt for license information.
# SPDX-License-Identifier: Unlicense
"""Python support specification metadata."""
from __future__ import annotations

import platform
from dataclasses import dataclass
from dataclasses import field
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import cached_property
from typing import TYPE_CHECKING
from typing import Sequence
from warnings import warn

from ozi_spec.base import Default

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from collections.abc import Mapping

    if sys.version_info >= (3, 11):
        from typing import Self
    elif sys.version_info < (3, 11):
        from typing_extensions import Self

pymajor, pyminor, pypatch = map(int, platform.python_version_tuple())
DATE_FORMAT = '%Y-%m-%d'
DEPRECATION_DELTA_WEEKS = 104


@dataclass(frozen=True, slots=True, eq=True)
class PythonSupport(Default):
    """Python version support for the OZI toolchain."""

    deprecation_schedule: dict[int, str] = field(
        default_factory=lambda: {
            8: date(2024, 10, 1).strftime(DATE_FORMAT),
            9: date(2025, 10, 1).strftime(DATE_FORMAT),
            10: date(2026, 10, 1).strftime(DATE_FORMAT),
            11: date(2027, 10, 1).strftime(DATE_FORMAT),
            12: date(2028, 10, 1).strftime(DATE_FORMAT),
            13: date(2029, 10, 1).strftime(DATE_FORMAT),
        },
    )
    major: str = field(init=False, default='3')
    current_date: str = field(
        init=False,
        compare=False,
        default_factory=lambda: datetime.now(tz=timezone.utc).date().strftime(DATE_FORMAT),
    )

    def __post_init__(self: Self) -> None:
        """Warn the user if the python version is deprecated or pending deprecation.

        :raises: FutureWarning
        """
        python3_eol = (
            datetime.strptime(
                self.deprecation_schedule.get(
                    pyminor,
                    date(2008, 12, 3).strftime(DATE_FORMAT),
                ),
                DATE_FORMAT,
            )
            .replace(tzinfo=timezone.utc)
            .date()
        )
        ozi_support_eol = python3_eol - timedelta(weeks=DEPRECATION_DELTA_WEEKS)
        if datetime.now(tz=timezone.utc).date() > python3_eol:  # pragma: no cover
            warn(
                f'Python {pymajor}.{pyminor}.{pypatch} is not supported as of {python3_eol}.',
                FutureWarning,
            )
        elif datetime.now(tz=timezone.utc).date() > ozi_support_eol:  # pragma: no cover
            warn(
                f'Python {pymajor}.{pyminor}.{pypatch} support is pending deprecation '
                f'as of {ozi_support_eol}.',
                FutureWarning,
            )

    @cached_property
    def _minor_versions(self: Self) -> list[int]:
        return sorted(
            [
                k
                for k, v in self.deprecation_schedule.items()
                if datetime.strptime(v, DATE_FORMAT).replace(tzinfo=timezone.utc)
                - timedelta(weeks=DEPRECATION_DELTA_WEEKS)
                > datetime.strptime(self.current_date, DATE_FORMAT).replace(
                    tzinfo=timezone.utc,
                )
            ],
        )[:4]

    @cached_property
    def bugfix_minor(self: Self) -> int:
        _, _, bugfix, *_ = self._minor_versions
        return bugfix

    @cached_property
    def bugfix(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.bugfix_minor)))

    @cached_property
    def security1_minor(self: Self) -> int:
        _, security1, *_ = self._minor_versions
        return security1

    @cached_property
    def security1(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.security1_minor)))

    @cached_property
    def security2_minor(self: Self) -> int:
        security2, *_ = self._minor_versions
        return security2

    @cached_property
    def security2(self: Self) -> str:
        return '.'.join(map(str, (self.major, self.security2_minor)))

    @cached_property
    def prerelease_minor(self: Self) -> int | None:
        _, _, _, *prerelease = self._minor_versions
        return prerelease[0] if prerelease else None

    @cached_property
    def prerelease(self: Self) -> str:
        if self.prerelease_minor:  # pragma: no cover
            return '.'.join(map(str, (self.major, self.prerelease_minor)))
        return ''  # pragma: defer to good-first-issue

    @cached_property
    def classifiers(self: Self) -> Sequence[tuple[str, str]]:  # pragma: no cover
        classifiers = [
            ('Classifier', f'Programming Language :: Python :: {self.major} :: Only'),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.security2}',
            ),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.security1}',
            ),
            (
                'Classifier',
                f'Programming Language :: Python :: {self.bugfix}',
            ),
        ]
        if self.prerelease_minor:  # pragma: defer to spec
            classifiers += [
                ('Classifier', f'Programming Language :: Python :: {self.prerelease}'),
            ]
        return classifiers


_python_support = PythonSupport()


@dataclass(slots=True, frozen=True, eq=True)
class Support(Default):
    """Python implementation and version support info for OZI-packaged projects."""

    classifiers: Sequence[tuple[str, str]] = field(
        default_factory=lambda: _python_support.classifiers,
    )
    implementations: tuple[str, ...] = ('CPython',)
    metadata_version: str = '2.1'
    major: str = '3'
    prerelease: str = _python_support.prerelease
    bugfix: str = _python_support.bugfix
    security1: str = _python_support.security1
    security2: str = _python_support.security2
    deprecation_schedule: Mapping[int, str] = field(
        default_factory=lambda: _python_support.deprecation_schedule,
    )
    deprecation_delta_weeks: int = DEPRECATION_DELTA_WEEKS
