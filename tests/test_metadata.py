# noqa: INP001
import sys
from contextlib import suppress


def test_metadata() -> None:
    if sys.version_info < (3, 11):
        with suppress(FutureWarning):
            from ozi_spec import METADATA
    else:
        from ozi_spec import METADATA
    METADATA.asdict()
