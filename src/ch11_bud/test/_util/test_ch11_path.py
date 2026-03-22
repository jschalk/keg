from inspect import getdoc as inspect_getdoc
from platform import system as platform_system
from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import create_rope
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch11_bud._ref.ch11_path import (
    BUDUNIT_FILENAME,
    CELL_MANDATE_FILENAME,
    CELLNODE_FILENAME,
    PERSONSPARK_FILENAME,
    PERSONTIME_FILENAME,
    SPARK_ALL_LESSON_FILENAME,
    SPARK_EXPRESSED_LESSON_FILENAME,
    create_bud_dir_path,
    create_buds_dir_path,
    create_budunit_json_path,
    create_cell_dir_path,
    create_cell_json_path,
    create_cell_partner_mandate_ledger_path,
    create_person_spark_csv_path,
    create_person_spark_dir_path,
    create_personspark_path,
    create_persontime_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch11_bud.test._util.ch11_env import get_temp_dir
from src.ref.keywords import Ch11Keywords as kw, ExampleStrs as exx


def test_create_buds_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    buds_dir = create_buds_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue)

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    expected_buds_dir = create_path(sue_dir, "buds")
    assert buds_dir == expected_buds_dir


def test_create_bud_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    timenum7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    generated_timenum_dir = create_bud_dir_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, timenum7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    expected_timenum_dir = create_path(buds_dir, timenum7)
    assert generated_timenum_dir == expected_timenum_dir


def test_create_budunit_json_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    timenum7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_bud_path = create_budunit_json_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, timenum7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    timenum_dir = create_path(buds_dir, timenum7)
    expected_bud_path_dir = create_path(timenum_dir, BUDUNIT_FILENAME)
    assert gen_bud_path == expected_bud_path_dir


def test_create_persontime_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    timenum7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_persontime_path = create_persontime_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, timenum7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    timenum_dir = create_path(buds_dir, timenum7)
    expected_persontime_path_dir = create_path(timenum_dir, PERSONTIME_FILENAME)
    assert gen_persontime_path == expected_persontime_path_dir


def test_create_cell_dir_path_ReturnsObj_Scenario0_No_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_cell_dir = create_cell_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7, [])

    # THEN
    timenum_dir = create_bud_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7)
    assert gen_cell_dir == timenum_dir


def test_create_cell_dir_path_ReturnsObj_Scenario1_One_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    x_bud_ancestors = [exx.yao]
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_cell_dir = create_cell_dir_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timenum_dir = create_bud_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7)
    tp_yao_dir = create_path(timenum_dir, exx.yao)
    assert gen_cell_dir == tp_yao_dir


def test_create_cell_dir_path_ReturnsObj_Scenario2_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    a23_lasso = lassounit_shop(exx.a23)
    x_bud_ancestors = [exx.yao, exx.bob, exx.zia]

    # WHEN
    gen_bud_celldepth_dir_path = create_cell_dir_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, tp7, bud_ancestors=x_bud_ancestors
    )

    # THEN
    timenum_dir = create_bud_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7)
    tp_yao_dir = create_path(timenum_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_tp_yao_bob_zia_dir = create_path(tp_yao_bob_dir, exx.zia)
    assert gen_bud_celldepth_dir_path == expected_tp_yao_bob_zia_dir


def test_create_cell_json_path_ReturnsObj_Scenario0_Empty_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    timenum7 = 7
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, timenum7
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    amy23_dir = create_path(x_moments_dir, "Amy23")
    persons_dir = create_path(amy23_dir, "persons")
    sue_dir = create_path(persons_dir, exx.sue)
    buds_dir = create_path(sue_dir, "buds")
    timenum_dir = create_path(buds_dir, timenum7)
    expected_cell_json_path = create_path(timenum_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_json_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    a23_lasso = lassounit_shop(exx.a23)
    bud_ancestors = [exx.yao, exx.bob]

    # WHEN
    gen_cell_json_path = create_cell_json_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timenum_dir = create_bud_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7)
    tp_yao_dir = create_path(timenum_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELLNODE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_cell_partner_mandate_ledger_path_ReturnsObj_Scenario1_Three_bud_ancestors():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    tp7 = 7
    a23_lasso = lassounit_shop(exx.a23)
    bud_ancestors = [exx.yao, exx.bob]

    # WHEN
    gen_cell_json_path = create_cell_partner_mandate_ledger_path(
        x_moment_mstr_dir, a23_lasso, exx.sue, tp7, bud_ancestors=bud_ancestors
    )

    # THEN
    timenum_dir = create_bud_dir_path(x_moment_mstr_dir, a23_lasso, exx.sue, tp7)
    tp_yao_dir = create_path(timenum_dir, exx.yao)
    tp_yao_bob_dir = create_path(tp_yao_dir, exx.bob)
    expected_cell_json_path = create_path(tp_yao_bob_dir, CELL_MANDATE_FILENAME)
    assert gen_cell_json_path == expected_cell_json_path


def test_create_person_spark_dir_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_e3_dir_path = create_person_spark_dir_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, "Amy23")
    a23_persons_dir = create_path(a23_dir, "persons")
    a23_bob_dir = create_path(a23_persons_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    expected_a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    assert gen_a23_e3_dir_path == expected_a23_bob_e3_dir


def test_create_person_spark_csv_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3
    a23_lasso = lassounit_shop(exx.a23)
    x4_filename = "some_file"

    # WHEN
    gen_csv_path = create_person_spark_csv_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3, x4_filename
    )

    # THEN
    a23_e3_dir_path = create_person_spark_dir_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3
    )
    csv_filename = f"{x4_filename}.csv"
    expected_a23_bob_e3_dir = create_path(a23_e3_dir_path, csv_filename)
    assert gen_csv_path == expected_a23_bob_e3_dir


def test_create_personspark_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_e3_person_path = create_personspark_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, "Amy23")
    a23_persons_dir = create_path(a23_dir, "persons")
    a23_bob_dir = create_path(a23_persons_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_person_path = create_path(a23_bob_e3_dir, PERSONSPARK_FILENAME)
    assert gen_a23_e3_person_path == expected_a23_bob_e3_person_path


def test_create_spark_all_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_e3_person_path = create_spark_all_lesson_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, "Amy23")
    a23_persons_dir = create_path(a23_dir, "persons")
    a23_bob_dir = create_path(a23_persons_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_all_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_ALL_LESSON_FILENAME
    )
    assert gen_a23_e3_person_path == expected_a23_bob_e3_all_lesson_path


def test_create_spark_expressed_lesson_path_ReturnsObj():
    # ESTABLISH
    x_moment_mstr_dir = get_temp_dir()
    spark3 = 3
    a23_lasso = lassounit_shop(exx.a23)

    # WHEN
    gen_a23_e3_person_path = create_spark_expressed_lesson_path(
        x_moment_mstr_dir, a23_lasso, exx.bob, spark3
    )

    # THEN
    x_moments_dir = create_path(x_moment_mstr_dir, "moments")
    a23_dir = create_path(x_moments_dir, "Amy23")
    a23_persons_dir = create_path(a23_dir, "persons")
    a23_bob_dir = create_path(a23_persons_dir, exx.bob)
    a23_sparks_dir = create_path(a23_bob_dir, "sparks")
    a23_bob_e3_dir = create_path(a23_sparks_dir, spark3)
    expected_a23_bob_e3_expressed_lesson_path = create_path(
        a23_bob_e3_dir, SPARK_EXPRESSED_LESSON_FILENAME
    )
    assert gen_a23_e3_person_path == expected_a23_bob_e3_expressed_lesson_path


LINUX_OS = platform_system() == "Linux"


def test_create_buds_dir_path_HasDocString():
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    # ESTABLISH
    doc_str = create_buds_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_buds_dir_path) == doc_str


def test_create_bud_dir_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_bud_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_bud_dir_path) == doc_str


def test_create_cell_dir_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_cell_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_person1", "ledger_person2", "ledger_person3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_dir_path) == doc_str


def test_create_cell_json_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_cell_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_person1", "ledger_person2", "ledger_person3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_cell_json_path) == doc_str


def test_create_cell_partner_mandate_ledger_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_cell_partner_mandate_ledger_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
        bud_ancestors=["ledger_person1", "ledger_person2", "ledger_person3"],
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    print(f"{doc_str=}")
    # WHEN / THEN
    assert (
        LINUX_OS or inspect_getdoc(create_cell_partner_mandate_ledger_path) == doc_str
    )


def test_create_budunit_json_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_budunit_json_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_budunit_json_path) == doc_str


def test_create_persontime_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_persontime_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        bud_time=kw.bud_time,
    )
    doc_str = doc_str.replace("buds\\bud_time", "buds\n\\bud_time")
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_persontime_path) == doc_str


def test_create_person_spark_dir_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_person_spark_dir_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_person_spark_dir_path) == doc_str


def test_create_person_spark_csv_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_person_spark_csv_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        spark_num=kw.spark_num,
        filename="filename",
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_person_spark_csv_path) == doc_str


def test_create_personspark_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_personspark_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_personspark_path) == doc_str


def test_create_spark_all_lesson_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_spark_all_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_all_lesson_path) == doc_str


def test_create_spark_expressed_lesson_path_HasDocString():
    # ESTABLISH
    moment_lasso = lassounit_shop(create_rope(kw.moment_rope))
    doc_str = create_spark_expressed_lesson_path(
        moment_mstr_dir="moment_mstr_dir",
        moment_lasso=moment_lasso,
        person_name=kw.person_name,
        spark_num=kw.spark_num,
    )
    doc_str = f"Returns path: {doc_str}"
    # WHEN / THEN
    assert LINUX_OS or inspect_getdoc(create_spark_expressed_lesson_path) == doc_str
