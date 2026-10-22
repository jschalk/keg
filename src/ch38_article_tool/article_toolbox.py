from dataclasses import dataclass
from pathlib import Path


def set_str_index(
    x_search_str: str, x_lines_list: list, x_matches_list: list, x_locations_dict: dict
) -> None:
    if x_search_str:
        for x_line_num, x_line_str in enumerate(x_lines_list, start=1):
            x_start_index = 0
            while True:
                x_col_index = x_line_str.find(x_search_str, x_start_index)
                if x_col_index == -1:
                    break
                x_matches_list.append((x_line_num, x_col_index + 1))
                x_start_index = x_col_index + 1

    x_locations_dict[x_search_str] = x_matches_list


def get_string_locations_dict(
    markdown_text: str, search_strings: list[str]
) -> dict[str, list[tuple[int, int]]]:
    """
    Locate each search string within a markdown document.

    Args:
        markdown_text: The full contents of the markdown file as a string.
        search_strings: The list of substrings to search for.

    Returns:
        A dict mapping each search string to a list of (line_number, column_number)
        tuples, both 1-indexed, for every occurrence found. A string with no
        occurrences maps to an empty list. Overlapping occurrences on the same
        line are all captured (search advances by 1 character, not by match length).
    """
    x_locations_dict: dict[str, list[tuple[int, int]]] = {}
    x_lines_list = markdown_text.splitlines()

    for x_search_str in search_strings:
        x_matches_list: list[tuple[int, int]] = []
        set_str_index(x_search_str, x_lines_list, x_matches_list, x_locations_dict)
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


@dataclass
class ArticleUnit:
    md_file_path: str = None
    ordered_required_strs: list[str] = None
    required_line_nums: list[int] = None
    missing_required: str = None
    out_of_order_req_index: list[int] = None
    out_of_order_req_str: str = None


def get_articleunit_from_file(
    file_path: Path, ordered_required_strs: list[str]
) -> ArticleUnit:
    file_str = Path(file_path).read_text(encoding="utf-8")
    str_loc_dict = get_string_locations_dict(file_str, ordered_required_strs)
    missing_required_lines = ""
    ordered_line_nums = []
    for required_str in ordered_required_strs:
        if not str_loc_dict.get(required_str):
            missing_required_lines += f", '{required_str}'"
            ordered_line_nums.append(None)
        else:
            ordered_line_nums.append(str_loc_dict.get(required_str)[0][0])
    failing_index = get_failing_index(ordered_line_nums)
    out_of_order_req_str = ""
    if failing_index:
        out_of_order_req_str = (
            f"{ordered_required_strs[failing_index]} is out of order."
        )

    return ArticleUnit(
        md_file_path=file_path,
        ordered_required_strs=ordered_required_strs,
        required_line_nums=ordered_line_nums,
        missing_required=missing_required_lines,
        out_of_order_req_index=failing_index,
        out_of_order_req_str=out_of_order_req_str,
    )
