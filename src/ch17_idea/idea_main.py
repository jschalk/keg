from csv import reader as csv_reader
from dataclasses import dataclass
from pandas import DataFrame
from src.ch00_py.dict_toolbox import (
    create_l2nested_csv_dict,
    extract_csv_headers,
    get_csv_column1_column2_metrics,
    get_positional_dict,
)
from src.ch07_person_logic.person_main import PersonUnit
from src.ch08_person_atom.atom_main import PersonAtom, atomrow_shop
from src.ch09_person_lesson.delta import (
    PersonDelta,
    get_dimens_cruds_persondelta,
    persondelta_shop,
)
from src.ch13_time.epoch_main import epochunit_shop
from src.ch14_moment.moment_main import MomentUnit, momentunit_shop
from src.ch17_idea._ref.ch17_semantic_types import MomentRope, PersonName
from src.ch17_idea.idea_config import get_idea_format_headers, get_idearef_from_file
from src.ch17_idea.idea_db_tool import (
    get_default_sorted_list,
    if_nan_return_None,
    save_dataframe_to_csv,
)


@dataclass
class IdeaRef:
    idea_name: str = None
    dimens: list[str] = None
    attributes: dict[str, dict[str, bool]] = None

    def set_attribute(self, x_attribute: str, otx_key: bool):
        self.attributes[x_attribute] = {"otx_key": otx_key}

    def get_headers_list(self) -> list[str]:
        return get_default_sorted_list(set(self.attributes.keys()))

    def get_otx_keys_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self.attributes.items()
            if otx_dict.get("otx_key") is True
        }
        return get_default_sorted_list(x_set)

    def get_otx_values_list(self) -> list[str]:
        x_set = {
            x_attr
            for x_attr, otx_dict in self.attributes.items()
            if otx_dict.get("otx_key") is False
        }
        return get_default_sorted_list(x_set)


def idearef_shop(x_idea_name: str, x_dimens: list[str]) -> IdeaRef:
    return IdeaRef(idea_name=x_idea_name, dimens=x_dimens, attributes={})


def get_idearef_obj(idea_name: str) -> IdeaRef:
    idearef_dict = get_idearef_from_file(idea_name)
    x_idearef = idearef_shop(idea_name, idearef_dict.get("dimens"))
    x_idearef.attributes = idearef_dict.get("attributes")
    return x_idearef


def get_ascending_bools(sorting_attributes: list[str]) -> list[bool]:
    return [True for _ in sorting_attributes]


def _get_headers_list(idea_name: str) -> list[str]:
    return get_idearef_obj(idea_name).get_headers_list()


def _generate_idea_dataframe(d2_list: list[list[str]], idea_name: str) -> DataFrame:
    return DataFrame(d2_list, columns=_get_headers_list(idea_name))


def create_idea_df(x_personunit: PersonUnit, idea_name: str) -> DataFrame:
    x_persondelta = persondelta_shop()
    x_persondelta.add_all_personatoms(x_personunit)
    x_idearef = get_idearef_obj(idea_name)
    x_moment_rope = x_personunit.planroot.get_plan_rope()
    x_person_name = x_personunit.person_name
    sorted_personatoms = _get_sorted_insert_str_personatoms(x_persondelta, x_idearef)
    d2_list = _create_d2_list(
        sorted_personatoms, x_idearef, x_moment_rope, x_person_name
    )
    d2_list = _delta_all_pledge_values(d2_list, x_idearef)
    x_idea = _generate_idea_dataframe(d2_list, idea_name)
    sorting_columns = x_idearef.get_headers_list()
    return _sort_dataframe(x_idea, sorting_columns)


def _get_sorted_insert_str_personatoms(
    x_persondelta: PersonDelta, x_idearef: IdeaRef
) -> list[PersonAtom]:
    dimen_set = set(x_idearef.dimens)
    curd_set = {"INSERT"}
    limited_delta = get_dimens_cruds_persondelta(x_persondelta, dimen_set, curd_set)
    return limited_delta.get_dimen_sorted_personatoms_list()


def _create_d2_list(
    sorted_personatoms: list[PersonAtom],
    x_idearef: IdeaRef,
    x_moment_rope: MomentRope,
    x_person_name: PersonName,
):
    d2_list = []
    for x_personatom in sorted_personatoms:
        d1_list = []
        for x_attribute in x_idearef.get_headers_list():
            if x_attribute == "moment_rope":
                d1_list.append(x_moment_rope)
            elif x_attribute == "person_name":
                d1_list.append(x_person_name)
            else:
                d1_list.append(x_personatom.get_value(x_attribute))
        d2_list.append(d1_list)
    return d2_list


def _delta_all_pledge_values(d2_list: list[list], x_idearef: IdeaRef) -> list[list]:
    if "pledge" in x_idearef.attributes:
        for x_count, x_header in enumerate(x_idearef.get_headers_list()):
            if x_header == "pledge":
                pledge_column_number = x_count
        for x_row in d2_list:
            if x_row[pledge_column_number] is True:
                x_row[pledge_column_number] = "Yes"
            else:
                x_row[pledge_column_number] = ""
    return d2_list


def _sort_dataframe(x_idea: DataFrame, sorting_columns: list[str]) -> DataFrame:
    ascending_bools = get_ascending_bools(sorting_columns)
    x_idea.sort_values(sorting_columns, ascending=ascending_bools, inplace=True)
    x_idea.reset_index(inplace=True)
    x_idea.drop(columns=["index"], inplace=True)
    return x_idea


def save_idea_csv(
    x_ideaname: str, x_personunit: PersonUnit, x_dir: str, x_filename: str
):
    x_dataframe = create_idea_df(x_personunit, x_ideaname)
    save_dataframe_to_csv(x_dataframe, x_dir, x_filename)


def get_csv_idearef(header_row: list[str]) -> IdeaRef:
    header_row = get_default_sorted_list(set(header_row))
    headers_str = "".join(f",{x_header}" for x_header in header_row)
    headers_str = headers_str[1:]
    headers_str = headers_str.replace("spark_face,", "")
    headers_str = headers_str.replace("spark_num,", "")
    x_ideaname = get_idea_format_headers().get(headers_str)
    return get_idearef_obj(x_ideaname)


def _remove_non_person_dimens_from_idearef(x_idearef: IdeaRef) -> IdeaRef:
    to_delete_dimen_set = {
        dimen for dimen in x_idearef.dimens if not dimen.startswith("person")
    }
    dimens_set = set(x_idearef.dimens)
    for to_delete_dimen in to_delete_dimen_set:
        if to_delete_dimen in dimens_set:
            dimens_set.remove(to_delete_dimen)
    x_idearef.dimens = list(dimens_set)
    return x_idearef


def make_persondelta(x_csv: str) -> PersonDelta:
    header_row, headerless_csv = extract_csv_headers(x_csv)
    x_idearef = get_csv_idearef(header_row)
    _remove_non_person_dimens_from_idearef(x_idearef)
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    x_dict = get_positional_dict(header_row)
    x_persondelta = persondelta_shop()

    for row in x_reader:
        x_atomrow = atomrow_shop(x_idearef.dimens, "INSERT")
        for x_header in header_row:
            if header_index := x_dict.get(x_header):
                x_atomrow.__dict__[x_header] = row[header_index]

        for x_personatom in x_atomrow.get_personatoms():
            x_persondelta.set_personatom(x_personatom)
    return x_persondelta


def get_csv_moment_rope_person_name_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[MomentRope, dict[PersonName, int]]:
    return get_csv_column1_column2_metrics(headerless_csv, delimiter)


def moment_rope_person_name_nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[MomentRope, dict[PersonName, str]]:
    return create_l2nested_csv_dict(headerless_csv, delimiter)


def moment_build_from_df(
    br00000_df: DataFrame,
    br00001_df: DataFrame,
    br00002_df: DataFrame,
    br00003_df: DataFrame,
    br00004_df: DataFrame,
    br00005_df: DataFrame,
    x_fund_grain: float,
    x_respect_grain: float,
    x_mana_grain: float,
    x_moments_dir: str,
) -> dict[MomentRope, MomentUnit]:
    moment_hours_dict = _get_moment_hours_dict(br00003_df)
    moment_months_dict = _get_moment_months_dict(br00004_df)
    moment_weekdays_dict = _get_moment_weekdays_dict(br00005_df)

    momentunit_dict = {}
    for index, row in br00000_df.iterrows():
        x_moment_rope = row["moment_rope"]
        x_epoch_config = {
            "c400_number": row["c400_number"],
            "hours_config": moment_hours_dict.get(x_moment_rope),
            "months_config": moment_months_dict.get(x_moment_rope),
            "monthday_index": row["monthday_index"],
            "epoch_label": row["epoch_label"],
            "weekdays_config": moment_weekdays_dict.get(x_moment_rope),
            "yr1_jan1_offset": row["yr1_jan1_offset"],
        }
        x_epoch = epochunit_shop(x_epoch_config)
        x_momentunit = momentunit_shop(
            moment_rope=x_moment_rope,
            moment_mstr_dir=x_moments_dir,
            epoch=x_epoch,
            knot=row["knot"],
            fund_grain=x_fund_grain,
            respect_grain=x_respect_grain,
            mana_grain=x_mana_grain,
            job_listen_rotations=row["job_listen_rotations"],
        )
        momentunit_dict[x_momentunit.moment_rope] = x_momentunit
        _add_budunits_from_df(x_momentunit, br00001_df)
        _add_paypurchases_from_df(x_momentunit, br00002_df)
    return momentunit_dict


def _get_moment_hours_dict(br00003_df: DataFrame) -> dict[str, list[str, str]]:
    moment_hours_dict = {}
    for y_moment_rope in br00003_df.moment_rope.unique():
        query_str = f"moment_rope == '{y_moment_rope}'"
        x_hours_list = [
            [row["hour_label"], row["cumulative_minute"]]
            for index, row in br00003_df.query(query_str).iterrows()
        ]
        moment_hours_dict[y_moment_rope] = x_hours_list
    return moment_hours_dict


def _get_moment_months_dict(br00004_df: DataFrame) -> dict[str, list[str, str]]:
    moment_months_dict = {}
    for y_moment_rope in br00004_df.moment_rope.unique():
        query_str = f"moment_rope == '{y_moment_rope}'"
        x_months_list = [
            [row["month_label"], row["cumulative_day"]]
            for index, row in br00004_df.query(query_str).iterrows()
        ]
        moment_months_dict[y_moment_rope] = x_months_list
    return moment_months_dict


def _get_moment_weekdays_dict(br00005_df: DataFrame) -> dict[str, list[str, str]]:
    moment_weekdays_dict = {}
    for y_moment_rope in br00005_df.moment_rope.unique():
        query_str = f"moment_rope == '{y_moment_rope}'"
        x_weekdays_list = [
            row["weekday_label"]
            for index, row in br00005_df.query(query_str).iterrows()
        ]
        moment_weekdays_dict[y_moment_rope] = x_weekdays_list
    return moment_weekdays_dict


def _add_budunits_from_df(x_momentunit: MomentUnit, br00001_df: DataFrame):
    query_str = f"moment_rope == '{x_momentunit.moment_rope}'"
    for index, row in br00001_df.query(query_str).iterrows():
        x_momentunit.add_budunit(
            person_name=row["person_name"],
            bud_time=row["bud_time"],
            quota=row["quota"],
            celldepth=if_nan_return_None(row["celldepth"]),
            allow_prev_to_offi_time_max_entry=True,
        )


def _add_paypurchases_from_df(x_momentunit: MomentUnit, br00002_df: DataFrame):
    query_str = f"moment_rope == '{x_momentunit.moment_rope}'"
    for index, row in br00002_df.query(query_str).iterrows():
        x_momentunit.add_paypurchase(
            person_name=row["person_name"],
            contact_name=row["contact_name"],
            tran_time=row["tran_time"],
            amount=row["amount"],
        )


def _add_time_offi_units_from_df(x_momentunit: MomentUnit, br00006_df: DataFrame):
    query_str = f"moment_rope == '{x_momentunit.moment_rope}'"
    for index, row in br00006_df.query(query_str).iterrows():
        x_momentunit.offi_times.add(row["offi_time"])
