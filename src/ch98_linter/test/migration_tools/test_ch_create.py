from ch00_py.file_toolbox import open_json
from ch98_linter.chapter_create_tool import create_chapter_files
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_create_chapter_files_CreatesFiles_Scenario0_Straightforward(temp3_fs):
    # ESTABLISH
    chapter_number = 98
    chapter_dict = {
        "src_dir": str(temp3_fs),
        "chapter_blurb": "Symon papers.",
        "chapter_content": "Symon and Symon related papers.",
        "chapter_description": "symon",
        "chapter_number": 98,
        "chapter_ref_catalogue": "y",
        "ontology summary": "Symon is an important writer. An ontological tentpole.",
    }
    chapter_dir = temp3_fs / "ch98_symon"
    ref_dir = chapter_dir / "_ref"
    chapter_init_py_path = chapter_dir / "__init__.py"
    ref_init_path = ref_dir / "__init__.py"
    ref_ai_summary_1min_path = ref_dir / f"ch{chapter_number:02}_ai_summary_1min.md"
    ref_ch_json_path = ref_dir / f"ch{chapter_number:02}_ref.json"
    ref_semantic_types_path = ref_dir / f"ch{chapter_number:02}_semantic_types.py"
    assert not os_path_exists(chapter_dir)
    assert not os_path_exists(ref_dir)
    assert not os_path_exists(chapter_init_py_path)
    assert not os_path_exists(ref_init_path)
    assert not os_path_exists(ref_ai_summary_1min_path)
    assert not os_path_exists(ref_ch_json_path)
    assert not os_path_exists(ref_semantic_types_path)

    # WHEN
    create_chapter_files(chapter_dict)

    # THEN
    assert os_path_exists(chapter_dir)
    assert os_path_exists(ref_dir)
    assert os_path_exists(chapter_init_py_path)
    assert os_path_exists(ref_init_path)
    assert os_path_exists(ref_ai_summary_1min_path)
    assert os_path_exists(ref_ch_json_path)
    assert os_path_exists(ref_semantic_types_path)
    assert chapter_init_py_path.read_text() == "pass"
    assert ref_init_path.read_text() == "pass"
    assert ref_ai_summary_1min_path.read_text() == ""
    expected_chapter_dict = {
        "chapter_blurb": "Symon papers.",
        "chapter_content": "Symon and Symon related papers.",
        "chapter_description": "ch98_symon",
        "chapter_number": 98,
        "chapter_ref_catalogue": "y",
        "ontology summary": "Symon is an important writer. An ontological tentpole.",
    }
    curr_chapter_dict = open_json(ref_ch_json_path)
    assert curr_chapter_dict == expected_chapter_dict, curr_chapter_dict
    assert ref_semantic_types_path.exists()


def test_create_chapter_files_CreatesFiles_Scenario1_ChDirExists(temp3_fs):
    # ESTABLISH
    chapter_dict = {
        "src_dir": str(temp3_fs),
        "chapter_blurb": "Symon papers.",
        "chapter_content": "Symon and Symon related papers.",
        "chapter_description": "symon",
        "chapter_number": 98,
        "chapter_ref_catalogue": "y",
        "ontology summary": "Symon is an important writer. An ontological tentpole.",
    }
    chapter_dir = temp3_fs / "ch98_symon"
    chapter_dir.mkdir()

    # WHEN / THEN
    with pytest_raises(FileExistsError):
        create_chapter_files(chapter_dict)
