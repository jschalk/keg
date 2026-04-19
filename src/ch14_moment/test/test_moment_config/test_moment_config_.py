from ch00_py.file_toolbox import create_path
from ch08_person_atom.atom_config import get_allowed_class_types
from ch14_moment.moment_config import (
    get_moment_args_class_types,
    get_moment_args_dimen_mapping,
    get_moment_args_set,
    get_moment_config_dict,
    get_moment_dimens,
    moment_config_path,
)
from os import getcwd as os_getcwd
from ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_moment_config_path_ReturnsObj_Moment() -> str:
    # ESTABLISH / WHEN / THEN
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch14_moment")
    assert moment_config_path() == create_path(chapter_dir, "moment_config.json")


def test_get_moment_config_dict_ReturnsObj():
    # ESTABLISH / WHEN
    moment_config = get_moment_config_dict()

    # THEN
    assert moment_config
    moment_config_dimens = set(moment_config.keys())
    assert kw.momentunit in moment_config_dimens
    assert kw.moment_budunit in moment_config_dimens
    assert kw.moment_paybook in moment_config_dimens
    assert kw.moment_epoch_hour in moment_config_dimens
    assert kw.moment_epoch_month in moment_config_dimens
    assert kw.moment_epoch_weekday in moment_config_dimens
    assert kw.moment_timeoffi in moment_config_dimens
    assert len(moment_config) == 7
    _validate_moment_config(moment_config)
    momentunit_dict = moment_config.get(kw.momentunit)
    moment_budunit_dict = moment_config.get(kw.moment_budunit)
    moment_paybook_dict = moment_config.get(kw.moment_paybook)
    moment_epoch_hour_dict = moment_config.get(kw.moment_epoch_hour)
    moment_epoch_month_dict = moment_config.get(kw.moment_epoch_month)
    moment_epoch_weekday_dict = moment_config.get(kw.moment_epoch_weekday)
    # moment_timeoffi_dict = moment_config.get(kw.moment_timeoffi)
    assert len(momentunit_dict.get(kw.jkeys)) == 1
    assert len(moment_budunit_dict.get(kw.jkeys)) == 3
    assert len(moment_paybook_dict.get(kw.jkeys)) == 4
    assert len(moment_epoch_hour_dict.get(kw.jkeys)) == 2
    assert len(moment_epoch_month_dict.get(kw.jkeys)) == 2
    assert len(moment_epoch_weekday_dict.get(kw.jkeys)) == 2
    # assert len(moment_timeoffi_dict.get(kw.jkeys)) == 2

    x_momentunit_jvalues = {
        kw.c400_number,
        kw.fund_grain,
        kw.monthday_index,
        kw.mana_grain,
        kw.respect_grain,
        kw.knot,
        kw.epoch_label,
        kw.yr1_jan1_offset,
        kw.job_listen_rotations,
    }
    print(f"{momentunit_dict.get(kw.jvalues).keys()=}")
    gen_jvalues = set(momentunit_dict.get(kw.jvalues).keys())
    assert gen_jvalues == x_momentunit_jvalues
    assert len(momentunit_dict.get(kw.jvalues)) == 9
    assert len(moment_budunit_dict.get(kw.jvalues)) == 2
    assert len(moment_paybook_dict.get(kw.jvalues)) == 1
    assert len(moment_epoch_hour_dict.get(kw.jvalues)) == 1
    assert len(moment_epoch_month_dict.get(kw.jvalues)) == 1
    assert len(moment_epoch_weekday_dict.get(kw.jvalues)) == 1
    # assert len(moment_timeoffi_dict.get(kw.jvalues)) == 1


def _validate_moment_config(moment_config: dict):
    accepted_class_typees = get_allowed_class_types()
    accepted_class_typees.add("str")
    accepted_class_typees.add(kw.TimeNum)

    # for every moment_format file there exists a unique moment_number with leading zeros to make 5 digits
    for moment_dimen, dimen_dict in moment_config.items():
        print(f"_validate_moment_config {moment_dimen=}")
        assert dimen_dict.get(kw.jkeys) is not None
        assert dimen_dict.get(kw.jvalues) is not None
        if moment_dimen == kw.moment_timeoffi:
            assert dimen_dict.get(kw.moment_static) == "False"
        else:
            assert dimen_dict.get(kw.moment_static) == "True"
        assert dimen_dict.get(kw.UPDATE) is None
        assert dimen_dict.get(kw.INSERT) is None
        assert dimen_dict.get(kw.DELETE) is None
        assert dimen_dict.get(kw.normal_specs) is None

        moment_jkeys_keys = set(dimen_dict.get(kw.jkeys).keys())
        for jkey_key in moment_jkeys_keys:
            jkey_dict = dimen_dict.get(kw.jkeys)
            print(f"_validate_moment_config {moment_dimen=} {jkey_key=} ")
            arg_dict = jkey_dict.get(jkey_key)
            assert arg_dict.get(kw.class_type) in accepted_class_typees
        moment_jvalues_keys = set(dimen_dict.get(kw.jvalues).keys())
        for jvalue_key in moment_jvalues_keys:
            jvalue_dict = dimen_dict.get(kw.jvalues)
            print(f"_validate_moment_config {moment_dimen=} {jvalue_key=} ")
            arg_dict = jvalue_dict.get(jvalue_key)
            assert arg_dict.get(kw.class_type) in accepted_class_typees


def test_get_moment_dimens_ReturnsObj():
    # ESTABLISH / WHEN
    moment_config_dimens = get_moment_dimens()

    # THEN
    assert kw.momentunit in moment_config_dimens
    assert kw.moment_budunit in moment_config_dimens
    assert kw.moment_paybook in moment_config_dimens
    assert kw.moment_epoch_hour in moment_config_dimens
    assert kw.moment_epoch_month in moment_config_dimens
    assert kw.moment_epoch_weekday in moment_config_dimens
    assert kw.moment_timeoffi in moment_config_dimens
    assert len(moment_config_dimens) == 7
    assert moment_config_dimens == set(get_moment_config_dict().keys())


def test_get_moment_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_moment_args_dimen_mapping = get_moment_args_dimen_mapping()

    # THEN
    assert x_moment_args_dimen_mapping
    x_hour = {kw.moment_epoch_hour}
    assert x_moment_args_dimen_mapping.get(kw.cumulative_minute) == x_hour
    assert x_moment_args_dimen_mapping.get(kw.fund_grain)
    moment_rope_dimens = x_moment_args_dimen_mapping.get(kw.moment_rope)
    assert kw.moment_epoch_hour in moment_rope_dimens
    assert kw.momentunit in moment_rope_dimens
    assert len(moment_rope_dimens) == 7
    assert len(x_moment_args_dimen_mapping) == 24


def get_moment_class_type(x_dimen: str, x_arg: str) -> str:
    moment_config_dict = get_moment_config_dict()
    dimen_dict = moment_config_dict.get(x_dimen)
    jvalues_dict = dimen_dict.get(kw.jvalues)
    jkeys_dict = dimen_dict.get(kw.jkeys)
    arg_dict = {}
    if jvalues_dict.get(x_arg):
        arg_dict = dimen_dict.get(kw.jvalues).get(x_arg)
    if jkeys_dict.get(x_arg):
        arg_dict = jkeys_dict.get(x_arg)
    return arg_dict.get(kw.class_type)


def all_args_class_types_are_correct(x_class_types) -> bool:
    x_moment_args_dimen_mapping = get_moment_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_moment_arg in x_sorted_class_types:
        x_dimens = list(x_moment_args_dimen_mapping.get(x_moment_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_moment_class_type(x_dimen, x_moment_arg)
        print(
            f"assert x_class_types.get({x_moment_arg}) == {x_class_type} {x_class_types.get(x_moment_arg)=}"
        )
        if x_class_types.get(x_moment_arg) != x_class_type:
            return False
    return True


def test_get_moment_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    moment_args_class_types = get_moment_args_class_types()

    # THEN
    moment_args_from_dimens = set(get_moment_args_dimen_mapping().keys())
    print(f"{moment_args_from_dimens=}")
    assert set(moment_args_class_types.keys()) == moment_args_from_dimens
    assert all_args_class_types_are_correct(moment_args_class_types)


def test_get_moment_args_set_ReturnsObj():
    # ESTABLISH / WHEN
    moment_args_set = get_moment_args_set()

    # THEN
    assert moment_args_set
    mapping_args_set = set(get_moment_args_dimen_mapping().keys())
    print(f"{mapping_args_set=}")
    assert moment_args_set == mapping_args_set
    assert len(moment_args_set) == 24
    expected_moment_args_set = {
        kw.contact_name,
        kw.amount,
        kw.knot,
        kw.c400_number,
        kw.cumulative_day,
        kw.cumulative_minute,
        kw.hour_label,
        kw.moment_rope,
        kw.fund_grain,
        kw.month_label,
        kw.monthday_index,
        kw.job_listen_rotations,
        kw.mana_grain,
        kw.person_name,
        kw.quota,
        kw.celldepth,
        kw.respect_grain,
        kw.bud_time,
        kw.tran_time,
        kw.offi_time,
        kw.epoch_label,
        kw.weekday_label,
        kw.weekday_order,
        kw.yr1_jan1_offset,
    }
    assert moment_args_set == expected_moment_args_set
