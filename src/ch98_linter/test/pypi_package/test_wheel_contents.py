"""
test_wheel_contents.py — Builds the wheel and confirms expected files are inside.

Usage:
    pytest test_wheel_contents.py -v -s

Run from the project root (same directory as pyproject.toml).
This test is slow (it builds the wheel) so keep it out of your default
test run and invoke it explicitly before publishing.
"""

from fnmatch import fnmatch as fnmatch_fnmatch
from pathlib import Path as pathlib_Path
from pytest import fixture as pytest_fixture, mark as pytest_mark, skip as pytest_skip
from shutil import rmtree as shutil_rmtree
from subprocess import run as subprocess_run
from zipfile import ZipFile as zipfile_ZipFile

# ── Configure: files that MUST exist inside the wheel ─────────────────────────
# Use forward slashes — zip paths are always forward-slash separated.
REQUIRED_FILES = [
    "ch20_brick/brick_formats/bk00119_planunit_v0_0_0.json",
    "ch20_brick/brick_formats/bk00136_problem_healer_v0_0_0.json",
    "ch23_idea_src/idea_config.json",
    # add more as you discover missing ones, e.g.:
]

# ── Glob patterns — any wheel entry matching these must number > 0 ─────────────
REQUIRED_GLOB_PATTERNS = [
    "*.json",
    "*.yaml",
]
# ──────────────────────────────────────────────────────────────────────────────


@pytest_fixture(scope="module")
def wheel_contents() -> list[str]:
    """Build the wheel and return the list of all file paths inside it."""
    dist_dir = pathlib_Path("dist")
    dist_dir.mkdir(exist_ok=True)

    # GIVEN a pyproject.toml exists in the current directory
    # WHEN we build the wheel
    result = subprocess_run(
        [
            "python",
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(dist_dir),
        ],
        capture_output=True,
        text=True,
    )

    # THEN the build must succeed
    assert (
        result.returncode == 0
    ), f"wheel build failed:\n{result.stdout}\n{result.stderr}"

    wheels = sorted(dist_dir.glob("*.whl"), key=lambda p: p.stat().st_mtime)
    assert wheels, "No .whl file found in dist/ after build."
    wheel_path = wheels[-1]
    print(f"\nInspecting wheel: {wheel_path.name}")

    with zipfile_ZipFile(wheel_path) as zf:
        return zf.namelist()


# # ── Test 1: exact file paths ───────────────────────────────────────────────────
@pytest_mark.local_only
@pytest_mark.build_tests
@pytest_mark.parametrize("expected_file", REQUIRED_FILES)
def test_ExactFileIsPresentIn_wheel(
    wheel_contents: list[str],
    expected_file: str,
):
    # ESTABLISH
    # A built wheel and an expected file path

    # WHEN
    matches = [entry for entry in wheel_contents if entry.endswith(expected_file)]

    # THEN
    assert matches, (
        f"'{expected_file}' not found in wheel.\n"
        f"  Likely causes:\n"
        f"  1. Missing __init__.py in one of its parent directories\n"
        f"  2. Not covered by [tool.setuptools.package-data] in pyproject.toml\n"
        f"  Fix: check every directory from src/ down to the file has __init__.py\n"
        f'       and pyproject.toml has: "*" = ["**/*.json"]'
    )


# ── Test 2: glob patterns — at least one match each ───────────────────────────
@pytest_mark.local_only
@pytest_mark.build_tests
@pytest_mark.parametrize("pattern", REQUIRED_GLOB_PATTERNS)
def test_GlobPatternHasAtLeastOneMatchIn_wheel(wheel_contents: list[str], pattern: str):
    # sourcery skip: no-conditionals-in-tests
    # GIVEN a built wheel and a glob pattern
    # WHEN we search all wheel entries for files matching the pattern
    matches = [
        entry
        for entry in wheel_contents
        if fnmatch_fnmatch(pathlib_Path(entry).name, pattern)
    ]

    # THEN skip if no such files exist in the project at all, fail if they exist but aren't in the wheel
    project_files = list(pathlib_Path("src").rglob(f"**/{pattern}"))
    if not project_files:
        pytest_skip(f"No {pattern} files exist in src/ — pattern not applicable")

    assert matches, (
        f"No files matching '{pattern}' found in the wheel but {len(project_files)} exist in src/.\n"
        f"  Check [tool.setuptools.package-data] in pyproject.toml."
    )


# ── Test 3: print all non-py files for visibility ─────────────────────────────
@pytest_mark.local_only
@pytest_mark.build_tests
def test_DataFilesIn_wheelAreVisible(wheel_contents: list[str]):
    # GIVEN a built wheel
    # WHEN we filter out .py files and dist-info metadata
    data_files = [
        f for f in wheel_contents if not f.endswith(".py") and ".dist-info/" not in f
    ]

    # THEN print them all for inspection (this test always passes)
    print(f"\nData files in wheel ({len(data_files)} total):")
    for f in sorted(data_files):
        print(f"  {f}")
    assert data_files
    shutil_rmtree("src//keg2.egg-info")
