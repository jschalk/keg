from pathlib import Path
from tomllib import load as tomllib_load


def get_version(pyproject_path="pyproject.toml"):
    path = Path(pyproject_path)

    if not path.exists():
        raise FileNotFoundError(f"{pyproject_path} not found")

    with path.open("rb") as f:
        data = tomllib_load(f)

    # Standard PEP 621 location
    if "project" in data and "version" in data["project"]:
        return data["project"]["version"]

    # Fallback: Poetry-style projects
    if "tool" in data and "poetry" in data["tool"]:
        return data["tool"]["poetry"].get("version")

    raise KeyError("Version not found in pyproject.toml")
