from ch00_py.dict_toolbox import get_empty_str_if_None as if_none_str
from ch07_person_logic.person_main import PersonUnit
from ch14_moment.moment_main import MomentUnit
from ch17_idea._ref.ch17_semantic_types import FaceName, KnotTerm, MomentRope
from ch17_idea.idea_config import get_idea_format_filename, get_idea_format_headers


def create_init_belief_idea_csv_strs() -> dict[str, str]:
    """Returns strings of csv headers with comma delimiter"""
    belief_idea_types = [
        "ii00100",
        "ii00101",
        "ii00102",
        "ii00103",
        "ii00104",
        "ii00105",
        # "ii00106",
        "ii00120",
        "ii00121",
        "ii00122",
        "ii00123",
        "ii00124",
        "ii00125",
        "ii00126",
        "ii00127",
        "ii00128",
        "ii00129",
        "ii00142",
        "ii00143",
        "ii00144",
        "ii00145",
    ]
    idea_format_headers = get_idea_format_headers()

    moment_csv_strs = {}
    for idea_type in belief_idea_types:
        idea_format_filename = get_idea_format_filename(idea_type)
        for idea_columns, idea_filename in idea_format_headers.items():
            if idea_filename == idea_format_filename:
                moment_csv_strs[idea_type] = f"spark_num,spark_face,{idea_columns}\n"
    return moment_csv_strs


def add_momentunits_to_belief_csv_strs(
    moments_dict: dict[MomentRope, MomentUnit],
    moment_csv_strs: dict[str, str],
    csv_delimiter: str,
):
    for x_moment in moments_dict.values():
        add_momentunit_to_belief_csv_strs(x_moment, moment_csv_strs, csv_delimiter)


def add_momentunit_to_belief_csv_strs(
    x_moment: MomentUnit, moment_csv_strs: dict[str, str], csv_delimiter: str
) -> dict[str, str]:
    ii00100_csv = moment_csv_strs.get("ii00100")
    ii00101_csv = moment_csv_strs.get("ii00101")
    ii00102_csv = moment_csv_strs.get("ii00102")
    ii00103_csv = moment_csv_strs.get("ii00103")
    ii00104_csv = moment_csv_strs.get("ii00104")
    ii00105_csv = moment_csv_strs.get("ii00105")
    ii00100_csv = _add_momentunit_to_ii00100_csv(ii00100_csv, x_moment, csv_delimiter)
    ii00101_csv = _add_budunit_to_ii00101_csv(ii00101_csv, x_moment, csv_delimiter)
    ii00102_csv = _add_paybook_to_ii00102_csv(ii00102_csv, x_moment, csv_delimiter)
    ii00103_csv = _add_hours_to_ii00103_csv(ii00103_csv, x_moment, csv_delimiter)
    ii00104_csv = _add_months_to_ii00104_csv(ii00104_csv, x_moment, csv_delimiter)
    ii00105_csv = _add_weekdays_to_ii00105_csv(ii00105_csv, x_moment, csv_delimiter)
    moment_csv_strs["ii00100"] = ii00100_csv
    moment_csv_strs["ii00101"] = ii00101_csv
    moment_csv_strs["ii00102"] = ii00102_csv
    moment_csv_strs["ii00103"] = ii00103_csv
    moment_csv_strs["ii00104"] = ii00104_csv
    moment_csv_strs["ii00105"] = ii00105_csv


def get_csv_compatible_knot(knot: KnotTerm, csv_delimiter: str) -> KnotTerm:
    if knot == csv_delimiter:
        knot = f"""\"{str(knot)}\""""
    return knot


def _add_momentunit_to_ii00100_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    x_row = [
        if_none_str(spark_num),
        if_none_str(spark_face),
        x_moment.moment_rope,
        x_moment.epoch.epoch_label,
        str(x_moment.epoch.c400_number),
        str(x_moment.epoch.yr1_jan1_offset),
        str(x_moment.epoch.monthday_index),
        str(x_moment.fund_grain),
        str(x_moment.mana_grain),
        str(x_moment.respect_grain),
        x_knot,
        str(x_moment.job_listen_rotations),
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def _add_budunit_to_ii00101_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for broker_person_name, personbudhistorys in x_moment.personbudhistorys.items():
        for bud_time, budunit in personbudhistorys.buds.items():
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_moment.moment_rope,
                broker_person_name,
                str(bud_time),
                x_knot,
                str(budunit.quota),
                str(budunit.celldepth),
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def _add_paybook_to_ii00102_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for person_name, tranunit in x_moment.paybook.tranunits.items():
        for contact_name, time_dict in tranunit.items():
            for tran_time, amount in time_dict.items():
                moment_rope = x_moment.moment_rope
                x_row = [
                    if_none_str(spark_face),
                    if_none_str(spark_num),
                    moment_rope,
                    person_name,
                    contact_name,
                    str(tran_time),
                    str(amount),
                    x_knot,
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def _add_hours_to_ii00103_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for hour_plan in x_moment.epoch.hours_config:
        x_row = [
            if_none_str(spark_num),
            if_none_str(spark_face),
            x_moment.moment_rope,
            str(hour_plan[1]),
            hour_plan[0],
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_ii00104_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for month_plan in x_moment.epoch.months_config:
        x_row = [
            if_none_str(spark_num),
            if_none_str(spark_face),
            x_moment.moment_rope,
            str(month_plan[1]),
            month_plan[0],
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_ii00105_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for count_x, weekday_label in enumerate(x_moment.epoch.weekdays_config):
        x_row = [
            if_none_str(spark_num),
            if_none_str(spark_face),
            x_moment.moment_rope,
            str(count_x),
            weekday_label,
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_person_to_ii00120_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for contactunit in x_person.contacts.values():
        for membership in contactunit.memberships.values():
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.planroot.get_plan_rope(),
                x_person.person_name,
                contactunit.contact_name,
                membership.group_title,
                if_none_str(membership.group_cred_lumen),
                if_none_str(membership.group_debt_lumen),
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00121_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for contactunit in x_person.contacts.values():
        x_row = [
            if_none_str(spark_num),
            if_none_str(spark_face),
            x_person.planroot.get_plan_rope(),
            x_person.person_name,
            contactunit.contact_name,
            if_none_str(contactunit.contact_cred_lumen),
            if_none_str(contactunit.contact_debt_lumen),
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_person_to_ii00122_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        for awardunit in planunit.awardunits.values():
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.person_name,
                planunit.get_plan_rope(),
                awardunit.awardee_title,
                if_none_str(awardunit.give_force),
                if_none_str(awardunit.take_force),
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00123_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for factunit in x_person.planroot.factunits.values():
        x_row = [
            if_none_str(spark_num),
            if_none_str(spark_face),
            x_person.person_name,
            x_person.planroot.get_plan_rope(),
            factunit.fact_context,
            factunit.fact_state,
            if_none_str(factunit.fact_lower),
            if_none_str(factunit.fact_upper),
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_person_to_ii00124_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        for group_title in planunit.workforceunit.labors:
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.person_name,
                planunit.get_plan_rope(),
                group_title,
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00125_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        for group_title in planunit.healerunit.healer_names:
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.person_name,
                planunit.get_plan_rope(),
                group_title,
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00126_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            for caseunit in reasonunit.cases.values():
                x_row = [
                    if_none_str(spark_face),
                    if_none_str(spark_num),
                    x_person.person_name,
                    planunit.get_plan_rope(),
                    reasonunit.reason_context,
                    caseunit.reason_state,
                    if_none_str(caseunit.reason_lower),
                    if_none_str(caseunit.reason_upper),
                    if_none_str(caseunit.reason_divisor),
                    x_knot,
                ]
                x_csv += csv_delimiter.join(x_row)
                x_csv += "\n"
    return x_csv


def add_person_to_ii00127_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        for reasonunit in planunit.reasonunits.values():
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.person_name,
                planunit.get_plan_rope(),
                reasonunit.reason_context,
                if_none_str(reasonunit.active_requisite),
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00128_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for planunit in x_person._plan_dict.values():
        if planunit != x_person.planroot:
            x_row = [
                if_none_str(spark_num),
                if_none_str(spark_face),
                x_person.person_name,
                planunit.get_plan_rope(),
                if_none_str(planunit.begin),
                if_none_str(planunit.close),
                if_none_str(planunit.addin),
                if_none_str(planunit.numor),
                if_none_str(planunit.denom),
                if_none_str(planunit.morph),
                if_none_str(planunit.gogo_want),
                if_none_str(planunit.stop_want),
                if_none_str(planunit.star),
                if_none_str(planunit.pledge),
                if_none_str(planunit.problem_bool),
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_ii00129_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    x_row = [
        if_none_str(spark_num),
        if_none_str(spark_face),
        x_person.planroot.get_plan_rope(),
        x_person.person_name,
        if_none_str(x_person.credor_respect),
        if_none_str(x_person.debtor_respect),
        if_none_str(x_person.fund_pool),
        if_none_str(x_person.max_tree_traverse),
        if_none_str(x_person.fund_grain),
        if_none_str(x_person.mana_grain),
        if_none_str(x_person.respect_grain),
        x_knot,
    ]
    x_csv += csv_delimiter.join(x_row)
    x_csv += "\n"
    return x_csv


def add_personunit_to_belief_csv_strs(
    x_person: PersonUnit, moment_csv_strs: dict[str, str], csv_delimiter: str
) -> str:
    """PersonUnit must be to be thinkouted."""
    ii00120_csv = moment_csv_strs.get("ii00120")
    ii00121_csv = moment_csv_strs.get("ii00121")
    ii00122_csv = moment_csv_strs.get("ii00122")
    ii00123_csv = moment_csv_strs.get("ii00123")
    ii00124_csv = moment_csv_strs.get("ii00124")
    ii00125_csv = moment_csv_strs.get("ii00125")
    ii00126_csv = moment_csv_strs.get("ii00126")
    ii00127_csv = moment_csv_strs.get("ii00127")
    ii00128_csv = moment_csv_strs.get("ii00128")
    ii00129_csv = moment_csv_strs.get("ii00129")
    ii00120_csv = add_person_to_ii00120_csv(ii00120_csv, x_person, csv_delimiter)
    ii00121_csv = add_person_to_ii00121_csv(ii00121_csv, x_person, csv_delimiter)
    ii00122_csv = add_person_to_ii00122_csv(ii00122_csv, x_person, csv_delimiter)
    ii00123_csv = add_person_to_ii00123_csv(ii00123_csv, x_person, csv_delimiter)
    ii00124_csv = add_person_to_ii00124_csv(ii00124_csv, x_person, csv_delimiter)
    ii00125_csv = add_person_to_ii00125_csv(ii00125_csv, x_person, csv_delimiter)
    ii00126_csv = add_person_to_ii00126_csv(ii00126_csv, x_person, csv_delimiter)
    ii00127_csv = add_person_to_ii00127_csv(ii00127_csv, x_person, csv_delimiter)
    ii00128_csv = add_person_to_ii00128_csv(ii00128_csv, x_person, csv_delimiter)
    ii00129_csv = add_person_to_ii00129_csv(ii00129_csv, x_person, csv_delimiter)
    moment_csv_strs["ii00120"] = ii00120_csv
    moment_csv_strs["ii00121"] = ii00121_csv
    moment_csv_strs["ii00122"] = ii00122_csv
    moment_csv_strs["ii00123"] = ii00123_csv
    moment_csv_strs["ii00124"] = ii00124_csv
    moment_csv_strs["ii00125"] = ii00125_csv
    moment_csv_strs["ii00126"] = ii00126_csv
    moment_csv_strs["ii00127"] = ii00127_csv
    moment_csv_strs["ii00128"] = ii00128_csv
    moment_csv_strs["ii00129"] = ii00129_csv
