from src.ch00_py.file_toolbox import create_path, save_file
from src.ch00_py.notebook_toolbox import get_imports_from_source
from src.ref.keywords import Ch00Keywords as kw, ExampleStrs as exx


def test_get_imports_from_source_ReturnsObj_Scenario0_empty_file_returns_empty_list():
    # ESTABLISH
    source = ""
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == []


def test_get_imports_from_source_ReturnsObj_Scenario1_simple_import():
    # ESTABLISH
    source = "import os"
    # WHEN / THEN
    assert get_imports_from_source(source) == ["import os"]


def test_get_imports_from_source_ReturnsObj_Scenario2_multiple_imports():
    # ESTABLISH
    source = """
import os
import sys
"""
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["import os", "import sys"]


def test_get_imports_from_source_ReturnsObj_Scenario3_import_with_alias():
    # ESTABLISH
    source = "import numpy as np"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["import numpy as np"]


def test_get_imports_from_source_ReturnsObj_Scenario4_dotted_import():
    # ESTABLISH
    source = "import numpy.linalg"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["import numpy.linalg"]


def test_get_imports_from_source_ReturnsObj_Scenario5_from_import():
    # ESTABLISH
    source = "from collections import defaultdict"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from collections import defaultdict"]


def test_get_imports_from_source_ReturnsObj_Scenario6_from_import_multiple_names():
    # ESTABLISH
    source = "from math import sin, cos"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from math import sin, cos"]


def test_get_imports_from_source_ReturnsObj_Scenario7_from_import_with_alias():
    # ESTABLISH
    source = "from module import thing as t"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from module import thing as t"]


def test_get_imports_from_source_ReturnsObj_Scenario8_relative_import():
    # ESTABLISH
    source = "from .utils import helper"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from .utils import helper"]


def test_get_imports_from_source_ReturnsObj_Scenario9_double_relative_import():
    # ESTABLISH
    source = "from ..core import value"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from ..core import value"]


def test_get_imports_from_source_ReturnsObj_Scenario10_all_import():
    # ESTABLISH
    source = "from package import *"
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from package import *"]


def test_get_imports_from_source_ReturnsObj_Scenario11_imports_inside_function_are_detected():
    # ESTABLISH
    source = """
def func():
    import os
"""
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["import os"]


def test_get_imports_from_source_ReturnsObj_Scenario12_imports_inside_try_except():
    # ESTABLISH
    source = """
try:
    import ujson as json
except ImportError:
    import json
"""
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["import ujson as json", "import json"]


def test_get_imports_from_source_ReturnsObj_Scenario13_type_checking_import():
    # ESTABLISH
    source = """
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypkg import MyType
"""
    # WHEN
    result = get_imports_from_source(source)
    # THEN
    assert result == ["from typing import TYPE_CHECKING", "from mypkg import MyType"]
