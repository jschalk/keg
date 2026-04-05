from copy import copy as copy_copy
from os import getcwd as os_getcwd
from src.ch00_py.file_toolbox import create_path, save_json
from src.ch07_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_args_sqlite_datatype_dict,
)
from src.ch08_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_person_dimens,
)
from src.ch14_moment.moment_config import (
    get_moment_args_dimen_mapping,
    get_moment_config_dict,
    get_moment_dimens,
)
from src.ch15_nabu.nabu_config import (
    get_nabu_args,
    get_nabu_config_dict,
    get_nabu_dimens,
    get_nabuable_args,
)
from src.ch16_translate.translate_config import (
    get_translate_args_dimen_mapping,
    get_translate_config_dict,
    get_translate_dimens,
    get_translateable_args,
)
from src.ch17_idea.idea_config import (
    get_allowed_curds,
    get_default_sorted_list,
    get_dimens_with_idea_element,
    get_idea_config_dict,
    get_idea_dimen_ref,
    get_idea_elements_sort_order,
    get_idea_format_filename,
    get_idea_format_filenames,
    get_idea_numbers,
    get_idea_sqlite_types,
    get_idearef_from_file,
    get_quick_ideas_column_ref,
    idea_config_path,
    idea_format_00013_planunit_v0_0_0,
    idea_format_00020_person_contact_membership_v0_0_0,
    idea_format_00021_person_contactunit_v0_0_0,
)
from src.ref.keywords import Ch17Keywords as kw


def test_get_idea_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_idea_elements_sort_order()

    # THEN
    atom_args = set(get_atom_args_dimen_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))
    moment_args = set(get_moment_args_dimen_mapping().keys())
    # print(f"{moment_args=}")
    # print(f"{moment_args.difference(set(table_sorting_priority))=}")
    assert moment_args.issubset(set(table_sorting_priority))
    nabu_args = get_nabu_args()
    assert nabu_args.issubset(set(table_sorting_priority))
    translate_args = set(get_translate_args_dimen_mapping().keys())
    # print(f"{moment_args=}")
    # print(f"{translate_args.difference(set(table_sorting_priority))=}")
    assert translate_args.issubset(set(table_sorting_priority))
    all_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
    # print(f"missing {all_person_dimen_delete_keys.difference(table_sorting_priority)}")
    assert all_person_dimen_delete_keys.issubset(table_sorting_priority)
    person_calc_args = set(get_all_person_calc_args().keys())
    # for person_calc_arg in person_calc_args.difference(table_sorting_priority):
    #     print(f"{person_calc_arg=}")
    print(f"{person_calc_args.difference(table_sorting_priority)=}")
    assert person_calc_args.issubset(table_sorting_priority)
    translateable_otx_cols = {f"{trl_arg}_otx" for trl_arg in get_translateable_args()}
    translateable_inx_cols = {f"{trl_arg}_inx" for trl_arg in get_translateable_args()}
    # print(f"{translateable_otx_cols=}")
    # print(f"{translateable_inx_cols=}")
    assert translateable_otx_cols.issubset(table_sorting_priority)
    assert translateable_inx_cols.issubset(table_sorting_priority)
    x_delete_keys = all_person_dimen_delete_keys
    translateable_delete_otx_cols = {f"{trl_arg}_otx" for trl_arg in x_delete_keys}
    translateable_delete_inx_cols = {f"{trl_arg}_inx" for trl_arg in x_delete_keys}
    # print(f"{translateable_delete_otx_cols=}")
    # print(f"{translateable_delete_inx_cols=}")
    assert translateable_delete_otx_cols.issubset(table_sorting_priority)
    assert translateable_delete_inx_cols.issubset(table_sorting_priority)
    nabuable_otx_cols = {f"{nabu_arg}_otx" for nabu_arg in get_nabuable_args()}
    nabuable_inx_cols = {f"{nabu_arg}_inx" for nabu_arg in get_nabuable_args()}
    assert nabuable_otx_cols.issubset(table_sorting_priority)
    assert nabuable_inx_cols.issubset(table_sorting_priority)

    # all the suffix otx/inx columns are only used in one
    assert table_sorting_priority[0] == kw.world_name
    assert table_sorting_priority[1] == kw.idea_number
    assert table_sorting_priority[2] == kw.source_dimen
    assert table_sorting_priority[3] == kw.translate_spark_num
    assert table_sorting_priority[4] == kw.spark_num
    assert table_sorting_priority[5] == kw.spark_face
    assert table_sorting_priority[6] == f"{kw.spark_face}_otx"
    assert table_sorting_priority[7] == f"{kw.spark_face}_inx"
    assert table_sorting_priority[8] == kw.moment_rope
    assert table_sorting_priority[9] == f"{kw.moment_rope}_otx"
    assert table_sorting_priority[10] == f"{kw.moment_rope}_inx"
    assert table_sorting_priority[11] == kw.epoch_label
    assert table_sorting_priority[12] == f"{kw.epoch_label}_otx"
    assert table_sorting_priority[13] == f"{kw.epoch_label}_inx"
    assert table_sorting_priority[14] == kw.offi_time
    assert table_sorting_priority[15] == f"{kw.offi_time}_otx"
    assert table_sorting_priority[16] == f"{kw.offi_time}_inx"
    assert table_sorting_priority[17] == kw.c400_number
    assert table_sorting_priority[18] == kw.yr1_jan1_offset
    assert table_sorting_priority[19] == kw.monthday_index
    assert table_sorting_priority[20] == kw.cumulative_day
    assert table_sorting_priority[21] == kw.month_label
    assert table_sorting_priority[22] == f"{kw.month_label}_otx"
    assert table_sorting_priority[23] == f"{kw.month_label}_inx"
    assert table_sorting_priority[24] == kw.cumulative_minute
    assert table_sorting_priority[25] == f"{kw.hour_label}"
    assert table_sorting_priority[26] == f"{kw.hour_label}_otx"
    assert table_sorting_priority[27] == f"{kw.hour_label}_inx"
    assert table_sorting_priority[28] == kw.weekday_order
    assert table_sorting_priority[29] == kw.weekday_label
    assert table_sorting_priority[30] == f"{kw.weekday_label}_otx"
    assert table_sorting_priority[31] == f"{kw.weekday_label}_inx"
    assert table_sorting_priority[32] == kw.person_name
    assert table_sorting_priority[33] == f"{kw.person_name}_otx"
    assert table_sorting_priority[34] == f"{kw.person_name}_inx"
    assert table_sorting_priority[35] == f"{kw.person_name}_ERASE"
    assert table_sorting_priority[36] == f"{kw.person_name}_ERASE_otx"
    assert table_sorting_priority[37] == f"{kw.person_name}_ERASE_inx"
    assert table_sorting_priority[38] == kw.contact_name
    assert table_sorting_priority[39] == f"{kw.contact_name}_otx"
    assert table_sorting_priority[40] == f"{kw.contact_name}_inx"
    assert table_sorting_priority[41] == f"{kw.contact_name}_ERASE"
    assert table_sorting_priority[42] == f"{kw.contact_name}_ERASE_otx"
    assert table_sorting_priority[43] == f"{kw.contact_name}_ERASE_inx"
    assert table_sorting_priority[44] == kw.group_title
    assert table_sorting_priority[45] == f"{kw.group_title}_otx"
    assert table_sorting_priority[46] == f"{kw.group_title}_inx"
    assert table_sorting_priority[47] == f"{kw.group_title}_ERASE"
    assert table_sorting_priority[48] == f"{kw.group_title}_ERASE_otx"
    assert table_sorting_priority[49] == f"{kw.group_title}_ERASE_inx"
    assert table_sorting_priority[50] == kw.plan_rope
    assert table_sorting_priority[51] == f"{kw.plan_rope}_otx"
    assert table_sorting_priority[52] == f"{kw.plan_rope}_inx"
    assert table_sorting_priority[53] == f"{kw.plan_rope}_ERASE"
    assert table_sorting_priority[54] == f"{kw.plan_rope}_ERASE_otx"
    assert table_sorting_priority[55] == f"{kw.plan_rope}_ERASE_inx"
    assert table_sorting_priority[56] == kw.reason_context
    assert table_sorting_priority[57] == f"{kw.reason_context}_otx"
    assert table_sorting_priority[58] == f"{kw.reason_context}_inx"
    assert table_sorting_priority[59] == f"{kw.reason_context}_ERASE"
    assert table_sorting_priority[60] == f"{kw.reason_context}_ERASE_otx"
    assert table_sorting_priority[61] == f"{kw.reason_context}_ERASE_inx"
    assert table_sorting_priority[62] == kw.fact_context
    assert table_sorting_priority[63] == f"{kw.fact_context}_otx"
    assert table_sorting_priority[64] == f"{kw.fact_context}_inx"
    assert table_sorting_priority[65] == f"{kw.fact_context}_ERASE"
    assert table_sorting_priority[66] == f"{kw.fact_context}_ERASE_otx"
    assert table_sorting_priority[67] == f"{kw.fact_context}_ERASE_inx"
    assert table_sorting_priority[68] == kw.reason_state
    assert table_sorting_priority[69] == f"{kw.reason_state}_otx"
    assert table_sorting_priority[70] == f"{kw.reason_state}_inx"
    assert table_sorting_priority[71] == f"{kw.reason_state}_ERASE"
    assert table_sorting_priority[72] == f"{kw.reason_state}_ERASE_otx"
    assert table_sorting_priority[73] == f"{kw.reason_state}_ERASE_inx"
    assert table_sorting_priority[74] == kw.fact_state
    assert table_sorting_priority[75] == f"{kw.fact_state}_otx"
    assert table_sorting_priority[76] == f"{kw.fact_state}_inx"
    assert table_sorting_priority[77] == kw.labor_title
    assert table_sorting_priority[78] == f"{kw.labor_title}_otx"
    assert table_sorting_priority[79] == f"{kw.labor_title}_inx"
    assert table_sorting_priority[80] == f"{kw.labor_title}_ERASE"
    assert table_sorting_priority[81] == f"{kw.labor_title}_ERASE_otx"
    assert table_sorting_priority[82] == f"{kw.labor_title}_ERASE_inx"
    assert table_sorting_priority[83] == kw.solo
    assert table_sorting_priority[84] == kw.awardee_title
    assert table_sorting_priority[85] == f"{kw.awardee_title}_otx"
    assert table_sorting_priority[86] == f"{kw.awardee_title}_inx"
    assert table_sorting_priority[87] == f"{kw.awardee_title}_ERASE"
    assert table_sorting_priority[88] == f"{kw.awardee_title}_ERASE_otx"
    assert table_sorting_priority[89] == f"{kw.awardee_title}_ERASE_inx"
    assert table_sorting_priority[90] == kw.healer_name
    assert table_sorting_priority[91] == f"{kw.healer_name}_otx"
    assert table_sorting_priority[92] == f"{kw.healer_name}_inx"
    assert table_sorting_priority[93] == f"{kw.healer_name}_ERASE"
    assert table_sorting_priority[94] == f"{kw.healer_name}_ERASE_otx"
    assert table_sorting_priority[95] == f"{kw.healer_name}_ERASE_inx"
    assert table_sorting_priority[96] == kw.bud_time
    assert table_sorting_priority[97] == f"{kw.bud_time}_otx"
    assert table_sorting_priority[98] == f"{kw.bud_time}_inx"
    assert table_sorting_priority[99] == kw.tran_time
    assert table_sorting_priority[100] == f"{kw.tran_time}_otx"
    assert table_sorting_priority[101] == f"{kw.tran_time}_inx"
    assert table_sorting_priority[102] == kw.begin
    assert table_sorting_priority[103] == kw.close
    assert table_sorting_priority[104] == kw.addin
    assert table_sorting_priority[105] == kw.numor
    assert table_sorting_priority[106] == kw.denom
    assert table_sorting_priority[107] == kw.morph
    assert table_sorting_priority[108] == kw.gogo_want
    assert table_sorting_priority[109] == kw.stop_want
    assert table_sorting_priority[110] == kw.active_requisite
    assert table_sorting_priority[111] == kw.contact_cred_lumen
    assert table_sorting_priority[112] == kw.contact_debt_lumen
    assert table_sorting_priority[113] == kw.group_cred_lumen
    assert table_sorting_priority[114] == kw.group_debt_lumen
    assert table_sorting_priority[115] == kw.credor_respect
    assert table_sorting_priority[116] == kw.debtor_respect
    assert table_sorting_priority[117] == kw.fact_lower
    assert table_sorting_priority[118] == f"{kw.fact_lower}_otx"
    assert table_sorting_priority[119] == f"{kw.fact_lower}_inx"
    assert table_sorting_priority[120] == kw.fact_upper
    assert table_sorting_priority[121] == f"{kw.fact_upper}_otx"
    assert table_sorting_priority[122] == f"{kw.fact_upper}_inx"
    assert table_sorting_priority[123] == kw.fund_pool
    assert table_sorting_priority[124] == kw.give_force
    assert table_sorting_priority[125] == kw.star
    assert table_sorting_priority[126] == kw.max_tree_traverse
    assert table_sorting_priority[127] == kw.reason_lower
    assert table_sorting_priority[128] == f"{kw.reason_lower}_otx"
    assert table_sorting_priority[129] == f"{kw.reason_lower}_inx"
    assert table_sorting_priority[130] == kw.reason_upper
    assert table_sorting_priority[131] == f"{kw.reason_upper}_otx"
    assert table_sorting_priority[132] == f"{kw.reason_upper}_inx"
    assert table_sorting_priority[133] == kw.reason_divisor
    assert table_sorting_priority[134] == kw.pledge
    assert table_sorting_priority[135] == kw.problem_bool
    assert table_sorting_priority[136] == kw.take_force
    assert table_sorting_priority[137] == kw.fund_grain
    assert table_sorting_priority[138] == kw.mana_grain
    assert table_sorting_priority[139] == kw.respect_grain
    assert table_sorting_priority[140] == kw.amount
    assert table_sorting_priority[141] == kw.otx_label
    assert table_sorting_priority[142] == kw.inx_label
    assert table_sorting_priority[143] == kw.otx_rope
    assert table_sorting_priority[144] == kw.inx_rope
    assert table_sorting_priority[145] == kw.otx_name
    assert table_sorting_priority[146] == kw.inx_name
    assert table_sorting_priority[147] == kw.otx_title
    assert table_sorting_priority[148] == kw.inx_title
    assert table_sorting_priority[149] == kw.otx_knot
    assert table_sorting_priority[150] == kw.inx_knot
    assert table_sorting_priority[151] == kw.otx_time
    assert table_sorting_priority[152] == kw.inx_time
    assert table_sorting_priority[153] == kw.knot
    assert table_sorting_priority[154] == kw.groupmark
    assert table_sorting_priority[155] == kw.unknown_str
    assert table_sorting_priority[156] == kw.quota
    assert table_sorting_priority[157] == kw.celldepth
    assert table_sorting_priority[158] == kw.job_listen_rotations
    assert table_sorting_priority[159] == kw.error_message
    assert table_sorting_priority[160] == kw.person_name_is_workforce
    assert table_sorting_priority[161] == kw.plan_active
    assert table_sorting_priority[162] == kw.plan_task
    assert table_sorting_priority[163] == kw.case_task
    assert table_sorting_priority[164] == kw.reason_active
    assert table_sorting_priority[165] == kw.reason_task
    assert table_sorting_priority[166] == kw.case_active
    assert table_sorting_priority[167] == kw.credor_pool
    assert table_sorting_priority[168] == kw.debtor_pool
    assert table_sorting_priority[169] == kw.rational
    assert table_sorting_priority[170] == kw.fund_give
    assert table_sorting_priority[171] == kw.fund_take
    assert table_sorting_priority[172] == kw.fund_onset
    assert table_sorting_priority[173] == kw.fund_cease
    assert table_sorting_priority[174] == kw.fund_ratio
    assert table_sorting_priority[175] == kw.fund_agenda_give
    assert table_sorting_priority[176] == kw.fund_agenda_take
    assert table_sorting_priority[177] == kw.fund_agenda_ratio_give
    assert table_sorting_priority[178] == kw.fund_agenda_ratio_take
    assert table_sorting_priority[179] == kw.inallocable_contact_debt_lumen
    assert table_sorting_priority[180] == kw.gogo_calc
    assert table_sorting_priority[181] == kw.stop_calc
    assert table_sorting_priority[182] == kw.tree_level
    assert table_sorting_priority[183] == kw.range_evaluated
    assert table_sorting_priority[184] == kw.descendant_pledge_count
    assert table_sorting_priority[185] == kw.healerunit_ratio
    assert table_sorting_priority[186] == kw.all_contact_cred
    assert table_sorting_priority[187] == kw.keeps_justified
    assert table_sorting_priority[188] == kw.offtrack_fund
    assert table_sorting_priority[189] == kw.parent_heir_active
    assert table_sorting_priority[190] == kw.irrational_contact_debt_lumen
    assert table_sorting_priority[191] == kw.sum_healerunit_plans_fund_total
    assert table_sorting_priority[192] == kw.keeps_buildable
    assert table_sorting_priority[193] == kw.all_contact_debt
    assert table_sorting_priority[194] == kw.tree_traverse_count
    assert table_sorting_priority[195] == kw.net_funds
    assert table_sorting_priority[196] == kw.fund_rank
    assert table_sorting_priority[197] == kw.pledges_count
    assert table_sorting_priority[198] == f"context_plan_{kw.close}"
    assert table_sorting_priority[199] == f"context_plan_{kw.denom}"
    assert table_sorting_priority[200] == f"context_plan_{kw.morph}"
    assert table_sorting_priority[201] == kw.inx_epoch_diff

    assert len(table_sorting_priority) == 202
    all_args = copy_copy(atom_args)
    all_args.update(all_person_dimen_delete_keys)
    all_args.update(moment_args)
    all_args.update(translate_args)
    all_args.update(person_calc_args)
    all_args.update(nabu_args)
    all_args.update(translateable_otx_cols)
    all_args.update(translateable_inx_cols)
    all_args.update(translateable_delete_otx_cols)
    all_args.update(translateable_delete_inx_cols)
    all_args.update(nabuable_otx_cols)
    all_args.update(nabuable_inx_cols)
    all_args.update()
    all_args.add(kw.idea_number)
    all_args.add(kw.spark_num)
    all_args.add(kw.spark_face)
    all_args.add(kw.source_dimen)
    all_args.add(kw.translate_spark_num)
    all_args.add(kw.error_message)
    all_args.add(kw.world_name)
    all_args.add(kw.net_funds)  # kpi columns
    all_args.add(kw.fund_rank)  # kpi columns
    all_args.add(kw.pledges_count)  # kpi columns
    all_args.add(f"context_plan_{kw.close}")  # nabu ReasonNum FactNum staging columns
    all_args.add(f"context_plan_{kw.denom}")  # nabu ReasonNum FactNum staging columns
    all_args.add(f"context_plan_{kw.morph}")  # nabu ReasonNum FactNum staging columns
    all_args.add(kw.inx_epoch_diff)  # nabu ReasonNum FactNum staging columns
    assert all_args == set(table_sorting_priority)

    x_no_underscoore_set = {x_arg.replace("_", "") for x_arg in table_sorting_priority}
    # x_dict = {}
    # for x_arg in sorted(table_sorting_priority):
    #     y_arg = x_arg.replace("_", "")
    #     if x_dict.get(y_arg) is None:
    #         x_dict[y_arg] = 0
    #     x_dict[y_arg] = x_dict.get(y_arg) + 1
    # print(f"{x_dict=}")
    assert len(x_no_underscoore_set) == len(table_sorting_priority)


def test_get_idea_sqlite_types_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_idea_sqlite_types()

    # THEN
    assert set(sqlite_types.keys()) == set(get_idea_elements_sort_order())
    assert sqlite_types.get(kw.idea_number) == "TEXT"
    assert sqlite_types.get(kw.spark_face) == "TEXT"
    assert sqlite_types.get(kw.translate_spark_num) == "INTEGER"
    assert sqlite_types.get(kw.spark_num) == "INTEGER"
    assert sqlite_types.get(kw.moment_rope) == "TEXT"
    assert sqlite_types.get(kw.person_name) == "TEXT"
    assert sqlite_types.get(kw.contact_name) == "TEXT"
    assert sqlite_types.get(kw.group_title) == "TEXT"
    assert sqlite_types.get(kw.plan_rope) == "TEXT"
    assert sqlite_types.get(kw.reason_context) == "TEXT"
    assert sqlite_types.get(kw.reason_state) == "TEXT"
    assert sqlite_types.get(kw.fact_state) == "TEXT"
    assert sqlite_types.get(kw.labor_title) == "TEXT"
    assert sqlite_types.get(kw.awardee_title) == "TEXT"
    assert sqlite_types.get(kw.healer_name) == "TEXT"
    assert sqlite_types.get(kw.offi_time) == "INTEGER"
    assert sqlite_types.get(kw.bud_time) == "INTEGER"
    assert sqlite_types.get(kw.tran_time) == "INTEGER"
    assert sqlite_types.get(kw.begin) == "REAL"
    assert sqlite_types.get(kw.close) == "REAL"
    assert sqlite_types.get(kw.addin) == "REAL"
    assert sqlite_types.get(kw.numor) == "INTEGER"
    assert sqlite_types.get(kw.denom) == "INTEGER"
    assert sqlite_types.get(kw.morph) == "INTEGER"
    assert sqlite_types.get(kw.gogo_want) == "REAL"
    assert sqlite_types.get(kw.stop_want) == "REAL"
    assert sqlite_types.get(kw.active_requisite) == "INTEGER"
    assert sqlite_types.get(kw.contact_cred_lumen) == "REAL"
    assert sqlite_types.get(kw.contact_debt_lumen) == "REAL"
    assert sqlite_types.get(kw.group_cred_lumen) == "REAL"
    assert sqlite_types.get(kw.group_debt_lumen) == "REAL"
    assert sqlite_types.get(kw.credor_respect) == "REAL"
    assert sqlite_types.get(kw.debtor_respect) == "REAL"
    assert sqlite_types.get(kw.fact_lower) == "REAL"
    assert sqlite_types.get(kw.fact_upper) == "REAL"
    assert sqlite_types.get(kw.fund_pool) == "REAL"
    assert sqlite_types.get(kw.give_force) == "REAL"
    assert sqlite_types.get(kw.star) == "INTEGER"
    assert sqlite_types.get(kw.max_tree_traverse) == "INTEGER"
    assert sqlite_types.get(kw.reason_upper) == "REAL"
    assert sqlite_types.get(kw.reason_lower) == "REAL"
    assert sqlite_types.get(kw.reason_divisor) == "INTEGER"
    assert sqlite_types.get(kw.problem_bool) == "INTEGER"
    assert sqlite_types.get(kw.take_force) == "REAL"
    assert sqlite_types.get(kw.fund_grain) == "REAL"
    assert sqlite_types.get(kw.mana_grain) == "REAL"
    assert sqlite_types.get(kw.pledge) == "INTEGER"
    assert sqlite_types.get(kw.respect_grain) == "REAL"
    assert sqlite_types.get(kw.amount) == "REAL"
    assert sqlite_types.get(kw.month_label) == "TEXT"
    assert sqlite_types.get(kw.hour_label) == "TEXT"
    assert sqlite_types.get(kw.cumulative_minute) == "INTEGER"
    assert sqlite_types.get(kw.cumulative_day) == "INTEGER"
    assert sqlite_types.get(kw.weekday_label) == "TEXT"
    assert sqlite_types.get(kw.weekday_order) == "INTEGER"
    assert sqlite_types.get(kw.otx_knot) == "TEXT"
    assert sqlite_types.get(kw.inx_knot) == "TEXT"
    assert sqlite_types.get(kw.unknown_str) == "TEXT"
    assert sqlite_types.get(kw.knot) == "TEXT"
    assert sqlite_types.get(kw.c400_number) == "INTEGER"
    assert sqlite_types.get(kw.yr1_jan1_offset) == "INTEGER"
    assert sqlite_types.get(kw.quota) == "REAL"
    assert sqlite_types.get(kw.celldepth) == "INTEGER"
    assert sqlite_types.get(kw.monthday_index) == "INTEGER"
    assert sqlite_types.get(kw.epoch_label) == "TEXT"
    assert sqlite_types.get(kw.error_message) == "TEXT"
    assert sqlite_types.get(kw.solo) == "INTEGER"
    assert sqlite_types.get(kw.inx_epoch_diff) == "INTEGER"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_person_calc_args_sqlite_datatype_dict().items():
        print(f"{x_arg=} {datatype=} {sqlite_types.get(x_arg)=}")
        assert sqlite_types.get(x_arg) == datatype

    assert set(sqlite_types.values()) == {"TEXT", "INTEGER", "REAL"}


def test_get_allowed_curds_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_allowed_curds() == {
        kw.insert_one_time,
        kw.insert_multiple,
        kw.delete_insert_update,
        kw.insert_update,
        kw.delete_insert,
        kw.delete_update,
        kw.INSERT,
        kw.DELETE,
        kw.UPDATE,
    }


def test_idea_config_path_ReturnsObj_Idea() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_idea")
    assert idea_config_path() == create_path(chapter_dir, "idea_config.json")


def test_get_idea_config_dict_ReturnsObj_Scenario0_IsFullyPopulated():
    # ESTABLISH / WHEN
    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config
    idea_config_dimens = set(x_idea_config.keys())
    assert kw.momentunit in idea_config_dimens
    assert kw.moment_budunit in idea_config_dimens
    assert kw.moment_paybook in idea_config_dimens
    assert kw.moment_epoch_hour in idea_config_dimens
    assert kw.moment_epoch_month in idea_config_dimens
    assert kw.moment_epoch_weekday in idea_config_dimens
    assert kw.moment_timeoffi in idea_config_dimens
    assert kw.person_contact_membership in idea_config_dimens
    assert kw.person_contactunit in idea_config_dimens
    assert kw.person_plan_awardunit in idea_config_dimens
    assert kw.person_plan_factunit in idea_config_dimens
    assert kw.person_plan_laborunit in idea_config_dimens
    assert kw.person_plan_healerunit in idea_config_dimens
    assert kw.person_plan_reason_caseunit in idea_config_dimens
    assert kw.person_plan_reasonunit in idea_config_dimens
    assert kw.person_planunit in idea_config_dimens
    assert kw.personunit in idea_config_dimens
    assert kw.nabu_timenum in idea_config_dimens
    assert kw.translate_name in idea_config_dimens
    assert kw.translate_title in idea_config_dimens
    assert kw.translate_label in idea_config_dimens
    assert kw.translate_rope in idea_config_dimens
    assert get_person_dimens().issubset(idea_config_dimens)
    assert get_moment_dimens().issubset(idea_config_dimens)
    assert get_nabu_dimens().issubset(idea_config_dimens)
    assert get_translate_dimens().issubset(idea_config_dimens)
    gen_all_dimens = get_person_dimens()
    gen_all_dimens.update(get_moment_dimens())
    gen_all_dimens.update(get_nabu_dimens())
    gen_all_dimens.update(get_translate_dimens())
    assert gen_all_dimens == idea_config_dimens
    assert len(x_idea_config) == 22
    _validate_idea_config(x_idea_config)


def get_idea_categorys():
    return {kw.person, kw.moment, kw.translate, kw.nabu}


def _validate_idea_config(x_idea_config: dict):
    # sourcery skip: low-code-quality
    atom_config_dict = get_atom_config_dict()
    moment_config_dict = get_moment_config_dict()
    nabu_config_dict = get_nabu_config_dict()
    translate_config_dict = get_translate_config_dict()
    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    for idea_dimen, idea_dict in x_idea_config.items():
        print(f"{idea_dimen=}")
        assert idea_dict.get(kw.idea_category) in get_idea_categorys()
        assert idea_dict.get(kw.jkeys) is not None
        assert idea_dict.get(kw.jvalues) is not None
        assert idea_dict.get(kw.allowed_crud) is not None
        assert idea_dict.get(kw.UPDATE) is None
        assert idea_dict.get(kw.INSERT) is None
        assert idea_dict.get(kw.DELETE) is None
        assert idea_dict.get(kw.normal_specs) is None
        if idea_dict.get(kw.idea_category) == kw.person:
            sub_dimen = atom_config_dict.get(idea_dimen)
        elif idea_dict.get(kw.idea_category) == kw.moment:
            sub_dimen = moment_config_dict.get(idea_dimen)
        elif idea_dict.get(kw.idea_category) == kw.nabu:
            sub_dimen = nabu_config_dict.get(idea_dimen)
        elif idea_dict.get(kw.idea_category) == kw.translate:
            sub_dimen = translate_config_dict.get(idea_dimen)

        assert idea_dict.get(kw.allowed_crud) in get_allowed_curds()

        UPDATE_dimen = sub_dimen.get(kw.UPDATE)
        INSERT_dimen = sub_dimen.get(kw.INSERT)
        DELETE_dimen = sub_dimen.get(kw.DELETE)
        idea_allowed_crud = idea_dict.get(kw.allowed_crud)
        # print(
        #     f"{idea_dimen=} {UPDATE_dimen} {INSERT_dimen} {DELETE_dimen=} {idea_allowed_crud=}"
        # )
        if idea_dimen in {
            kw.moment_epoch_hour,
            kw.moment_epoch_month,
            kw.moment_epoch_weekday,
            kw.momentunit,
            "map_otx2inx",
            kw.nabu_timenum,
            kw.translate_title,
            kw.translate_name,
            kw.translate_label,
            kw.translate_rope,
        }:
            assert idea_allowed_crud == kw.insert_one_time
        elif idea_dimen in {kw.moment_budunit, kw.moment_paybook, kw.moment_timeoffi}:
            assert idea_allowed_crud == kw.insert_multiple
        elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen != None:
            assert idea_allowed_crud == kw.delete_insert_update
        elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen is None:
            assert idea_allowed_crud == kw.insert_update
        elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen != None:
            assert idea_allowed_crud == kw.delete_insert
        elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen != None:
            assert idea_allowed_crud == kw.delete_update
        elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen is None:
            assert idea_allowed_crud == kw.UPDATE
        elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen is None:
            assert idea_allowed_crud == kw.INSERT
        elif UPDATE_dimen is None and INSERT_dimen is None and DELETE_dimen != None:
            assert idea_allowed_crud == kw.DELETE
        else:
            assert idea_allowed_crud == f"{kw.allowed_crud} not checked by test"

        sub_jkeys_keys = set(sub_dimen.get(kw.jkeys).keys())
        idea_jkeys_keys = set(idea_dict.get(kw.jkeys).keys())
        # print(f"   {sub_jkeys_keys=}")
        # print(f"  {idea_jkeys_keys=}")
        assert kw.spark_face in idea_jkeys_keys
        assert kw.spark_num in idea_jkeys_keys
        if idea_dict.get(kw.idea_category) in {kw.person} and kw.plan in idea_dimen:
            assert kw.moment_rope not in idea_jkeys_keys, idea_dimen
        elif idea_dict.get(kw.idea_category) in {kw.moment, kw.person}:
            assert kw.moment_rope in idea_jkeys_keys
            # print(f"2{idea_dimen=}")
            if idea_dict.get(kw.idea_category) in {kw.person}:
                idea_jkeys_keys.remove(kw.moment_rope)
        if idea_dict.get(kw.idea_category) in {kw.person}:
            idea_jkeys_keys.remove(kw.person_name)
        idea_jkeys_keys.remove(kw.spark_face)
        idea_jkeys_keys.remove(kw.spark_num)
        assertion_failure_str = f"{idea_dimen=} {sub_jkeys_keys=} {idea_jkeys_keys=}"
        assert sub_jkeys_keys == idea_jkeys_keys, assertion_failure_str

        expected_jvalues_keys = set(sub_dimen.get(kw.jvalues).keys())
        # all moment and plan dimen must have knot jvalue because they all have rope keys
        if idea_dict.get(kw.idea_category) in {kw.moment, kw.person}:
            expected_jvalues_keys.add(kw.knot)
        # print(f"{idea_dimen=}")
        # if kw.moment_rope in expected_jvalues_keys:
        #     expected_jvalues_keys.remove(kw.moment_rope)

        idea_jvalues_dict = idea_dict.get(kw.jvalues)
        idea_jvalues_keys = set(idea_jvalues_dict.keys())
        # print(f" {expected_jvalues_keys=}")
        # print(f"{idea_jvalues_keys=}")
        assert expected_jvalues_keys == idea_jvalues_keys


def test_get_idea_format_filenames_ReturnsObj_CheckSome_idea_format_filesnames_Exist():
    # ESTABLISH
    idea_filenames_set = get_idea_format_filenames()

    # WHEN / THEN
    assert idea_format_00021_person_contactunit_v0_0_0() in idea_filenames_set
    assert idea_format_00020_person_contact_membership_v0_0_0() in idea_filenames_set
    assert idea_format_00013_planunit_v0_0_0() in idea_filenames_set


def change_erase_attrs(idea_attrs: set):
    idea_attrs_list = get_default_sorted_list(idea_attrs)
    if idea_attrs_list[-1].find("_ERASE") > 0:
        delete_attr_with_erase = idea_attrs_list[-1]
        delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
        idea_attrs.remove(delete_attr_with_erase)
        idea_attrs.add(delete_attr_without_erase)


def test_get_idea_format_filenames_ReturnsObj_Validate_idea_format_files():
    # sourcery skip:  no-conditionals-in-tests
    # ESTABLISH / WHEN
    idea_filenames_sorted = list(get_idea_format_filenames())

    # THEN
    idea_filenames_sorted.sort(key=lambda x: x)
    print(f"{len(idea_filenames_sorted)=}")

    all_dimen_keys_dict = {
        dimen: set(dict.get(kw.jkeys).keys())
        for dimen, dict in get_idea_config_dict().items()
    }

    valid_idea_dimens = set()
    valid_idea_dimens.update(get_person_dimens())
    valid_idea_dimens.update(get_moment_dimens())
    valid_idea_dimens.update(get_nabu_dimens())
    valid_idea_dimens.update(get_translate_dimens())
    print("get_idea_config_dict")
    config_dict = get_idea_config_dict()

    # for every idea_format file there exists a unique idea_number with leading zeros to make 5 digits
    idea_numbers_set = set()
    for idea_filename in idea_filenames_sorted:
        ref_dict = get_idearef_from_file(idea_filename)
        # print(f"{idea_filename=} {ref_dict.get(kw.idea_number)=}")
        idea_number_value = ref_dict.get(kw.idea_number)
        assert idea_number_value
        assert idea_number_value[2:8] == idea_filename[12:17]
        idea_numbers_set.add(idea_number_value)

        format_dimens = ref_dict.get(kw.dimens)
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for idea_format_dimen in format_dimens:
            assert idea_format_dimen in valid_idea_dimens

        assert ref_dict.get(kw.attributes)
        idea_format_attributes = ref_dict.get(kw.attributes)
        for idea_attribute, attr_dict in idea_format_attributes.items():
            # print(f"{idea_attribute=}")
            assert kw.otx_key in set(attr_dict.keys())
            otx_key_value = attr_dict.get(kw.otx_key)
            for idea_format_dimen in format_dimens:
                format_config = config_dict.get(idea_format_dimen)
                dimen_required_attrs = set(format_config.get(kw.jkeys).keys())
                dimen_optional_attrs = set(format_config.get(kw.jvalues).keys())
                attr_in_required = idea_attribute in dimen_required_attrs
                attr_in_optional = idea_attribute in dimen_optional_attrs
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{idea_format_dimen=} {idea_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str
        # check all implied dimens are there
        idea_attrs = set(ref_dict.get(kw.attributes).keys())
        change_erase_attrs(idea_attrs)

        for x_dimen, dimen_keys in all_dimen_keys_dict.items():
            # if x_dimen == kw.person_plan_factunit and x_dimen in format_dimens:
            #     print(f"{idea_number_value}  {x_dimen=} {idea_attrs_list=}")
            if dimen_keys.issubset(idea_attrs):
                if x_dimen not in format_dimens:
                    print(f"MISSING {x_dimen=} {idea_number_value} {idea_attrs=}")
                assert x_dimen in format_dimens
            else:
                # dimen_keys_list = get_default_sorted_list(dimen_keys)
                #     idea_attrs_list[-1] = idea_attrs_list[-1].removesuffix("_ERASE")
                #     idea_attrs = set(idea_attrs_list)
                if x_dimen in format_dimens:
                    print(
                        f"SHOULDNT BE {x_dimen=} {idea_number_value} : {get_default_sorted_list(idea_attrs)}"
                    )
                    # print(
                    #     f"SHOULDNT BE {x_dimen=} {idea_number_value} : {get_default_sorted_list(dimen_keys)}"
                    # )
                assert x_dimen not in format_dimens

    # assert kw.spark_face in idea_format_attributes
    # assert kw.spark_num in idea_format_attributes

    # confirm every ideanumber is unique
    assert len(idea_numbers_set) == len(idea_filenames_sorted)
    assert idea_numbers_set == get_idea_numbers()


def test_get_idea_format_filename_ReturnsObj():
    # ESTABLISH
    br00021_str = "br00021"
    br00020_str = "br00020"
    br00013_str = "br00013"

    # WHEN
    br00021_filename = get_idea_format_filename(br00021_str)
    br00020_filename = get_idea_format_filename(br00020_str)
    br00013_filename = get_idea_format_filename(br00013_str)

    # THEN
    assert br00021_filename == idea_format_00021_person_contactunit_v0_0_0()
    assert br00020_filename == idea_format_00020_person_contact_membership_v0_0_0()
    assert br00013_filename == idea_format_00013_planunit_v0_0_0()

    all_set = {get_idea_format_filename(br) for br in get_idea_numbers()}
    assert all_set == get_idea_format_filenames()


def set_idea_config_json(dimen: str, build_order: int):
    x_idea_config = get_idea_config_dict()
    dimen_dict = x_idea_config.get(dimen)
    dimen_dict[kw.build_order] = build_order
    x_idea_config[dimen] = dimen_dict
    save_json(idea_config_path(), None, x_idea_config)


def test_get_idea_config_dict_ReturnsObj_Scenario1_Check_build_order():
    # ESTABLISH / WHEN
    bo = kw.build_order
    # set_idea_config_json(kw.translate_name, 0)
    # set_idea_config_json(kw.translate_title, 1)
    # set_idea_config_json(kw.translate_label, 2)
    # set_idea_config_json(kw.translate_rope, 3)
    # set_idea_config_json(kw.momentunit, 5)
    # set_idea_config_json(kw.moment_epoch_hour, 6)
    # set_idea_config_json(kw.moment_epoch_month, 7)
    # set_idea_config_json(kw.moment_epoch_weekday, 8)
    # set_idea_config_json(kw.person_contact_membership, 9)
    # set_idea_config_json(kw.person_contactunit, 10)
    # set_idea_config_json(kw.person_plan_awardunit, 11)
    # set_idea_config_json(kw.person_plan_factunit, 12)
    # set_idea_config_json(kw.person_plan_laborunit, 14)
    # set_idea_config_json(kw.person_plan_healerunit, 15)
    # set_idea_config_json(kw.person_plan_reason_caseunit, 16)
    # set_idea_config_json(kw.person_plan_reasonunit, 17)
    # set_idea_config_json(kw.person_planunit, 18)
    # set_idea_config_json(kw.personunit, 19)
    # set_idea_config_json(kw.moment_budunit, 20)
    # set_idea_config_json(kw.moment_paybook, 21)

    x_idea_config = get_idea_config_dict()

    # THEN
    assert x_idea_config.get(kw.translate_name).get(bo) == 0
    assert x_idea_config.get(kw.translate_title).get(bo) == 1
    assert x_idea_config.get(kw.translate_label).get(bo) == 2
    assert x_idea_config.get(kw.translate_rope).get(bo) == 3
    assert x_idea_config.get(kw.nabu_timenum).get(bo) == 4
    assert x_idea_config.get(kw.momentunit).get(bo) == 5
    assert x_idea_config.get(kw.moment_epoch_hour).get(bo) == 6
    assert x_idea_config.get(kw.moment_epoch_month).get(bo) == 7
    assert x_idea_config.get(kw.moment_epoch_weekday).get(bo) == 8
    assert x_idea_config.get(kw.person_contact_membership).get(bo) == 9
    assert x_idea_config.get(kw.person_contactunit).get(bo) == 10
    assert x_idea_config.get(kw.person_plan_awardunit).get(bo) == 11
    assert x_idea_config.get(kw.person_plan_factunit).get(bo) == 12
    assert x_idea_config.get(kw.person_plan_laborunit).get(bo) == 14
    assert x_idea_config.get(kw.person_plan_healerunit).get(bo) == 15
    assert x_idea_config.get(kw.person_plan_reason_caseunit).get(bo) == 16
    assert x_idea_config.get(kw.person_plan_reasonunit).get(bo) == 17
    assert x_idea_config.get(kw.person_planunit).get(bo) == 18
    assert x_idea_config.get(kw.personunit).get(bo) == 19
    assert x_idea_config.get(kw.moment_budunit).get(bo) == 20
    assert x_idea_config.get(kw.moment_paybook).get(bo) == 21
    assert x_idea_config.get(kw.moment_timeoffi).get(bo) == 22
    builder_order_dict = {}
    for dimen_key, dimen_dict in x_idea_config.items():
        dimen_builder_order = dimen_dict.get(bo)
        assert dimen_builder_order is not None
        print(
            f"{dimen_key:30} build order: {dimen_builder_order:2} {sorted(builder_order_dict.keys())=}"
        )
        assert not builder_order_dict.get(dimen_builder_order)
        builder_order_dict[dimen_builder_order] = dimen_key
    print(f"{sorted(builder_order_dict.keys())=}")


def test_get_idea_config_dict_ReturnsObj_Scenario0_Person():
    # ESTABLISH / WHEN
    person_idea_config = get_idea_config_dict(kw.person)

    # THEN
    assert not person_idea_config.get(kw.translate_name)
    assert not person_idea_config.get(kw.translate_title)
    assert not person_idea_config.get(kw.translate_label)
    assert not person_idea_config.get(kw.translate_rope)
    assert not person_idea_config.get(kw.nabu_timenum)
    assert not person_idea_config.get(kw.momentunit)
    assert not person_idea_config.get(kw.moment_epoch_hour)
    assert not person_idea_config.get(kw.moment_epoch_month)
    assert not person_idea_config.get(kw.moment_epoch_weekday)
    assert person_idea_config.get(kw.person_contact_membership)
    assert person_idea_config.get(kw.person_contactunit)
    assert person_idea_config.get(kw.person_plan_awardunit)
    assert person_idea_config.get(kw.person_plan_factunit)
    assert person_idea_config.get(kw.person_plan_laborunit)
    assert person_idea_config.get(kw.person_plan_healerunit)
    assert person_idea_config.get(kw.person_plan_reason_caseunit)
    assert person_idea_config.get(kw.person_plan_reasonunit)
    assert person_idea_config.get(kw.person_planunit)
    assert person_idea_config.get(kw.personunit)
    assert not person_idea_config.get(kw.moment_budunit)
    assert not person_idea_config.get(kw.moment_paybook)
    assert not person_idea_config.get(kw.moment_timeoffi)


def test_get_idea_config_dict_ReturnsObj_Scenario1_CountDimens():
    # ESTABLISH / WHEN / THEN
    assert len(get_idea_config_dict(idea_categorys={kw.person})) == 10
    assert len(get_idea_config_dict(idea_categorys={kw.moment})) == 7
    assert len(get_idea_config_dict(idea_categorys={kw.nabu})) == 1
    assert len(get_idea_config_dict(idea_categorys={kw.translate})) == 4
    assert len(get_idea_config_dict({kw.nabu, kw.translate})) == 5


def test_get_quick_ideas_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_idea_quick_column_ref = get_quick_ideas_column_ref()

    # THEN
    assert len(x_idea_quick_column_ref) == len(get_idea_numbers())
    assert x_idea_quick_column_ref.get("br00000") == {
        kw.spark_num,
        kw.spark_face,
        kw.c400_number,
        kw.moment_rope,
        kw.fund_grain,
        kw.monthday_index,
        kw.mana_grain,
        kw.respect_grain,
        kw.knot,
        kw.epoch_label,
        kw.yr1_jan1_offset,
        kw.job_listen_rotations,
    }


def _create_expected_idea_dimen_ref() -> dict[str, list[str]]:
    idea_numbers_sorted = list(get_idea_numbers())
    idea_numbers_sorted.sort(key=lambda x: x)
    expected_idea_dimen_ref = {}
    for idea_number in idea_numbers_sorted:
        idea_format_filename = get_idea_format_filename(idea_number)
        x_idearef = get_idearef_from_file(idea_format_filename)
        dimens_list = x_idearef.get(kw.dimens)
        for x_dimen in dimens_list:
            if expected_idea_dimen_ref.get(x_dimen) is None:
                expected_idea_dimen_ref[x_dimen] = {idea_number}
            else:
                expected_idea_dimen_ref.get(x_dimen).add(idea_number)
    return expected_idea_dimen_ref


def print_sorted(obj, indent=0):
    """Pretty-print dictionaries with sorted keys and sets printed in sorted order."""
    space = " " * indent

    if isinstance(obj, dict):
        print(space + "{")
        for key in sorted(obj):
            print(f"{space}  {repr(key)}: ", end="")
            print_sorted(obj[key], indent + 4)
        print(space + "}")

    elif isinstance(obj, set):
        # print set elements in sorted order but keep set notation
        items = sorted(obj)
        print(space + "{" + ", ".join(repr(x) for x in items) + "}")

    elif isinstance(obj, (list, tuple)):
        open_c, close_c = ("[", "]") if isinstance(obj, list) else ("(", ")")
        print(space + open_c)
        for item in obj:
            print_sorted(item, indent + 4)
        print(space + close_c)

    else:
        print(space + repr(obj))


def test_get_idea_dimen_ref_ReturnsObj():
    # ESTABLISH
    expected_idea_dimen_ref = _create_expected_idea_dimen_ref()
    # print(f"{expected_idea_dimen_ref=}")
    print_sorted(expected_idea_dimen_ref)

    # WHEN / THEN
    assert get_idea_dimen_ref() == expected_idea_dimen_ref


def test_get_dimens_with_idea_element_ReturnsObj_Scenario0_offi_time():
    # ESTABLISH / WHEN / THEN
    assert get_dimens_with_idea_element(kw.offi_time) == {kw.moment_timeoffi}
