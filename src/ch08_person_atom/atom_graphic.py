from dataclasses import dataclass
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch08_person_atom.atom_config import get_normal_table_name
from src.ch08_person_atom.atom_main import PersonAtom, personatom_shop


@dataclass
class AtomPlotlyShape:
    x_personatom: PersonAtom
    base_width: float = None
    base_h: float = None
    level: float = None
    level_width0: float = None
    level_width1: float = None
    display_str: str = None
    color: str = None

    def set_attrs(self):
        self.base_width = 0.1
        self.base_h = 0.2
        self.tree_level = 0
        self.tree_level_width0 = 0.1
        self.tree_level_width1 = 0.9
        self.display_str = f"{get_normal_table_name(self.x_personatom.dimen)} {self.x_personatom.crud_str} Order: {self.x_personatom.atom_order}"

    def set_level(self, x_level, x_width0, x_width1, color=None):
        self.tree_level = x_level
        self.tree_level_width0 = x_width0
        self.tree_level_width1 = x_width1
        self.color = color


def get_insert_rect(dimen: str) -> AtomPlotlyShape:
    x_personatom = personatom_shop(dimen, "INSERT")
    x_personatom.set_atom_order()
    atom_rect = AtomPlotlyShape(x_personatom=x_personatom)
    atom_rect.set_attrs()
    return atom_rect


def get_update_rect(dimen: str) -> AtomPlotlyShape:
    x_personatom = personatom_shop(dimen, "UPDATE")
    x_personatom.set_atom_order()
    atom_rect = AtomPlotlyShape(x_personatom=x_personatom)
    atom_rect.set_attrs()
    return atom_rect


def get_delete_rect(dimen: str) -> AtomPlotlyShape:
    x_personatom = personatom_shop(dimen, "DELETE")
    x_personatom.set_atom_order()
    atom_rect = AtomPlotlyShape(x_personatom=x_personatom)
    atom_rect.set_attrs()
    return atom_rect


def add_ch08rect(fig, x, y, text):
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=x,
        y=y,
        text=text,
        showarrow=False,
    )


def add_atom_rect(fig: plotly_Figure, atomplotyshape: AtomPlotlyShape):
    level_bump = atomplotyshape.tree_level * 0.05
    home_form_x0 = atomplotyshape.base_width
    home_form_x1 = 1 - atomplotyshape.base_width
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * atomplotyshape.tree_level_width0)
    shape_x1 = home_form_x0 + (home_width * atomplotyshape.tree_level_width1)
    shape_y0 = level_bump + atomplotyshape.base_h
    shape_y1 = level_bump + atomplotyshape.base_h + 0.05
    x_color = "RoyalBlue" if atomplotyshape.color is None else atomplotyshape.color
    fig.add_shape(
        type="rect",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_ch08rect(fig, x=text_x, y=text_y, text=atomplotyshape.display_str)


def add_groupunits_circle(fig: plotly_Figure):
    home_form_x0 = 0.2
    home_form_x1 = 1 - 0.2
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0 + (home_width * 0.425)
    shape_x1 = home_form_x0 + (home_width * 0.575)
    shape_y0 = 0.325
    shape_y1 = 0.425
    x_color = "Green"
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=8,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = (shape_y0 + shape_y1) / 2
    text_x = (shape_x0 + shape_x1) / 2
    add_ch08rect(fig, x=text_x, y=text_y, text="GroupUnits")


def add_different_plans_circle(fig: plotly_Figure):
    home_form_x0 = 0.2
    home_form_x1 = 1 - 0.2
    home_width = home_form_x1 - home_form_x0
    shape_x0 = home_form_x0
    shape_x1 = home_form_x0 + home_width
    shape_y0 = 0.54
    shape_y1 = 0.75
    x_color = "Grey"
    fig.add_shape(
        type="circle",
        xref="paper",
        yref="paper",
        x0=shape_x0,
        y0=shape_y0,
        x1=shape_x1,
        y1=shape_y1,
        line=dict(
            color=x_color,
            width=3,
        ),
        fillcolor=None,  # "LightSkyBlue",
    )
    text_y = shape_y1 - 0.01
    text_x = (shape_x0 + shape_x1) / 2
    add_ch08rect(fig, x=text_x, y=text_y, text="Different Plans")


def get_personatom_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 4])
    fig.update_yaxes(range=[0, 15])
    return fig


def personatom_periodic_table0() -> plotly_Figure:
    fig = get_personatom_base_fig()

    case_str = "person_plan_reason_caseunit"
    person_partnerunit_insert = get_insert_rect("person_partnerunit")
    person_partner_membership_insert = get_insert_rect("person_partner_membership")
    person_planunit_insert = get_insert_rect("person_planunit")
    person_plan_awardunit_insert = get_insert_rect("person_plan_awardunit")
    person_plan_laborunit_insert = get_insert_rect("person_plan_laborunit")
    person_plan_healerunit_insert = get_insert_rect("person_plan_healerunit")
    person_plan_factunit_insert = get_insert_rect("person_plan_factunit")
    person_plan_reasonunit_insert = get_insert_rect("person_plan_reasonunit")
    person_plan_reason_caseunit_insert = get_insert_rect(case_str)
    person_partnerunit_update = get_update_rect("person_partnerunit")
    person_partner_membership_update = get_update_rect("person_partner_membership")
    person_planunit_update = get_update_rect("person_planunit")
    person_plan_awardunit_update = get_update_rect("person_plan_awardunit")
    person_plan_factunit_update = get_update_rect("person_plan_factunit")
    person_plan_reason_caseunit_update = get_update_rect(case_str)
    person_plan_reasonunit_update = get_update_rect("person_plan_reasonunit")
    person_plan_reason_caseunit_delete = get_delete_rect(case_str)
    person_plan_reasonunit_delete = get_delete_rect("person_plan_reasonunit")
    person_plan_factunit_delete = get_delete_rect("person_plan_factunit")
    person_plan_laborunit_delete = get_delete_rect("person_plan_laborunit")
    person_plan_healerunit_delete = get_delete_rect("person_plan_healerunit")
    person_plan_awardunit_delete = get_delete_rect("person_plan_awardunit")
    person_planunit_delete = get_delete_rect("person_planunit")
    person_partner_membership_delete = get_delete_rect("person_partner_membership")
    person_partnerunit_delete = get_delete_rect("person_partnerunit")
    personunit_update = get_update_rect("personunit")

    green_str = "Green"
    person_partnerunit_insert.set_level(0, 0, 0.25, green_str)
    person_partnerunit_update.set_level(0, 0.25, 0.75, green_str)
    person_partnerunit_delete.set_level(0, 0.75, 1, green_str)
    person_partner_membership_insert.set_level(1, 0, 0.3, green_str)
    person_partner_membership_update.set_level(1, 0.3, 0.7, green_str)
    person_partner_membership_delete.set_level(1, 0.7, 1, green_str)
    person_plan_healerunit_insert.set_level(3, 0.2, 0.4)
    person_plan_healerunit_delete.set_level(3, 0.6, 0.8)
    person_plan_laborunit_insert.set_level(4, 0.2, 0.4)
    person_plan_laborunit_delete.set_level(4, 0.6, 0.8)
    person_plan_awardunit_insert.set_level(5, 0.2, 0.4, green_str)
    person_plan_awardunit_update.set_level(5, 0.4, 0.6, green_str)
    person_plan_awardunit_delete.set_level(5, 0.6, 0.8, green_str)
    person_planunit_insert.set_level(6, 0, 0.3, green_str)
    person_planunit_update.set_level(6, 0.3, 0.7, green_str)
    person_planunit_delete.set_level(6, 0.7, 1, green_str)
    person_plan_reasonunit_insert.set_level(7, 0.2, 0.4)
    person_plan_reasonunit_update.set_level(7, 0.4, 0.6)
    person_plan_reasonunit_delete.set_level(7, 0.6, 0.8)
    person_plan_reason_caseunit_insert.set_level(8, 0.2, 0.4)
    person_plan_reason_caseunit_update.set_level(8, 0.4, 0.6)
    person_plan_reason_caseunit_delete.set_level(8, 0.6, 0.8)
    person_plan_factunit_insert.set_level(9, 0.2, 0.4)
    person_plan_factunit_update.set_level(9, 0.4, 0.6)
    person_plan_factunit_delete.set_level(9, 0.6, 0.8)
    personunit_update.set_level(-2, 0, 1, green_str)

    # person_planunit_insert = get_insert_rect(kw.person_planunit)
    # person_plan_awardunit_insert = get_insert_rect(kw.person_plan_awardunit)
    # person_plan_laborunit_insert = get_insert_rect(kw.person_plan_laborunit)
    # person_plan_healerunit_insert = get_insert_rect(kw.person_plan_healerunit)
    # person_plan_factunit_insert = get_insert_rect(kw.person_plan_factunit)
    # person_plan_reasonunit_insert = get_insert_rect(kw.person_plan_reasonunit)
    # person_plan_reason_caseunit_insert = get_insert_rect(case_str)
    # person_planunit_update = get_update_rect(kw.person_planunit)
    # person_plan_awardunit_update = get_update_rect(kw.person_plan_awardunit)
    # person_plan_factunit_update = get_update_rect(kw.person_plan_factunit)
    # person_plan_reason_caseunit_update = get_update_rect(case_str)
    # person_plan_reasonunit_update = get_update_rect(kw.person_plan_reasonunit)
    # person_plan_reason_caseunit_delete = get_delete_rect(case_str)
    # person_plan_reasonunit_delete = get_delete_rect(kw.person_plan_reasonunit)
    # person_plan_factunit_delete = get_delete_rect(kw.person_plan_factunit)
    # person_plan_laborunit_delete = get_delete_rect(kw.person_plan_laborunit)
    # person_plan_healerunit_delete = get_delete_rect(kw.person_plan_healerunit)
    # person_plan_awardunit_delete = get_delete_rect(kw.person_plan_awardunit)
    # person_planunit_delete = get_delete_rect(kw.person_planunit)
    # personunit_update = get_update_rect(kw.personunit)

    # WHEN / THEN

    # Add shapes
    add_atom_rect(fig, person_partnerunit_insert)
    add_atom_rect(fig, person_partner_membership_insert)
    add_atom_rect(fig, person_plan_laborunit_insert)
    add_atom_rect(fig, person_plan_healerunit_insert)
    add_atom_rect(fig, person_plan_factunit_insert)
    add_atom_rect(fig, person_plan_reasonunit_insert)
    add_atom_rect(fig, person_plan_reason_caseunit_insert)
    add_atom_rect(fig, person_partnerunit_update)
    add_atom_rect(fig, person_partner_membership_update)
    add_atom_rect(fig, person_plan_factunit_update)
    add_atom_rect(fig, person_plan_reason_caseunit_update)
    add_atom_rect(fig, person_plan_reasonunit_update)
    add_atom_rect(fig, person_plan_reason_caseunit_delete)
    add_atom_rect(fig, person_plan_reasonunit_delete)
    add_atom_rect(fig, person_plan_factunit_delete)
    add_atom_rect(fig, person_plan_laborunit_delete)
    add_atom_rect(fig, person_plan_healerunit_delete)
    add_atom_rect(fig, person_plan_awardunit_insert)
    add_atom_rect(fig, person_plan_awardunit_update)
    add_atom_rect(fig, person_plan_awardunit_delete)
    add_atom_rect(fig, person_planunit_insert)
    add_atom_rect(fig, person_planunit_update)
    add_atom_rect(fig, person_planunit_delete)
    add_atom_rect(fig, person_partner_membership_delete)
    add_atom_rect(fig, person_partnerunit_delete)
    add_atom_rect(fig, personunit_update)
    add_groupunits_circle(fig)
    add_different_plans_circle(fig)

    fig.add_trace(
        plotly_Scatter(
            x=[2.0],
            y=[13],
            text=["Periodic Table of PersonAtoms"],
            mode="text",
        )
    )

    return fig
