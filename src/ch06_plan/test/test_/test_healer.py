from ch06_plan.healer import HealerUnit, get_healerunit_from_dict, healerunit_shop
from ref.keywords import ExampleStrs as exx


def test_HealerUnit_Exists():
    # ESTABLISH
    run_healer_names = {exx.run}

    # WHEN
    x_healerunit = HealerUnit(healer_names=run_healer_names)

    # THEN
    assert x_healerunit
    assert x_healerunit.healer_names == run_healer_names


def test_healerunit_shop_ReturnsWithCorrectAttributes_v1():
    # ESTABLISH
    run_healer_names = {exx.run}

    # WHEN
    x_healerunit = healerunit_shop(healer_names=run_healer_names)

    # THEN
    assert x_healerunit
    assert x_healerunit.healer_names == run_healer_names


def test_healerunit_shop_ifEmptyReturnsWithCorrectAttributes():
    # ESTABLISH / WHEN
    x_healerunit = healerunit_shop()

    # THEN
    assert x_healerunit
    assert x_healerunit.healer_names == set()


def test_HealerUnit_to_dict_ReturnsDictWithSingle_group_title():
    # ESTABLISH
    bob_healer_name = "Bob"
    run_healer_names = {bob_healer_name}
    x_healerunit = healerunit_shop(healer_names=run_healer_names)

    # WHEN
    obj_dict = x_healerunit.to_dict()

    # THEN
    assert obj_dict is not None
    run_list = [bob_healer_name]
    example_dict = {"healerunit_healer_names": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerUnit_set_healer_name_Sets_healer_names_v1():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    assert len(x_healerunit.healer_names) == 0

    # WHEN
    x_healerunit.set_healer_name(x_healer_name=exx.yao)

    # THEN
    assert len(x_healerunit.healer_names) == 1


def test_HealerUnit_del_healer_name_Deletes_healer_names_v1():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    x_healerunit.set_healer_name(x_healer_name=exx.yao)
    x_healerunit.set_healer_name(x_healer_name=exx.sue)
    assert len(x_healerunit.healer_names) == 2

    # WHEN
    x_healerunit.del_healer_name(x_healer_name=exx.sue)

    # THEN
    assert len(x_healerunit.healer_names) == 1


def test_HealerUnit_healer_name_exists_ReturnsObj():
    # ESTABLISH
    x_healerunit = healerunit_shop()
    assert x_healerunit.healer_name_exists(exx.yao) is False
    assert x_healerunit.healer_name_exists(exx.sue) is False

    # WHEN
    x_healerunit.set_healer_name(x_healer_name=exx.yao)

    # THEN
    assert x_healerunit.healer_name_exists(exx.yao)
    assert x_healerunit.healer_name_exists(exx.sue) is False


def test_HealerUnit_any_healer_name_exists_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_healerunit = healerunit_shop()
    assert x_healerunit.any_healer_name_exists() is False

    # WHEN / THEN
    x_healerunit.set_healer_name(x_healer_name=exx.sue)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    x_healerunit.set_healer_name(x_healer_name=exx.yao)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    x_healerunit.del_healer_name(x_healer_name=exx.yao)
    assert x_healerunit.any_healer_name_exists()

    # WHEN / THEN
    x_healerunit.del_healer_name(x_healer_name=exx.sue)
    assert x_healerunit.any_healer_name_exists() is False


def test_get_healerunit_from_dict_ReturnsObj():
    # ESTABLISH
    empty_dict = {}

    # WHEN / THEN
    assert get_healerunit_from_dict(empty_dict) == healerunit_shop()

    # WHEN / THEN
    static_healerunit = healerunit_shop()
    static_healerunit.set_healer_name(x_healer_name=exx.sue)
    static_healerunit.set_healer_name(x_healer_name=exx.yao)

    sue_dict = {"healerunit_healer_names": [exx.sue, exx.yao]}
    assert get_healerunit_from_dict(sue_dict) == static_healerunit
