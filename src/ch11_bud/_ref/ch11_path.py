from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson._ref.ch09_path import create_moment_persons_dir_path
from src.ch09_person_lesson.lasso import LassoUnit
from src.ch11_bud._ref.ch11_semantic_types import PersonName

MOMENT_FILENAME = "moment.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_partner_mandate_ledger.json"
PERSONTIME_FILENAME = "persontime.json"
PERSONSPARK_FILENAME = "person.json"
SPARK_ALL_LESSON_FILENAME = "all_lesson.json"
SPARK_EXPRESSED_LESSON_FILENAME = "expressed_lesson.json"


def create_buds_dir_path(
    moment_mstr_dir: str, moment_lasso: LassoUnit, person_name: PersonName
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    person_dir = create_path(persons_dir, person_name)
    return create_path(person_dir, "buds")


def create_bud_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time"""
    buds_dir = create_buds_dir_path(moment_mstr_dir, moment_lasso, person_name)
    return create_path(buds_dir, bud_time)


def create_budunit_json_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\budunit.json"""
    timenum_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time
    )
    return create_path(timenum_dir, "budunit.json")


def create_persontime_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\persontime.json"""
    timenum_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time
    )
    return create_path(timenum_dir, "persontime.json")


def create_cell_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
    bud_ancestors: list[PersonName],
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\ledger_person1\\ledger_person2\\ledger_person3"""
    bud_celldepth_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_person in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_person)
    return bud_celldepth_dir


def create_cell_json_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
    bud_ancestors: list[PersonName] = None,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\ledger_person1\\ledger_person2\\ledger_person3\\cell.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_partner_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
    bud_ancestors: list[PersonName] = None,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\ledger_person1\\ledger_person2\\ledger_person3\\cell_partner_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_partner_mandate_ledger.json")


def create_person_spark_dir_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\sparks\\spark_num"""
    persons_dir = create_moment_persons_dir_path(moment_mstr_dir, moment_lasso)
    moment_person_dir = create_path(persons_dir, person_name)
    moment_sparks_dir = create_path(moment_person_dir, "sparks")
    return create_path(moment_sparks_dir, spark_num)


def create_person_spark_csv_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
    filename: str,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\sparks\\spark_num\\filename.csv"""
    spark_dir = create_person_spark_dir_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    return create_path(spark_dir, f"{filename}.csv")


def create_personspark_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\sparks\\spark_num\\person.json"""
    person_spark_dir_path = create_person_spark_dir_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    person_filename = "person.json"
    return create_path(person_spark_dir_path, person_filename)


def create_spark_all_lesson_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\sparks\\spark_num\\all_lesson.json"""
    person_spark_dir_path = create_person_spark_dir_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    all_lesson_filename = "all_lesson.json"
    return create_path(person_spark_dir_path, all_lesson_filename)


def create_spark_expressed_lesson_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    spark_num: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\sparks\\spark_num\\expressed_lesson.json"""
    person_spark_dir_path = create_person_spark_dir_path(
        moment_mstr_dir, moment_lasso, person_name, spark_num
    )
    expressed_lesson_filename = "expressed_lesson.json"
    return create_path(person_spark_dir_path, expressed_lesson_filename)
