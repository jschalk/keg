from ch07_person_logic.person_graphic import (
    display_plantree,
    personunit_graph0,
    personunit_graph1,
    personunit_graph2,
    personunit_graph3,
    personunit_graph4,
)
from ch07_person_logic.test._util.ch07_examples import (
    get_personunit_with_4_levels,
    get_personunit_with_4_levels_and_2reasons,
    get_personunit_x1_3levels_1reason_1facts,
)
from ref.keywords import Ch07Keywords as kw


def test_personunit_graph_Showsgraph0PersonGraph(graphics_bool):
    # ESTABLISH / WHEN / THEN
    display_plantree(get_personunit_with_4_levels(), graphics_bool)
    display_plantree(
        get_personunit_with_4_levels_and_2reasons(), kw.case_task, graphics_bool
    )
    display_plantree(get_personunit_x1_3levels_1reason_1facts(), graphics_bool)
    personunit_graph0(graphics_bool)
    personunit_graph1(graphics_bool)
    personunit_graph2(graphics_bool)
    personunit_graph3(graphics_bool)
    personunit_graph4(graphics_bool)
