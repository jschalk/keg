from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_row_count
from src.ch13_time.test._util.ch13_examples import Ch13ExampleStrs as wx
from src.ch18_world_etl.etl_config import create_prime_tablename
from src.ch18_world_etl.etl_sqlstr import (
    create_sound_and_heard_tables,
    get_update_prnfact_inx_epoch_diff_sqlstr,
)
from src.ch18_world_etl.obj2db_person import insert_h_agg_obj
from src.ch18_world_etl.test._util.ch18_env import cursor0
from src.ch18_world_etl.test._util.ch18_examples import (
    get_bob_five_with_mop_dayly,
    insert_nabtime_h_agg_otx_inx_time as insert_otx_inx_time,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_get_update_prnfact_inx_epoch_diff_sqlstr_Scenario0_Simple_SetColumnValues(
    cursor0: Cursor,
):
    # ESTABLISH
    spark7 = 7
    bob_person = get_bob_five_with_mop_dayly()
    bob_person.add_fact(wx.time_rope, wx.time_rope, 0, 100)
    create_sound_and_heard_tables(cursor0)
    h_agg_table = create_prime_tablename(kw.prnfact, "h", "agg", "put")
    otx_time = 199
    inx_time = 13
    moment_rope = bob_person.planroot.get_plan_rope()
    insert_otx_inx_time(cursor0, spark7, exx.yao, moment_rope, otx_time, inx_time)
    insert_h_agg_obj(cursor0, bob_person, spark7, exx.yao)
    # TODO create SQL query that selects only the fields of interest (ok that it cannot be reused in other tests)
    print(f"{h_agg_table=}")
    sel_prnfact_str = f"SELECT {kw.inx_epoch_diff} FROM {h_agg_table};"
    assert get_row_count(cursor0, h_agg_table) == 1
    assert cursor0.execute(sel_prnfact_str).fetchone()[0] is None

    # WHEN
    cursor0.execute(get_update_prnfact_inx_epoch_diff_sqlstr())

    # THEN
    assert get_row_count(cursor0, h_agg_table) == 1
    after_inx_epoch_diff = cursor0.execute(sel_prnfact_str).fetchone()[0]
    assert after_inx_epoch_diff
    assert after_inx_epoch_diff == otx_time - inx_time
    assert after_inx_epoch_diff == 186
