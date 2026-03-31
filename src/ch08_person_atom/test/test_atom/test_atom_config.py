from src.ch00_py.dict_toolbox import get_from_nested_dict
from src.ch07_person_logic.person_config import get_person_config_dict
from src.ch08_person_atom._ref.ch08_semantic_types import CRUD_command
from src.ch08_person_atom.atom_config import (
    get_all_person_dimen_delete_keys,
    get_all_person_dimen_keys,
    get_allowed_class_types,
    get_atom_args_class_types,
    get_atom_args_dimen_mapping,
    get_atom_config_dict,
    get_atom_order as q_order,
    get_delete_key_name,
    get_flattened_atom_table_build,
    get_normalized_person_table_build,
    get_person_dimens,
    get_sorted_jkey_keys,
    is_person_dimen,
    set_mog,
)
from src.ref.keywords import Ch08Keywords as kw


def test_CRUD_command_Exists():
    # ESTABLISH / WHEN / THEN
    assert CRUD_command(kw.UPDATE) == str(kw.UPDATE)
    assert CRUD_command(kw.DELETE) == str(kw.DELETE)
    assert CRUD_command(kw.INSERT) == str(kw.INSERT)


def test_get_person_dimens_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_person_dimens() == set(get_atom_config_dict().keys())
    assert kw.person_contactunit in get_person_dimens()
    assert is_person_dimen(kw.planroot) is False


def test_get_all_person_dimen_keys_ReturnsObj():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN
    all_person_dimen_keys = get_all_person_dimen_keys()

    # THEN
    assert not all_person_dimen_keys.isdisjoint({kw.contact_name})
    expected_person_keys = set()
    for person_dimen in get_person_dimens():
        expected_person_keys.update(_get_atom_config_jkey_keys(person_dimen))

    expected_person_keys.add(kw.person_name)
    print(f"{expected_person_keys=}")
    assert all_person_dimen_keys == expected_person_keys


def test_get_delete_key_name_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_delete_key_name("Fay") == "Fay_ERASE"
    assert get_delete_key_name("run") == "run_ERASE"
    assert get_delete_key_name("") is None


def test_get_all_person_dimen_delete_keys_ReturnsObj():
    # ESTABLISH / WHEN
    all_person_dimen_delete_keys = get_all_person_dimen_delete_keys()

    # THEN
    assert not all_person_dimen_delete_keys.isdisjoint(
        {get_delete_key_name(kw.contact_name)}
    )
    expected_person_delete_keys = {
        get_delete_key_name(person_dimen_key)
        for person_dimen_key in get_all_person_dimen_keys()
    }
    print(f"{expected_person_delete_keys=}")
    assert all_person_dimen_delete_keys == expected_person_delete_keys


def test_get_atom_config_dict_ReturnsObj_Mirrors_person_config():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    atom_config_dict = get_atom_config_dict()

    # THEN
    person_config_dict = get_person_config_dict()
    atom_config_dimens = set(atom_config_dict.keys())
    person_config_dimens = set(person_config_dict.keys())
    assert atom_config_dimens.issubset(person_config_dimens)
    assert person_config_dimens.difference(atom_config_dimens) == {kw.person_groupunit}
    for atom_dimen, dimen_dict in atom_config_dict.items():
        for attr_key, atom_attr_dict in dimen_dict.items():
            if attr_key in kw.jkeys:
                atom_attr_keys = set(atom_attr_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(atom_attr_keys)=}")
                person_jkeys_dict = person_config_dict.get(atom_dimen).get(kw.jkeys)
                person_jkeys_keys = set(person_jkeys_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(person_jkeys_keys)=}")
                assert atom_attr_keys.issubset(person_jkeys_keys)
            elif attr_key in kw.jvalues:
                atom_attr_keys = set(atom_attr_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(atom_attr_keys)=}")
                person_dict = person_config_dict.get(atom_dimen).get(kw.jvalues)
                person_keys = set(person_dict.keys())
                print(f"{atom_dimen=} {attr_key=} {len(person_keys)=}")
                assert atom_attr_keys.issubset(person_keys)


def _check_every_crud_dict_has_element(atom_config_dict, atom_order_str):
    for dimen, dimen_dict in atom_config_dict.items():
        if dimen_dict.get(kw.INSERT) is not None:
            dimen_insert = dimen_dict.get(kw.INSERT)
            if dimen_insert.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.INSERT} {dimen_insert.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.UPDATE) is not None:
            dimen_update = dimen_dict.get(kw.UPDATE)
            if dimen_update.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.UPDATE} {dimen_update.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.DELETE) is not None:
            dimen_delete = dimen_dict.get(kw.DELETE)
            if dimen_delete.get(atom_order_str) is None:
                x_str = f"Missing from {dimen} {kw.DELETE} {dimen_delete.get(atom_order_str)=}"
                print(x_str)
                return False

        if dimen_dict.get(kw.normal_specs) is None:
            print(f"{dimen=} {kw.normal_specs} is missing")
            return False
    return True


def test_get_atom_config_dict_EveryCrudOperationHasPersonDeltaOrderGroup():
    # ESTABLISH
    atom_order_str = "atom_order"
    mog = atom_order_str

    # WHEN / THEN
    assert _check_every_crud_dict_has_element(get_atom_config_dict(), atom_order_str)
    # # Simple script for editing atom_config.json
    # set_mog(kw.INSERT, kw.person_contactunit, 0)
    # set_mog(kw.INSERT, kw.person_contact_membership, 1)
    # set_mog(kw.INSERT, kw.person_planunit, 2)
    # set_mog(kw.INSERT, kw.person_plan_awardunit, 3)
    # set_mog(kw.INSERT, kw.person_plan_laborunit, 4)
    # set_mog(kw.INSERT, kw.person_plan_healerunit, 5)
    # set_mog(kw.INSERT, kw.person_plan_factunit, 6)
    # set_mog(kw.INSERT, kw.person_plan_reasonunit, 7)
    # set_mog(kw.INSERT, kw.person_plan_reason_caseunit, 8)
    # set_mog(kw.UPDATE, kw.person_contactunit, 9)
    # set_mog(kw.UPDATE, kw.person_contact_membership, 10)
    # set_mog(kw.UPDATE, kw.person_planunit, 11)
    # set_mog(kw.UPDATE, kw.person_plan_awardunit, 12)
    # set_mog(kw.UPDATE, kw.person_plan_factunit, 13)
    # set_mog(kw.UPDATE, kw.person_plan_reason_caseunit, 14)
    # set_mog(kw.UPDATE, kw.person_plan_reasonunit, 15)
    # set_mog(kw.DELETE, kw.person_plan_reason_caseunit, 16)
    # set_mog(kw.DELETE, kw.person_plan_reasonunit, 17)
    # set_mog(kw.DELETE, kw.person_plan_factunit, 18)
    # set_mog(kw.DELETE, kw.person_plan_laborunit, 19)
    # set_mog(kw.DELETE, kw.person_plan_healerunit, 20)
    # set_mog(kw.DELETE, kw.person_plan_awardunit, 21)
    # set_mog(kw.DELETE, kw.person_planunit, 22)
    # set_mog(kw.DELETE, kw.person_contact_membership, 23)
    # set_mog(kw.DELETE, kw.person_contactunit, 24)
    # set_mog(kw.UPDATE, kw.personunit, 25)

    assert 0 == q_order(kw.INSERT, kw.person_contactunit)
    assert 1 == q_order(kw.INSERT, kw.person_contact_membership)
    assert 2 == q_order(kw.INSERT, kw.person_planunit)
    assert 3 == q_order(kw.INSERT, kw.person_plan_awardunit)
    assert 4 == q_order(kw.INSERT, kw.person_plan_laborunit)
    assert 5 == q_order(kw.INSERT, kw.person_plan_healerunit)
    assert 6 == q_order(kw.INSERT, kw.person_plan_factunit)
    assert 7 == q_order(kw.INSERT, kw.person_plan_reasonunit)
    assert 8 == q_order(kw.INSERT, kw.person_plan_reason_caseunit)
    assert 9 == q_order(kw.UPDATE, kw.person_contactunit)
    assert 10 == q_order(kw.UPDATE, kw.person_contact_membership)
    assert 11 == q_order(kw.UPDATE, kw.person_planunit)
    assert 12 == q_order(kw.UPDATE, kw.person_plan_awardunit)
    assert 13 == q_order(kw.UPDATE, kw.person_plan_factunit)
    assert 14 == q_order(kw.UPDATE, kw.person_plan_reason_caseunit)
    assert 15 == q_order(kw.UPDATE, kw.person_plan_reasonunit)
    assert 16 == q_order(kw.DELETE, kw.person_plan_reason_caseunit)
    assert 17 == q_order(kw.DELETE, kw.person_plan_reasonunit)
    assert 18 == q_order(kw.DELETE, kw.person_plan_factunit)
    assert 19 == q_order(kw.DELETE, kw.person_plan_laborunit)
    assert 20 == q_order(kw.DELETE, kw.person_plan_healerunit)
    assert 21 == q_order(kw.DELETE, kw.person_plan_awardunit)
    assert 22 == q_order(kw.DELETE, kw.person_planunit)
    assert 23 == q_order(kw.DELETE, kw.person_contact_membership)
    assert 24 == q_order(kw.DELETE, kw.person_contactunit)
    assert 25 == q_order(kw.UPDATE, kw.personunit)


def person_config_jkeys(person_config: dict[str, dict], dimen: str) -> set[str]:
    """Return expected atom_config jkeys from person_config"""
    jkeys = set(person_config.get(dimen).get(kw.jkeys).keys())
    jkeys.remove(kw.person_name)
    return jkeys


def person_config_jvalues(person_config: dict[str, dict], dimen: str) -> set[str]:
    """Return expected atom_config jvalues from person_config"""
    expected_jvalues = set()
    for jvalue_arg, jvalue_dict in person_config.get(dimen).get(kw.jvalues).items():
        if jvalue_dict.get("calc_by_conpute") == False:
            expected_jvalues.add(jvalue_arg)
    if kw.knot in expected_jvalues:
        expected_jvalues.remove(kw.knot)
    return expected_jvalues


def test_get_atom_config_dict_CheckPersonConfigArgs():
    # ESTABLISH
    p_config = get_person_config_dict()

    # WHEN / THEN
    # print(person_config.get(kw.personunit).get(kw.jkeys).keys())
    # print(person_config.get(kw.person_contact_membership).get(kw.jkeys).keys())
    # print(person_config.get(kw.person_plan_reasonunit).get(kw.jvalues).keys())
    prnmemb_k_args = person_config_jkeys(p_config, kw.person_contact_membership)
    prncont_k_args = person_config_jkeys(p_config, kw.person_contactunit)
    prnawar_k_args = person_config_jkeys(p_config, kw.person_plan_awardunit)
    prnfact_k_args = person_config_jkeys(p_config, kw.person_plan_factunit)
    prnheal_k_args = person_config_jkeys(p_config, kw.person_plan_healerunit)
    prncase_k_args = person_config_jkeys(p_config, kw.person_plan_reason_caseunit)
    prnreas_k_args = person_config_jkeys(p_config, kw.person_plan_reasonunit)
    prnplan_k_args = person_config_jkeys(p_config, kw.person_planunit)
    prnunit_k_args = person_config_jkeys(p_config, kw.personunit)
    prnmemb_v_args = person_config_jvalues(p_config, kw.person_contact_membership)
    prncont_v_args = person_config_jvalues(p_config, kw.person_contactunit)
    prnawar_v_args = person_config_jvalues(p_config, kw.person_plan_awardunit)
    prnfact_v_args = person_config_jvalues(p_config, kw.person_plan_factunit)
    prnheal_v_args = person_config_jvalues(p_config, kw.person_plan_healerunit)
    prncase_v_args = person_config_jvalues(p_config, kw.person_plan_reason_caseunit)
    prnreas_v_args = person_config_jvalues(p_config, kw.person_plan_reasonunit)
    prnplan_v_args = person_config_jvalues(p_config, kw.person_planunit)
    prnunit_v_args = person_config_jvalues(p_config, kw.personunit)

    assert prnmemb_k_args == atom_config_k_args(kw.person_contact_membership)
    assert prncont_k_args == atom_config_k_args(kw.person_contactunit)
    assert prnawar_k_args == atom_config_k_args(kw.person_plan_awardunit)
    assert prnfact_k_args == atom_config_k_args(kw.person_plan_factunit)
    assert prnheal_k_args == atom_config_k_args(kw.person_plan_healerunit)
    assert prncase_k_args == atom_config_k_args(kw.person_plan_reason_caseunit)
    assert prnreas_k_args == atom_config_k_args(kw.person_plan_reasonunit)
    assert prnplan_k_args == atom_config_k_args(kw.person_planunit)
    assert prnunit_k_args == atom_config_k_args(kw.personunit)

    assert prnmemb_v_args == atom_config_v_args(kw.person_contact_membership)
    assert prncont_v_args == atom_config_v_args(kw.person_contactunit)
    assert prnawar_v_args == atom_config_v_args(kw.person_plan_awardunit)
    assert prnfact_v_args == atom_config_v_args(kw.person_plan_factunit)
    assert prnheal_v_args == atom_config_v_args(kw.person_plan_healerunit)
    assert prncase_v_args == atom_config_v_args(kw.person_plan_reason_caseunit)
    assert prnreas_v_args == atom_config_v_args(kw.person_plan_reasonunit)
    assert prnplan_v_args == atom_config_v_args(kw.person_planunit)
    assert prnunit_v_args == atom_config_v_args(kw.personunit)


def atom_config_k_args(x_dimen: str) -> set[str]:
    jkeys_key_list = [x_dimen, kw.jkeys]
    return set(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list).keys())


def atom_config_v_args(x_dimen: str) -> set[int]:
    jvalues_key_list = [x_dimen, kw.jvalues]
    return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


def _get_atom_config_jkeys_len(x_dimen: str) -> int:
    return len(atom_config_k_args(x_dimen))


def _get_atom_config_jvalues_len(x_dimen: str) -> int:
    return len(atom_config_v_args(x_dimen))


def test_get_atom_config_dict_CheckEachDimenArgCount():
    # ESTABLISH / WHEN / THEN
    assert _get_atom_config_jkeys_len(kw.personunit) == 0
    assert _get_atom_config_jkeys_len(kw.person_contactunit) == 1
    assert _get_atom_config_jkeys_len(kw.person_contact_membership) == 2
    assert _get_atom_config_jkeys_len(kw.person_planunit) == 1
    assert _get_atom_config_jkeys_len(kw.person_plan_awardunit) == 2
    assert _get_atom_config_jkeys_len(kw.person_plan_reasonunit) == 2
    assert _get_atom_config_jkeys_len(kw.person_plan_reason_caseunit) == 3
    assert _get_atom_config_jkeys_len(kw.person_plan_laborunit) == 2
    assert _get_atom_config_jkeys_len(kw.person_plan_healerunit) == 2
    assert _get_atom_config_jkeys_len(kw.person_plan_factunit) == 2

    assert _get_atom_config_jvalues_len(kw.personunit) == 7
    assert _get_atom_config_jvalues_len(kw.person_contactunit) == 2
    assert _get_atom_config_jvalues_len(kw.person_contact_membership) == 2
    assert _get_atom_config_jvalues_len(kw.person_planunit) == 11
    assert _get_atom_config_jvalues_len(kw.person_plan_awardunit) == 2
    assert _get_atom_config_jvalues_len(kw.person_plan_reasonunit) == 1
    assert _get_atom_config_jvalues_len(kw.person_plan_reason_caseunit) == 3
    assert _get_atom_config_jvalues_len(kw.person_plan_laborunit) == 1
    assert _get_atom_config_jvalues_len(kw.person_plan_healerunit) == 0
    assert _get_atom_config_jvalues_len(kw.person_plan_factunit) == 3


def _has_every_element(x_arg, x_dict) -> bool:
    arg_elements = {kw.class_type, kw.sqlite_datatype, kw.column_ordinal}
    for arg_element in arg_elements:
        if x_dict.get(arg_element) is None:
            print(f"{arg_element} failed for {x_arg=}")
            return False
    return True


def _every_dimen_dict_has_arg_elements(dimen_dict: dict) -> bool:
    for jkey, x_dict in dimen_dict.get(kw.jkeys).items():
        if not _has_every_element(jkey, x_dict):
            return False
    if dimen_dict.get(kw.jvalues) is not None:
        for jvalue, x_dict in dimen_dict.get(kw.jvalues).items():
            if not _has_every_element(jvalue, x_dict):
                return False
    return True


def check_every_arg_dict_has_elements(atom_config_dict):
    for dimen_key, dimen_dict in atom_config_dict.items():
        print(f"{dimen_key=}")
        assert _every_dimen_dict_has_arg_elements(dimen_dict)
    return True


def test_atom_config_AllArgsHave_class_type_sqlite_datatype():
    # ESTABLISH / WHEN / THEN
    assert check_every_arg_dict_has_elements(get_atom_config_dict())


def check_necessary_nesting_order_exists() -> bool:
    atom_config = get_atom_config_dict()
    multi_jkey_dict = {}
    for atom_key, atom_value in atom_config.items():
        jkeys = atom_value.get(kw.jkeys)
        if len(jkeys) > 1:
            multi_jkey_dict[atom_key] = jkeys
    # print(f"{multi_jkey_dict.keys()=}")
    for atom_key, jkeys in multi_jkey_dict.items():
        for jkey_key, jkeys_dict in jkeys.items():
            jkey_nesting_order = jkeys_dict.get(kw.nesting_order)
            print(f"{atom_key=} {jkey_key=} {jkey_nesting_order=}")
            if jkey_nesting_order is None:
                return False
    return True


def test_atom_config_NestingOrderExists():
    # When ChangUnit places an PersonAtom in a nested dictionary ChangUnit.personatoms
    # the order of required argments decides the location. The order must be
    # the same. All atom_config elements with two or more required args
    # must assign to each of those args a nesting order

    # ESTABLISH / WHEN / THEN
    # grab every atom_config with multiple required args
    assert check_necessary_nesting_order_exists()


def _get_atom_config_jvalue_keys(x_dimen: str) -> set[str]:
    jvalues_key_list = [x_dimen, kw.jvalues]
    return set(get_from_nested_dict(get_atom_config_dict(), jvalues_key_list).keys())


def _get_atom_config_jkey_keys(x_dimen: str) -> set[str]:
    jkeys_key_list = [x_dimen, kw.jkeys]
    return set(get_from_nested_dict(get_atom_config_dict(), jkeys_key_list).keys())


def unique_jvalues():
    jvalue_keys = set()
    jvalue_key_count = 0
    for atom_dimen in get_atom_config_dict().keys():
        new_jvalue_keys = _get_atom_config_jvalue_keys(atom_dimen)
        jvalue_key_count += len(new_jvalue_keys)
        jvalue_keys.update(new_jvalue_keys)
        # print(f"{atom_dimen} {_get_atom_config_jvalue_keys(atom_dimen)}")
    return jvalue_keys, jvalue_key_count


def test_get_atom_config_dict_CheckEveryOptionalArgHasUniqueKey():
    # ESTABLISH / WHEN
    jvalue_keys, jvalue_key_count = unique_jvalues()

    # THEN
    print(f"{jvalue_key_count=} {len(jvalue_keys)=}")
    assert jvalue_key_count == len(jvalue_keys)


def unique_jkeys():
    jkey_keys = set()
    jkey_key_count = 0
    for atom_dimen in get_atom_config_dict().keys():
        new_jkey_keys = _get_atom_config_jkey_keys(atom_dimen)
        if kw.plan_rope in new_jkey_keys:
            new_jkey_keys.remove(kw.plan_rope)
        if kw.reason_context in new_jkey_keys:
            new_jkey_keys.remove(kw.reason_context)
        if kw.contact_name in new_jkey_keys:
            new_jkey_keys.remove(kw.contact_name)
        if kw.group_title in new_jkey_keys:
            new_jkey_keys.remove(kw.group_title)
        print(f"{atom_dimen} {new_jkey_keys=}")
        jkey_key_count += len(new_jkey_keys)
        jkey_keys.update(new_jkey_keys)
    return jkey_keys, jkey_key_count


def test_get_atom_config_dict_SomeRequiredArgAreUnique():
    # ESTABLISH / WHEN
    jkey_keys, jkey_key_count = unique_jkeys()

    # THEN
    print(f"{jkey_key_count=} {len(jkey_keys)=}")
    assert jkey_key_count == len(jkey_keys)


def test_get_sorted_jkey_keys_ReturnsObj_person_contactunit():
    # ESTABLISH
    x_dimen = kw.person_contactunit

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [kw.contact_name]


def test_get_sorted_jkey_keys_ReturnsObj_person_plan_reason_caseunit():
    # ESTABLISH
    x_dimen = kw.person_plan_reason_caseunit

    # WHEN
    x_sorted_jkey_keys = get_sorted_jkey_keys(x_dimen)

    # THEN
    assert x_sorted_jkey_keys == [
        kw.plan_rope,
        kw.reason_context,
        kw.reason_state,
    ]


def test_get_flattened_atom_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    atom_columns = get_flattened_atom_table_build()

    # THEN
    assert len(atom_columns) == 103
    assert atom_columns.get("personunit_UPDATE_credor_respect") == "REAL"
    # print(f"{atom_columns.keys()=}")


def test_get_normalized_person_table_build_ReturnsObj():
    # ESTABLISH / WHEN
    normalized_person_table_build = get_normalized_person_table_build()
    nx = normalized_person_table_build

    # THEN
    assert len(nx) == 10
    cat_personunit = nx.get(kw.personunit)
    cat_contactunit = nx.get(kw.person_contactunit)
    cat_membership = nx.get(kw.person_contact_membership)
    cat_plan = nx.get(kw.person_planunit)
    cat_awardunit = nx.get(kw.person_plan_awardunit)
    cat_reason = nx.get(kw.person_plan_reasonunit)
    cat_case = nx.get(kw.person_plan_reason_caseunit)
    cat_laborunit = nx.get(kw.person_plan_laborunit)
    cat_healerunit = nx.get(kw.person_plan_healerunit)
    cat_fact = nx.get(kw.person_plan_factunit)

    assert cat_personunit is not None
    assert cat_contactunit is not None
    assert cat_membership is not None
    assert cat_plan is not None
    assert cat_awardunit is not None
    assert cat_reason is not None
    assert cat_case is not None
    assert cat_laborunit is not None
    assert cat_healerunit is not None
    assert cat_fact is not None

    normal_specs_personunit = cat_personunit.get(kw.normal_specs)
    normal_specs_contactunit = cat_contactunit.get(kw.normal_specs)
    normal_specs_membership = cat_membership.get(kw.normal_specs)
    normal_specs_plan = cat_plan.get(kw.normal_specs)
    normal_specs_awardunit = cat_awardunit.get(kw.normal_specs)
    normal_specs_reason = cat_reason.get(kw.normal_specs)
    normal_specs_case = cat_case.get(kw.normal_specs)
    normal_specs_laborunit = cat_laborunit.get(kw.normal_specs)
    normal_specs_healerunit = cat_healerunit.get(kw.normal_specs)
    normal_specs_fact = cat_fact.get(kw.normal_specs)

    columns_str = "columns"
    print(f"{cat_personunit.keys()=}")
    print(f"{kw.normal_specs=}")
    assert normal_specs_personunit is not None
    assert normal_specs_contactunit is not None
    assert normal_specs_membership is not None
    assert normal_specs_plan is not None
    assert normal_specs_awardunit is not None
    assert normal_specs_reason is not None
    assert normal_specs_case is not None
    assert normal_specs_laborunit is not None
    assert normal_specs_healerunit is not None
    assert normal_specs_fact is not None

    table_name_personunit = normal_specs_personunit.get(kw.normal_table_name)
    table_name_contactunit = normal_specs_contactunit.get(kw.normal_table_name)
    table_name_membership = normal_specs_membership.get(kw.normal_table_name)
    table_name_plan = normal_specs_plan.get(kw.normal_table_name)
    table_name_awardunit = normal_specs_awardunit.get(kw.normal_table_name)
    table_name_reason = normal_specs_reason.get(kw.normal_table_name)
    table_name_case = normal_specs_case.get(kw.normal_table_name)
    table_name_laborunit = normal_specs_laborunit.get(kw.normal_table_name)
    table_name_healerunit = normal_specs_healerunit.get(kw.normal_table_name)
    table_name_fact = normal_specs_fact.get(kw.normal_table_name)

    assert table_name_personunit == "person"
    assert table_name_contactunit == "contactunit"
    assert table_name_membership == "membership"
    assert table_name_plan == "plan"
    assert table_name_awardunit == "awardunit"
    assert table_name_reason == "reason"
    assert table_name_case == "case"
    assert table_name_laborunit == "laborunit"
    assert table_name_healerunit == kw.healerunit
    assert table_name_fact == "fact"

    assert len(cat_personunit) == 2
    assert cat_personunit.get(columns_str) is not None

    personunit_columns = cat_personunit.get(columns_str)
    assert len(personunit_columns) == 8
    assert personunit_columns.get(kw.plan_uid) is not None
    assert personunit_columns.get(kw.max_tree_traverse) is not None
    assert personunit_columns.get(kw.credor_respect) is not None
    assert personunit_columns.get(kw.debtor_respect) is not None
    assert personunit_columns.get(kw.fund_pool) is not None
    assert personunit_columns.get(kw.fund_grain) is not None
    assert personunit_columns.get(kw.respect_grain) is not None
    assert personunit_columns.get(kw.mana_grain) is not None

    assert len(cat_contactunit) == 2
    contactunit_columns = cat_contactunit.get(columns_str)
    assert len(contactunit_columns) == 4
    assert contactunit_columns.get(kw.plan_uid) is not None
    assert contactunit_columns.get(kw.contact_name) is not None
    assert contactunit_columns.get(kw.contact_cred_lumen) is not None
    assert contactunit_columns.get(kw.contact_debt_lumen) is not None

    contact_name_dict = contactunit_columns.get(kw.contact_name)
    assert len(contact_name_dict) == 2
    assert contact_name_dict.get(kw.sqlite_datatype) == "TEXT"
    assert contact_name_dict.get("nullable") is False
    contact_debt_lumen_dict = contactunit_columns.get("contact_debt_lumen")
    assert len(contact_name_dict) == 2
    assert contact_debt_lumen_dict.get(kw.sqlite_datatype) == "REAL"
    assert contact_debt_lumen_dict.get("nullable") is True

    assert len(cat_plan) == 2
    plan_columns = cat_plan.get(columns_str)
    assert len(plan_columns) == 13
    assert plan_columns.get(kw.plan_uid) is not None
    assert plan_columns.get(kw.plan_rope) is not None
    assert plan_columns.get(kw.begin) is not None
    assert plan_columns.get(kw.close) is not None

    gogo_want_dict = plan_columns.get(kw.gogo_want)
    stop_want_dict = plan_columns.get(kw.stop_want)
    assert len(gogo_want_dict) == 2
    assert len(stop_want_dict) == 2
    assert gogo_want_dict.get(kw.sqlite_datatype) == "REAL"
    assert stop_want_dict.get(kw.sqlite_datatype) == "REAL"
    assert gogo_want_dict.get("nullable") is True
    assert stop_want_dict.get("nullable") is True


def test_get_atom_args_dimen_mapping_ReturnsObj():
    # ESTABLISH / WHEN
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()

    # THEN
    assert x_atom_args_dimen_mapping
    assert x_atom_args_dimen_mapping.get(kw.stop_want)
    assert x_atom_args_dimen_mapping.get(kw.stop_want) == {kw.person_planunit}
    assert x_atom_args_dimen_mapping.get(kw.plan_rope)
    rope_dimens = x_atom_args_dimen_mapping.get(kw.plan_rope)
    assert kw.person_plan_factunit in rope_dimens
    assert kw.person_plan_laborunit in rope_dimens
    assert len(rope_dimens) == 7
    assert len(x_atom_args_dimen_mapping) == 41


def get_class_type(x_dimen: str, x_arg: str) -> str:
    atom_config_dict = get_atom_config_dict()
    dimen_dict = atom_config_dict.get(x_dimen)
    optional_dict = dimen_dict.get(kw.jvalues)
    required_dict = dimen_dict.get(kw.jkeys)
    arg_dict = {}
    if optional_dict.get(x_arg):
        arg_dict = dimen_dict.get(kw.jvalues).get(x_arg)
    if required_dict.get(x_arg):
        arg_dict = required_dict.get(x_arg)
    return arg_dict.get(kw.class_type)


def test_get_class_type_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_class_type(kw.person_contactunit, kw.contact_name) == kw.NameTerm
    assert get_class_type(kw.person_planunit, kw.gogo_want) == "float"


def test_get_allowed_class_types_ReturnsObj():
    # ESTABLISH
    x_allowed_class_types = {
        "int",
        kw.ReasonNum,
        kw.FactNum,
        kw.NameTerm,
        kw.TitleTerm,
        kw.LabelTerm,
        kw.RopeTerm,
        kw.KnotTerm,
        "float",
        "bool",
    }

    # WHEN / THEN
    assert get_allowed_class_types() == x_allowed_class_types


def test_get_atom_config_dict_ValidatePythonTypes():
    # make sure all atom config python types are valid and repeated args are the same
    # ESTABLISH WHEN / THEN
    assert all_atom_config_class_types_are_valid(get_allowed_class_types())


def all_atom_config_class_types_are_valid(allowed_class_types):
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
    for x_atom_arg, dimens in x_atom_args_dimen_mapping.items():
        old_class_type = None
        x_class_type = ""
        for x_dimen in dimens:
            x_class_type = get_class_type(x_dimen, x_atom_arg)
            # print(f"{x_class_type=} {x_atom_arg=} {x_dimen=}")
            if x_class_type not in allowed_class_types:
                return False

            if old_class_type is None:
                old_class_type = x_class_type
            # confirm each atom_arg has same data type in all dimens
            print(f"{x_class_type=} {old_class_type=} {x_atom_arg=} {x_dimen=}")
            if x_class_type != old_class_type:
                return False
            old_class_type = x_class_type
    return True


def all_atom_args_class_types_are_correct(x_class_types) -> bool:
    x_atom_args_dimen_mapping = get_atom_args_dimen_mapping()
    x_sorted_class_types = sorted(list(x_class_types.keys()))
    for x_atom_arg in x_sorted_class_types:
        x_dimens = list(x_atom_args_dimen_mapping.get(x_atom_arg))
        x_dimen = x_dimens[0]
        x_class_type = get_class_type(x_dimen, x_atom_arg)
        print(
            f"assert x_class_types.get({x_atom_arg}) == {x_class_type} {x_class_types.get(x_atom_arg)=}"
        )
        if x_class_types.get(x_atom_arg) != x_class_type:
            return False
    return True


def test_get_atom_args_class_types_ReturnsObj():
    # ESTABLISH / WHEN
    x_class_types = get_atom_args_class_types()

    # THEN
    assert x_class_types.get(kw.contact_name) == kw.NameTerm
    assert x_class_types.get(kw.addin) == "float"
    assert x_class_types.get(kw.awardee_title) == kw.TitleTerm
    assert x_class_types.get(kw.reason_context) == kw.RopeTerm
    assert x_class_types.get(kw.active_requisite) == "bool"
    assert x_class_types.get(kw.begin) == "float"
    assert x_class_types.get(kw.respect_grain) == "float"
    assert x_class_types.get(kw.close) == "float"
    assert x_class_types.get(kw.contact_cred_lumen) == "float"
    assert x_class_types.get(kw.group_cred_lumen) == "float"
    assert x_class_types.get(kw.credor_respect) == "float"
    assert x_class_types.get(kw.contact_debt_lumen) == "float"
    assert x_class_types.get(kw.group_debt_lumen) == "float"
    assert x_class_types.get(kw.debtor_respect) == "float"
    assert x_class_types.get(kw.denom) == "int"
    assert x_class_types.get(kw.reason_divisor) == "int"
    assert x_class_types.get(kw.fact_context) == kw.RopeTerm
    assert x_class_types.get(kw.fact_upper) == kw.FactNum
    assert x_class_types.get(kw.fact_lower) == kw.FactNum
    assert x_class_types.get(kw.fund_grain) == "float"
    assert x_class_types.get(kw.fund_pool) == "float"
    assert x_class_types.get(kw.give_force) == "float"
    assert x_class_types.get(kw.gogo_want) == "float"
    assert x_class_types.get(kw.group_title) == kw.TitleTerm
    assert x_class_types.get(kw.healer_name) == kw.NameTerm
    assert x_class_types.get(kw.star) == "int"
    assert x_class_types.get(kw.max_tree_traverse) == "int"
    assert x_class_types.get(kw.morph) == "bool"
    assert x_class_types.get(kw.reason_state) == kw.RopeTerm
    assert x_class_types.get(kw.reason_upper) == kw.ReasonNum
    assert x_class_types.get(kw.numor) == "int"
    assert x_class_types.get(kw.reason_lower) == kw.ReasonNum
    assert x_class_types.get(kw.mana_grain) == "float"
    assert x_class_types.get(kw.fact_state) == kw.RopeTerm
    assert x_class_types.get(kw.pledge) == "bool"
    assert x_class_types.get(kw.problem_bool) == "bool"
    assert x_class_types.get(kw.plan_rope) == kw.RopeTerm
    assert x_class_types.get(kw.solo) == "int"
    assert x_class_types.get(kw.stop_want) == "float"
    assert x_class_types.get(kw.take_force) == "float"
    assert x_class_types.get(kw.labor_title) == kw.TitleTerm
    assert x_class_types.keys() == get_atom_args_dimen_mapping().keys()
    assert all_atom_args_class_types_are_correct(x_class_types)
