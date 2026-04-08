from os import listdir as os_listdir
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.ch00_py.dict_toolbox import get_empty_list_if_None
from src.ch00_py.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_json,
    save_json,
    set_dir,
)
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_moment_persons_dir_path
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_person_file, save_person_file
from src.ch11_bud._ref.ch11_path import (
    CELLNODE_FILENAME,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_personspark_path,
    create_persontime_path,
)
from src.ch11_bud._ref.ch11_semantic_types import (
    PersonName,
    RopeTerm,
    SparkInt,
    TimeNum,
)
from src.ch11_bud.bud_main import BudUnit, get_budunit_from_dict
from src.ch11_bud.cell_main import CellUnit, cellunit_get_from_dict, cellunit_shop


def get_personspark_obj(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
) -> PersonUnit:
    personspark_json_path = create_personspark_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    return open_person_file(personspark_json_path)


def collect_person_spark_dir_sets(
    moment_mstr_dir: str, moment_lasso: RopeTerm
) -> dict[PersonName, set[SparkInt]]:
    x_dict = {}
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    set_dir(persons_dir)
    for person_name in os_listdir(persons_dir):
        person_dir = create_path(persons_dir, person_name)
        sparks_dir = create_path(person_dir, "sparks")
        set_dir(sparks_dir)
        person_sparks_dirs = {
            int(spark_num_dir)
            for spark_num_dir in os_listdir(sparks_dir)
            if os_path_isdir(create_path(sparks_dir, spark_num_dir))
        }
        x_dict[person_name] = person_sparks_dirs
    return x_dict


def get_persons_downhill_spark_nums(
    person_sparks_sets: dict[PersonName, set[SparkInt]],
    downhill_persons: set[PersonName] = None,
    ref_spark_num: SparkInt = None,
) -> dict[PersonName, SparkInt]:
    x_dict = {}
    if downhill_persons:
        for person_name in downhill_persons:
            if spark_set := person_sparks_sets.get(person_name):
                _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, person_name)
    else:
        for person_name, spark_set in person_sparks_sets.items():
            _add_downhill_spark_num(x_dict, spark_set, ref_spark_num, person_name)
    return x_dict


def _add_downhill_spark_num(
    x_dict: dict[PersonName, SparkInt],
    spark_set: set[SparkInt],
    ref_spark_num: SparkInt,
    downhill_person: PersonName,
):
    if spark_set:
        if ref_spark_num:
            if downhill_spark_nums := {ei for ei in spark_set if ei <= ref_spark_num}:
                x_dict[downhill_person] = max(downhill_spark_nums)
        else:
            x_dict[downhill_person] = max(spark_set)


def save_arbitrary_personspark(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: str,
    spark_num: int,
    contacts: list[list] = None,
    facts: list[tuple[RopeTerm, RopeTerm, float, float]] = None,
) -> str:
    contacts = get_empty_list_if_None(contacts)
    facts = get_empty_list_if_None(facts)
    x_personunit = personunit_shop(person_name, moment_lasso.moment_rope)
    for contact_list in contacts:
        try:
            contact_cred_lumen = contact_list[1]
        except Exception:
            contact_cred_lumen = None
        x_personunit.add_contactunit(contact_list[0], contact_cred_lumen)
    for fact_tup in facts:
        x_reason_context = fact_tup[0]
        x_fact_state = fact_tup[1]
        x_fact_lower = fact_tup[2]
        x_fact_upper = fact_tup[3]
        x_personunit.add_fact(
            x_reason_context, x_fact_state, x_fact_lower, x_fact_upper, True
        )
    x_personspark_path = create_personspark_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    save_json(x_personspark_path, None, x_personunit.to_dict())
    return x_personspark_path


def cellunit_add_json_file(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    time_person_name: str,
    bud_time: int,
    spark_num: int,
    bud_ancestors: list[PersonName] = None,
    quota: int = None,
    celldepth: int = None,
    mana_grain: int = None,
):
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_lasso, time_person_name, bud_time, bud_ancestors
    )
    x_cell = cellunit_shop(
        time_person_name, bud_ancestors, spark_num, celldepth, mana_grain, quota
    )
    cellunit_save_to_dir(cell_dir, x_cell)


def cellunit_save_to_dir(dirpath: str, x_cell: CellUnit):
    save_json(dirpath, CELLNODE_FILENAME, x_cell.to_dict())


def cellunit_get_from_dir(dirpath: str) -> CellUnit:
    cell_json_path = create_path(dirpath, CELLNODE_FILENAME)
    if os_path_exists(cell_json_path):
        return cellunit_get_from_dict(open_json(cell_json_path))


def create_cell_contact_mandate_ledger_json(dirpath: str):
    if cell := cellunit_get_from_dir(dirpath):
        cell.calc_contact_mandate_ledger()
        save_json(
            dirpath, "cell_contact_mandate_ledger.json", cell.contact_mandate_ledger
        )


def save_bud_file(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    x_bud: BudUnit = None,
):
    x_bud.calc_magnitude()
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_lasso, person_name, x_bud.bud_time
    )
    save_json(bud_json_path, None, x_bud.to_dict(), replace=True)


def bud_file_exists(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    x_bud_time: TimeNum = None,
) -> bool:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_lasso, person_name, x_bud_time
    )
    return os_path_exists(bud_json_path)


def open_bud_file(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    x_bud_time: TimeNum = None,
) -> BudUnit:
    bud_json_path = create_budunit_json_path(
        moment_mstr_dir, moment_lasso, person_name, x_bud_time
    )
    if bud_file_exists(moment_mstr_dir, moment_lasso, person_name, x_bud_time):
        return get_budunit_from_dict(open_json(bud_json_path))


class SaveValidPersontimeError(Exception):
    pass


def save_persontime_file(
    moment_mstr_dir: str,
    x_persontime: PersonUnit,
    x_bud_time: TimeNum = None,
):
    x_persontime.conpute()
    if x_persontime.rational is False:
        raise SaveValidPersontimeError(
            "persontime could not be saved PersonUnit.rational is False"
        )
    persontime_json_path = create_persontime_path(
        moment_mstr_dir,
        lassounit_shop(x_persontime.planroot.get_plan_rope(), x_persontime.knot),
        x_persontime.person_name,
        x_bud_time,
    )
    save_person_file(persontime_json_path, None, x_persontime)


def persontime_file_exists(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    x_bud_time: TimeNum = None,
) -> bool:
    persontime_json_path = create_persontime_path(
        moment_mstr_dir, moment_lasso, person_name, x_bud_time
    )
    return os_path_exists(persontime_json_path)


def open_persontime_file(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    x_bud_time: TimeNum = None,
) -> bool:
    persontime_json_path = create_persontime_path(
        moment_mstr_dir, moment_lasso, person_name, x_bud_time
    )
    # if self.persontime_file_exists(x_bud_time):
    return open_person_file(persontime_json_path)


def get_timenum_dirs(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> list[TimeNum]:
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_lasso, person_name)
    x_dict = get_dir_file_strs(buds_dir, include_dirs=True, include_files=False)
    return [int(x_timenum) for x_timenum in sorted(list(x_dict.keys()))]
