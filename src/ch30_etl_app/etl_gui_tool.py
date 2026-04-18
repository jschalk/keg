from dataclasses import dataclass
from io import StringIO
import pandas as pd
from pandas import (
    DataFrame as pandas_DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    read_csv as pandas_read_csv,
    read_excel as pandas_read_excel,
)
from pathlib import Path
from platform import system as platform_system
from src.ch00_py.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.ch00_py.file_toolbox import create_path, delete_dir
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch07_person_logic.person_main import personunit_shop
from src.ch13_time.epoch_config import get_creg_config, get_five_config
from src.ch13_time.epoch_main import epochunit_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch17_idea.idea_belief_csv import (
    add_momentunits_to_belief_csv_strs,
    add_personunit_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from src.ch17_idea.idea_db_tool import (
    csv_dict_to_excel,
    prettify_excel_file,
    remove_empty_sheets,
)
from src.ch21_world.world import worlddir_shop
from sys import platform
from typing import Callable


@dataclass
class ETLAppSettings:
    mono: str
    bg: str
    bg_card: str
    bg_red: str
    border: str
    accent: str
    accent_dim: str
    fg: str
    fg_dim: str
    fg_black: str
    entry_bg: str
    btn_active: str
    platform_font: str


def get_app_glb_attrs() -> ETLAppSettings:
    is_windows = platform_system() == "Windows"
    platform_font = ("Courier New", 17, "bold") if is_windows else ("Menlo", 16, "bold")
    return ETLAppSettings(
        mono=("Courier New", 9) if is_windows else ("Menlo", 10),
        bg="#1a1a1f",
        bg_card="#22222a",
        bg_red="#ff5f57",
        border="#33333d",
        accent="#e8c547",
        accent_dim="#b89a2f",
        fg="#e4e4e8",
        fg_dim="#7a7a88",
        fg_black="#0d0d10",
        entry_bg="#13131a",
        btn_active="#f0d060",
        platform_font=platform_font,
    )


def get_app_default_me_personname() -> str:
    return "Emmanuel"


def get_app_default_you_personname() -> str:
    return "Steve"


def get_app_default_world_name() -> str:
    return "my_first_world"


def get_app_default_dir(is_windows: bool | None = None) -> Path:
    if is_windows is None:
        is_windows = platform_system().lower().startswith("win")
    return Path("C:/keg/worlds") if is_windows else Path.home() / "keg" / "worlds"


def get_app_default_dirs(default_root: Path) -> dict[str, Path]:
    x_world_name = get_app_default_world_name()
    x_worlddir = worlddir_shop(world_name=x_world_name, worlds_dir=default_root)
    return {
        "world_name": x_world_name,
        "working": x_worlddir.worlds_dir,
        "beliefs_src": x_worlddir.beliefs_src_dir,
        "ideas_src": x_worlddir.ideas_src_dir,
        "output": x_worlddir.output_dir,
    }


def fill_spark_face_in_directory(directory: str, face_name: str) -> None:
    """
    For every Excel file in a directory:
    - For every sheet:
        - If 'spark_face' column exists
        - Replace empty / NaN / 'nan' values with `face_name`
    - Overwrites the original file
    """
    directory_path = Path(directory)

    for file_path in directory_path.glob("*.xlsx"):
        # Load all sheets
        sheets = pandas_read_excel(file_path, sheet_name=None)

        updated_sheets = {}
        file_modified = False

        for sheet_name, df in sheets.items():
            if "spark_face" in df.columns:
                # Cast column to string dtype
                df["spark_face"] = df["spark_face"].astype("string")
                # Normalize values: treat "", "nan", None as missing
                mask = (
                    df["spark_face"].isna()
                    | (df["spark_face"].astype(str).str.strip().str.lower() == "nan")
                    | (df["spark_face"].astype(str).str.strip() == "")
                )

                if mask.any():
                    df.loc[mask, "spark_face"] = face_name
                    file_modified = True

            updated_sheets[sheet_name] = df

        # Only rewrite file if something changed
        if file_modified:
            with pandas_ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
                for sheet_name, df in updated_sheets.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)


def create_simple_1m2p2pledges_belief_csvs() -> dict[str, str]:
    mmt01_rope = create_rope("mmt01")
    steve_name = "Steve"
    emman_name = "Emmanuel"
    steve_person = personunit_shop(steve_name, mmt01_rope)
    emman_person = personunit_shop(emman_name, mmt01_rope)
    steve_person.add_contactunit(steve_name)
    steve_person.add_contactunit(emman_name)
    emman_person.add_contactunit(emman_name)
    emman_person.add_contactunit(steve_name)
    music_rope = emman_person.make_l1_rope("enjoy music")
    golf_rope = emman_person.make_l1_rope("play disc golf")
    steve_person.add_plan(music_rope, 1, True)
    emman_person.add_plan(golf_rope, 1, True)
    belief_csv_strs = create_init_belief_idea_csv_strs()
    steve_person.conpute()
    emman_person.conpute()
    add_personunit_to_belief_csv_strs(steve_person, belief_csv_strs, ",")
    add_personunit_to_belief_csv_strs(emman_person, belief_csv_strs, ",")
    return transform_ii00029_into_ii00013_in_csvs(belief_csv_strs, mmt01_rope)


def create_simple_1m2p5pledges_belief_csvs() -> dict[str, str]:
    mmt01_rope = create_rope("mmt01")
    steve_name = "Steve"
    emman_name = "Emmanuel"
    steve_person = personunit_shop(steve_name, mmt01_rope)
    emman_person = personunit_shop(emman_name, mmt01_rope)
    steve_person.add_contactunit(steve_name)
    steve_person.add_contactunit(emman_name)
    emman_person.add_contactunit(emman_name)
    emman_person.add_contactunit(steve_name)
    home_rope = emman_person.make_l1_rope("clean home")
    dishes_rope = emman_person.make_rope(home_rope, "clean dishes with baking soda")
    clothes_rope = emman_person.make_rope(home_rope, "clean clothes with baking soda")
    counters_str = "clean kitchen counters with baking soda"
    counters_rope = emman_person.make_rope(home_rope, counters_str)
    handout_str = "give neighbor any baking soda they want"
    handout_rope = emman_person.make_rope(home_rope, handout_str)
    ask_rope = emman_person.make_rope(home_rope, "ask neighbor to use baking soda")
    music_rope = emman_person.make_l1_rope("enjoy music")
    steve_person.add_plan(music_rope, 1, True)
    steve_person.add_plan(dishes_rope, 10, True)
    steve_person.add_plan(clothes_rope, 12, True)
    steve_person.add_plan(counters_rope, 5, True)
    steve_person.add_plan(handout_rope, 20, True)
    steve_person.add_plan(ask_rope, 3, True)
    emman_person.add_plan(music_rope, 10, True)
    belief_csv_strs = create_init_belief_idea_csv_strs()
    steve_person.conpute()
    emman_person.conpute()
    add_personunit_to_belief_csv_strs(steve_person, belief_csv_strs, ",")
    add_personunit_to_belief_csv_strs(emman_person, belief_csv_strs, ",")
    return transform_ii00029_into_ii00013_in_csvs(belief_csv_strs, mmt01_rope)


def create_simple_2m2p5pledges_belief_csvs() -> dict[str, str]:
    # sourcery skip: extract-duplicate-method
    mmt01_rope = create_rope("mmt01")
    steve_name = "Steve"
    emman_name = "Emmanuel"
    m1_steve_person = personunit_shop(steve_name, mmt01_rope)
    m1_emman_person = personunit_shop(emman_name, mmt01_rope)
    m1_steve_person.add_contactunit(steve_name)
    m1_steve_person.add_contactunit(emman_name)
    m1_emman_person.add_contactunit(emman_name)
    m1_emman_person.add_contactunit(steve_name)
    home_rope = m1_emman_person.make_l1_rope("clean home")
    dishes_rope = m1_emman_person.make_rope(home_rope, "clean dishes with baking soda")
    clothes_rope = m1_emman_person.make_rope(
        home_rope, "clean clothes with baking soda"
    )
    counters_str = "clean kitchen counters with baking soda"
    counters_rope = m1_emman_person.make_rope(home_rope, counters_str)
    handout_str = "give neighbor any baking soda they want"
    handout_rope = m1_emman_person.make_rope(home_rope, handout_str)
    ask_rope = m1_emman_person.make_rope(home_rope, "ask neighbor to use baking soda")
    music_rope = m1_emman_person.make_l1_rope("enjoy music")
    m1_steve_person.add_plan(music_rope, 1, True)
    m1_steve_person.add_plan(dishes_rope, 10, True)
    m1_steve_person.add_plan(clothes_rope, 12, True)
    m1_steve_person.add_plan(counters_rope, 5, True)
    m1_steve_person.add_plan(handout_rope, 20, True)
    m1_steve_person.add_plan(ask_rope, 3, True)
    m1_emman_person.add_plan(music_rope, 10, True)
    belief_csv_strs = create_init_belief_idea_csv_strs()
    m1_steve_person.conpute()
    m1_emman_person.conpute()
    add_personunit_to_belief_csv_strs(m1_steve_person, belief_csv_strs, ",")
    add_personunit_to_belief_csv_strs(m1_emman_person, belief_csv_strs, ",")

    # add heart moment
    heart01_rope = create_rope("heart01")
    steve_name = "Steve"
    emman_name = "Emmanuel"
    h1_steve_person = personunit_shop(steve_name, heart01_rope)
    h1_emman_person = personunit_shop(emman_name, heart01_rope)
    h1_steve_person.add_contactunit(steve_name)
    h1_steve_person.add_contactunit(emman_name)
    h1_emman_person.add_contactunit(emman_name)
    h1_emman_person.add_contactunit(steve_name)
    dance_rope = h1_emman_person.make_l1_rope("dance")
    disco_rope = h1_emman_person.make_rope(dance_rope, "disco")
    bebop_rope = h1_emman_person.make_rope(dance_rope, "bebop")
    tango_rope = h1_emman_person.make_rope(dance_rope, "tango")
    h1_emman_person.add_plan(disco_rope, 1, True)
    h1_steve_person.add_plan(bebop_rope, 10, True)
    h1_steve_person.add_plan(tango_rope, 3, True)
    h1_steve_person.conpute()
    h1_emman_person.conpute()
    add_personunit_to_belief_csv_strs(h1_steve_person, belief_csv_strs, ",")
    add_personunit_to_belief_csv_strs(h1_emman_person, belief_csv_strs, ",")
    return transform_ii00029_into_ii00013_in_csvs(belief_csv_strs, heart01_rope)


def create_emmanuel_lovemaking_belief_csvs() -> dict[str, str]:
    mlove01_rope = create_rope("loving moment")
    emman_name = "Emmanuel"
    mlove_name = "MyLove"
    emman_person = personunit_shop(emman_name, mlove01_rope)
    mlove_person = personunit_shop(mlove_name, mlove01_rope)
    emman_person.add_contactunit(emman_name)
    emman_person.add_contactunit(mlove_name)
    mlove_person.add_contactunit(mlove_name)
    mlove_person.add_contactunit(emman_name)
    mlove_rope = emman_person.make_l1_rope("make love")
    emman_person.add_plan(mlove_rope, 1, True)
    belief_csv_strs = create_init_belief_idea_csv_strs()
    emman_person.conpute()
    add_personunit_to_belief_csv_strs(emman_person, belief_csv_strs, ",")
    return transform_ii00029_into_ii00013_in_csvs(belief_csv_strs, mlove01_rope)


def transform_ii00029_into_ii00013_in_csvs(belief_csv_strs, moment_rope) -> dict:
    ii00013_csv = ""
    for sheetname_key, csv_str in belief_csv_strs.items():
        if sheetname_key == "ii00028":
            ii00013_csv = transform_ii00029_into_ii00013_csv(csv_str, moment_rope)
    belief_csv_strs["ii00013"] = ii00013_csv
    return {
        sheetname_key: csv_str
        for sheetname_key, csv_str in belief_csv_strs.items()
        if sheetname_key not in {"ii00020", "ii00029", "ii00028"}
    }


def transform_ii00029_into_ii00013_csv(csv_str: str, moment_rope: str):
    # Load CSV into DataFrame
    # String → DataFrame
    df = pandas_read_csv(StringIO(csv_str))

    # Delete column if it exists
    to_delete_columns = {
        "begin",
        "close",
        "addin",
        "numor",
        "denom",
        "morph",
        "gogo_want",
        "stop_want",
        "problem_bool",
    }
    for to_delete_column in to_delete_columns:
        if to_delete_column in df.columns:
            df = df.drop(columns=[to_delete_column])

    # Add new column
    df.insert(2, "moment_rope", moment_rope)

    # DataFrame → CSV string
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()


def create_five_time_config_belief_csvs() -> dict[str, str]:
    team_five_rope = create_rope("teamfive")
    five_epochunit = epochunit_shop(get_five_config())
    five_moment = momentunit_shop(team_five_rope, None, five_epochunit)
    moments = {five_moment.moment_rope: five_moment}
    belief_csv_strs = create_init_belief_idea_csv_strs()
    add_momentunits_to_belief_csv_strs(moments, belief_csv_strs, ",")

    with_spark_face_csvs = {}
    for csv_key, csv_str in belief_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "spark_face", "ESchalk")
        csv_str = delete_column_from_csv_string(csv_str, "spark_num")
        with_spark_face_csvs[csv_key] = csv_str
    return with_spark_face_csvs


def create_elpaso_time_config_belief_csvs() -> dict[str, str]:
    elpaso_rope = create_rope("ElPaso")
    creg_epochunit = epochunit_shop(get_creg_config())
    elpaso_moment = momentunit_shop(elpaso_rope, None, creg_epochunit)
    moments = {elpaso_moment.moment_rope: elpaso_moment}
    belief_csv_strs = create_init_belief_idea_csv_strs()
    add_momentunits_to_belief_csv_strs(moments, belief_csv_strs, ",")

    with_spark_face_csvs = {}
    for csv_key, csv_str in belief_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "spark_face", "ESchalk")
        csv_str = delete_column_from_csv_string(csv_str, "spark_num")
        with_spark_face_csvs[csv_key] = csv_str
    return with_spark_face_csvs


def create_emmanuel_belief_belief_csvs() -> dict[str, str]:
    # TODO dict[str, str]s and save to file
    # prnt("create_emmanuel_belief_file...")
    pass


def create_example_moment_ledger_belief_csvs() -> dict[str, str]:
    # TODO dict[str, str]s and save to file
    # prnt("create_example_moment_ledger_file...")
    pass


def create_example_moment_budget_belief_csvs() -> dict[str, str]:
    # TODO dict[str, str]s and save to file
    # prnt("create_example_moment_budget_file...")
    pass


def save_and_prettify_excel_file(
    belief_csvs: dict[str, str], dest_dir, dest_filename: str
):
    dest_dir = str(dest_dir)
    dest_file_path = create_path(dest_dir, dest_filename)
    delete_dir(dest_file_path)
    csv_dict_to_excel(belief_csvs, dest_dir, dest_filename)
    remove_empty_sheets(dest_file_path)
    prettify_excel_file(dest_file_path)


def create_simple_1m2p2pledges_belief_file(dest_dir: str):
    dest_filename = "simple_2p2pledges_example.xlsx"
    belief_csvs = create_simple_1m2p2pledges_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_simple_1m2p5pledges_belief_file(dest_dir: str):
    dest_filename = "simple_2p5pledges_example.xlsx"
    belief_csvs = create_simple_1m2p5pledges_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_simple_2m2p5pledges_belief_file(dest_dir: str):
    dest_filename = "simple_2m2p5pledges_example.xlsx"
    belief_csvs = create_simple_2m2p5pledges_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_emmanuel_lovemaking_belief_file(dest_dir: str):
    dest_filename = "emmanuel_lovemaking_example.xlsx"
    belief_csvs = create_emmanuel_lovemaking_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_five_time_config_file(dest_dir: str):
    dest_filename = "five_belief.xlsx"
    belief_csvs = create_five_time_config_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_elpaso_time_config_file(dest_dir: str):
    dest_filename = "elpaso_belief.xlsx"
    belief_csvs = create_elpaso_time_config_belief_csvs()
    save_and_prettify_excel_file(belief_csvs, dest_dir, dest_filename)


def create_emmanuel_belief_file(file_path: str):
    # TODO dict[str, str]s and save to file
    # prnt("create_emmanuel_belief_file...")
    pass


def create_example_moment_ledger_file(file_path: str):
    # TODO dict[str, str]s and save to file
    # prnt("create_example_moment_ledger_file...")
    pass


def create_example_moment_budget_file(file_path: str):
    # TODO dict[str, str]s and save to file
    # prnt("create_example_moment_budget_file...")
    pass


def get_option_table_options() -> dict[str, Callable]:
    return {
        "2 persons, 2 tasks example": create_simple_1m2p2pledges_belief_file,
        "2 persons, 5 tasks example": create_simple_1m2p5pledges_belief_file,
        "2 moments, 2 persons, 5 tasks example": create_simple_2m2p5pledges_belief_file,
        "lovemaking example": create_emmanuel_lovemaking_belief_file,
        "Create TeamFive Moment with Five time": create_five_time_config_file,
        "Create El Paso Moment with standard time.": create_elpaso_time_config_file,
        "create_emmanuel_belief_file": create_emmanuel_belief_file,
        "create_example_moment_ledger_file": create_example_moment_ledger_file,
        "create_example_moment_budget_file": create_example_moment_budget_file,
    }


# def add_title1_label(title_frame):
#     ax = get_app_glb_attrs()
#     app1_str = "Keg Listening App#1"
#     tk.Label(
#         title_frame,
#         text=app1_str,
#         font=ax.platform_font,
#         bg=ax.bg,
#         fg=ax.accent,
#         anchor="w",
#     ).pack(side="left")
