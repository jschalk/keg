from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises
from src.linter.style import find_incorrect_imports


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    content = """\
import os
import src.ch51_old_chapter
from src.ch54_helpers import func
import src.ch53_calendar_viewer
from src.ch55_utils import helper
from src.ch55_utils import helper as h
from src.ch53.tools import alpha, beta as b
def inside_func():
    import src.ch60_bikehouse
    from src.ch61_more import thing
# relative import that should NOT match:
from .ch62_local import nope
"""
    fp = tmp_path / "sample.py"
    fp.write_text(content, encoding="utf-8")
    return fp


def test_threshold_52(sample_file):
    result = find_incorrect_imports(sample_file, 52)
    assert "import src.ch53_calendar_viewer" in result
    assert "from src.ch55_utils import helper" in result
    assert "from src.ch55_utils import helper as h" in result
    assert "from src.ch53.tools import alpha, beta as b" in result
    assert "import src.ch60_bikehouse" in result
    assert "from src.ch61_more import thing" in result
    # ensure lower/equal series are excluded
    assert all("ch51" not in r and "ch57" not in r for r in result)


def test_high_threshold_only_top_matches(sample_file):
    result = find_incorrect_imports(sample_file, 59)
    assert "import src.ch60_bikehouse" in result
    assert "from src.ch61_more import thing" in result
    assert all("ch53" not in r and "ch55" not in r for r in result)


def test_no_matches(sample_file):
    result = find_incorrect_imports(sample_file, 99)
    assert result == []


def test_missing_file():
    with pytest_raises(FileNotFoundError):
        find_incorrect_imports("nope.py", 10)
