from pytest import raises as pytest_raises
from src.ch01_allot.allot import default_grain_num_if_None, validate_pool_num
from src.ch04_rope.rope import create_rope, default_knot_if_None, get_default_rope
from src.ch07_person_logic._ref.ch07_semantic_types import RespectNum
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_PersonUnit_Exists():
    # ESTABLISH /  WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person
    assert x_person.person_name is None
    assert x_person.contacts is None
    assert x_person.planroot is None
    assert x_person.credor_respect is None
    assert x_person.debtor_respect is None
    assert x_person.max_tree_traverse is None
    assert x_person.knot is None
    assert x_person.fund_pool is None
    assert x_person.fund_grain is None
    assert x_person.respect_grain is None
    assert x_person.mana_grain is None
    assert x_person.last_lesson_id is None
    # calculated attr
    assert x_person._plan_dict is None
    assert x_person._keep_dict is None
    assert x_person._healers_dict is None
    assert x_person.tree_traverse_count is None
    assert x_person.rational is None
    assert x_person.keeps_justified is None
    assert x_person.keeps_buildable is None
    assert x_person.sum_healerunit_plans_fund_total is None
    assert x_person.offtrack_kids_star_set is None
    assert x_person.offtrack_fund is None
    assert x_person.reason_contexts is None
    assert x_person.range_inheritors is None
    assert str(type(x_person.planroot)).find("None") == 8
    obj_attrs = set(x_person.__dict__.keys())
    print(sorted(list(obj_attrs)))
    assert obj_attrs == {
        "_plan_dict",
        "_healers_dict",
        "_keep_dict",
        kw.keeps_buildable,
        kw.keeps_justified,
        kw.offtrack_fund,
        kw.offtrack_kids_star_set,
        kw.range_inheritors,
        kw.rational,
        kw.reason_contexts,
        kw.sum_healerunit_plans_fund_total,
        kw.tree_traverse_count,
        kw.contacts,
        kw.knot,
        kw.planroot,
        kw.credor_respect,
        kw.debtor_respect,
        kw.groupunits,
        kw.fund_grain,
        kw.fund_pool,
        kw.last_lesson_id,
        kw.max_tree_traverse,
        kw.person_name,
        kw.mana_grain,
        kw.respect_grain,
    }


def test_personunit_shop_ReturnsObj_Scenario0_RaiseErrorWhen_planroot_rope_IsLabel():
    # ESTABLISH
    iowa_str = "Iowa"

    # WHEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_name=exx.sue, planroot_rope=iowa_str, knot=exx.slash)

    # THEN
    exception_str = f"Person '{exx.sue}' cannot set planroot_rope='{iowa_str}' where knot='{exx.slash}'"
    assert str(excinfo.value) == exception_str


def test_personunit_shop_ReturnsObj_Scenario1_WithParameters():
    # ESTABLISH
    slash_knot = "/"
    iowa_rope = create_rope("Iowa", None, slash_knot)
    x_fund_pool = 555
    x_fund_grain = 7
    x_respect_grain = 5
    x_mana_grain = 1

    # WHEN
    x_person = personunit_shop(
        person_name=exx.sue,
        planroot_rope=iowa_rope,
        knot=slash_knot,
        fund_pool=x_fund_pool,
        fund_grain=x_fund_grain,
        respect_grain=x_respect_grain,
        mana_grain=x_mana_grain,
    )

    # THEN
    assert x_person
    assert x_person.person_name == exx.sue
    assert x_person.contacts == {}
    assert x_person.planroot is not None
    assert x_person.planroot.get_plan_rope() == iowa_rope
    assert x_person.max_tree_traverse == 3
    assert x_person.knot == slash_knot
    assert x_person.fund_pool == x_fund_pool
    assert x_person.fund_grain == x_fund_grain
    assert x_person.respect_grain == x_respect_grain
    assert x_person.mana_grain == x_mana_grain
    assert x_person.credor_respect == RespectNum(validate_pool_num())
    assert x_person.debtor_respect == RespectNum(validate_pool_num())
    assert not x_person.last_lesson_id
    # calculated attr
    assert x_person._plan_dict == {}
    assert x_person._keep_dict == {}
    assert x_person._healers_dict == {}
    assert not x_person.tree_traverse_count
    assert x_person.rational is False
    assert x_person.keeps_justified is False
    assert x_person.keeps_buildable is False
    assert x_person.sum_healerunit_plans_fund_total == 0
    assert x_person.offtrack_kids_star_set == set()
    assert not x_person.offtrack_fund
    assert x_person.reason_contexts == set()
    assert x_person.range_inheritors == {}
    print(f"{type(x_person.planroot)=}") == 0
    assert str(type(x_person.planroot)).find(".plan.PlanUnit'>") > 0


def test_personunit_shop_ReturnsObj_Scenario2_WithoutParameters():
    # ESTABLISH / WHEN
    x_person = personunit_shop()

    # THEN
    assert x_person.person_name == ""
    assert x_person.knot == default_knot_if_None()
    assert x_person.fund_pool == validate_pool_num()
    assert x_person.fund_grain == default_grain_num_if_None()
    assert x_person.respect_grain == default_grain_num_if_None()
    assert x_person.mana_grain == default_grain_num_if_None()
    assert x_person.planroot.get_plan_rope() == get_default_rope()
    assert x_person.planroot.fund_grain == x_person.fund_grain
    assert x_person.planroot.knot == x_person.knot
    assert x_person.planroot.plan_uid == 1
    assert x_person.planroot.tree_level == 0
    assert x_person.planroot.knot == x_person.knot
    assert x_person.planroot.parent_rope == ""


def test_PersonUnit_set_max_tree_traverse_SetsInt():
    # ESTABLISH
    zia_person = personunit_shop(person_name=exx.zia)
    assert zia_person.max_tree_traverse == 3

    # WHEN
    zia_person.set_max_tree_traverse(x_int=11)

    # THEN
    assert zia_person.max_tree_traverse == 11


def test_PersonUnit_set_max_tree_traverse_RaisesError_Scenario0():
    # ESTABLISH
    zia_person = personunit_shop(person_name=exx.zia)
    assert zia_person.max_tree_traverse == 3
    zia_tree_traverse = 1

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        zia_person.set_max_tree_traverse(x_int=zia_tree_traverse)
    exception_str = "set_max_tree_traverse: '1' must be number that is 2 or greater"
    assert str(excinfo.value) == exception_str


def test_PersonUnit_set_max_tree_traverse_RaisesError_Scenario1():
    # ESTABLISH
    zia_person = personunit_shop(person_name=exx.zia)
    assert zia_person.max_tree_traverse == 3

    # WHEN / THEN
    zia_tree_traverse = 3.5
    with pytest_raises(Exception) as excinfo:
        zia_person.set_max_tree_traverse(x_int=zia_tree_traverse)
    exception_str = f"set_max_tree_traverse: '{zia_tree_traverse}' must be number that is 2 or greater"
    assert str(excinfo.value) == exception_str


def test_PersonUnit_make_rope_ReturnsObj():
    # ESTABLISH
    slash_knot = "/"
    a45_rope = create_rope("amy45", None, slash_knot)
    sue_person = personunit_shop(exx.sue, a45_rope, knot=slash_knot)
    v1_casa_rope = sue_person.make_l1_rope(exx.casa)

    # WHEN
    v2_casa_rope = sue_person.make_l1_rope(exx.casa)

    # THEN
    assert v1_casa_rope == v2_casa_rope


def test_PersonUnit_set_last_lesson_id_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    assert sue_person.last_lesson_id is None

    # WHEN
    x_last_lesson_id = 89
    sue_person.set_last_lesson_id(x_last_lesson_id)

    # THEN
    assert sue_person.last_lesson_id == x_last_lesson_id


def test_PersonUnit_set_last_lesson_id_RaisesError():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    old_last_lesson_id = 89
    sue_person.set_last_lesson_id(old_last_lesson_id)

    # WHEN / THEN
    new_last_lesson_id = 72
    assert new_last_lesson_id < old_last_lesson_id
    with pytest_raises(Exception) as excinfo:
        sue_person.set_last_lesson_id(new_last_lesson_id)
    exception_str = f"Cannot set _last_lesson_id to {new_last_lesson_id} because it is less than {old_last_lesson_id}."
    assert str(excinfo.value) == exception_str


def test_PersonUnit_del_last_lesson_id_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    old_last_lesson_id = 89
    sue_person.set_last_lesson_id(old_last_lesson_id)
    assert sue_person.last_lesson_id is not None

    # WHEN
    sue_person.del_last_lesson_id()

    # THEN
    assert sue_person.last_lesson_id is None


def test_PersonUnit_set_fund_pool_SetsAttr():
    # ESTABLISH
    sue_person = personunit_shop("Sue", exx.a23)
    sue_fund_pool = 99000
    assert sue_person.fund_pool == validate_pool_num()

    # WHEN
    sue_person.set_fund_pool(sue_fund_pool)

    # THEN
    assert sue_person.fund_pool == 99000


def test_PersonUnit_set_fund_pool_RaisesErrorWhenArgIsNotMultiple():
    # ESTABLISH
    zia_person = personunit_shop(exx.zia)
    x_fund_pool = 23
    zia_person.set_fund_pool(x_fund_pool)
    assert zia_person.fund_grain == 1
    assert zia_person.fund_pool == x_fund_pool

    # WHEN
    new_fund_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_person.set_fund_pool(new_fund_pool)

    # THEN
    exception_str = f"Person '{exx.zia}' cannot set fund_pool='{new_fund_pool}'. It is not divisible by fund_grain '{zia_person.fund_grain}'"
    assert str(excinfo.value) == exception_str
