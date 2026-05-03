from ch00_py.file_toolbox import create_path
from ch24_idea_dst._ref.ch24_path import create_idea0001_path
from inspect import getdoc as inspect_getdoc
from pytest import mark as pytest_mark
from ref.keywords import Ch24Keywords as kw, ExampleStrs as exx

IDEA0001_FILENAME = "idea0001.xlsx"


def test_ch24_path_constants_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert IDEA0001_FILENAME == "idea0001.xlsx"


def test_create_idea0001_path_ReturnsObj(temp3_dir):
    # ESTABLISH
    output_dir = temp3_dir

    # WHEN
    gen_idea0001_xlsx_path = create_idea0001_path(output_dir)

    # THEN
    expected_idea0001_path = create_path(output_dir, IDEA0001_FILENAME)
    assert gen_idea0001_xlsx_path == expected_idea0001_path


@pytest_mark.skip_on_linux
def test_create_idea0001_path_HasDocString():
    # ESTABLISH
    doc_str = create_idea0001_path(output_dir="output_dir")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert inspect_getdoc(create_idea0001_path) == doc_str
