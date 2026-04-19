from ch00_py.file_toolbox import create_path
from ch17_idea.idea_config import get_idea_types, get_quick_ideas_column_ref
from ch17_idea.idea_db_tool import get_all_excel_sheet_names
from ch18_etl_config.etl_config import get_etl_stage_types_config_dict
from dataclasses import dataclass
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    read_excel as pandas_read_excel,
)
from pathlib import Path


def get_all_excel_ideasheets(dir: str) -> set[tuple[str, str, str]]:
    return get_all_excel_sheet_names(dir, get_idea_types())


@dataclass
class IdeaFileRef:
    file_dir: str = None
    filename: str = None
    sheet_name: str = None
    idea_type: str = None

    def get_csv_filename(self) -> str:
        return "" if self.idea_type is None else f"{self.idea_type}.csv"


def get_all_ideafilerefs(dir: str) -> list[IdeaFileRef]:
    ideasheets = get_all_excel_ideasheets(dir)
    candidate_ideas = set()
    for dir, filename, sheet_name in ideasheets:
        for idea_type in get_idea_types():
            if sheet_name.find(idea_type) >= 0:
                candidate_ideas.add((dir, filename, sheet_name, idea_type))

    candidate_ideas = sorted(candidate_ideas, key=lambda x: (x[0], x[1], x[2]))
    idea_dfs = []
    for dir, filename, sheet_name, idea_type in candidate_ideas:
        idea_columns = get_quick_ideas_column_ref().get(idea_type)
        file_path = create_path(dir, filename)
        df = pandas_read_excel(file_path, sheet_name=sheet_name)
        if idea_columns.issubset(set(df.columns)):
            idea_dfs.append(IdeaFileRef(dir, filename, sheet_name, idea_type))
    return idea_dfs


def get_etl_db_sheets_tier2_order() -> list:
    etl_config = get_etl_stage_types_config_dict()
    x_list = sorted(etl_config.keys(), key=lambda k: etl_config[k]["stage_type_order"])
    final_list = x_list[:2]
    final_list.extend(["ideax_raw", "ideax_agg", "ideax_vld"])
    final_list.extend(x_list[5:])
    return final_list


def reorder_etl_db_sheets(filepath: str | Path) -> None:
    """
    Reorders sheets in an Excel file based on:
      1. Prefix priority (tier1_prefixes)
      2. Postfix priority (tier2_postfixes)
      3. Original order fallback

    Modifies the file in place.
    """
    # tier1_prefixes = ["ii"]
    tier2_postfixes = get_etl_db_sheets_tier2_order()
    filepath = Path(filepath)

    # Read all sheets
    sheets: dict[str, DataFrame] = pandas_read_excel(filepath, sheet_name=None)

    original_order = list(sheets.keys())

    def sort_key(sheet_name: str):
        # Tier 1: prefix match
        # for i, prefix in enumerate(tier1_prefixes):
        #     if sheet_name.startswith(prefix):
        #         return (0, i, sheet_name)

        # Tier 2: postfix match
        for i, postfix in enumerate(tier2_postfixes):
            if sheet_name.endswith(postfix):
                return (1, i, sheet_name)

        # Tier 3: fallback (do not preserve original order)
        return (2, sheet_name)

    # Sort sheet names
    sorted_sheet_names = sorted(sheets.keys(), key=sort_key)

    # Write back in new order
    with pandas_ExcelWriter(filepath, engine="xlsxwriter") as writer:
        for sheet_name in sorted_sheet_names:
            sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
