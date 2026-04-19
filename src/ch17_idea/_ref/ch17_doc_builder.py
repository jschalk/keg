from ch00_py.file_toolbox import create_path, open_json
from ch17_idea.idea_config import get_default_sorted_list, get_idea_formats_dir
from pathlib import Path


def get_idea_md(idea_config) -> str:
    # Create per-idea Markdown file
    idea = idea_config["idea_type"]
    attr_names = set(idea_config["attributes"].keys())
    dimens = list(idea_config["dimens"])
    sorted_attrs = get_default_sorted_list(attr_names)

    idea_md_lines = [
        f"# Idea `{idea}`\n",
        f"## Dimens `{dimens}`\n",
        "## Attributes",
        *(f"- `{attr}`" for attr in sorted_attrs),
    ]
    return "\n".join(idea_md_lines) + "\n"


def get_idea_mds(idea_format_dir: str = None) -> dict[str,]:
    if not idea_format_dir:
        idea_format_dir = get_idea_formats_dir()

    idea_formats_dir = Path(idea_format_dir)
    idea_mds = {}
    for json_path in sorted(idea_formats_dir.glob("*.json")):
        idea_format = open_json(json_path)
        idea_type = idea_format["idea_type"]
        idea_mds[idea_type] = get_idea_md(idea_format)

    return idea_mds


def get_idea_formats_md():
    idea_formats_dir = Path(get_idea_formats_dir())

    manifest_lines = []
    for json_path in sorted(idea_formats_dir.glob("*.json")):
        data = open_json(json_path)

        idea = data["idea_type"]
        attr_names = set(data["attributes"].keys())
        sorted_attrs = get_default_sorted_list(attr_names)
        idea_md_path = create_path("idea_formats", f"{idea}.md")
        manifest_line = f"- [`{idea}`]({idea_md_path}): " + ", ".join(sorted_attrs)
        manifest_lines.append(manifest_line)

    # Where the Markdown manifest will be written
    return "# Idea Manifest\n\n" + "\n".join(manifest_lines)
