from src.ch00_py.plotly_toolbox import conditional_fig_show
from src.ch07_person_logic.person_graphic import (
    display_plantree,
    fund_graph0,
    get_person_agenda_plotly_fig,
    get_person_partners_plotly_fig,
)
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_laundry_example1,
    get_personunit_with_4_levels,
    get_personunit_with_4_levels_and_2reasons,
    get_personunit_x1_3levels_1reason_1facts,
    personunit_v001_with_large_agenda,
)
from src.ref.keywords import Ch07Keywords as kw, ExampleStrs as exx


def test_display_plantree_Scenario0(graphics_bool):
    # ESTABLISH
    # a_person = get_1label_person()
    # a_person = get_2label_person()
    # a_person = get_3label_person()
    # a_person = get_5labelHG_person()
    # a_person = get_7labelJroot_person()
    a_person = get_personunit_with_4_levels()
    # a_person = personunit_v001()
    a_person.conpute()
    print(f"Person {a_person.planroot.plan_label}: Labels ({len(a_person._plan_dict)})")

    # WHEN / THEN
    x_fig = display_plantree(a_person, graphics_bool)


def test_display_plantree_Scenario1_shows_case_tasks(graphics_bool):
    # ESTABLISH
    # a_person = get_1label_person()
    # a_person = get_2label_person()
    # a_person = get_3label_person()
    # a_person = get_5labelHG_person()
    # a_person = get_7labelJroot_person()
    a_person = get_personunit_laundry_example1()
    # a_person = personunit_v001()
    a_person.conpute()
    print(f"Person {a_person.planroot.plan_label}: Labels ({len(a_person._plan_dict)})")

    # WHEN / THEN
    display_plantree(a_person, mode=kw.case_task, graphics_bool=graphics_bool)


def test_get_person_partners_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    luca_person = personunit_shop()
    luca_person.set_credor_respect(500)
    luca_person.set_debtor_respect(400)
    yao_partner_cred_lumen = 66
    yao_partner_debt_lumen = 77
    luca_person.add_partnerunit(exx.yao, yao_partner_cred_lumen, yao_partner_debt_lumen)
    sue_partner_cred_lumen = 434
    sue_partner_debt_lumen = 323
    luca_person.add_partnerunit(exx.sue, sue_partner_cred_lumen, sue_partner_debt_lumen)

    # WHEN
    x_fig = get_person_partners_plotly_fig(luca_person)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_person_agenda_plotly_fig_DisplaysInfo(graphics_bool):
    # ESTABLISH
    yao_person = personunit_v001_with_large_agenda()
    assert len(yao_person.get_agenda_dict()) == 69

    # WHEN
    x_fig = get_person_agenda_plotly_fig(yao_person)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_PersonUnit_fund_graph0_VisualizesCirculation(graphics_bool):
    # ESTABLISH
    sue_person = personunit_shop(person_name="Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    cat_str = "cat situation"
    cat_rope = sue_person.make_rope(casa_rope, cat_str)
    hun_n_str = "not hungry"
    hun_n_rope = sue_person.make_rope(cat_rope, hun_n_str)
    hun_y_str = "hungry"
    hun_y_rope = sue_person.make_rope(cat_rope, hun_y_str)
    clean_str = "cleaning"
    clean_rope = sue_person.make_rope(casa_rope, clean_str)
    sweep_rope = sue_person.make_rope(clean_rope, exx.sweep)
    dish_str = "clean dishes"
    dish_rope = sue_person.make_rope(clean_rope, dish_str)
    sue_person.add_plan(casa_rope, star=30)
    sue_person.add_plan(cat_rope, star=30)
    sue_person.add_plan(hun_n_rope, star=30)
    sue_person.add_plan(hun_y_rope, star=30)
    sue_person.add_plan(clean_rope, star=30)
    sue_person.add_plan(sweep_rope, star=30, pledge=True)
    sue_person.add_plan(dish_rope, star=30, pledge=True)
    dinner_str = "cat have dinner"
    dinner_rope = sue_person.make_l1_rope(dinner_str)
    sue_person.add_plan(dinner_rope, star=30, pledge=True)

    # WHEN / THEN
    fund_graph0(sue_person, kw.case_task, graphics_bool)
