from src.ch07_person_logic.person_main import personunit_shop
from src.ch08_person_atom.atom_main import personatom_shop
from src.ch09_person_lesson.delta import persondelta_shop
from src.ch09_person_lesson.legible import create_legible_list
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def test_create_legible_list_ReturnsObj_contact_membership_INSERT():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_contact_membership
    bowlers_str = f"{sue_person.knot}bowlers"
    group_cred_lumen_value = 81
    group_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.INSERT)
    yao_personatom.set_arg(kw.group_title, bowlers_str)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(kw.group_cred_lumen, group_cred_lumen_value)
    yao_personatom.set_arg(kw.group_debt_lumen, group_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Group '{bowlers_str}' has new membership {exx.yao} with group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_contact_membership_UPDATE_group_cred_lumen_group_debt_lumen():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_contact_membership
    group_cred_lumen_str = kw.group_cred_lumen
    group_debt_lumen_str = kw.group_debt_lumen
    bowlers_str = f"{sue_person.knot}bowlers"
    group_cred_lumen_value = 81
    group_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.group_title, bowlers_str)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(group_cred_lumen_str, group_cred_lumen_value)
    yao_personatom.set_arg(group_debt_lumen_str, group_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Group '{bowlers_str}' membership {exx.yao} has new group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_contact_membership_UPDATE_group_cred_lumen():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_contact_membership
    group_cred_lumen_str = kw.group_cred_lumen
    bowlers_str = f"{sue_person.knot}bowlers"
    group_cred_lumen_value = 81
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.group_title, bowlers_str)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(group_cred_lumen_str, group_cred_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Group '{bowlers_str}' membership {exx.yao} has new group_cred_lumen_value{group_cred_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_contact_membership_UPDATE_group_debt_lumen():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_contact_membership
    group_debt_lumen_str = kw.group_debt_lumen
    bowlers_str = f"{sue_person.knot}bowlers"
    group_debt_lumen_value = 43
    yao_personatom = personatom_shop(dimen, kw.UPDATE)
    yao_personatom.set_arg(kw.group_title, bowlers_str)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    yao_personatom.set_arg(group_debt_lumen_str, group_debt_lumen_value)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Group '{bowlers_str}' membership {exx.yao} has new group_debt_lumen_value={group_debt_lumen_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_contact_membership_DELETE():
    # ESTABLISH
    sue_person = personunit_shop("Sue")
    dimen = kw.person_contact_membership
    bowlers_str = f"{sue_person.knot}bowlers"
    yao_personatom = personatom_shop(dimen, kw.DELETE)
    yao_personatom.set_arg(kw.group_title, bowlers_str)
    yao_personatom.set_arg(kw.contact_name, exx.yao)
    # print(f"{yao_personatom=}")
    x_persondelta = persondelta_shop()
    x_persondelta.set_personatom(yao_personatom)

    # WHEN
    legible_list = create_legible_list(x_persondelta, sue_person)

    # THEN
    x_str = f"Group '{bowlers_str}' no longer has membership {exx.yao}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
