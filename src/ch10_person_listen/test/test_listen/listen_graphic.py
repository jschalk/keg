from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch00_py.plotly_toolbox import (
    add_2_curve,
    add_direc_rect,
    add_keep__rect,
    add_rect_arrow,
    add_simp_rect,
    conditional_fig_show,
)
from src.ch01_allot.allot import default_pool_num
from src.ch07_person_logic.person_graphic import display_plantree
from src.ch07_person_logic.person_main import PersonUnit
from src.ref.keywords import ExampleStrs as exx


def get_lessonfilehandler_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def get_listen_structures0_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_lessonfilehandler_base_fig()
        sue_gut_str = f"{exx.sue}.gut"
        sue_job_str = f"{exx.sue}.job"
        yao_job_str = f"{exx.yao}.job"
        bob_job_str = f"{exx.bob}.job"
        dir_job_str = f"jobs directory"
        dir_gut_str = f"guts directory"

        green_str = "Green"
        med_purple = "MediumPurple"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 6.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, 1.0, 2.0, 2.0, sue_job_str, green_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, yao_job_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, bob_job_str)
        add_direc_rect(fig, 0.7, 0.7, 6.3, 2.3, dir_job_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 5,4 5.5,2", color=med_purple)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3,4 3.5,2", color=med_purple)
        add_rect_arrow(fig, 1.75, 2, 1.75, 6.8, green_str)
        add_rect_arrow(fig, 3.43, 2.3, 3.5, 2, med_purple)
        add_rect_arrow(fig, 5.41, 2.3, 5.5, 2, med_purple)

        fig.add_trace(
            plotly_Scatter(
                x=[4.0, 4.0],
                y=[9.0, 8.75],
                text=[
                    "momentity Person Listening Structures",
                    "The gut person listens to other's job persons and builds a new person from itself and others",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures1_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_lessonfilehandler_base_fig()
        sue_gut_str = f"{exx.sue}.gut"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=exx.blue)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=exx.blue)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=exx.blue)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, exx.blue)

        sue_duty_str = f"{exx.sue} duty"
        sue_vision_str = f"{exx.sue} vision"
        d_sue1_p1 = f"Healer = {exx.sue} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Mana = {default_pool_num()} "
        d_bob1_p1 = f"Healer = {exx.bob} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Keep = keep1"
        d_bob1_p4 = f"Mana = {default_pool_num()} "
        d_sue2_p1 = f"Healer = {exx.sue} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Keep = keep3"
        d_sue2_p4 = f"Mana={default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_keep__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_simp_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_keep__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[2.0],
                y=[13],
                text=["Person Listening Structures"],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures2_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_lessonfilehandler_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_gut_str = f"{exx.sue}.gut"
        sue_job_str = f"{exx.sue}.job"
        dir_job_str = f"jobs dir"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_job_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_job_str)

        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 7.4,5.1 7.5,5", color=exx.blue)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.4 5.4,5.2 5.5,5", color=exx.blue)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=exx.blue)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, exx.blue)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=exx.blue)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=exx.blue)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=exx.blue)
        add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, exx.blue)

        sue_duty_str = f"{exx.sue} duty"
        sue_vision_str = f"{exx.sue} vision"
        d_sue1_p1 = f"Healer = {exx.sue} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Mana = {default_pool_num()} "
        d_bob1_p1 = f"Healer = {exx.bob} "
        d_bob1_p2 = "Problem = problem1"
        d_bob1_p3 = "Keep = keep1"
        d_bob1_p4 = f"Mana = {default_pool_num()} "
        d_sue2_p1 = f"Healer = {exx.sue} "
        d_sue2_p2 = "Problem = problem2"
        d_sue2_p3 = "Keep = keep3"
        d_sue2_p4 = f"Mana={default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 4.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 4.0, 6.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 5.7, 2.1, 5.7, 3.9, green_str)
        add_keep__rect(
            fig, 4.7, 0.7, 6.3, 6.7, d_bob1_p1, d_bob1_p2, d_bob1_p3, d_bob1_p4
        )
        add_simp_rect(fig, 7.0, 4.0, 8.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 7.7, 2.1, 7.7, 3.9, green_str)
        add_keep__rect(
            fig, 6.7, 0.7, 8.3, 6.7, d_sue2_p1, d_sue2_p2, d_sue2_p3, d_sue2_p4
        )

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Person Listening Structures",
                    "Circulation of Persons to Keeps",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_listen_structures3_fig(graphics_bool: bool = False) -> plotly_Figure:
    if graphics_bool:
        fig = get_lessonfilehandler_base_fig()
        fig.update_yaxes(range=[-4, 10])
        sue_gut_str = f"{exx.sue}.gut"
        sue_job_str = f"{exx.sue}.job"
        dir_job_str = f"jobs dir"
        dir_gut_str = f"guts dir"

        green_str = "Green"
        add_simp_rect(fig, 1.0, 7.0, 2.0, 8.0, sue_gut_str, green_str)
        add_direc_rect(fig, 0.7, 6.7, 2.3, 8.3, dir_gut_str)
        add_simp_rect(fig, 1.0, -2.0, 2.0, -1.0, sue_job_str, green_str)
        add_direc_rect(fig, 0.7, -2.3, 2.3, -0.7, dir_job_str)

        add_rect_arrow(fig, 3.85, 3.8, 4, 3.6, exx.blue)
        add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 7.4,2.1 7.5,2", color=exx.blue)
        add_2_curve(fig, path="M 4,3.6 C 4.3,3.4 5.4,2.2 5.5,2", color=exx.blue)
        add_2_curve(fig, path="M 1.75,6.8 C 2,5.5 3.4,5.2 3.5,5", color=exx.blue)
        add_rect_arrow(fig, 1.85, 6.5, 1.75, 6.8, exx.blue)
        # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 7.4,0.4 7.5,1", color=exx.blue)
        # add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 5.4,0.4 5.5,1", color=exx.blue)
        add_2_curve(fig, path="M 1.75,-0.8 C 2,-0.2 3.4,0.4 3.5,1", color=exx.blue)
        add_rect_arrow(fig, 1.71, -1.0, 1.75, -0.8, exx.blue)

        sue_duty_str = f"{exx.sue} duty"
        sue_vision_str = f"{exx.sue} vision"
        bob_vision_str = f"{exx.bob} vision"
        yao_vision_str = f"{exx.yao} vision"
        d_sue1_p1 = f"Healer = {exx.sue} "
        d_sue1_p2 = "Problem = problem1"
        d_sue1_p3 = "Keep = keep1"
        d_sue1_p4 = f"Mana = {default_pool_num()} "

        add_simp_rect(fig, 3.0, 4.0, 4.0, 5.0, sue_duty_str)
        add_simp_rect(fig, 3.0, 1.0, 4.0, 2.0, sue_vision_str)
        add_rect_arrow(fig, 3.7, 2.1, 3.7, 3.9, green_str)
        add_keep__rect(
            fig, 2.7, 0.7, 8.3, 6.7, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4
        )
        add_simp_rect(fig, 5.0, 1.0, 6.0, 2.0, yao_vision_str)
        add_simp_rect(fig, 7.0, 1.0, 8.0, 2.0, bob_vision_str)

        green_str = "Green"
        fig.add_trace(
            plotly_Scatter(
                x=[5, 5, 5],
                y=[9, 8.5, 8.0],
                text=[
                    "Person Listening Structures",
                    "Circulation of Persons to Keeps",
                    "(Requires justification by problem and with unique name)",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def fund_graph13(
    x_person: PersonUnit, mode: str = None, graphics_bool: bool = False
) -> plotly_Figure:
    fig = display_plantree(x_person, mode, False)
    fig.update_xaxes(range=[-1, 11])
    fig.update_yaxes(range=[-5, 3])

    green_str = "Green"
    d_sue1_p1 = "How fund is distributed."
    d_sue1_p2 = "Regular Fund: Green arrows, all fund_grains end up at PartnerUnits"
    d_sue1_p3 = "Agenda Fund: Blue arrows, fund_grains from active case_tasks"
    d_sue1_p4 = f"Mana = {default_pool_num()} "
    workforceunit_str = "      AwardUnits"
    add_simp_rect(fig, 2, -0.3, 3, 0.3, workforceunit_str)
    add_rect_arrow(fig, 2, 0.1, 1.2, 0.1, green_str)
    add_rect_arrow(fig, 2, -0.1, 1.2, -0.1, exx.blue)
    add_simp_rect(fig, 4, -1.2, 5, -0.8, workforceunit_str)
    add_rect_arrow(fig, 4, -0.9, 3.1, -0.9, green_str)
    add_rect_arrow(fig, 4, -1.1, 3.1, -1.1, exx.blue)
    add_simp_rect(fig, 4, -3.2, 5, -2.8, workforceunit_str)
    add_rect_arrow(fig, 4, -2.9, 3.1, -2.9, green_str)
    add_keep__rect(fig, -0.5, -4.5, 10, 2.3, d_sue1_p1, d_sue1_p2, d_sue1_p3, d_sue1_p4)
    groupunit_str = "GroupUnit"
    orange_str = "orange"
    add_simp_rect(fig, 5.5, -0.2, 6.25, 0.4, groupunit_str, orange_str)
    add_simp_rect(fig, 5.5, -0.8, 6.25, -0.2, groupunit_str, orange_str)
    add_simp_rect(fig, 5.5, -1.4, 6.25, -0.8, groupunit_str, orange_str)
    add_rect_arrow(fig, 9, -3.9, 3.1, -3.9, green_str)
    add_rect_arrow(fig, 9, -1.9, 3.1, -1.9, green_str)
    add_rect_arrow(fig, 9, -2.1, 3.1, -2.1, exx.blue)
    add_rect_arrow(fig, 5.5, 0.1, 3, 0.1, green_str)
    add_rect_arrow(fig, 5.5, -0.1, 3, -0.1, exx.blue)
    add_rect_arrow(fig, 5.5, -0.9, 5, -0.9, green_str)
    add_rect_arrow(fig, 5.5, -1.1, 5, -1.1, exx.blue)
    add_rect_arrow(fig, 5.5, -1.3, 5, -2.9, green_str)
    membership_str = "membership"
    darkred_str = "DarkRed"
    add_simp_rect(fig, 7, 0.4, 7.75, 1, membership_str, darkred_str)
    add_simp_rect(fig, 7, -0.2, 7.75, 0.4, membership_str, darkred_str)
    add_simp_rect(fig, 7, -0.8, 7.75, -0.2, membership_str, darkred_str)
    add_simp_rect(fig, 7, -1.4, 7.75, -0.8, membership_str, darkred_str)
    add_rect_arrow(fig, 7, -0.4, 6.25, -0.4, exx.blue)
    add_rect_arrow(fig, 7, -0.6, 6.25, -0.6, green_str)
    add_rect_arrow(fig, 9, -0.4, 7.75, -0.4, exx.blue)
    add_rect_arrow(fig, 9, -0.6, 7.75, -0.6, green_str)
    partnerunit_str = "partnerunit"
    purple_str = "purple"
    add_simp_rect(fig, 9, -0.4, 9.75, 0.2, partnerunit_str, purple_str)
    add_simp_rect(fig, 9, -1.0, 9.75, -0.4, partnerunit_str, purple_str)
    add_simp_rect(fig, 9, -1.6, 9.75, -1.0, partnerunit_str, purple_str)
    add_simp_rect(fig, 9, -2.2, 9.75, -1.6, partnerunit_str, purple_str)
    add_simp_rect(fig, 9, -4.0, 9.75, -2.2, partnerunit_str, purple_str)

    conditional_fig_show(fig, graphics_bool)
