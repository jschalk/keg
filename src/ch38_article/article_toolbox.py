from dataclasses import dataclass
from pathlib import Path
from re import IGNORECASE as re_IGNORECASE, search as re_search, match as re_match
from pathlib import Path


def set_snippet_indexs(
    x_search_snippet: str,
    x_lines_list: list,
    x_matches_list: list,
    x_locations_dict: dict,
) -> None:
    if x_search_snippet:
        for x_line_num, x_line_snippet in enumerate(x_lines_list, start=1):
            x_start_index = 0
            while True:
                x_col_index = x_line_snippet.find(x_search_snippet, x_start_index)
                if x_col_index == -1:
                    break
                x_matches_list.append((x_line_num, x_col_index + 1))
                x_start_index = x_col_index + 1

    x_locations_dict[x_search_snippet] = x_matches_list


def get_snippets_locations_dict(
    markdown_text: str, search_snippets: set[str]
) -> dict[str, list[tuple[int, int]]]:
    """
    Locate each search string within a markdown document.

    Args:
        markdown_text: The full contents of the markdown file as a string.
        search_snippets: The list of substrings to search for.

    Returns:
        A dict mapping each search string to a list of (line_number, column_number)
        tuples, both 1-indexed, for every occurrence found. A string with no
        occurrences maps to an empty list. Overlapping occurrences on the same
        line are all captured (search advances by 1 character, not by match length).
    """
    x_locations_dict: dict[str, list[tuple[int, int]]] = {}
    x_lines_list = markdown_text.splitlines()

    for x_search_snippet in search_snippets:
        x_matches_list: list[tuple[int, int]] = []
        set_snippet_indexs(
            x_search_snippet, x_lines_list, x_matches_list, x_locations_dict
        )
    return x_locations_dict


def get_failing_index(numbers: list[int | None]) -> int | None:
    previous = None

    for i, number in enumerate(numbers):
        if number is None:
            continue

        if previous is not None and number <= previous:
            return i

        previous = number

    return None


def get_default_article_snippets_order() -> list[str]:
    return ["**Author:**", "**Date:**", "**Source:**", "**Copied to Keg:**"]


@dataclass
class ArticleUnit:
    md_file_path: str = None
    required_snippets: list[str] = None
    ordered_line_nums: list[int] = None
    missing_required: str = None
    ordered_snippets: str = None
    out_of_order_req_index: list[int] = None
    out_of_order_req_str: str = None


def get_ordered_line_nums(file_str: str, ordered_snippets: set[str]) -> list[int]:
    str_loc_dict = get_snippets_locations_dict(file_str, ordered_snippets)
    ordered_line_nums = []
    for ordered_str in ordered_snippets:
        if not str_loc_dict.get(ordered_str):
            ordered_line_nums.append(None)
        else:
            ordered_line_nums.append(str_loc_dict.get(ordered_str)[0][0])
    return ordered_line_nums


def get_articleunit_from_file(
    file_path: Path, required_snippets: list[str], ordered_snippets: list[str]
) -> ArticleUnit:
    file_str = Path(file_path).read_text(encoding="utf-8")
    missing_required_lines = "".join(
        f", '{required_snippet}'"
        for required_snippet in required_snippets
        if required_snippet not in file_str
    )
    ordered_line_nums = get_ordered_line_nums(file_str, ordered_snippets)
    failing_index = get_failing_index(ordered_line_nums)
    out_of_order_req_str = ""
    if failing_index:
        out_of_order_req_str = f"{ordered_snippets[failing_index]} is out of order."

    return ArticleUnit(
        md_file_path=file_path,
        required_snippets=required_snippets,
        ordered_line_nums=ordered_line_nums,
        missing_required=missing_required_lines,
        out_of_order_req_index=failing_index,
        out_of_order_req_str=out_of_order_req_str,
    )


def get_markdown_file_metadata(directory: Path) -> dict[str, dict[str, str | None]]:
    """Return author and date metadata from first-level Markdown files."""
    result = {}

    for file_path in directory.glob("*.md"):
        if "catalogue" in file_path.stem:
            continue

        content = file_path.read_text(encoding="utf-8")
        first_line = next(
            (line.strip() for line in content.splitlines() if line.strip()),
            "",
        )
        post_match = re_match(r"^#\s+(.+?)\s*#*$", first_line)

        author_match = re_search(
            r"\*\*Author:\*\*\s*(.*?)\s*(?:<br\s*/?>|\n)", content, re_IGNORECASE
        )
        date_match = re_search(
            r"\*\*Date:\*\*\s*(.*?)\s*(?:<br\s*/?>|\n)", content, re_IGNORECASE
        )

        result[file_path.name] = {
            "author": author_match.group(1).strip() if author_match else None,
            "date": date_match.group(1).strip() if date_match else None,
            "post": post_match.group(1).strip() if post_match else None,
        }

    return result


def create_markdown_table_of_contents(
    metadata: dict[str, dict[str, str | None]],
) -> str:
    """Return a Markdown table of contents."""

    for file_metadata in metadata.values():
        file_metadata["author"] = file_metadata.get("author") or "Unknown author"
        file_metadata["date"] = file_metadata.get("date") or "Undated"
        file_metadata["post"] = file_metadata.get("post") or "Untitled"

    sorted_items = sorted(
        metadata.items(),
        key=lambda item: (
            item[1].get("author", "").lower(),
            item[1].get("post", "").lower(),
        ),
    )

    lines = ["# Table of Contents", ""]
    for file_name, file_metadata in sorted_items:
        title = Path(file_name).stem.replace("_", " ").replace("-", " ").title()
        author = file_metadata.get("author") or "Unknown author"
        date = file_metadata.get("date") or "Undated"
        post = file_metadata.get("post") or "Untitled"

        lines.extend([f"**[{post}](./{file_name})** {author} - {date}<br>", ""])
    lines.extend(["---"])
    md_body = "\n".join(lines).rstrip() + "\n"
    md_trailer = """
**Author:** Algorithm<br>
**Date:** May not be up to date<br>
**Source:** Generated automatically from chapter contents<br>
**Copied to Keg:** N/A <br>
"""
    return f"{md_body}{md_trailer}"
