from os.path import exists as os_path_exists
from pathlib import Path
from pytest import fixture as pytest_fixture
from shutil import rmtree as shutil_rmtree
from src.ch00_py.file_toolbox import count_dirs_files, create_path, save_file
from tempfile import mkdtemp as tempfile_mkdtemp


@pytest_fixture
def ex_directory():
    """Fixture to create a temporary directory with files and subdirectories."""
    test_dir = Path(tempfile_mkdtemp())  # Create a temp directory

    # Create subdirectories
    (test_dir / "subdir1").mkdir()
    (test_dir / "subdir2").mkdir()

    # Create files
    (test_dir / "file1.txt").touch()
    (test_dir / "file2.log").touch()
    (test_dir / "subdir1/file3.doc").touch()  # File inside subdir (should be counted)

    yield test_dir  # Provide the test directory to the test function

    # Cleanup after the test
    shutil_rmtree(test_dir)


def test_count_dirs_files_ReturnsObj_Scenario0(ex_directory):
    # ESTABLISH / WHEN / THEN
    assert count_dirs_files(ex_directory) == 5

    # WHEN / THEN
    save_file(ex_directory, "testing.txt", "")
    assert count_dirs_files(ex_directory) == 6

    # WHEN / THEN
    test2_dir = create_path(ex_directory, "testing2")
    save_file(test2_dir, "testing.txt", "")
    assert count_dirs_files(ex_directory) == 8


def test_count_dirs_files_ReturnsObj_Scenario1_DoesNotCreateDir(temp3_fs, temp3_dir):
    # ESTABLISH
    env_dir = temp3_dir
    sub1_dir = create_path(env_dir, "sub1")
    assert os_path_exists(sub1_dir) is False

    # WHEN
    dirs_files_count = count_dirs_files(sub1_dir)

    # THEN
    assert dirs_files_count == 0
    assert os_path_exists(sub1_dir) is False
