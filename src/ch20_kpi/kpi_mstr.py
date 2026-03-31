from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import get_db_tables
from src.ch00_py.file_toolbox import create_path, get_level1_dirs, save_file, set_dir
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch13_time.calendar_markdown import get_calendarmarkdown_str
from src.ch14_moment.moment_frame import get_moment_epochholder
from src.ch14_moment.moment_main import open_moment_file
from src.ch17_idea.idea_db_tool import save_table_to_csv
from src.ch20_kpi.kpi_sqlstr import get_create_kpi001_sqlstr, get_create_kpi002_sqlstr


def create_populate_kpi001_table(cursor: sqlite3_Cursor):
    cursor.execute("DROP TABLE IF EXISTS moment_kpi001_contact_nets")
    cursor.execute(get_create_kpi001_sqlstr())


def create_populate_kpi002_table(cursor: sqlite3_Cursor):
    cursor.execute("DROP TABLE IF EXISTS moment_kpi002_person_pledges")
    cursor.execute(get_create_kpi002_sqlstr())


def get_all_kpi_functions() -> dict[str, set[str]]:
    """
    Returns a dict of all KPI ids and their functions.
    """
    return {
        "moment_kpi001_contact_nets": create_populate_kpi001_table,
        "moment_kpi002_person_pledges": create_populate_kpi002_table,
    }


def get_bundles_config() -> dict[str]:
    """
    Returns a set of all KPI strings.
    """
    return {
        "default_kpi_bundle": {
            "moment_kpi001_contact_nets",
            "moment_kpi002_person_pledges",
        }
    }


def get_kpi_set_from_bundle(bundle_id: str = None) -> set[str]:
    """
    Returns a set of KPI strings from the specified bundle.
    """
    bundles_config = get_bundles_config()
    if bundle_id is None:
        bundle_id = "default_kpi_bundle"

    return bundles_config.get(bundle_id, set())


def populate_kpi_bundle(cursor: sqlite3_Cursor, bundle_id: str = None):
    """If bundle_id is None, create default kpis"""

    bundle_kpi_ids = get_kpi_set_from_bundle(bundle_id)
    for kpi_id in bundle_kpi_ids:
        if kpi_id == "moment_kpi001_contact_nets":
            create_populate_kpi001_table(cursor)
        if kpi_id == "moment_kpi002_person_pledges":
            create_populate_kpi002_table(cursor)


def create_kpi_csvs(db_path: str, dst_dir: str):
    with sqlite3_connect(db_path) as db_conn:
        cursor = db_conn.cursor()
        kpi_tables = get_db_tables(db_conn, "kpi")
        for kpi_table in kpi_tables:
            save_table_to_csv(cursor, dst_dir, kpi_table)
    db_conn.close()


def create_calendar_markdown_files(moment_mstr_dir: str, output_dir: str):
    set_dir(output_dir)
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_calendar_md_path = create_path(output_dir, f"{moment_label}_calendar.md")
        moment_lasso = lassounit_shop(create_rope(moment_label))
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        moment_epochholder = get_moment_epochholder(x_momentunit)
        moment_year_num = moment_epochholder._year_num
        moment_epoch_config = x_momentunit.epoch.to_dict()
        x_calendarmarkdown = get_calendarmarkdown_str(
            moment_epoch_config, moment_year_num
        )
        save_file(moment_calendar_md_path, None, x_calendarmarkdown)

    # a23_calendar_md_path = create_path(output_dir, f"{exx.a23}_calendar.md")
