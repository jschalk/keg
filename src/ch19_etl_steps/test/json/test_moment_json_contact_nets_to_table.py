from sqlite3 import Cursor
from src.ch00_py.db_toolbox import db_table_exists, get_row_count
from src.ch00_py.file_toolbox import save_json
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud.bud_main import tranbook_shop
from src.ch14_moment.moment_main import momentunit_shop
from src.ch19_etl_steps.etl_main import (
    CREATE_MOMENT_CONTACT_NETS_SQLSTR,
    etl_moment_json_contact_nets_to_moment_contact_nets_table,
    insert_tranunit_contacts_net,
)
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_insert_tranunit_contacts_net_PopulatesDatabase(cursor0: Cursor):
    # ESTABLISH
    a23_tranbook = tranbook_shop(exx.a23)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_tranbook.add_tranunit(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    a23_tranbook.add_tranunit(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    a23_tranbook.add_tranunit(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    a23_tranbook.add_tranunit(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    moment_contact_nets_tablename = kw.moment_contact_nets
    cursor0.execute(CREATE_MOMENT_CONTACT_NETS_SQLSTR)
    assert get_row_count(cursor0, moment_contact_nets_tablename) == 0

    # WHEN
    insert_tranunit_contacts_net(cursor0, a23_tranbook)

    # THEN
    assert get_row_count(cursor0, moment_contact_nets_tablename) == 2
    select_sqlstr = f"SELECT moment_rope, person_name, {kw.person_net_amount} FROM {moment_contact_nets_tablename}"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    assert rows == [
        (exx.a23, exx.bob, t55_bob_amount),
        (exx.a23, exx.yao, t55_yao_amount + t66_yao_amount + t77_yao_amount),
    ]


def test_etl_moment_json_contact_nets_to_moment_contact_nets_table_PopulatesDatabase(
    temp3_fs, cursor0: Cursor
):
    # ESTABLISH
    mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, mstr_dir)
    t55_tran_time = 5505
    t55_yao_amount = -55
    t55_bob_amount = 600
    t66_tran_time = 6606
    t66_yao_amount = -66
    t77_tran_time = 7707
    t77_yao_amount = -77
    a23_moment.add_paypurchase(exx.sue, exx.yao, t55_tran_time, t55_yao_amount)
    a23_moment.add_paypurchase(exx.sue, exx.yao, t66_tran_time, t66_yao_amount)
    a23_moment.add_paypurchase(exx.sue, exx.bob, t55_tran_time, t55_bob_amount)
    a23_moment.add_paypurchase(exx.yao, exx.yao, t77_tran_time, t77_yao_amount)
    a23_lasso = lassounit_shop(exx.a23)
    a23_json_path = create_moment_json_path(mstr_dir, a23_lasso)
    save_json(a23_json_path, None, a23_moment.to_dict())

    moment_contact_nets_tablename = kw.moment_contact_nets
    assert not db_table_exists(cursor0, moment_contact_nets_tablename)

    # WHEN
    etl_moment_json_contact_nets_to_moment_contact_nets_table(cursor0, mstr_dir)

    # THEN
    assert get_row_count(cursor0, moment_contact_nets_tablename) == 2
    select_sqlstr = f"SELECT moment_rope, person_name, {kw.person_net_amount} FROM {moment_contact_nets_tablename}"
    cursor0.execute(select_sqlstr)
    rows = cursor0.fetchall()
    assert rows == [
        (exx.a23, exx.bob, t55_bob_amount),
        (exx.a23, exx.yao, t55_yao_amount + t66_yao_amount + t77_yao_amount),
    ]
