from src.ch00_py.dict_toolbox import get_empty_str_if_None as if_none_str
from src.ch07_person_logic.person_main import PersonUnit
from src.ch14_moment.moment_main import MomentUnit
from src.ch17_idea._ref.ch17_semantic_types import FaceName, KnotTerm, MomentRope
from src.ch17_idea.idea_config import (
    get_brick_format_filename,
    get_brick_format_headers,
)


def create_init_belief_idea_csv_strs() -> dict[str, str]:
    """Returns strings of csv headers with comma delimiter"""
    belief_brick_types = [
        "br00000",
        "br00001",
        "br00002",
        "br00003",
        "br00004",
        "br00005",
        # "br00006",
        "br00020",
        "br00021",
        "br00022",
        "br00023",
        "br00024",
        "br00025",
        "br00026",
        "br00027",
        "br00028",
        "br00029",
        "br00042",
        "br00043",
        "br00044",
        "br00045",
    ]
    brick_format_headers = get_brick_format_headers()

    moment_csv_strs = {}
    for brick_type in belief_brick_types:
        brick_format_filename = get_brick_format_filename(brick_type)
        for idea_columns, idea_filename in brick_format_headers.items():
            if idea_filename == brick_format_filename:
                moment_csv_strs[brick_type] = f"spark_num,spark_face,{idea_columns}\n"
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
    br00000_csv = moment_csv_strs.get("br00000")
    br00001_csv = moment_csv_strs.get("br00001")
    br00002_csv = moment_csv_strs.get("br00002")
    br00003_csv = moment_csv_strs.get("br00003")
    br00004_csv = moment_csv_strs.get("br00004")
    br00005_csv = moment_csv_strs.get("br00005")
    br00000_csv = _add_momentunit_to_br00000_csv(br00000_csv, x_moment, csv_delimiter)
    br00001_csv = _add_budunit_to_br00001_csv(br00001_csv, x_moment, csv_delimiter)
    br00002_csv = _add_paybook_to_br00002_csv(br00002_csv, x_moment, csv_delimiter)
    br00003_csv = _add_hours_to_br00003_csv(br00003_csv, x_moment, csv_delimiter)
    br00004_csv = _add_months_to_br00004_csv(br00004_csv, x_moment, csv_delimiter)
    br00005_csv = _add_weekdays_to_br00005_csv(br00005_csv, x_moment, csv_delimiter)
    moment_csv_strs["br00000"] = br00000_csv
    moment_csv_strs["br00001"] = br00001_csv
    moment_csv_strs["br00002"] = br00002_csv
    moment_csv_strs["br00003"] = br00003_csv
    moment_csv_strs["br00004"] = br00004_csv
    moment_csv_strs["br00005"] = br00005_csv


def get_csv_compatible_knot(knot: KnotTerm, csv_delimiter: str) -> KnotTerm:
    if knot == csv_delimiter:
        knot = f"""\"{str(knot)}\""""
    return knot


def _add_momentunit_to_br00000_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    x_row = [
        if_none_str(spark_face),
        if_none_str(spark_num),
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


def _add_budunit_to_br00001_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
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


def _add_paybook_to_br00002_csv(
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


def _add_hours_to_br00003_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for hour_plan in x_moment.epoch.hours_config:
        x_row = [
            if_none_str(spark_face),
            if_none_str(spark_num),
            x_moment.moment_rope,
            str(hour_plan[1]),
            hour_plan[0],
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_months_to_br00004_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for month_plan in x_moment.epoch.months_config:
        x_row = [
            if_none_str(spark_face),
            if_none_str(spark_num),
            x_moment.moment_rope,
            str(month_plan[1]),
            month_plan[0],
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def _add_weekdays_to_br00005_csv(
    x_csv: str,
    x_moment: MomentUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_moment.knot, csv_delimiter)
    for count_x, weekday_label in enumerate(x_moment.epoch.weekdays_config):
        x_row = [
            if_none_str(spark_face),
            if_none_str(spark_num),
            x_moment.moment_rope,
            str(count_x),
            weekday_label,
            x_knot,
        ]
        x_csv += csv_delimiter.join(x_row)
        x_csv += "\n"
    return x_csv


def add_person_to_br00020_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
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


def add_person_to_br00021_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for contactunit in x_person.contacts.values():
        x_row = [
            if_none_str(spark_face),
            if_none_str(spark_num),
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


def add_person_to_br00022_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
                x_person.planroot.get_plan_rope(),
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


def add_person_to_br00023_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    for factunit in x_person.planroot.factunits.values():
        x_row = [
            if_none_str(spark_face),
            if_none_str(spark_num),
            x_person.planroot.get_plan_rope(),
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


def add_person_to_br00024_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
                x_person.planroot.get_plan_rope(),
                x_person.person_name,
                planunit.get_plan_rope(),
                group_title,
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_br00025_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
                x_person.planroot.get_plan_rope(),
                x_person.person_name,
                planunit.get_plan_rope(),
                group_title,
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_br00026_csv(
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
                    x_person.planroot.get_plan_rope(),
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


def add_person_to_br00027_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
                x_person.planroot.get_plan_rope(),
                x_person.person_name,
                planunit.get_plan_rope(),
                reasonunit.reason_context,
                if_none_str(reasonunit.active_requisite),
                x_knot,
            ]
            x_csv += csv_delimiter.join(x_row)
            x_csv += "\n"
    return x_csv


def add_person_to_br00028_csv(
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
                if_none_str(spark_face),
                if_none_str(spark_num),
                x_person.planroot.get_plan_rope(),
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


def add_person_to_br00029_csv(
    x_csv: str,
    x_person: PersonUnit,
    csv_delimiter: str,
    spark_face: FaceName = None,
    spark_num: int = None,
) -> str:
    x_knot = get_csv_compatible_knot(x_person.knot, csv_delimiter)
    x_row = [
        if_none_str(spark_face),
        if_none_str(spark_num),
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
    br00020_csv = moment_csv_strs.get("br00020")
    br00021_csv = moment_csv_strs.get("br00021")
    br00022_csv = moment_csv_strs.get("br00022")
    br00023_csv = moment_csv_strs.get("br00023")
    br00024_csv = moment_csv_strs.get("br00024")
    br00025_csv = moment_csv_strs.get("br00025")
    br00026_csv = moment_csv_strs.get("br00026")
    br00027_csv = moment_csv_strs.get("br00027")
    br00028_csv = moment_csv_strs.get("br00028")
    br00029_csv = moment_csv_strs.get("br00029")
    br00020_csv = add_person_to_br00020_csv(br00020_csv, x_person, csv_delimiter)
    br00021_csv = add_person_to_br00021_csv(br00021_csv, x_person, csv_delimiter)
    br00022_csv = add_person_to_br00022_csv(br00022_csv, x_person, csv_delimiter)
    br00023_csv = add_person_to_br00023_csv(br00023_csv, x_person, csv_delimiter)
    br00024_csv = add_person_to_br00024_csv(br00024_csv, x_person, csv_delimiter)
    br00025_csv = add_person_to_br00025_csv(br00025_csv, x_person, csv_delimiter)
    br00026_csv = add_person_to_br00026_csv(br00026_csv, x_person, csv_delimiter)
    br00027_csv = add_person_to_br00027_csv(br00027_csv, x_person, csv_delimiter)
    br00028_csv = add_person_to_br00028_csv(br00028_csv, x_person, csv_delimiter)
    br00029_csv = add_person_to_br00029_csv(br00029_csv, x_person, csv_delimiter)
    moment_csv_strs["br00020"] = br00020_csv
    moment_csv_strs["br00021"] = br00021_csv
    moment_csv_strs["br00022"] = br00022_csv
    moment_csv_strs["br00023"] = br00023_csv
    moment_csv_strs["br00024"] = br00024_csv
    moment_csv_strs["br00025"] = br00025_csv
    moment_csv_strs["br00026"] = br00026_csv
    moment_csv_strs["br00027"] = br00027_csv
    moment_csv_strs["br00028"] = br00028_csv
    moment_csv_strs["br00029"] = br00029_csv
