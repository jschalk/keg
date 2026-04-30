# test_pip_version.py
import importlib
import pytest
import subprocess
import sys

# # TODO reactivate this test and get it working
# def test_download_and_check_version(tmp_path, check_pip):
#     # sourcery skip: no-conditionals-in-tests
#     if not check_pip:
#         pytest.skip("use --check-pip to run this test")

#     package_name = "keg2"

#     install_dir = tmp_path / "site"
#     install_dir.mkdir()

#     subprocess.check_call(
#         [
#             sys.executable,
#             "-m",
#             "pip",
#             "install",
#             package_name,
#             "--target",
#             str(install_dir),
#         ]
#     )

#     sys.path.insert(0, str(install_dir))
#     module = importlib.import_module(package_name)
#     print(f"{module.__name__} version: {module.__version__}")
#     # expected_version = get_version()
#     # print(f"{expected_version}")
#     assert module.__version__ == "huh"
