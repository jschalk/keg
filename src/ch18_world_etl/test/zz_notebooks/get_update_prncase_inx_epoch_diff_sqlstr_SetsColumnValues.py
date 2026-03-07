import marimo

__generated_with = "0.20.2"
app = marimo.App()

with app.setup(hide_code=True):
    # source file: src\ch18_world_etl\test\z_heard\test_heard_agg_update_reasonnum_columns.py
    # source test name: test_get_update_prncase_inx_epoch_diff_sqlstr_SetsColumnValues
    from sqlite3 import Cursor, connect as sqlite3_connect
    from src.ch06_plan.test._util.ch06_examples import get_range_attrs
    from src.ch07_person_logic.person_tool import (
        PersonUnit,
        person_plan_factunit_exists,
        person_plan_factunit_get_obj,
        person_plan_reason_caseunit_exists,
        person_plan_reason_caseunit_get_obj,
        person_plan_reasonunit_get_obj,
        person_planunit_get_obj,
    )
    from src.ch13_time.epoch_main import (
        DEFAULT_EPOCH_LENGTH,
        add_epoch_planunit,
        get_c400_constants,
    )
    from src.ch13_time.epoch_reason import set_epoch_cases_by_args_dict
    from src.ch13_time.test._util.ch13_examples import (
        Ch13ExampleStrs as wx,
        get_bob_five_person,
        get_lizzy9_config,
    )
    from src.ch15_nabu.nabu_config import get_nabu_config_dict
    from src.ch17_idea.idea_config import get_dimens_with_idea_element
    from src.ch18_world_etl.etl_nabu import (
        add_epoch_frame_to_db_personunit,
        add_frame_to_db_caseunit,
        add_frame_to_db_factunit,
        add_frame_to_db_personunit,
        add_frame_to_db_reasonunit,
    )
    from src.ch18_world_etl.etl_sqlstr import (
        create_prime_tablename as prime_tbl,
        create_sound_and_heard_tables,
        get_update_heard_agg_timenum_sqlstr,
        get_update_heard_agg_timenum_sqlstrs,
        get_update_prncase_inx_epoch_diff_sqlstr,
        update_heard_agg_timenum_columns,
    )
    from src.ch18_world_etl.obj2db_person import insert_h_agg_obj
    from src.ch18_world_etl.test._util.ch18_env import cursor0
    from src.ch18_world_etl.test._util.ch18_examples import (
        get_bob_five_with_mop_dayly,
        insert_mmtoffi_special_offi_time_otx as insert_offi_time_otx,
        insert_mmtunit_special_c400_number as insert_c400_number,
        insert_nabtime_h_agg_otx_inx_time as insert_otx_inx_time,
        insert_prncase_special_h_agg as insert_prncase,
        select_mmtoffi_special_offi_time_inx as select_offi_time_inx,
        select_prncase_special_h_agg as select_prncase,
    )
    from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx

    conn = sqlite3_connect(":memory:")
    cursor0 = conn.cursor()
    print("cursor0 created for SQLite db in memory.")


@app.cell
def _():
    # ESTABLISH
    spark7 = 7
    bob_person = get_bob_five_with_mop_dayly()
    create_sound_and_heard_tables(cursor0)
    otx_time = 199
    inx_time = 13
    m_label = bob_person.planroot.get_plan_rope()
    insert_otx_inx_time(cursor0, spark7, exx.yao, m_label, otx_time, inx_time)
    insert_h_agg_obj(cursor0, bob_person, spark7, exx.yao)
    prncase_old_objs = select_prncase(
        cursor0, spark7, exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
    )
    prncase_old_obj0 = prncase_old_objs[0]
    assert prncase_old_obj0.inx_epoch_diff is None
    return inx_time, otx_time, spark7


@app.cell
def _():
    # WHEN
    update_sql = get_update_prncase_inx_epoch_diff_sqlstr()
    cursor0.execute(update_sql)
    return


@app.cell
def _(inx_time, otx_time, spark7):
    # THEN
    prncase_new_objs = select_prncase(
        cursor0, spark7, exx.bob, wx.mop_rope, wx.day_rope, wx.day_rope
    )
    prncase_new_obj0 = prncase_new_objs[0]
    assert prncase_new_obj0.inx_epoch_diff == otx_time - inx_time
    assert prncase_new_obj0.inx_epoch_diff == 186
    return


@app.cell
def _(FROM, SELECT):
    SELECT * FROM 
    return


if __name__ == "__main__":
    app.run()
