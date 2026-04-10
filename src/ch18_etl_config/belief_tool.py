from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.csv_toolbox import (
    delete_column_from_csv_string,
    replace_csv_column_from_string,
)
from src.ch00_py.file_toolbox import create_path, get_level1_dirs
from src.ch04_rope.rope import create_rope, default_knot_if_None
from src.ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud.bud_filehandler import open_person_file
from src.ch14_moment.moment_main import open_moment_file
from src.ch17_idea.brick_belief_csv import (
    add_momentunit_to_belief_csv_strs,
    add_personunit_to_belief_csv_strs,
    create_init_belief_idea_csv_strs,
)
from src.ch17_idea.idea_db_tool import csv_dict_to_excel, prettify_excel
from src.ch18_etl_config._ref.ch18_path import (
    create_belief0001_path,
    create_moment_mstr_path,
    create_world_db_path,
)
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)


def add_to_br00042_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    trltitl_s_vld_tablename = prime_tbl("TRLTITL", "s_vld")
    trlcore_s_vld_tablename = prime_tbl("TRLCORE", "s_vld")

    select_sqlstr = f"""
SELECT
  "" spark_num
, trltitl.spark_face
, trltitl.otx_title
, trltitl.inx_title
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
FROM {trltitl_s_vld_tablename} trltitl
JOIN {trlcore_s_vld_tablename} trlcore ON trlcore.spark_face = trltitl.spark_face
ORDER BY 
  spark_num
, trltitl.spark_face
, trltitl.otx_title
, trltitl.inx_title
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00043_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    trlname_s_vld_tablename = prime_tbl("TRLNAME", "s_vld")
    trlcore_s_vld_tablename = prime_tbl("TRLCORE", "s_vld")
    select_sqlstr = f"""
SELECT
  "" spark_num
, trlname.spark_face
, trlname.otx_name
, trlname.inx_name
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
FROM {trlname_s_vld_tablename} trlname
JOIN {trlcore_s_vld_tablename} trlcore ON trlcore.spark_face = trlname.spark_face
ORDER BY 
  trlname.spark_face
, trlname.otx_name
, trlname.inx_name
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00044_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    trllabe_s_vld_tablename = prime_tbl("TRLLABE", "s_vld")
    trlcore_s_vld_tablename = prime_tbl("TRLCORE", "s_vld")

    select_sqlstr = f"""
SELECT
  "" spark_num
, trllabe.spark_face
, trllabe.otx_label
, trllabe.inx_label
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
FROM {trllabe_s_vld_tablename} trllabe
JOIN {trlcore_s_vld_tablename} trlcore ON trlcore.spark_face = trllabe.spark_face
ORDER BY 
  trllabe.spark_face
, trllabe.otx_label
, trllabe.inx_label
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_to_br00045_csv(x_csv: str, cursor: sqlite3_Cursor, csv_delimiter: str) -> str:
    trlrope_s_vld_tablename = prime_tbl("TRLROPE", "s_vld")
    trlcore_s_vld_tablename = prime_tbl("TRLCORE", "s_vld")

    select_sqlstr = f"""
SELECT
  "" spark_num
, trlrope.spark_face
, trlrope.otx_rope
, trlrope.inx_rope
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
FROM {trlrope_s_vld_tablename} trlrope
JOIN {trlcore_s_vld_tablename} trlcore ON trlcore.spark_face = trlrope.spark_face
ORDER BY 
  trlrope.spark_face
, trlrope.otx_rope
, trlrope.inx_rope
, trlcore.otx_knot
, trlcore.inx_knot
, trlcore.unknown_str
;
"""
    cursor.execute(select_sqlstr)
    rows = cursor.fetchall()
    for row in rows:
        x_csv += f"{csv_delimiter.join(row)}\n"
    return x_csv


def add_translate_rows_to_belief_csv_strs(
    cursor: sqlite3_Cursor, moment_csv_strs: dict[str, str], csv_delimiter: str
):
    br00042_csv = moment_csv_strs.get("br00042")
    br00043_csv = moment_csv_strs.get("br00043")
    br00044_csv = moment_csv_strs.get("br00044")
    br00045_csv = moment_csv_strs.get("br00045")
    br00042_csv = add_to_br00042_csv(br00042_csv, cursor, csv_delimiter)
    br00043_csv = add_to_br00043_csv(br00043_csv, cursor, csv_delimiter)
    br00044_csv = add_to_br00044_csv(br00044_csv, cursor, csv_delimiter)
    br00045_csv = add_to_br00045_csv(br00045_csv, cursor, csv_delimiter)
    moment_csv_strs["br00042"] = br00042_csv
    moment_csv_strs["br00043"] = br00043_csv
    moment_csv_strs["br00044"] = br00044_csv
    moment_csv_strs["br00045"] = br00045_csv


def collect_belief_csv_strs(world_dir: str) -> dict[str, str]:
    moment_mstr_dir = create_moment_mstr_path(world_dir)
    x_csv_strs = create_init_belief_idea_csv_strs()
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        x_knot = default_knot_if_None()
        moment_rope = create_rope(moment_label, None, x_knot)
        moment_lasso = lassounit_shop(moment_rope, x_knot)
        x_momentunit = open_moment_file(moment_mstr_dir, moment_lasso)
        add_momentunit_to_belief_csv_strs(x_momentunit, x_csv_strs, ",")
        moment_dir = create_path(moments_dir, moment_lasso.make_path())
        persons_dir = create_path(moment_dir, "persons")
        for person_name in get_level1_dirs(persons_dir):
            person_dir = create_path(persons_dir, person_name)
            gut_dir = create_path(person_dir, "gut")
            gut_person_path = create_path(gut_dir, f"{person_name}.json")
            if os_path_exists(gut_person_path):
                gut_person = open_person_file(gut_person_path)
                add_personunit_to_belief_csv_strs(gut_person, x_csv_strs, ",")
    world_db_path = create_world_db_path(world_dir)
    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        add_translate_rows_to_belief_csv_strs(cursor, x_csv_strs, ",")
    db_conn.close()

    return x_csv_strs


def create_belief0001_file(
    world_dir: str,
    output_dir: str,
    world_name: str,
    prettify_excel_bool: bool = True,
):
    belief_csv_strs = collect_belief_csv_strs(world_dir)
    with_spark_face_csvs = {}
    for csv_key, csv_str in belief_csv_strs.items():
        csv_str = replace_csv_column_from_string(csv_str, "spark_face", world_name)
        csv_str = delete_column_from_csv_string(csv_str, "spark_num")
        with_spark_face_csvs[csv_key] = csv_str

    csv_dict_to_excel(with_spark_face_csvs, output_dir, "belief0001.xlsx")

    # Hard to test function to prettify the excel file
    if prettify_excel_bool:
        belief0001_path = create_belief0001_path(output_dir)
        prettify_excel(belief0001_path)
