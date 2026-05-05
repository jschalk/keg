from ch17_brick._ref.ch17_semantic_types import SheetName
from inspect import getdoc as inspect_getdoc
from ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_SheetName_Exists():
    # ESTABLISH
    br00104_str = "br00104"
    # WHEN
    br00104_sheetname = SheetName(br00104_str)
    # THEN
    assert br00104_sheetname == br00104_str
    doc_str = f"A string used as {kw.SheetName} for SpreadSheet files."
    assert inspect_getdoc(br00104_sheetname) == doc_str
