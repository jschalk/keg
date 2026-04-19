from ch00_py.plotly_toolbox import conditional_fig_show
from ch08_person_atom.atom_graphic import personatom_periodic_table0

# from ch07_person_logic.test._util.example_persons import (
#     personunit_v001_with_large_agenda,
#     get_personunit_with_4_levels,
#     get_personunit_with_4_levels_and_2reasons,
#     get_personunit_x1_3levels_1reason_1facts,
# )
# from ch07_person_logic.person import personunit_shop


def test_personatom_periodic_table0_ShowsGraph0(graphics_bool):
    # ESTABLISH / WHEN
    personatom_periodic_table0_fig = personatom_periodic_table0()

    # THEN
    conditional_fig_show(personatom_periodic_table0_fig, graphics_bool)
