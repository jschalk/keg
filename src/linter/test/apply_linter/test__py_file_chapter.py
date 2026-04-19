from linter.style import find_incorrect_imports
from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, raises as pytest_raises


@pytest_fixture
def sample_file(tmp_path: pathlib_Path):
    content = """\
import os
import ch51_old_chapter
from ch54_helpers import func
import ch53_calendar_viewer
from ch55_utils import helper
from ch55_utils import helper as h
from ch53.tools import alpha, beta as b
def inside_func():
    import ch60_bikehouse
    from ch61_more import thing
# relative import that should NOT match:
from .ch62_local import nope
"""
    fp = tmp_path / "sample.py"
    fp.write_text(content, encoding="utf-8")
    return fp


# TODO fix and reactivate test
# def test_find_incorrect_imports_ReturnsObj_Scenario0_threshold_52(sample_file):
#     # ESTABLISH / WHEN
#     result = find_incorrect_imports(sample_file, 52)
#     # THEN
#     print(f"{result=}")
#     assert "import ch53_calendar_viewer" in result
#     assert "from ch55_utils import helper" in result
#     assert "from ch55_utils import helper as h" in result
#     assert "from ch53.tools import alpha, beta as b" in result
#     assert "import ch60_bikehouse" in result
#     assert "from ch61_more import thing" in result
#     # ensure lower/equal series are excluded
#     assert all("ch51" not in r and "ch57" not in r for r in result)


# # TODO fix and reactivate test
# def test_find_incorrect_imports_ReturnsObj_Scenario1_high_threshold_only_top_matches(
#     sample_file,
# ):
#     # ESTABLISH / WHEN
#     result = find_incorrect_imports(sample_file, 59)
#     # THEN
#     assert "import ch60_bikehouse" in result
#     assert "from ch61_more import thing" in result
#     assert all("ch53" not in r and "ch55" not in r for r in result)


def test_find_incorrect_imports_ReturnsObj_Scenario2_no_matches(sample_file):
    # ESTABLISH / WHEN
    result = find_incorrect_imports(sample_file, 99)
    # THEN
    assert result == []


def test_find_incorrect_imports_ReturnsObj_Scenario3_missing_file():
    # ESTABLISH / WHEN / THEN
    with pytest_raises(FileNotFoundError):
        find_incorrect_imports("nope.py", 10)
