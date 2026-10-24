from ch00_py.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from ch00_py.file_toolbox import create_path, delete_dir
from ch05_rope.rope import create_rope, default_knot_if_None
from ch08_person_logic.person_main import personunit_shop
from ch14_time.epoch_config import get_creg_config, get_five_config
from ch14_time.epoch_main import epochunit_shop
from ch15_moment.moment_main import momentunit_shop
from ch20_brick.brick_db_tool import (
    csv_dict_to_excel,
    prettify_excel_file,
    remove_empty_sheets,
)
from ch23_idea_src.idea_csv import (
    add_momentunits_to_idea_csv_strs,
    add_personunit_to_idea_csv_strs,
    create_init_idea_csv_strs,
)
from ch32_world.world import worlddir_shop
from ch90_puncher_app._ref.ch90_semantic_types import PersonName
from dataclasses import dataclass
from io import StringIO
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    read_csv as pandas_read_csv,
    read_excel as pandas_read_excel,
)
from pathlib import Path
from platform import system as platform_system
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
    return "hope1"


def get_app_default_dir(is_windows: bool | None = None) -> Path:
    if is_windows is None:
        is_windows = platform_system().lower().startswith("win")
    return Path("C:/keg/worlds") if is_windows else Path.home() / "keg" / "worlds"


def get_app_default_dirs(default_root: Path) -> dict[str, Path]:
    x_world_name = get_app_default_world_name()
    x_worlddir = worlddir_shop(world_name=x_world_name, worlds_dir=default_root)
    return {
        "world_name": x_world_name,
        "worlds": x_worlddir.worlds_dir,
        "ideas_src": x_worlddir.ideas_src_dir,
        "bricks_src": x_worlddir.bricks_src_dir,
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


def create_simple_1m2p2pledges_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    mmt01_rope = create_rope("mmt01")
    me_person = personunit_shop(me_name, mmt01_rope)
    you_person = personunit_shop(you_name, mmt01_rope)
    me_person.add_contactunit(me_name)
    me_person.add_contactunit(you_name)
    you_person.add_contactunit(you_name)
    you_person.add_contactunit(me_name)
    music_rope = you_person.make_l1_rope("enjoy music")
    golf_rope = you_person.make_l1_rope("play disc golf")
    me_person.add_plan(music_rope, 1, True)
    you_person.add_plan(golf_rope, 1, True)
    idea_csv_strs = create_init_idea_csv_strs()
    me_person.thinkout()
    you_person.thinkout()
    add_personunit_to_idea_csv_strs(me_person, idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(you_person, idea_csv_strs, ",")
    return transform_ii00129_into_ii00002_in_csvs(idea_csv_strs, mmt01_rope)


def create_simple_1m2p5pledges_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    mmt01_rope = create_rope("mmt01")
    me_person = personunit_shop(me_name, mmt01_rope)
    you_person = personunit_shop(you_name, mmt01_rope)
    me_person.add_contactunit(me_name)
    me_person.add_contactunit(you_name)
    you_person.add_contactunit(you_name)
    you_person.add_contactunit(me_name)
    casa_rope = you_person.make_l1_rope("clean casa")
    dishes_rope = you_person.make_rope(casa_rope, "clean dishes with baking soda")
    clothes_rope = you_person.make_rope(casa_rope, "clean clothes with baking soda")
    counters_str = "clean kitchen counters with baking soda"
    counters_rope = you_person.make_rope(casa_rope, counters_str)
    handout_str = "give neighbor any baking soda they want"
    handout_rope = you_person.make_rope(casa_rope, handout_str)
    ask_rope = you_person.make_rope(casa_rope, "ask neighbor to use baking soda")
    music_rope = you_person.make_l1_rope("enjoy music")
    me_person.add_plan(music_rope, 1, True)
    me_person.add_plan(dishes_rope, 10, True)
    me_person.add_plan(clothes_rope, 12, True)
    me_person.add_plan(counters_rope, 5, True)
    me_person.add_plan(handout_rope, 20, True)
    me_person.add_plan(ask_rope, 3, True)
    you_person.add_plan(music_rope, 10, True)
    idea_csv_strs = create_init_idea_csv_strs()
    me_person.thinkout()
    you_person.thinkout()
    add_personunit_to_idea_csv_strs(me_person, idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(you_person, idea_csv_strs, ",")
    return transform_ii00129_into_ii00002_in_csvs(idea_csv_strs, mmt01_rope)


def create_simple_2m2p5pledges_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    # sourcery skip: extract-duplicate-method
    mmt01_rope = create_rope("mmt01")
    m1_me_person = personunit_shop(me_name, mmt01_rope)
    m1_you_person = personunit_shop(you_name, mmt01_rope)
    m1_me_person.add_contactunit(me_name)
    m1_me_person.add_contactunit(you_name)
    m1_you_person.add_contactunit(you_name)
    m1_you_person.add_contactunit(me_name)
    casa_rope = m1_you_person.make_l1_rope("clean casa")
    dishes_rope = m1_you_person.make_rope(casa_rope, "clean dishes with baking soda")
    clothes_rope = m1_you_person.make_rope(casa_rope, "clean clothes with baking soda")
    counters_str = "clean kitchen counters with baking soda"
    counters_rope = m1_you_person.make_rope(casa_rope, counters_str)
    handout_str = "give neighbor any baking soda they want"
    handout_rope = m1_you_person.make_rope(casa_rope, handout_str)
    ask_rope = m1_you_person.make_rope(casa_rope, "ask neighbor to use baking soda")
    music_rope = m1_you_person.make_l1_rope("enjoy music")
    m1_me_person.add_plan(music_rope, 1, True)
    m1_me_person.add_plan(dishes_rope, 10, True)
    m1_me_person.add_plan(clothes_rope, 12, True)
    m1_me_person.add_plan(counters_rope, 5, True)
    m1_me_person.add_plan(handout_rope, 20, True)
    m1_me_person.add_plan(ask_rope, 3, True)
    m1_you_person.add_plan(music_rope, 10, True)
    idea_csv_strs = create_init_idea_csv_strs()
    m1_me_person.thinkout()
    m1_you_person.thinkout()
    add_personunit_to_idea_csv_strs(m1_me_person, idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(m1_you_person, idea_csv_strs, ",")

    # add sport moment
    sport01_rope = create_rope("sport01")
    h1_me_person = personunit_shop(me_name, sport01_rope)
    h1_you_person = personunit_shop(you_name, sport01_rope)
    h1_me_person.add_contactunit(me_name)
    h1_me_person.add_contactunit(you_name)
    h1_you_person.add_contactunit(you_name)
    h1_you_person.add_contactunit(me_name)
    dance_rope = h1_you_person.make_l1_rope("dance")
    disco_rope = h1_you_person.make_rope(dance_rope, "disco")
    bebop_rope = h1_you_person.make_rope(dance_rope, "bebop")
    tango_rope = h1_you_person.make_rope(dance_rope, "tango")
    h1_you_person.add_plan(disco_rope, 1, True)
    h1_me_person.add_plan(bebop_rope, 10, True)
    h1_me_person.add_plan(tango_rope, 3, True)
    h1_me_person.thinkout()
    h1_you_person.thinkout()
    add_personunit_to_idea_csv_strs(h1_me_person, idea_csv_strs, ",")
    add_personunit_to_idea_csv_strs(h1_you_person, idea_csv_strs, ",")
    return transform_ii00129_into_ii00002_in_csvs(idea_csv_strs, sport01_rope)


def create_emmanuel_lovemaking_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    mlove01_rope = create_rope("loving moment")
    mlove_name = "MyLove"
    you_person = personunit_shop(you_name, mlove01_rope)
    mlove_person = personunit_shop(mlove_name, mlove01_rope)
    you_person.add_contactunit(you_name)
    you_person.add_contactunit(mlove_name)
    mlove_person.add_contactunit(mlove_name)
    mlove_person.add_contactunit(you_name)
    mlove_rope = you_person.make_l1_rope("make love")
    you_person.add_plan(mlove_rope, 1, True)
    idea_csv_strs = create_init_idea_csv_strs()
    you_person.thinkout()
    add_personunit_to_idea_csv_strs(you_person, idea_csv_strs, ",")
    return transform_ii00129_into_ii00002_in_csvs(idea_csv_strs, mlove01_rope)


def transform_ii00129_into_ii00002_in_csvs(idea_csv_strs, moment_rope) -> dict:
    ii00002_csv = ""
    for sheetname_key, csv_str in idea_csv_strs.items():
        if sheetname_key == "ii00128":
            ii00002_csv = transform_ii00129_into_ii00002_csv(csv_str, moment_rope)
    idea_csv_strs["ii00002"] = ii00002_csv
    return {
        sheetname_key: csv_str
        for sheetname_key, csv_str in idea_csv_strs.items()
        if sheetname_key not in {"ii00120", "ii00129", "ii00128"}
    }


def transform_ii00129_into_ii00002_csv(csv_str: str, moment_rope: str):
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


def create_five_time_config_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    team_five_rope = create_rope("teamfive")
    five_epochunit = epochunit_shop(get_five_config())
    five_moment = momentunit_shop(team_five_rope, None, five_epochunit)
    moments = {five_moment.moment_rope: five_moment}
    idea_csv_strs = create_init_idea_csv_strs()
    add_momentunits_to_idea_csv_strs(moments, idea_csv_strs, ",")

    with_spark_face_csvs = {}
    for csv_key, csv_str in idea_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "spark_face", "ESchalk")
        csv_str = delete_column_from_csv_string(csv_str, "spark_num")
        with_spark_face_csvs[csv_key] = csv_str
    return with_spark_face_csvs


# Consider creating check this still works in gui
def create_elpaso_time_config_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    elpaso_rope = create_rope("ElPaso")
    creg_epochunit = epochunit_shop(get_creg_config())
    elpaso_moment = momentunit_shop(elpaso_rope, None, creg_epochunit)
    moments = {elpaso_moment.moment_rope: elpaso_moment}
    idea_csv_strs = create_init_idea_csv_strs()
    add_momentunits_to_idea_csv_strs(moments, idea_csv_strs, ",")

    with_spark_face_csvs = {}
    for csv_key, csv_str in idea_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "spark_face", "ESchalk")
        csv_str = delete_column_from_csv_string(csv_str, "spark_num")
        with_spark_face_csvs[csv_key] = csv_str
    return with_spark_face_csvs


def create_emmanuel_idea_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    # Consider creating dict[str, str]s and save to file
    # prnt("create_emmanuel_idea_file...")
    pass


def create_example_moment_ledger_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    # Consider creating dict[str, str]s and save to file
    # prnt("create_example_moment_ledger_file...")
    pass


def create_example_moment_budget_idea_csvs(
    me_name: PersonName, you_name: PersonName
) -> dict[str, str]:
    # Consider creating dict[str, str]s and save to file
    # prnt("create_example_moment_budget_file...")
    pass


def save_and_prettify_excel_file(
    idea_csvs: dict[str, str], dest_dir, dest_filename: str
):
    dest_dir = str(dest_dir)
    dest_file_path = create_path(dest_dir, dest_filename)
    delete_dir(dest_file_path)
    csv_dict_to_excel(idea_csvs, dest_dir, dest_filename)
    remove_empty_sheets(dest_file_path)
    prettify_excel_file(dest_file_path)


def create_simple_1m2p2pledges_idea_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "simple_2p2pledges_example.xlsx"
    idea_csvs = create_simple_1m2p2pledges_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_simple_1m2p5pledges_idea_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "simple_2p5pledges_example.xlsx"
    idea_csvs = create_simple_1m2p5pledges_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_simple_2m2p5pledges_idea_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "simple_2m2p5pledges_example.xlsx"
    idea_csvs = create_simple_2m2p5pledges_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_emmanuel_lovemaking_idea_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "emmanuel_lovemaking_example.xlsx"
    idea_csvs = create_emmanuel_lovemaking_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_five_time_config_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "five_idea.xlsx"
    idea_csvs = create_five_time_config_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_elpaso_time_config_file(
    dest_dir: str, me_name: PersonName, you_name: PersonName
):
    dest_filename = "elpaso_idea.xlsx"
    idea_csvs = create_elpaso_time_config_idea_csvs(me_name, you_name)
    save_and_prettify_excel_file(idea_csvs, dest_dir, dest_filename)


def create_emmanuel_idea_file(
    file_path: str, me_name: PersonName, you_name: PersonName
):
    # Consider creating dict[str, str]s and save to file
    # prnt("create_emmanuel_idea_file...")
    pass


def create_example_moment_ledger_file(
    file_path: str, me_name: PersonName, you_name: PersonName
):
    # Consider creating dict[str, str]s and save to file
    # prnt("create_example_moment_ledger_file...")
    pass


def create_example_moment_budget_file(
    file_path: str, me_name: PersonName, you_name: PersonName
):
    # Consider creating dict[str, str]s and save to file
    # prnt("create_example_moment_budget_file...")
    pass


def create_monopoly_idea_file(
    file_path: str, me_name: PersonName, you_name: PersonName
):
    # Consider creating dict[str, str]s and save to file
    # prnt("create_example_moment_budget_file...")
    pass


def get_option_table_options() -> dict[str, Callable]:
    return {
        "2 persons, 2 tasks example": create_simple_1m2p2pledges_idea_file,
        "2 persons, 5 tasks example": create_simple_1m2p5pledges_idea_file,
        "2 moments, 2 persons, 5 tasks example": create_simple_2m2p5pledges_idea_file,
        "lovemaking example": create_emmanuel_lovemaking_idea_file,
        "Create TeamFive Moment with Five time": create_five_time_config_file,
        "Create El Paso Moment with standard time.": create_elpaso_time_config_file,
        "create_emmanuel_idea_file": create_emmanuel_idea_file,
        "create_example_moment_ledger_file": create_example_moment_ledger_file,
        "create_example_moment_budget_file": create_example_moment_budget_file,
        "Monopoly Example": create_monopoly_idea_file,
    }
