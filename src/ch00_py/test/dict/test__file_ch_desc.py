from ch00_py.chapter_desc_main import get_chapter_descs, valid_chapter_numbers
from pytest import raises as pytest_raises
from unittest.mock import patch


def test_get_chapter_descs_Scenario0_RemovesLinterAndRef():
    # ESTABLISH
    with patch("ch00_py.chapter_desc_main.get_level1_dirs") as mock_get_dirs, patch(
        "ch00_py.chapter_desc_main.create_path"
    ) as mock_create_path:
        mock_get_dirs.return_value = [
            "intro",
            "chapter1",
            "linter",
            "ref",
            "chapter2",
        ]

        mock_create_path.side_effect = lambda src, d: f"{src}/{d}"

        # WHEN
        chapter_descs = get_chapter_descs()

        # THEN
        print(f"{chapter_descs}")
        assert chapter_descs == {
            "intro": "src/intro",
            "chapter1": "src/chapter1",
            "chapter2": "src/chapter2",
        }


def test_get_chapter_descs_Scenario1_GetsLevel1Directories():
    # ESTABLISH
    with patch("ch00_py.chapter_desc_main.get_level1_dirs") as mock_get_dirs, patch(
        "ch00_py.chapter_desc_main.create_path"
    ):
        mock_get_dirs.return_value = ["chapter1", "linter", "ref"]

        # WHEN
        get_chapter_descs()

        # THEN
        mock_get_dirs.assert_called_once_with("src")


def test_get_chapter_descs_Scenario2_RaisesErrorIf_linterIsMissing():
    """
    Current behavior: list.remove will raise ValueError
    if 'linter' or 'ref' are not present.
    """
    # ESTABLISH / WHEN / THEN
    with patch("ch00_py.chapter_desc_main.get_level1_dirs") as mock_get_dirs:
        mock_get_dirs.return_value = ["chapter1", "chapter2"]

        with pytest_raises(ValueError):
            get_chapter_descs()


def test_valid_chapter_numbers_ReturnsObj_Scenario0():
    # ESTABLISH / WHEN / THEN
    assert valid_chapter_numbers({})
    assert valid_chapter_numbers({"ch82": "dir/dir2/dir"})
    assert valid_chapter_numbers({"ch82": "/re/ch82_0", "ch83": "/re/ch83_1"})
    assert not valid_chapter_numbers({"ch82_x": "/re/ch82_0", "ch82_y": "/re/ch82_1"})
