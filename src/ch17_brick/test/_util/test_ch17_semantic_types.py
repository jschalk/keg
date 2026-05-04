from ch17_brick._ref.ch17_semantic_types import SheetName
from inspect import getdoc as inspect_getdoc
from ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_SheetName_Exists():
    # ESTABLISH
    ii00104_str = "ii00104"
    # WHEN
    ii00104_sheetname = SheetName(ii00104_str)
    # THEN
    assert ii00104_sheetname == ii00104_str
    doc_str = f"A string used as {kw.SheetName} for SpreadSheet files."
    assert inspect_getdoc(ii00104_sheetname) == doc_str
