from ch00_py.dict_toolbox import normalize_obj
from ch00_py.file_toolbox import create_path, save_json
from ch08_person_logic.person_config import (
    get_all_person_calc_args,
    get_person_calc_args_sqlite_datatype_dict,
)
from ch09_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_person_dimens,
)
from ch15_moment.moment_config import (
    get_moment_args_dimen_mapping,
    get_moment_config_dict,
    get_moment_dimens,
)
from ch16_nabu.nabu_config import (
    get_nabu_args,
    get_nabu_config_dict,
    get_nabu_dimens,
    get_nabuable_args,
)
from ch17_jargon.jargon_config import (
    get_jargon_args_dimen_mapping,
    get_jargon_config_dict,
    get_jargon_dimens,
    get_jargonable_args,
)
from ch18_speech.speech_config import (
    # get_speech_args_dimen_mapping,
    get_speech_config_dict,
    # get_speech_dimens,
    get_speechable_args,
    get_speech_args_dimen_mapping,
)
from ch20_brick.brick_config import (
    BrickFormatsEnum,
    brick_config_path,
    get_allowed_curds,
    get_brick_config_dict,
    get_brick_dimen_ref,
    get_brick_format_filename,
    get_brick_format_filenames,
    get_brick_sqlite_types,
    get_brick_types,
    get_brickref_from_file,
    get_default_sorted_list,
    get_dimens_with_brick_element,
    get_quick_bricks_column_ref,
)
from ch99_glossary.ch_keyword import Ch20Keywords as kw
from ch99_glossary.sorter import get_keg_elements_sort_order
from copy import copy as copy_copy
from pathlib import Path as pathlib_Path
from unittest.mock import patch as mock_patch


def test_get_keg_elements_sort_order_ReturnsObj():
    # ESTABLISH / WHEN
    table_sorting_priority = get_keg_elements_sort_order()

    # THEN
    atom_args = set(get_atom_args_dimen_mapping().keys())
    assert atom_args.issubset(set(table_sorting_priority))

    # Moment args
    moment_args = set(get_moment_args_dimen_mapping().keys())
    # print(f"{moment_args=}")
    # print(f"{moment_args.difference(set(table_sorting_priority))=}")
    assert moment_args.issubset(set(table_sorting_priority))

    # dimen_delete_keys args
    all_person_dimen_delete_keys = get_all_person_dimen_delete_keys()
    # print(f"missing {all_person_dimen_delete_keys.difference(table_sorting_priority)}")
    assert all_person_dimen_delete_keys.issubset(table_sorting_priority)

    # nabo args
    nabu_args = get_nabu_args()
    assert nabu_args.issubset(set(table_sorting_priority))
    nabuable_otx_cols = {f"{nabu_arg}_otx" for nabu_arg in get_nabuable_args()}
    nabuable_inx_cols = {f"{nabu_arg}_inx" for nabu_arg in get_nabuable_args()}
    assert nabuable_otx_cols.issubset(table_sorting_priority)
    assert nabuable_inx_cols.issubset(table_sorting_priority)

    # jargon args
    jargon_args = set(get_jargon_args_dimen_mapping().keys())
    # print(f"{moment_args=}")
    # print(f"{jargon_args.difference(set(table_sorting_priority))=}")
    assert jargon_args.issubset(set(table_sorting_priority))
    jargonable_otx_cols = {f"{trl_arg}_otx" for trl_arg in get_jargonable_args()}
    jargonable_inx_cols = {f"{trl_arg}_inx" for trl_arg in get_jargonable_args()}
    # print(f"{jargonable_otx_cols=}")
    # print(f"{jargonable_inx_cols=}")
    assert jargonable_otx_cols.issubset(table_sorting_priority)
    assert jargonable_inx_cols.issubset(table_sorting_priority)
    x_delete_keys = all_person_dimen_delete_keys
    jargonable_delete_otx_cols = {f"{trl_arg}_otx" for trl_arg in x_delete_keys}
    jargonable_delete_inx_cols = {f"{trl_arg}_inx" for trl_arg in x_delete_keys}
    # print(f"{jargonable_delete_otx_cols=}")
    # print(f"{jargonable_delete_inx_cols=}")
    assert jargonable_delete_otx_cols.issubset(table_sorting_priority)
    assert jargonable_delete_inx_cols.issubset(table_sorting_priority)

    # speech args
    speech_args = set(get_speech_args_dimen_mapping().keys())
    # print(f"{moment_args=}")
    # print(f"{speech_args.difference(set(table_sorting_priority))=}")
    assert speech_args.issubset(set(table_sorting_priority))
    speechable_iux_cols = {f"{trl_arg}_iux" for trl_arg in get_speechable_args()}
    speechable_aux_cols = {f"{trl_arg}_aux" for trl_arg in get_speechable_args()}
    # print(f"{sorted(speechable_iux_cols.union(speechable_aux_cols))=}")
    # print(f"{speechable_aux_cols=}")
    assert speechable_iux_cols.issubset(table_sorting_priority)
    assert speechable_aux_cols.issubset(table_sorting_priority)
    x_delete_keys = all_person_dimen_delete_keys
    speechable_delete_iux_cols = {f"{trl_arg}_iux" for trl_arg in x_delete_keys}
    speechable_delete_aux_cols = {f"{trl_arg}_aux" for trl_arg in x_delete_keys}
    # print(f"{sorted(speechable_delete_iux_cols.union(speechable_delete_aux_cols))=}")
    # print(f"{speechable_delete_aux_cols=}")
    print(f"{speechable_delete_iux_cols.difference(table_sorting_priority)=}")
    assert speechable_delete_iux_cols.issubset(table_sorting_priority)
    assert speechable_delete_aux_cols.issubset(table_sorting_priority)

    # person calculated args
    person_calc_args = set(get_all_person_calc_args().keys())
    # for person_calc_arg in person_calc_args.difference(table_sorting_priority):
    #     print(f"{person_calc_arg=}")
    print(f"{person_calc_args.difference(table_sorting_priority)=}")
    assert person_calc_args.issubset(table_sorting_priority)

    # all the suffix otx/inx columns are only used in one
    assert table_sorting_priority[0] == kw.world_name
    assert table_sorting_priority[1] == kw.brick_type
    assert table_sorting_priority[2] == kw.source_dimen
    assert table_sorting_priority[3] == kw.jargon_spark_num
    assert table_sorting_priority[4] == kw.spark_num
    assert table_sorting_priority[5] == kw.spark_face
    assert table_sorting_priority[6] == f"{kw.spark_face}_otx"
    assert table_sorting_priority[7] == f"{kw.spark_face}_inx"
    assert table_sorting_priority[8] == kw.flare_num
    assert table_sorting_priority[9] == kw.flare_audie
    assert table_sorting_priority[10] == f'{kw.flare_audie}_aux'
    assert table_sorting_priority[11] == f'{kw.flare_audie}_iux'
    assert table_sorting_priority[12] == kw.moment_rope
    assert table_sorting_priority[13] == f"{kw.moment_rope}_otx"
    assert table_sorting_priority[14] == f"{kw.moment_rope}_inx"
    assert table_sorting_priority[15] == 'moment_rope_aux'
    assert table_sorting_priority[16] == 'moment_rope_iux'
    assert table_sorting_priority[17] == kw.epoch_label
    assert table_sorting_priority[18] == f"{kw.epoch_label}_otx"
    assert table_sorting_priority[19] == f"{kw.epoch_label}_inx"
    assert table_sorting_priority[20] == f"{kw.epoch_label}_aux"
    assert table_sorting_priority[21] == f"{kw.epoch_label}_iux"
    assert table_sorting_priority[22] == kw.offi_time
    assert table_sorting_priority[23] == f"{kw.offi_time}_otx"
    assert table_sorting_priority[24] == f"{kw.offi_time}_inx"
    assert table_sorting_priority[25] == kw.c400_number
    assert table_sorting_priority[26] == kw.yr1_jan1_offset
    assert table_sorting_priority[27] == kw.monthday_index
    assert table_sorting_priority[28] == kw.cumulative_day
    assert table_sorting_priority[29] == kw.month_label
    assert table_sorting_priority[30] == f"{kw.month_label}_otx"
    assert table_sorting_priority[31] == f"{kw.month_label}_inx"
    assert table_sorting_priority[32] == f"{kw.month_label}_aux"
    assert table_sorting_priority[33] == f"{kw.month_label}_iux"
    assert table_sorting_priority[34] == kw.cumulative_minute
    assert table_sorting_priority[35] == f"{kw.hour_label}"
    assert table_sorting_priority[36] == f"{kw.hour_label}_otx"
    assert table_sorting_priority[37] == f"{kw.hour_label}_inx"
    assert table_sorting_priority[38] == f"{kw.hour_label}_aux"
    assert table_sorting_priority[39] == f"{kw.hour_label}_iux"
    assert table_sorting_priority[40] == kw.weekday_order
    assert table_sorting_priority[41] == kw.weekday_label
    assert table_sorting_priority[42] == f"{kw.weekday_label}_otx"
    assert table_sorting_priority[43] == f"{kw.weekday_label}_inx"
    assert table_sorting_priority[44] == f"{kw.weekday_label}_aux"
    assert table_sorting_priority[45] == f"{kw.weekday_label}_iux"
    assert table_sorting_priority[46] == kw.person_name
    assert table_sorting_priority[47] == f"{kw.person_name}_otx"
    assert table_sorting_priority[48] == f"{kw.person_name}_inx"
    assert table_sorting_priority[49] == f"{kw.person_name}_ERASE"
    assert table_sorting_priority[50] == f"{kw.person_name}_ERASE_otx"
    assert table_sorting_priority[51] == f"{kw.person_name}_ERASE_inx"
    assert table_sorting_priority[52] == f"{kw.person_name}_aux"
    assert table_sorting_priority[53] == f"{kw.person_name}_iux"
    assert table_sorting_priority[54] == f"{kw.person_name}_ERASE_aux"
    assert table_sorting_priority[55] == f"{kw.person_name}_ERASE_iux"
    assert table_sorting_priority[56] == kw.contact_name
    assert table_sorting_priority[57] == f"{kw.contact_name}_otx"
    assert table_sorting_priority[58] == f"{kw.contact_name}_inx"
    assert table_sorting_priority[59] == f"{kw.contact_name}_ERASE"
    assert table_sorting_priority[60] == f"{kw.contact_name}_ERASE_otx"
    assert table_sorting_priority[61] == f"{kw.contact_name}_ERASE_inx"
    assert table_sorting_priority[62] == f"{kw.contact_name}_aux"
    assert table_sorting_priority[63] == f"{kw.contact_name}_iux"
    assert table_sorting_priority[64] == f"{kw.contact_name}_ERASE_aux"
    assert table_sorting_priority[65] == f"{kw.contact_name}_ERASE_iux"
    assert table_sorting_priority[66] == kw.group_title
    assert table_sorting_priority[67] == f"{kw.group_title}_otx"
    assert table_sorting_priority[68] == f"{kw.group_title}_inx"
    assert table_sorting_priority[69] == f"{kw.group_title}_ERASE"
    assert table_sorting_priority[70] == f"{kw.group_title}_ERASE_otx"
    assert table_sorting_priority[71] == f"{kw.group_title}_ERASE_inx"
    assert table_sorting_priority[72] == f"{kw.group_title}_aux"
    assert table_sorting_priority[73] == f"{kw.group_title}_iux"
    assert table_sorting_priority[74] == f"{kw.group_title}_ERASE_aux"
    assert table_sorting_priority[75] == f"{kw.group_title}_ERASE_iux"
    assert table_sorting_priority[76] == kw.plan_rope
    assert table_sorting_priority[77] == f"{kw.plan_rope}_otx"
    assert table_sorting_priority[78] == f"{kw.plan_rope}_inx"
    assert table_sorting_priority[79] == f"{kw.plan_rope}_ERASE"
    assert table_sorting_priority[80] == f"{kw.plan_rope}_ERASE_otx"
    assert table_sorting_priority[81] == f"{kw.plan_rope}_ERASE_inx"
    assert table_sorting_priority[82] == f"{kw.plan_rope}_aux"
    assert table_sorting_priority[83] == f"{kw.plan_rope}_iux"
    assert table_sorting_priority[84] == f"{kw.plan_rope}_ERASE_aux"
    assert table_sorting_priority[85] == f"{kw.plan_rope}_ERASE_iux"
    assert table_sorting_priority[86] == kw.reason_context
    assert table_sorting_priority[87] == f"{kw.reason_context}_otx"
    assert table_sorting_priority[88] == f"{kw.reason_context}_inx"
    assert table_sorting_priority[89] == f"{kw.reason_context}_ERASE"
    assert table_sorting_priority[90] == f"{kw.reason_context}_ERASE_otx"
    assert table_sorting_priority[91] == f"{kw.reason_context}_ERASE_inx"
    assert table_sorting_priority[92] == f"{kw.reason_context}_aux"
    assert table_sorting_priority[93] == f"{kw.reason_context}_iux"
    assert table_sorting_priority[94] == f"{kw.reason_context}_ERASE_aux"
    assert table_sorting_priority[95] == f"{kw.reason_context}_ERASE_iux"
    assert table_sorting_priority[96] == kw.fact_context
    assert table_sorting_priority[97] == f"{kw.fact_context}_otx"
    assert table_sorting_priority[98] == f"{kw.fact_context}_inx"
    assert table_sorting_priority[99] == f"{kw.fact_context}_ERASE"
    assert table_sorting_priority[100] == f"{kw.fact_context}_ERASE_otx"
    assert table_sorting_priority[101] == f"{kw.fact_context}_ERASE_inx"
    assert table_sorting_priority[102] == f"{kw.fact_context}_aux"
    assert table_sorting_priority[103] == f"{kw.fact_context}_iux"
    assert table_sorting_priority[104] == f"{kw.fact_context}_ERASE_aux"
    assert table_sorting_priority[105] == f"{kw.fact_context}_ERASE_iux"
    assert table_sorting_priority[106] == kw.reason_state
    assert table_sorting_priority[107] == f"{kw.reason_state}_otx"
    assert table_sorting_priority[108] == f"{kw.reason_state}_inx"
    assert table_sorting_priority[109] == f"{kw.reason_state}_ERASE"
    assert table_sorting_priority[110] == f"{kw.reason_state}_ERASE_otx"
    assert table_sorting_priority[111] == f"{kw.reason_state}_ERASE_inx"
    assert table_sorting_priority[112] == f"{kw.reason_state}_aux"
    assert table_sorting_priority[113] == f"{kw.reason_state}_iux"
    assert table_sorting_priority[114] == f"{kw.reason_state}_ERASE_aux"
    assert table_sorting_priority[115] == f"{kw.reason_state}_ERASE_iux"
    assert table_sorting_priority[116] == kw.fact_state
    assert table_sorting_priority[117] == f"{kw.fact_state}_otx"
    assert table_sorting_priority[118] == f"{kw.fact_state}_inx"
    assert table_sorting_priority[119] == f"{kw.fact_state}_aux"
    assert table_sorting_priority[120] == f"{kw.fact_state}_iux"
    assert table_sorting_priority[121] == kw.labor_title
    assert table_sorting_priority[122] == f"{kw.labor_title}_otx"
    assert table_sorting_priority[123] == f"{kw.labor_title}_inx"
    assert table_sorting_priority[124] == f"{kw.labor_title}_ERASE"
    assert table_sorting_priority[125] == f"{kw.labor_title}_ERASE_otx"
    assert table_sorting_priority[126] == f"{kw.labor_title}_ERASE_inx"
    assert table_sorting_priority[127] == f"{kw.labor_title}_aux"
    assert table_sorting_priority[128] == f"{kw.labor_title}_iux"
    assert table_sorting_priority[129] == f"{kw.labor_title}_ERASE_aux"
    assert table_sorting_priority[130] == f"{kw.labor_title}_ERASE_iux"
    assert table_sorting_priority[131] == kw.solo
    assert table_sorting_priority[132] == kw.awardee_title
    assert table_sorting_priority[133] == f"{kw.awardee_title}_otx"
    assert table_sorting_priority[134] == f"{kw.awardee_title}_inx"
    assert table_sorting_priority[135] == f"{kw.awardee_title}_ERASE"
    assert table_sorting_priority[136] == f"{kw.awardee_title}_ERASE_otx"
    assert table_sorting_priority[137] == f"{kw.awardee_title}_ERASE_inx"
    assert table_sorting_priority[138] == f"{kw.awardee_title}_aux"
    assert table_sorting_priority[139] == f"{kw.awardee_title}_iux"
    assert table_sorting_priority[140] == f"{kw.awardee_title}_ERASE_aux"
    assert table_sorting_priority[141] == f"{kw.awardee_title}_ERASE_iux"
    assert table_sorting_priority[142] == kw.healer_name
    assert table_sorting_priority[143] == f"{kw.healer_name}_otx"
    assert table_sorting_priority[144] == f"{kw.healer_name}_inx"
    assert table_sorting_priority[145] == f"{kw.healer_name}_ERASE"
    assert table_sorting_priority[146] == f"{kw.healer_name}_ERASE_otx"
    assert table_sorting_priority[147] == f"{kw.healer_name}_ERASE_inx"
    assert table_sorting_priority[148] == f"{kw.healer_name}_aux"
    assert table_sorting_priority[149] == f"{kw.healer_name}_iux"
    assert table_sorting_priority[150] == f"{kw.healer_name}_ERASE_aux"
    assert table_sorting_priority[151] == f"{kw.healer_name}_ERASE_iux"
    assert table_sorting_priority[152] == kw.bud_time
    assert table_sorting_priority[153] == f"{kw.bud_time}_otx"
    assert table_sorting_priority[154] == f"{kw.bud_time}_inx"
    assert table_sorting_priority[155] == kw.tran_time
    assert table_sorting_priority[156] == f"{kw.tran_time}_otx"
    assert table_sorting_priority[157] == f"{kw.tran_time}_inx"
    assert table_sorting_priority[158] == kw.begin
    assert table_sorting_priority[159] == kw.close
    assert table_sorting_priority[160] == kw.addin
    assert table_sorting_priority[161] == kw.numor
    assert table_sorting_priority[162] == kw.denom
    assert table_sorting_priority[163] == kw.morph
    assert table_sorting_priority[164] == kw.gogo_want
    assert table_sorting_priority[165] == kw.stop_want
    assert table_sorting_priority[166] == kw.active_requisite
    assert table_sorting_priority[167] == kw.contact_cred_mass
    assert table_sorting_priority[168] == kw.contact_debt_mass
    assert table_sorting_priority[169] == kw.group_cred_mass
    assert table_sorting_priority[170] == kw.group_debt_mass
    assert table_sorting_priority[171] == kw.credor_respect
    assert table_sorting_priority[172] == kw.debtor_respect
    assert table_sorting_priority[173] == kw.fact_lower
    assert table_sorting_priority[174] == f"{kw.fact_lower}_otx"
    assert table_sorting_priority[175] == f"{kw.fact_lower}_inx"
    assert table_sorting_priority[176] == kw.fact_upper
    assert table_sorting_priority[177] == f"{kw.fact_upper}_otx"
    assert table_sorting_priority[178] == f"{kw.fact_upper}_inx"
    assert table_sorting_priority[179] == kw.fund_pool
    assert table_sorting_priority[180] == kw.give_force
    assert table_sorting_priority[181] == kw.poynt
    assert table_sorting_priority[182] == kw.max_tree_traverse
    assert table_sorting_priority[183] == kw.reason_lower
    assert table_sorting_priority[184] == f"{kw.reason_lower}_otx"
    assert table_sorting_priority[185] == f"{kw.reason_lower}_inx"
    assert table_sorting_priority[186] == kw.reason_upper
    assert table_sorting_priority[187] == f"{kw.reason_upper}_otx"
    assert table_sorting_priority[188] == f"{kw.reason_upper}_inx"
    assert table_sorting_priority[189] == kw.reason_divisor
    assert table_sorting_priority[190] == kw.pledge
    assert table_sorting_priority[191] == kw.problem_bool
    assert table_sorting_priority[192] == kw.take_force
    assert table_sorting_priority[193] == kw.fund_grain
    assert table_sorting_priority[194] == kw.mana_grain
    assert table_sorting_priority[195] == kw.respect_grain
    assert table_sorting_priority[196] == kw.amount
    assert table_sorting_priority[197] == kw.otx_label
    assert table_sorting_priority[198] == kw.inx_label
    assert table_sorting_priority[199] == kw.otx_rope
    assert table_sorting_priority[200] == kw.inx_rope
    assert table_sorting_priority[201] == kw.otx_name
    assert table_sorting_priority[202] == kw.inx_name
    assert table_sorting_priority[203] == kw.otx_title
    assert table_sorting_priority[204] == kw.inx_title
    assert table_sorting_priority[205] == kw.otx_knot
    assert table_sorting_priority[206] == kw.inx_knot
    assert table_sorting_priority[207] == kw.otx_time
    assert table_sorting_priority[208] == kw.inx_time
    assert table_sorting_priority[209] == "iux_name"
    assert table_sorting_priority[210] == "aux_name"
    assert table_sorting_priority[211] == "iux_title"
    assert table_sorting_priority[212] == "aux_title"
    assert table_sorting_priority[213] == "iux_label"
    assert table_sorting_priority[214] == "aux_label"
    assert table_sorting_priority[215] == "iux_rope"
    assert table_sorting_priority[216] == "aux_rope"
    assert table_sorting_priority[217] == "iux_knot"
    assert table_sorting_priority[218] == "aux_knot"
    assert table_sorting_priority[219] == kw.knot
    assert table_sorting_priority[220] == kw.groupmark
    assert table_sorting_priority[221] == kw.unknown_str
    assert table_sorting_priority[222] == kw.quota
    assert table_sorting_priority[223] == kw.celldepth
    assert table_sorting_priority[224] == kw.job_listen_rotations
    assert table_sorting_priority[225] == kw.error_message
    assert table_sorting_priority[226] == kw.person_name_is_workforce
    assert table_sorting_priority[227] == kw.plan_active
    assert table_sorting_priority[228] == kw.plan_task
    assert table_sorting_priority[229] == kw.case_task
    assert table_sorting_priority[230] == kw.reason_active
    assert table_sorting_priority[231] == kw.reason_task
    assert table_sorting_priority[232] == kw.case_active
    assert table_sorting_priority[233] == kw.credor_pool
    assert table_sorting_priority[234] == kw.debtor_pool
    assert table_sorting_priority[235] == kw.rational
    assert table_sorting_priority[236] == kw.fund_give
    assert table_sorting_priority[237] == kw.fund_take
    assert table_sorting_priority[238] == kw.fund_onset
    assert table_sorting_priority[239] == kw.fund_cease
    assert table_sorting_priority[240] == kw.fund_ratio
    assert table_sorting_priority[241] == kw.fund_agenda_give
    assert table_sorting_priority[242] == kw.fund_agenda_take
    assert table_sorting_priority[243] == kw.fund_agenda_ratio_give
    assert table_sorting_priority[244] == kw.fund_agenda_ratio_take
    assert table_sorting_priority[245] == kw.inallocable_contact_debt_mass
    assert table_sorting_priority[246] == kw.gogo_calc
    assert table_sorting_priority[247] == kw.stop_calc
    assert table_sorting_priority[248] == kw.tree_level
    assert table_sorting_priority[249] == kw.range_evaluated
    assert table_sorting_priority[250] == kw.descendant_pledge_count
    assert table_sorting_priority[251] == kw.healerunit_ratio
    assert table_sorting_priority[252] == kw.all_contact_cred
    assert table_sorting_priority[253] == kw.keeps_justified
    assert table_sorting_priority[254] == kw.offtrack_fund
    assert table_sorting_priority[255] == kw.parent_heir_active
    assert table_sorting_priority[256] == kw.irrational_contact_debt_mass
    assert table_sorting_priority[257] == kw.sum_healerunit_plans_fund_total
    assert table_sorting_priority[258] == kw.keeps_buildable
    assert table_sorting_priority[259] == kw.all_contact_debt
    assert table_sorting_priority[260] == kw.tree_traverse_count
    assert table_sorting_priority[261] == kw.net_funds
    assert table_sorting_priority[262] == kw.fund_rank
    assert table_sorting_priority[263] == kw.pledges_count
    assert table_sorting_priority[264] == f"context_plan_{kw.close}"
    assert table_sorting_priority[265] == f"context_plan_{kw.denom}"
    assert table_sorting_priority[266] == f"context_plan_{kw.morph}"
    assert table_sorting_priority[267] == kw.inx_epoch_diff

    assert len(table_sorting_priority) == 268
    all_args = copy_copy(atom_args)
    all_args.update(all_person_dimen_delete_keys)
    all_args.update(moment_args)
    all_args.update(person_calc_args)
    all_args.update(nabu_args)
    all_args.update(jargon_args)
    all_args.update(jargonable_otx_cols)
    all_args.update(jargonable_inx_cols)
    all_args.update(jargonable_delete_otx_cols)
    all_args.update(jargonable_delete_inx_cols)
    all_args.update(speech_args)
    all_args.update(speechable_iux_cols)
    all_args.update(speechable_aux_cols)
    all_args.update(speechable_delete_iux_cols)
    all_args.update(speechable_delete_aux_cols)
    all_args.update(nabuable_otx_cols)
    all_args.update(nabuable_inx_cols)
    all_args.update()
    all_args.add(kw.brick_type)
    all_args.add(kw.spark_num)
    all_args.add(kw.spark_face)
    all_args.add(kw.source_dimen)
    all_args.add(kw.jargon_spark_num)
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


def test_get_brick_sqlite_types_ReturnsObj():
    # ESTABLISH / WHEN
    sqlite_types = get_brick_sqlite_types()

    # THEN
    # for arg in sorted(get_keg_elements_sort_order()):
    #     sqlite_type = sqlite_types.get(arg)
    #     print(f""" "{arg}": "{sqlite_type}", """)

    for arg, sqlite_type in sqlite_types.items():
        print(f"""assert sqlite_types.get(kw.{arg}) == "{sqlite_type}" """)

    assert sqlite_types.get(kw.active_requisite) == "INTEGER"
    assert sqlite_types.get(kw.addin) == "REAL"
    assert sqlite_types.get(kw.all_contact_cred) == "INTEGER"
    assert sqlite_types.get(kw.all_contact_debt) == "INTEGER"
    assert sqlite_types.get(kw.amount) == "REAL"
    assert sqlite_types.get(kw.aux_knot) == "TEXT"
    assert sqlite_types.get(kw.aux_label) == "TEXT"
    assert sqlite_types.get(kw.aux_name) == "TEXT"
    assert sqlite_types.get(kw.aux_rope) == "TEXT"
    assert sqlite_types.get(kw.aux_title) == "TEXT"
    assert sqlite_types.get(kw.awardee_title) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_ERASE) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_aux) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_inx) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_iux) == "TEXT"
    assert sqlite_types.get(kw.awardee_title_otx) == "TEXT"
    assert sqlite_types.get(kw.begin) == "REAL"
    assert sqlite_types.get(kw.brick_type) == "TEXT"
    assert sqlite_types.get(kw.bud_time) == "INTEGER"
    assert sqlite_types.get(kw.bud_time_inx) == "INTEGER"
    assert sqlite_types.get(kw.bud_time_otx) == "INTEGER"
    assert sqlite_types.get(kw.c400_number) == "INTEGER"
    assert sqlite_types.get(kw.case_active) == "INTEGER"
    assert sqlite_types.get(kw.case_task) == "INTEGER"
    assert sqlite_types.get(kw.celldepth) == "INTEGER"
    assert sqlite_types.get(kw.close) == "REAL"
    assert sqlite_types.get(kw.contact_cred_mass) == "REAL"
    assert sqlite_types.get(kw.contact_debt_mass) == "REAL"
    assert sqlite_types.get(kw.contact_name) == "TEXT"
    assert sqlite_types.get(kw.contact_name_ERASE) == "TEXT"
    assert sqlite_types.get(kw.contact_name_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.contact_name_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.contact_name_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.contact_name_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.contact_name_aux) == "TEXT"
    assert sqlite_types.get(kw.contact_name_inx) == "TEXT"
    assert sqlite_types.get(kw.contact_name_iux) == "TEXT"
    assert sqlite_types.get(kw.contact_name_otx) == "TEXT"
    assert sqlite_types.get(kw.context_plan_close) == "REAL"
    assert sqlite_types.get(kw.context_plan_denom) == "REAL"
    assert sqlite_types.get(kw.context_plan_morph) == "REAL"
    assert sqlite_types.get(kw.credor_pool) == "REAL"
    assert sqlite_types.get(kw.credor_respect) == "REAL"
    assert sqlite_types.get(kw.cumulative_day) == "INTEGER"
    assert sqlite_types.get(kw.cumulative_minute) == "INTEGER"
    assert sqlite_types.get(kw.debtor_pool) == "REAL"
    assert sqlite_types.get(kw.debtor_respect) == "REAL"
    assert sqlite_types.get(kw.denom) == "INTEGER"
    assert sqlite_types.get(kw.descendant_pledge_count) == "INTEGER"
    assert sqlite_types.get(kw.epoch_label) == "TEXT"
    assert sqlite_types.get(kw.epoch_label_aux) == "TEXT"
    assert sqlite_types.get(kw.epoch_label_inx) == "TEXT"
    assert sqlite_types.get(kw.epoch_label_iux) == "TEXT"
    assert sqlite_types.get(kw.epoch_label_otx) == "TEXT"
    assert sqlite_types.get(kw.error_message) == "TEXT"
    assert sqlite_types.get(kw.fact_context) == "TEXT"
    assert sqlite_types.get(kw.fact_context_ERASE) == "TEXT"
    assert sqlite_types.get(kw.fact_context_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.fact_context_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.fact_context_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.fact_context_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.fact_context_aux) == "TEXT"
    assert sqlite_types.get(kw.fact_context_inx) == "TEXT"
    assert sqlite_types.get(kw.fact_context_iux) == "TEXT"
    assert sqlite_types.get(kw.fact_context_otx) == "TEXT"
    assert sqlite_types.get(kw.fact_lower) == "REAL"
    assert sqlite_types.get(kw.fact_lower_inx) == "REAL"
    assert sqlite_types.get(kw.fact_lower_otx) == "REAL"
    assert sqlite_types.get(kw.fact_state) == "TEXT"
    assert sqlite_types.get(kw.fact_state_aux) == "TEXT"
    assert sqlite_types.get(kw.fact_state_inx) == "TEXT"
    assert sqlite_types.get(kw.fact_state_iux) == "TEXT"
    assert sqlite_types.get(kw.fact_state_otx) == "TEXT"
    assert sqlite_types.get(kw.fact_upper) == "REAL"
    assert sqlite_types.get(kw.fact_upper_inx) == "REAL"
    assert sqlite_types.get(kw.fact_upper_otx) == "REAL"
    assert sqlite_types.get(kw.flare_audie_aux) == "TEXT"
    assert sqlite_types.get(kw.flare_audie_iux) == "TEXT"
    assert sqlite_types.get(kw.fund_agenda_give) == "REAL"
    assert sqlite_types.get(kw.fund_agenda_ratio_give) == "REAL"
    assert sqlite_types.get(kw.fund_agenda_ratio_take) == "REAL"
    assert sqlite_types.get(kw.fund_agenda_take) == "REAL"
    assert sqlite_types.get(kw.fund_cease) == "REAL"
    assert sqlite_types.get(kw.fund_give) == "REAL"
    assert sqlite_types.get(kw.fund_grain) == "REAL"
    assert sqlite_types.get(kw.fund_onset) == "REAL"
    assert sqlite_types.get(kw.fund_pool) == "REAL"
    assert sqlite_types.get(kw.fund_rank) == "INTEGER"
    assert sqlite_types.get(kw.fund_ratio) == "REAL"
    assert sqlite_types.get(kw.fund_take) == "REAL"
    assert sqlite_types.get(kw.give_force) == "REAL"
    assert sqlite_types.get(kw.gogo_calc) == "REAL"
    assert sqlite_types.get(kw.gogo_want) == "REAL"
    assert sqlite_types.get(kw.group_cred_mass) == "REAL"
    assert sqlite_types.get(kw.group_debt_mass) == "REAL"
    assert sqlite_types.get(kw.group_title) == "TEXT"
    assert sqlite_types.get(kw.group_title_ERASE) == "TEXT"
    assert sqlite_types.get(kw.group_title_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.group_title_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.group_title_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.group_title_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.group_title_aux) == "TEXT"
    assert sqlite_types.get(kw.group_title_inx) == "TEXT"
    assert sqlite_types.get(kw.group_title_iux) == "TEXT"
    assert sqlite_types.get(kw.group_title_otx) == "TEXT"
    assert sqlite_types.get(kw.groupmark) == "TEXT"
    assert sqlite_types.get(kw.healer_name) == "TEXT"
    assert sqlite_types.get(kw.healer_name_ERASE) == "TEXT"
    assert sqlite_types.get(kw.healer_name_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.healer_name_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.healer_name_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.healer_name_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.healer_name_aux) == "TEXT"
    assert sqlite_types.get(kw.healer_name_inx) == "TEXT"
    assert sqlite_types.get(kw.healer_name_iux) == "TEXT"
    assert sqlite_types.get(kw.healer_name_otx) == "TEXT"
    assert sqlite_types.get(kw.healerunit_ratio) == "REAL"
    assert sqlite_types.get(kw.hour_label) == "TEXT"
    assert sqlite_types.get(kw.hour_label_aux) == "TEXT"
    assert sqlite_types.get(kw.hour_label_inx) == "TEXT"
    assert sqlite_types.get(kw.hour_label_iux) == "TEXT"
    assert sqlite_types.get(kw.hour_label_otx) == "TEXT"
    assert sqlite_types.get(kw.inallocable_contact_debt_mass) == "REAL"
    assert sqlite_types.get(kw.inx_epoch_diff) == "INTEGER"
    assert sqlite_types.get(kw.inx_knot) == "TEXT"
    assert sqlite_types.get(kw.inx_label) == "TEXT"
    assert sqlite_types.get(kw.inx_name) == "TEXT"
    assert sqlite_types.get(kw.inx_rope) == "TEXT"
    assert sqlite_types.get(kw.inx_time) == "INTEGER"
    assert sqlite_types.get(kw.inx_title) == "TEXT"
    assert sqlite_types.get(kw.irrational_contact_debt_mass) == "REAL"
    assert sqlite_types.get(kw.iux_knot) == "TEXT"
    assert sqlite_types.get(kw.iux_label) == "TEXT"
    assert sqlite_types.get(kw.iux_name) == "TEXT"
    assert sqlite_types.get(kw.iux_rope) == "TEXT"
    assert sqlite_types.get(kw.iux_title) == "TEXT"
    assert sqlite_types.get(kw.jargon_spark_num) == "INTEGER"
    assert sqlite_types.get(kw.job_listen_rotations) == "INTEGER"
    assert sqlite_types.get(kw.keeps_buildable) == "INTEGER"
    assert sqlite_types.get(kw.keeps_justified) == "INTEGER"
    assert sqlite_types.get(kw.knot) == "TEXT"
    assert sqlite_types.get(kw.labor_title) == "TEXT"
    assert sqlite_types.get(kw.labor_title_ERASE) == "TEXT"
    assert sqlite_types.get(kw.labor_title_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.labor_title_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.labor_title_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.labor_title_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.labor_title_aux) == "TEXT"
    assert sqlite_types.get(kw.labor_title_inx) == "TEXT"
    assert sqlite_types.get(kw.labor_title_iux) == "TEXT"
    assert sqlite_types.get(kw.labor_title_otx) == "TEXT"
    assert sqlite_types.get(kw.mana_grain) == "REAL"
    assert sqlite_types.get(kw.max_tree_traverse) == "INTEGER"
    assert sqlite_types.get(kw.moment_rope) == "TEXT"
    assert sqlite_types.get(kw.moment_rope_aux) == "TEXT"
    assert sqlite_types.get(kw.moment_rope_inx) == "TEXT"
    assert sqlite_types.get(kw.moment_rope_iux) == "TEXT"
    assert sqlite_types.get(kw.moment_rope_otx) == "TEXT"
    assert sqlite_types.get(kw.month_label) == "TEXT"
    assert sqlite_types.get(kw.month_label_aux) == "TEXT"
    assert sqlite_types.get(kw.month_label_inx) == "TEXT"
    assert sqlite_types.get(kw.month_label_iux) == "TEXT"
    assert sqlite_types.get(kw.month_label_otx) == "TEXT"
    assert sqlite_types.get(kw.monthday_index) == "INTEGER"
    assert sqlite_types.get(kw.morph) == "INTEGER"
    assert sqlite_types.get(kw.net_funds) == "REAL"
    assert sqlite_types.get(kw.numor) == "INTEGER"
    assert sqlite_types.get(kw.offi_time) == "INTEGER"
    assert sqlite_types.get(kw.offi_time_inx) == "INTEGER"
    assert sqlite_types.get(kw.offi_time_otx) == "INTEGER"
    assert sqlite_types.get(kw.offtrack_fund) == "REAL"
    assert sqlite_types.get(kw.otx_knot) == "TEXT"
    assert sqlite_types.get(kw.otx_label) == "TEXT"
    assert sqlite_types.get(kw.otx_name) == "TEXT"
    assert sqlite_types.get(kw.otx_rope) == "TEXT"
    assert sqlite_types.get(kw.otx_time) == "INTEGER"
    assert sqlite_types.get(kw.otx_title) == "TEXT"
    assert sqlite_types.get(kw.parent_heir_active) == "INTEGER"
    assert sqlite_types.get(kw.person_name) == "TEXT"
    assert sqlite_types.get(kw.person_name_ERASE) == "TEXT"
    assert sqlite_types.get(kw.person_name_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.person_name_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.person_name_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.person_name_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.person_name_aux) == "TEXT"
    assert sqlite_types.get(kw.person_name_inx) == "TEXT"
    assert sqlite_types.get(kw.person_name_is_workforce) == "INTEGER"
    assert sqlite_types.get(kw.person_name_iux) == "TEXT"
    assert sqlite_types.get(kw.person_name_otx) == "TEXT"
    assert sqlite_types.get(kw.plan_active) == "INTEGER"
    assert sqlite_types.get(kw.plan_rope) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_ERASE) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_aux) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_inx) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_iux) == "TEXT"
    assert sqlite_types.get(kw.plan_rope_otx) == "TEXT"
    assert sqlite_types.get(kw.plan_task) == "INTEGER"
    assert sqlite_types.get(kw.pledge) == "INTEGER"
    assert sqlite_types.get(kw.pledges_count) == "INTEGER"
    assert sqlite_types.get(kw.poynt) == "INTEGER"
    assert sqlite_types.get(kw.problem_bool) == "INTEGER"
    assert sqlite_types.get(kw.quota) == "REAL"
    assert sqlite_types.get(kw.range_evaluated) == "INTEGER"
    assert sqlite_types.get(kw.rational) == "INTEGER"
    assert sqlite_types.get(kw.reason_active) == "INTEGER"
    assert sqlite_types.get(kw.reason_context) == "TEXT"
    assert sqlite_types.get(kw.reason_context_ERASE) == "TEXT"
    assert sqlite_types.get(kw.reason_context_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.reason_context_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.reason_context_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.reason_context_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.reason_context_aux) == "TEXT"
    assert sqlite_types.get(kw.reason_context_inx) == "TEXT"
    assert sqlite_types.get(kw.reason_context_iux) == "TEXT"
    assert sqlite_types.get(kw.reason_context_otx) == "TEXT"
    assert sqlite_types.get(kw.reason_divisor) == "INTEGER"
    assert sqlite_types.get(kw.reason_lower) == "REAL"
    assert sqlite_types.get(kw.reason_lower_inx) == "REAL"
    assert sqlite_types.get(kw.reason_lower_otx) == "REAL"
    assert sqlite_types.get(kw.reason_state) == "TEXT"
    assert sqlite_types.get(kw.reason_state_ERASE) == "TEXT"
    assert sqlite_types.get(kw.reason_state_ERASE_aux) == "TEXT"
    assert sqlite_types.get(kw.reason_state_ERASE_inx) == "TEXT"
    assert sqlite_types.get(kw.reason_state_ERASE_iux) == "TEXT"
    assert sqlite_types.get(kw.reason_state_ERASE_otx) == "TEXT"
    assert sqlite_types.get(kw.reason_state_aux) == "TEXT"
    assert sqlite_types.get(kw.reason_state_inx) == "TEXT"
    assert sqlite_types.get(kw.reason_state_iux) == "TEXT"
    assert sqlite_types.get(kw.reason_state_otx) == "TEXT"
    assert sqlite_types.get(kw.reason_task) == "INTEGER"
    assert sqlite_types.get(kw.reason_upper) == "REAL"
    assert sqlite_types.get(kw.reason_upper_inx) == "REAL"
    assert sqlite_types.get(kw.reason_upper_otx) == "REAL"
    assert sqlite_types.get(kw.respect_grain) == "REAL"
    assert sqlite_types.get(kw.solo) == "INTEGER"
    assert sqlite_types.get(kw.source_dimen) == "TEXT"
    assert sqlite_types.get(kw.spark_face) == "TEXT"
    assert sqlite_types.get(kw.spark_face_inx) == "TEXT"
    assert sqlite_types.get(kw.spark_face_otx) == "TEXT"
    assert sqlite_types.get(kw.spark_num) == "INTEGER"
    assert sqlite_types.get(kw.stop_calc) == "REAL"
    assert sqlite_types.get(kw.stop_want) == "REAL"
    assert sqlite_types.get(kw.sum_healerunit_plans_fund_total) == "REAL"
    assert sqlite_types.get(kw.take_force) == "REAL"
    assert sqlite_types.get(kw.tran_time) == "INTEGER"
    assert sqlite_types.get(kw.tran_time_inx) == "INTEGER"
    assert sqlite_types.get(kw.tran_time_otx) == "INTEGER"
    assert sqlite_types.get(kw.tree_level) == "INTEGER"
    assert sqlite_types.get(kw.tree_traverse_count) == "INTEGER"
    assert sqlite_types.get(kw.unknown_str) == "TEXT"
    assert sqlite_types.get(kw.weekday_label) == "TEXT"
    assert sqlite_types.get(kw.weekday_label_aux) == "TEXT"
    assert sqlite_types.get(kw.weekday_label_inx) == "TEXT"
    assert sqlite_types.get(kw.weekday_label_iux) == "TEXT"
    assert sqlite_types.get(kw.weekday_label_otx) == "TEXT"
    assert sqlite_types.get(kw.weekday_order) == "INTEGER"
    assert sqlite_types.get(kw.world_name) == "TEXT"
    assert sqlite_types.get(kw.yr1_jan1_offset) == "INTEGER"

    # sourcery skip: no-loop-in-tests
    for x_arg, datatype in get_person_calc_args_sqlite_datatype_dict().items():
        # print(f"{x_arg=} {datatype=} {sqlite_types.get(x_arg)=}")
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


def test_brick_config_path_ReturnsObj_Brick() -> str:
    # ESTABLISH / WHEN / THEN
    chapter_dir = create_path(kw.src, "ch20_brick")
    assert brick_config_path() == create_path(chapter_dir, "brick_config.json")


def test_brick_config_UsesAliasedImport():
    # ESTABLISH the ch20_brick.brick_config module
    from ch20_brick import brick_config as brick_config_module

    # WHEN we inspect the module's namespace
    # THEN os_path_exists must exist as an attribute and must be os.path.exists
    from os.path import exists as os_path_exists

    assert hasattr(brick_config_module, "os_path_exists"), (
        "ch20_brick.brick_config does not import exists as os_path_exists.\n"
        "  The mock in test_brick_config_path_UsesModuleRelativePathWhenSrcUnavailable\n"
        "  will not work without this exact import alias."
    )
    assert brick_config_module.os_path_exists is os_path_exists, (
        "os_path_exists in ch20_brick.brick_config is not os.path.exists.\n"
        "  It may have been reassigned or imported incorrectly."
    )


def test_brick_config_path_UsesModuleRelativePathWhenSrcUnavailable():
    # ESTABLISH os_path_exists returns False (simulates pip install environment)
    with mock_patch("ch20_brick.brick_config.os_path_exists", return_value=False):

        # WHEN brick_config_path is called without src/ available
        path = pathlib_Path(brick_config_path()).resolve()

    # THEN path must be relative to the module file, not the cwd src/ path
    from ch20_brick import brick_config as brick_config_module

    expected = (
        pathlib_Path(brick_config_module.__file__).resolve().parent
        / "brick_config.json"
    )

    assert path == expected, (
        f"returned : {path}\n"
        f"expected : {expected}\n"
        f"  The Path(__file__) backup is not being used."
    )
    assert path.exists(), f"Backup path does not exist: '{path}'"


def test_get_brick_config_dict_ReturnsObj_Scenario0_IsFullyPopulated():
    # ESTABLISH / WHEN
    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config
    brick_config_dimens = set(x_brick_config.keys())
    assert kw.momentunit in brick_config_dimens
    assert kw.moment_budunit in brick_config_dimens
    assert kw.moment_ceckbook in brick_config_dimens
    assert kw.moment_epoch_hour in brick_config_dimens
    assert kw.moment_epoch_month in brick_config_dimens
    assert kw.moment_epoch_weekday in brick_config_dimens
    assert kw.moment_timeoffi in brick_config_dimens
    assert kw.person_contact_membership in brick_config_dimens
    assert kw.person_contactunit in brick_config_dimens
    assert kw.person_plan_awardunit in brick_config_dimens
    assert kw.person_plan_factunit in brick_config_dimens
    assert kw.person_plan_laborunit in brick_config_dimens
    assert kw.person_plan_healerunit in brick_config_dimens
    assert kw.person_plan_reason_caseunit in brick_config_dimens
    assert kw.person_plan_reasonunit in brick_config_dimens
    assert kw.person_planunit in brick_config_dimens
    assert kw.personunit in brick_config_dimens
    assert kw.nabu_timenum in brick_config_dimens
    assert kw.jargon_name in brick_config_dimens
    assert kw.jargon_title in brick_config_dimens
    assert kw.jargon_label in brick_config_dimens
    assert kw.jargon_rope in brick_config_dimens
    assert get_person_dimens().issubset(brick_config_dimens)
    assert get_moment_dimens().issubset(brick_config_dimens)
    assert get_nabu_dimens().issubset(brick_config_dimens)
    assert get_jargon_dimens().issubset(brick_config_dimens)
    gen_all_dimens = get_person_dimens()
    gen_all_dimens.update(get_moment_dimens())
    gen_all_dimens.update(get_nabu_dimens())
    gen_all_dimens.update(get_jargon_dimens())
    assert gen_all_dimens == brick_config_dimens
    assert len(x_brick_config) == 22
    _validate_brick_config(x_brick_config)


def get_brick_categorys():
    return {kw.person, kw.moment, kw.jargon, kw.nabu}


def _validate_brick_config(x_brick_config: dict):
    # sourcery skip: low-code-quality
    atom_config_dict = get_atom_config_dict()
    moment_config_dict = get_moment_config_dict()
    nabu_config_dict = get_nabu_config_dict()
    jargon_config_dict = get_jargon_config_dict()
    # for every brick_format file there exists a unique brick_type with leading zeros to make 5 digits
    for brick_dimen, brick_dict in x_brick_config.items():
        print(f"{brick_dimen=}")
        assert brick_dict.get(kw.brick_category) in get_brick_categorys()
        assert brick_dict.get(kw.jkeys) is not None
        assert brick_dict.get(kw.jvalues) is not None
        assert brick_dict.get(kw.allowed_crud) is not None
        assert brick_dict.get(kw.UPDATE) is None
        assert brick_dict.get(kw.INSERT) is None
        assert brick_dict.get(kw.DELETE) is None
        assert brick_dict.get(kw.normal_specs) is None
        if brick_dict.get(kw.brick_category) == kw.person:
            sub_dimen = atom_config_dict.get(brick_dimen)
        elif brick_dict.get(kw.brick_category) == kw.moment:
            sub_dimen = moment_config_dict.get(brick_dimen)
        elif brick_dict.get(kw.brick_category) == kw.nabu:
            sub_dimen = nabu_config_dict.get(brick_dimen)
        elif brick_dict.get(kw.brick_category) == kw.jargon:
            sub_dimen = jargon_config_dict.get(brick_dimen)

        assert brick_dict.get(kw.allowed_crud) in get_allowed_curds()

        UPDATE_dimen = sub_dimen.get(kw.UPDATE)
        INSERT_dimen = sub_dimen.get(kw.INSERT)
        DELETE_dimen = sub_dimen.get(kw.DELETE)
        brick_allowed_crud = brick_dict.get(kw.allowed_crud)
        # print(
        #     f"{brick_dimen=} {UPDATE_dimen} {INSERT_dimen} {DELETE_dimen=} {brick_allowed_crud=}"
        # )
        if brick_dimen in {
            kw.moment_epoch_hour,
            kw.moment_epoch_month,
            kw.moment_epoch_weekday,
            kw.momentunit,
            "map_otx2inx",
            kw.nabu_timenum,
            kw.jargon_title,
            kw.jargon_name,
            kw.jargon_label,
            kw.jargon_rope,
        }:
            assert brick_allowed_crud == kw.insert_one_time
        elif brick_dimen in {kw.moment_budunit, kw.moment_ceckbook, kw.moment_timeoffi}:
            assert brick_allowed_crud == kw.insert_multiple
        elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen != None:
            assert brick_allowed_crud == kw.delete_insert_update
        elif UPDATE_dimen != None and INSERT_dimen != None and DELETE_dimen is None:
            assert brick_allowed_crud == kw.insert_update
        elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen != None:
            assert brick_allowed_crud == kw.delete_insert
        elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen != None:
            assert brick_allowed_crud == kw.delete_update
        elif UPDATE_dimen != None and INSERT_dimen is None and DELETE_dimen is None:
            assert brick_allowed_crud == kw.UPDATE
        elif UPDATE_dimen is None and INSERT_dimen != None and DELETE_dimen is None:
            assert brick_allowed_crud == kw.INSERT
        elif UPDATE_dimen is None and INSERT_dimen is None and DELETE_dimen != None:
            assert brick_allowed_crud == kw.DELETE
        else:
            assert brick_allowed_crud == f"{kw.allowed_crud} not checked by test"

        sub_jkeys_keys = set(sub_dimen.get(kw.jkeys).keys())
        brick_jkeys_keys = set(brick_dict.get(kw.jkeys).keys())
        # print(f"   {sub_jkeys_keys=}")
        # print(f"  {brick_jkeys_keys=}")
        assert kw.spark_face in brick_jkeys_keys
        assert kw.spark_num in brick_jkeys_keys
        if brick_dict.get(kw.brick_category) in {kw.person} and kw.plan in brick_dimen:
            assert kw.moment_rope not in brick_jkeys_keys, brick_dimen
        elif brick_dict.get(kw.brick_category) in {kw.moment, kw.person}:
            assert kw.moment_rope in brick_jkeys_keys
            # print(f"2{brick_dimen=}")
            if brick_dict.get(kw.brick_category) in {kw.person}:
                brick_jkeys_keys.remove(kw.moment_rope)
        if brick_dict.get(kw.brick_category) in {kw.person}:
            brick_jkeys_keys.remove(kw.person_name)
        brick_jkeys_keys.remove(kw.spark_face)
        brick_jkeys_keys.remove(kw.spark_num)
        assertion_failure_str = f"{brick_dimen=} {sub_jkeys_keys=} {brick_jkeys_keys=}"
        assert sub_jkeys_keys == brick_jkeys_keys, assertion_failure_str

        expected_jvalues_keys = set(sub_dimen.get(kw.jvalues).keys())
        # all moment and plan dimen must have knot jvalue because they all have rope keys
        if brick_dict.get(kw.brick_category) in {kw.moment, kw.person}:
            expected_jvalues_keys.add(kw.knot)
        # print(f"{brick_dimen=}")
        # if kw.moment_rope in expected_jvalues_keys:
        #     expected_jvalues_keys.remove(kw.moment_rope)

        brick_jvalues_dict = brick_dict.get(kw.jvalues)
        brick_jvalues_keys = set(brick_jvalues_dict.keys())
        # print(f" {expected_jvalues_keys=}")
        # print(f"{brick_jvalues_keys=}")
        assert expected_jvalues_keys == brick_jvalues_keys


def test_get_brick_format_filenames_ReturnsObj_CheckSome_brick_format_filesnames_Exist():
    # ESTABLISH
    brick_filenames_set = get_brick_format_filenames()

    # WHEN / THEN
    ifx = BrickFormatsEnum
    assert ifx.bk00121_person_contactunit_v0_0_0 in brick_filenames_set
    assert ifx.bk00120_person_contact_membership_v0_0_0 in brick_filenames_set
    assert ifx.bk00002_planunit_v0_0_0 in brick_filenames_set


def change_erase_attrs(brick_attrs: set):
    brick_attrs_list = get_default_sorted_list(brick_attrs)
    if brick_attrs_list[-1].find("_ERASE") > 0:
        delete_attr_with_erase = brick_attrs_list[-1]
        delete_attr_without_erase = delete_attr_with_erase.replace("_ERASE", "")
        brick_attrs.remove(delete_attr_with_erase)
        brick_attrs.add(delete_attr_without_erase)


def test_get_brick_format_filenames_ReturnsObj_Validate_brick_format_files():
    # sourcery skip:  no-conditionals-in-tests
    # ESTABLISH / WHEN
    brick_filenames_sorted = list(get_brick_format_filenames())

    # THEN
    brick_filenames_sorted.sort(key=lambda x: x)
    print(f"{len(brick_filenames_sorted)=}")

    all_dimen_keys_dict = {
        dimen: set(dict.get(kw.jkeys).keys())
        for dimen, dict in get_brick_config_dict().items()
    }

    valid_brick_dimens = set()
    valid_brick_dimens.update(get_person_dimens())
    valid_brick_dimens.update(get_moment_dimens())
    valid_brick_dimens.update(get_nabu_dimens())
    valid_brick_dimens.update(get_jargon_dimens())
    print("get_brick_config_dict")
    config_dict = get_brick_config_dict()

    # for every brick_format file there exists a unique brick_type with leading zeros to make 5 digits
    brick_types_set = set()
    for brick_filename in brick_filenames_sorted:
        ref_dict = get_brickref_from_file(brick_filename)
        # print(f"{brick_filename=} {ref_dict.get(kw.brick_type)=}")
        brick_type_value = ref_dict.get(kw.brick_type)
        assert brick_type_value
        assert brick_type_value[2:8] == brick_filename[2:7]
        brick_types_set.add(brick_type_value)

        format_dimens = ref_dict.get(kw.dimens)
        assert format_dimens is not None
        assert len(format_dimens) > 0
        for brick_format_dimen in format_dimens:
            assert brick_format_dimen in valid_brick_dimens

        assert ref_dict.get(kw.attributes)
        brick_format_attributes = ref_dict.get(kw.attributes)
        for brick_attribute, attr_dict in brick_format_attributes.items():
            # print(f"{brick_attribute=}")
            assert kw.otx_key in set(attr_dict.keys())
            otx_key_value = attr_dict.get(kw.otx_key)
            for brick_format_dimen in format_dimens:
                format_config = config_dict.get(brick_format_dimen)
                dimen_required_attrs = set(format_config.get(kw.jkeys).keys())
                dimen_optional_attrs = set(format_config.get(kw.jvalues).keys())
                attr_in_required = brick_attribute in dimen_required_attrs
                attr_in_optional = brick_attribute in dimen_optional_attrs
                attr_in_keys = attr_in_required or attr_in_optional
                assert_fail_str = (
                    f"{brick_format_dimen=} {brick_attribute=} {otx_key_value=}"
                )
                if attr_in_keys and otx_key_value:
                    assert attr_in_required, assert_fail_str
                elif attr_in_keys:
                    assert attr_in_optional, assert_fail_str
        # check all implied dimens are there
        brick_attrs = set(ref_dict.get(kw.attributes).keys())
        change_erase_attrs(brick_attrs)

        for x_dimen, dimen_keys in all_dimen_keys_dict.items():
            # if x_dimen == kw.person_plan_factunit and x_dimen in format_dimens:
            #     print(f"{brick_type_value}  {x_dimen=} {brick_attrs_list=}")
            if dimen_keys.issubset(brick_attrs):
                if x_dimen not in format_dimens:
                    print(f"MISSING {x_dimen=} {brick_type_value} {brick_attrs=}")
                assert x_dimen in format_dimens
            else:
                # dimen_keys_list = get_default_sorted_list(dimen_keys)
                #     brick_attrs_list[-1] = brick_attrs_list[-1].removesuffix("_ERASE")
                #     brick_attrs = set(brick_attrs_list)
                if x_dimen in format_dimens:
                    print(
                        f"SHOULDNT BE {x_dimen=} {brick_type_value} : {get_default_sorted_list(brick_attrs)}"
                    )
                    # print(
                    #     f"SHOULDNT BE {x_dimen=} {brick_type_value} : {get_default_sorted_list(dimen_keys)}"
                    # )
                assert x_dimen not in format_dimens

    # assert kw.spark_face in brick_format_attributes
    # assert kw.spark_num in brick_format_attributes

    # confirm every bricknumber is unique
    assert len(brick_types_set) == len(brick_filenames_sorted)
    assert brick_types_set == get_brick_types()


def test_get_brick_format_filename_ReturnsObj():
    # ESTABLISH
    bk00121_str = "bk00121"
    bk00120_str = "bk00120"
    bk00002_str = "bk00002"

    # WHEN
    bk00121_filename = get_brick_format_filename(bk00121_str)
    bk00120_filename = get_brick_format_filename(bk00120_str)
    bk00002_filename = get_brick_format_filename(bk00002_str)

    # THEN
    ifx = BrickFormatsEnum
    assert bk00121_filename == ifx.bk00121_person_contactunit_v0_0_0
    assert bk00120_filename == ifx.bk00120_person_contact_membership_v0_0_0
    assert bk00002_filename == ifx.bk00002_planunit_v0_0_0

    all_set = {
        get_brick_format_filename(brick_type) for brick_type in get_brick_types()
    }
    assert all_set == get_brick_format_filenames()


def set_brick_config_json(dimen: str, build_order: int):
    x_brick_config = get_brick_config_dict()
    dimen_dict = x_brick_config.get(dimen)
    dimen_dict[kw.build_order] = build_order
    x_brick_config[dimen] = dimen_dict
    save_json(brick_config_path(), None, x_brick_config)


def test_get_brick_config_dict_ReturnsObj_Scenario1_Check_build_order():
    # ESTABLISH / WHEN
    bo = kw.build_order
    # set_brick_config_json(kw.jargon_name, 0)
    # set_brick_config_json(kw.jargon_title, 1)
    # set_brick_config_json(kw.jargon_label, 2)
    # set_brick_config_json(kw.jargon_rope, 3)
    # set_brick_config_json(kw.momentunit, 5)
    # set_brick_config_json(kw.moment_epoch_hour, 6)
    # set_brick_config_json(kw.moment_epoch_month, 7)
    # set_brick_config_json(kw.moment_epoch_weekday, 8)
    # set_brick_config_json(kw.person_contact_membership, 9)
    # set_brick_config_json(kw.person_contactunit, 10)
    # set_brick_config_json(kw.person_plan_awardunit, 11)
    # set_brick_config_json(kw.person_plan_factunit, 12)
    # set_brick_config_json(kw.person_plan_laborunit, 14)
    # set_brick_config_json(kw.person_plan_healerunit, 15)
    # set_brick_config_json(kw.person_plan_reason_caseunit, 16)
    # set_brick_config_json(kw.person_plan_reasonunit, 17)
    # set_brick_config_json(kw.person_planunit, 18)
    # set_brick_config_json(kw.personunit, 19)
    # set_brick_config_json(kw.moment_budunit, 20)
    # set_brick_config_json(kw.moment_ceckbook, 21)

    x_brick_config = get_brick_config_dict()

    # THEN
    assert x_brick_config.get(kw.jargon_name).get(bo) == 0
    assert x_brick_config.get(kw.jargon_title).get(bo) == 1
    assert x_brick_config.get(kw.jargon_label).get(bo) == 2
    assert x_brick_config.get(kw.jargon_rope).get(bo) == 3
    assert x_brick_config.get(kw.nabu_timenum).get(bo) == 4
    assert x_brick_config.get(kw.momentunit).get(bo) == 5
    assert x_brick_config.get(kw.moment_epoch_hour).get(bo) == 6
    assert x_brick_config.get(kw.moment_epoch_month).get(bo) == 7
    assert x_brick_config.get(kw.moment_epoch_weekday).get(bo) == 8
    assert x_brick_config.get(kw.person_contact_membership).get(bo) == 9
    assert x_brick_config.get(kw.person_contactunit).get(bo) == 10
    assert x_brick_config.get(kw.person_plan_awardunit).get(bo) == 11
    assert x_brick_config.get(kw.person_plan_factunit).get(bo) == 12
    assert x_brick_config.get(kw.person_plan_laborunit).get(bo) == 14
    assert x_brick_config.get(kw.person_plan_healerunit).get(bo) == 15
    assert x_brick_config.get(kw.person_plan_reason_caseunit).get(bo) == 16
    assert x_brick_config.get(kw.person_plan_reasonunit).get(bo) == 17
    assert x_brick_config.get(kw.person_planunit).get(bo) == 18
    assert x_brick_config.get(kw.personunit).get(bo) == 19
    assert x_brick_config.get(kw.moment_budunit).get(bo) == 20
    assert x_brick_config.get(kw.moment_ceckbook).get(bo) == 21
    assert x_brick_config.get(kw.moment_timeoffi).get(bo) == 22
    builder_order_dict = {}
    for dimen_key, dimen_dict in x_brick_config.items():
        dimen_builder_order = dimen_dict.get(bo)
        assert dimen_builder_order is not None
        print(
            f"{dimen_key:30} build order: {dimen_builder_order:2} {sorted(builder_order_dict.keys())=}"
        )
        assert not builder_order_dict.get(dimen_builder_order)
        builder_order_dict[dimen_builder_order] = dimen_key
    print(f"{sorted(builder_order_dict.keys())=}")


def test_get_brick_config_dict_ReturnsObj_Scenario2_Person():
    # ESTABLISH / WHEN
    person_brick_config = get_brick_config_dict(kw.person)

    # THEN
    assert not person_brick_config.get(kw.jargon_name)
    assert not person_brick_config.get(kw.jargon_title)
    assert not person_brick_config.get(kw.jargon_label)
    assert not person_brick_config.get(kw.jargon_rope)
    assert not person_brick_config.get(kw.nabu_timenum)
    assert not person_brick_config.get(kw.momentunit)
    assert not person_brick_config.get(kw.moment_epoch_hour)
    assert not person_brick_config.get(kw.moment_epoch_month)
    assert not person_brick_config.get(kw.moment_epoch_weekday)
    assert person_brick_config.get(kw.person_contact_membership)
    assert person_brick_config.get(kw.person_contactunit)
    assert person_brick_config.get(kw.person_plan_awardunit)
    assert person_brick_config.get(kw.person_plan_factunit)
    assert person_brick_config.get(kw.person_plan_laborunit)
    assert person_brick_config.get(kw.person_plan_healerunit)
    assert person_brick_config.get(kw.person_plan_reason_caseunit)
    assert person_brick_config.get(kw.person_plan_reasonunit)
    assert person_brick_config.get(kw.person_planunit)
    assert person_brick_config.get(kw.personunit)
    assert not person_brick_config.get(kw.moment_budunit)
    assert not person_brick_config.get(kw.moment_ceckbook)
    assert not person_brick_config.get(kw.moment_timeoffi)


def test_get_brick_config_dict_ReturnsObj_Scenario3_CountDimens():
    # ESTABLISH / WHEN / THEN
    assert len(get_brick_config_dict(brick_categorys={kw.person})) == 10
    assert len(get_brick_config_dict(brick_categorys={kw.moment})) == 7
    assert len(get_brick_config_dict(brick_categorys={kw.nabu})) == 1
    assert len(get_brick_config_dict(brick_categorys={kw.jargon})) == 4
    assert len(get_brick_config_dict({kw.nabu, kw.jargon})) == 5


def test_get_quick_bricks_column_ref_ReturnsObj():
    # ESTABLISH / WHEN
    x_brick_quick_column_ref = get_quick_bricks_column_ref()

    # THEN
    assert len(x_brick_quick_column_ref) == len(get_brick_types())
    assert x_brick_quick_column_ref.get("bk00100") == {
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


def _create_expected_brick_dimen_ref() -> dict[str, list[str]]:
    brick_types_sorted = list(get_brick_types())
    brick_types_sorted.sort(key=lambda x: x)
    expected_brick_dimen_ref = {}
    for brick_type in brick_types_sorted:
        brick_format_filename = get_brick_format_filename(brick_type)
        x_brickref = get_brickref_from_file(brick_format_filename)
        dimens_list = x_brickref.get(kw.dimens)
        for x_dimen in dimens_list:
            if expected_brick_dimen_ref.get(x_dimen) is None:
                expected_brick_dimen_ref[x_dimen] = {brick_type}
            else:
                expected_brick_dimen_ref.get(x_dimen).add(brick_type)
    return expected_brick_dimen_ref


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


def test_get_brick_dimen_ref_ReturnsObj():
    # ESTABLISH
    expected_brick_dimen_ref = _create_expected_brick_dimen_ref()
    # print(f"{expected_brick_dimen_ref=}")
    print_sorted(normalize_obj(expected_brick_dimen_ref))

    # WHEN / THEN
    assert get_brick_dimen_ref() == expected_brick_dimen_ref


def test_get_dimens_with_brick_element_ReturnsObj_Scenario0_offi_time():
    # ESTABLISH / WHEN / THEN
    assert get_dimens_with_brick_element(kw.offi_time) == {kw.moment_timeoffi}
