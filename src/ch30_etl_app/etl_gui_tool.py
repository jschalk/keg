from src.ch00_py.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.ch00_py.file_toolbox import create_path, delete_dir
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch13_time.epoch_config import get_creg_config, get_five_config
from src.ch13_time.epoch_main import epochunit_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch17_idea.idea_belief import (
    add_momentunits_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from src.ch17_idea.idea_db_tool import (
    csv_dict_to_excel,
    prettify_excel,
    remove_empty_sheets,
)

TEAMFIVE = "TeamFive"


def create_five_time_config_belief_csvs() -> dict[str, str]:
    team_five_rope = create_rope(TEAMFIVE)
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
    prettify_excel(dest_file_path)


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
