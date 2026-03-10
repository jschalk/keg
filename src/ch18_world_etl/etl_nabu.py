from dataclasses import dataclass
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.db_toolbox import create_insert_query, get_row_count, get_table_columns
from src.ch00_py.dict_toolbox import get_empty_set_if_None
from src.ch05_reason.reason_main import caseunit_shop
from src.ch07_person_logic.person_tool import add_frame_to_caseunit
from src.ch14_moment.moment_config import get_moment_dimens
from src.ch15_nabu.nabu_config import get_nabu_dimens
from src.ch17_idea.idea_config import (
    get_default_sorted_list,
    get_idea_config_dict,
    get_idea_sqlite_types,
)
from src.ch18_world_etl._ref.ch18_semantic_types import (
    FaceName,
    FactNum,
    MomentRope,
    PersonName,
    ReasonNum,
    RopeTerm,
    SparkInt,
    TimeNum,
)
from src.ch18_world_etl.etl_config import (
    etl_idea_category_config_dict,
    get_dimen_abbv7,
    get_etl_category_stages_dict,
    get_prime_columns,
    remove_inx_columns,
    remove_otx_columns,
)
from src.ch18_world_etl.etl_main import etl_heard_raw_tables_to_heard_agg_tables
from src.ch18_world_etl.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)


# TODO create test for add_frame_to_db_personunit
def add_frame_to_db_personunit():
    pass


# TODO create test for add_frame_to_db_personunit
def add_frame_to_db_caseunit(
    cursor: sqlite3_Cursor,
    plan_close: float,
    plan_denom: float,
    plan_morph: float,
):
    update_sql = get_add_frame_to_db_caseunit_sqlstr()
    # UPDATE PRNCASE WHERE SPARK_NUM is equal to prncase_obj using rules from "add_frame_to_caseunit"
    cursor.execute(update_sql)


# TODO create test for add_frame_to_db_personunit
def add_frame_to_db_factunit():
    pass


# TODO create test for add_frame_to_db_personunit
def add_frame_to_db_reasonunit():
    pass


# TODO create test for add_frame_to_db_personunit
def add_epoch_frame_to_db_personunit():
    pass
