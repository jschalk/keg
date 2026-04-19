from ch00_py.version_reader import get_version
from pathlib import Path


def test_get_version_ReturnsObj_Scenario0_Mocked(tmp_path):
    # ESTABLISH
    pyproject = tmp_path / "pyproject.toml"

    pyproject.write_text(
        """
[project]
name = "test-project"
version = "1.2.3"
"""
    )
    # WHEN
    result = get_version(pyproject)
    # THEN
    assert result == "1.2.3"


def test_get_version_ReturnsObj_Scenario1_CurrentFile():
    # ESTABLISH / WHEN
    version = get_version()
    # THEN
    assert isinstance(version, str)
    assert version  # not empty
