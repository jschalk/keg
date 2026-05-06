from ch00_py.db_toolbox import (
    delete_all_duplicate_rows,
    get_row_count,
    get_table_columns,
)
from ch00_py.dict_toolbox import set_in_nested_dict
from ch00_py.file_toolbox import get_level1_dirs, save_file, save_json
from ch04_rope.rope import create_rope
from ch09_person_lesson._ref.ch09_path import (
    create_moment_json_path,
    create_moments_dir_path,
)
from ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from ch11_bud.bud_main import MomentRope
from ch16_translate.translate_config import (
    get_translate_args_obj_types,
    translateable_obj_types,
)
from ch18_etl_config._ref.ch18_path import create_moment_ote1_csv_path
from ch18_etl_config.etl_csv import save_to_split_csvs
from ch18_etl_config.etl_sqlstr import (
    CREATE_MOMENT_OTE1_AGG_SQLSTR,
    INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR,
    create_update_heard_raw_empty_inx_col_sqlstr,
    create_update_heard_raw_existing_inx_col_sqlstr,
    get_insert_heard_agg_sqlstrs,
    get_insert_heard_vld_sqlstrs,
    get_insert_into_heard_raw_sqlstrs,
    get_moment_heard_select1_sqlstrs,
    get_person_heard_vld_tablenames,
    update_heard_agg_timenum_columns,
)
from copy import copy as copy_copy
from sqlite3 import Connection as sqlite3_Connection, Cursor as sqlite3_Cursor


def set_all_heard_raw_inx_columns(cursor: sqlite3_Cursor):
    translate_args = get_translate_args_obj_types()
    for heard_raw_tablename, otx_columnname in get_all_heard_raw_otx_columns(cursor):
        columnname_without_otx = otx_columnname[:-4]
        x_arg = copy_copy(columnname_without_otx)
        if x_arg[-5:] == "ERASE":
            x_arg = x_arg[:-6]
        arg_obj_type = translate_args.get(x_arg)
        set_heard_raw_inx_column(
            cursor, heard_raw_tablename, columnname_without_otx, arg_obj_type
        )


def get_all_heard_raw_otx_columns(cursor: sqlite3_Cursor) -> set[tuple[str, str]]:
    """Returns tuple of all columns ending in 'otx'. Tuple: (TableName, ColumnName)"""

    otx_tble_columns = set()
    for heard_raw_tablename in get_insert_into_heard_raw_sqlstrs().keys():
        for columnname in get_table_columns(cursor, heard_raw_tablename):
            if columnname[-3:] in {"otx"}:
                otx_tble_columns.add((heard_raw_tablename, columnname))
    return otx_tble_columns


def set_heard_raw_inx_column(
    cursor: sqlite3_Cursor,
    heard_raw_tablename: str,
    column_without_otx: str,
    arg_obj_type: str,
):
    if arg_obj_type in translateable_obj_types():
        translate_type_abbv = None
        if arg_obj_type == "NameTerm":
            translate_type_abbv = "name"
        elif arg_obj_type == "TitleTerm":
            translate_type_abbv = "title"
        elif arg_obj_type == "LabelTerm":
            translate_type_abbv = "label"
        elif arg_obj_type == "RopeTerm":
            translate_type_abbv = "rope"
        update_calc_inx_sqlstr = create_update_heard_raw_existing_inx_col_sqlstr(
            translate_type_abbv, heard_raw_tablename, column_without_otx
        )
        cursor.execute(update_calc_inx_sqlstr)
    update_empty_inx_sqlstr = create_update_heard_raw_empty_inx_col_sqlstr(
        heard_raw_tablename, column_without_otx
    )
    cursor.execute(update_empty_inx_sqlstr)


def etl_heard_raw_tables_to_heard_agg_tables(cursor: sqlite3_Cursor):
    set_all_heard_raw_inx_columns(cursor)
    for h_agg_tablename, insert_h_agg_sqlstr in get_insert_heard_agg_sqlstrs().items():
        cursor.execute(insert_h_agg_sqlstr)
        delete_all_duplicate_rows(cursor, h_agg_tablename, exclude_postfix="_inx")
    update_heard_agg_timenum_columns(cursor)


def etl_heard_agg_tables_to_heard_vld_tables(cursor: sqlite3_Cursor):
    for h_vld_tablename, insert_h_vld_sqlstr in get_insert_heard_vld_sqlstrs().items():
        cursor.execute(insert_h_vld_sqlstr)
        delete_all_duplicate_rows(cursor, h_vld_tablename)


def get_moment_dict_from_sqlstrs(
    cursor: sqlite3_Cursor, fu1_sqlstrs: dict[str, str], moment_rope: MomentRope
) -> dict:
    cursor.execute(fu1_sqlstrs.get("momentunit"))
    momentunit_row = cursor.fetchone()
    if not momentunit_row:
        return None  # momentunit not found

    epoch_label = momentunit_row[1]
    c400_number = momentunit_row[2]
    yr1_jan1_offset = momentunit_row[3]
    monthday_index = momentunit_row[4]

    moment_dict: dict[str, any] = {"moment_rope": momentunit_row[0], "epoch": {}}
    if (
        epoch_label is not None
        and c400_number is not None
        and yr1_jan1_offset is not None
        and monthday_index is not None
    ):
        if epoch_label:
            moment_dict["epoch"]["epoch_label"] = epoch_label
        if c400_number:
            moment_dict["epoch"]["c400_number"] = c400_number
        if yr1_jan1_offset:
            moment_dict["epoch"]["yr1_jan1_offset"] = yr1_jan1_offset
        if monthday_index:
            moment_dict["epoch"]["monthday_index"] = monthday_index

    if fund_grain := momentunit_row[5]:
        moment_dict["fund_grain"] = fund_grain
    if mana_grain := momentunit_row[6]:
        moment_dict["mana_grain"] = mana_grain
    if respect_grain := momentunit_row[7]:
        moment_dict["respect_grain"] = respect_grain
    if knot := momentunit_row[8]:
        moment_dict["knot"] = knot

    cursor.execute(fu1_sqlstrs.get("moment_paybook"))
    _set_moment_dict_mmtpayy(cursor, moment_dict, moment_rope)

    cursor.execute(fu1_sqlstrs.get("moment_budunit"))
    _set_moment_dict_momentbud(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_hour"))
    _set_moment_dict_mmthour(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_month"))
    _set_moment_dict_mmtmont(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_epoch_weekday"))
    _set_moment_dict_mmtweek(cursor, moment_dict)

    cursor.execute(fu1_sqlstrs.get("moment_timeoffi"))
    _set_moment_dict_timeoffi(cursor, moment_dict)
    return moment_dict


def _set_moment_dict_mmtpayy(
    cursor: sqlite3_Cursor, moment_dict: dict, x_moment_rope: str
):
    tranunits_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_person_name = mmtpayy_row[1]
        row_contact_name = mmtpayy_row[2]
        row_tran_time = mmtpayy_row[3]
        row_amount = mmtpayy_row[4]
        keylist = [row_person_name, row_contact_name, row_tran_time]
        set_in_nested_dict(tranunits_dict, keylist, row_amount)
    paybook_dict = {"moment_rope": x_moment_rope, "tranunits": tranunits_dict}
    moment_dict["paybook"] = paybook_dict


def _set_moment_dict_momentbud(cursor: sqlite3_Cursor, moment_dict: dict):
    personbudhistorys_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_person_name = mmtpayy_row[1]
        row_bud_time = mmtpayy_row[2]
        row_knot = mmtpayy_row[3]
        row_quota = mmtpayy_row[4]
        row_celldepth = mmtpayy_row[5]
        person_keylist = [row_person_name, "person_name"]
        set_in_nested_dict(personbudhistorys_dict, person_keylist, row_person_name)
        keylist = [row_person_name, "buds", row_bud_time]
        bud_timenum_dict = {
            "bud_time": row_bud_time,
            "quota": row_quota,
            "celldepth": row_celldepth,
        }
        set_in_nested_dict(personbudhistorys_dict, keylist, bud_timenum_dict)
    moment_dict["personbudhistorys"] = personbudhistorys_dict


def _set_moment_dict_mmthour(cursor: sqlite3_Cursor, moment_dict: dict):
    hours_config_list = []
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_cumulative_minute = mmtpayy_row[1]
        row_hour_label = mmtpayy_row[2]
        hours_config_list.append([row_hour_label, row_cumulative_minute])
    if hours_config_list:
        moment_dict["epoch"]["hours_config"] = hours_config_list


def _set_moment_dict_mmtmont(cursor: sqlite3_Cursor, moment_dict: dict):
    months_config_list = []
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_cumulative_day = mmtpayy_row[1]
        row_month_label = mmtpayy_row[2]
        months_config_list.append([row_month_label, row_cumulative_day])
    if months_config_list:
        moment_dict["epoch"]["months_config"] = months_config_list


def _set_moment_dict_mmtweek(cursor: sqlite3_Cursor, moment_dict: dict):
    weekday_dict = {}
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_weekday_order = mmtpayy_row[1]
        row_weekday_label = mmtpayy_row[2]
        weekday_dict[row_weekday_order] = row_weekday_label
    weekday_config_list = [weekday_dict[key] for key in sorted(weekday_dict.keys())]
    if weekday_dict:
        moment_dict["epoch"]["weekdays_config"] = weekday_config_list


def _set_moment_dict_timeoffi(cursor: sqlite3_Cursor, moment_dict: dict):
    offi_times_set = set()
    for mmtpayy_row in cursor.fetchall():
        row_moment_rope = mmtpayy_row[0]
        row_offi_time = mmtpayy_row[1]
        offi_times_set.add(row_offi_time)
    moment_dict["offi_times"] = list(offi_times_set)


def get_moment_dict_from_heard_tables(
    cursor: sqlite3_Cursor, moment_rope: MomentRope
) -> dict:
    fu1_sqlstrs = get_moment_heard_select1_sqlstrs(moment_rope)
    return get_moment_dict_from_sqlstrs(cursor, fu1_sqlstrs, moment_rope)


def etl_heard_vld_tables_to_mind_moment_jsons(
    cursor: sqlite3_Cursor, moment_mstr_dir: str
):
    """One reason file architecture is used instead of database is because it scales well and
    demonstrates how and where domains of data exist. However because of the difficulties in
    using moment_rope to create file paths Database may be the way to go. Maybe hashing moment_ropes
    to uids that can be used as folders. Then store in the hash folder a file like moment_data.json
    that contains the moment_rope. Then a mapping of moment_ropes to hashs can be created by walking
    through folders and reading moment_data.json"""
    select_moment_rope_sqlstr = """SELECT moment_rope FROM momentunit_h_vld;"""
    cursor.execute(select_moment_rope_sqlstr)
    for moment_label_set in cursor.fetchall():
        moment_label = moment_label_set[0]
        moment_dict = get_moment_dict_from_heard_tables(cursor, moment_label)
        moment_lasso = lassounit_shop(create_rope(moment_label))
        moment_json_path = create_moment_json_path(moment_mstr_dir, moment_lasso)
        save_json(moment_json_path, None, moment_dict)


def etl_heard_raw_tables_to_lego_moment_ote1_agg(conn_or_cursor: sqlite3_Connection):
    """Create Database Table that holds all spark_num to bud_time pairs. Include moment_rope and person_name"""
    conn_or_cursor.execute(CREATE_MOMENT_OTE1_AGG_SQLSTR)
    conn_or_cursor.execute(INSERT_MOMENT_OTE1_AGG_FROM_HEARD_SQLSTR)
    delete_all_duplicate_rows(conn_or_cursor, "moment_ote1_agg")


def etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    """One reason file architecture is used instead of database is because it scales well and
    demonstrates how and where domains of data exist. However because of the difficulties in
    using moment_rope to create file paths Database may be the way to go. Maybe hashing moment_ropes
    to uids that can be used as folders. Then store in the hash folder a file like moment_data.json
    that contains the moment_rope. Then a mapping of moment_ropes to hashs can be created by walking
    through folders and reading moment_data.json"""
    empty_ote1_csv_str = """moment_rope,person_name,spark_num,bud_time,error_message
"""
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for moment_label in get_level1_dirs(moments_dir):
        moment_lasso = lassounit_shop(create_rope(moment_label))
        ote1_csv_path = create_moment_ote1_csv_path(moment_mstr_dir, moment_lasso)
        save_file(ote1_csv_path, None, empty_ote1_csv_str)

    save_to_split_csvs(conn_or_cursor, "moment_ote1_agg", ["moment_rope"], moments_dir)


def etl_heard_vld_to_lego_spark_person_csvs(
    conn_or_cursor: sqlite3_Connection, moment_mstr_dir: str
):
    """consider getting rid of this step and having downstream lego_spark_person_csvs users go to database
    would fix save to split csv issue that's annoying
    One reason file architecture is used instead of database is because it scales well and
    demonstrates how and where domains of data exist. However because of the difficulties in
    using moment_rope to create file paths Database may be the way to go. Maybe hashing moment_ropes
    to uids that can be used as folders. Then store in the hash folder a file like moment_data.json
    that contains the moment_rope. Then a mapping of moment_ropes to hashs can be created by walking
    through folders and reading moment_data.json"""
    moments_dir = create_moments_dir_path(moment_mstr_dir)
    for prnxxxx_table in get_person_heard_vld_tablenames():
        if get_row_count(conn_or_cursor, prnxxxx_table) > 0:
            table_columns = set(get_table_columns(conn_or_cursor, prnxxxx_table))
            key_columns = ["moment_rope", "person_name", "spark_num"]
            if "moment_rope" not in table_columns:
                key_columns = ["plan_rope", "person_name", "spark_num"]
            save_to_split_csvs(
                conn_or_cursor=conn_or_cursor,
                tablename=prnxxxx_table,
                key_columns=key_columns,
                dst_dir=moments_dir,
                col1_prefix="persons",
                col2_prefix="sparks",
            )
