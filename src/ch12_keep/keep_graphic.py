from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch00_py.plotly_toolbox import add_2_curve, conditional_fig_show
from src.ch01_allot.allot import default_pool_num as default_point_magnitude


def green_str() -> str:
    return "green"


def get_light_sea_green_str() -> str:
    return "LightSeaGreen"


def blue_str() -> str:
    return "blue"


def purple_str() -> str:
    return "purple"


def red_str() -> str:
    return "red"


def darkred_str() -> str:
    return "darkred"


def black_str() -> str:
    return "black"


def ben_str() -> str:
    return "ben"


def buz_str() -> str:
    return "Buz"


def car_str() -> str:
    return "Carl"


def joc_str() -> str:
    return "Joc"


def luc_str() -> str:
    return "Luca"


def ell_str() -> str:
    return "Ellery"


def ric_str() -> str:
    return "Rico"


def sue_str() -> str:
    return "Sue"


def xio_str() -> str:
    return "Xio"


def yao_str() -> str:
    return "Yao"


def zia_str() -> str:
    return "Zia"


def add_keep_river_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None, point_supply=None
):
    if x_color is None:
        x_color = get_light_sea_green_str()
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_ch_xx_rect(fig, x0, y1, display_str)
    if point_supply is not None:
        point_percent = f"{int(((x1 - x0) * 12.5))}%"
        add_ch_xx_rect(fig, x0, y1 - 0.2, str(point_percent))
        point_amt = round((((x1 - x0) * 12.5) / 100) * point_supply)
        add_ch_xx_rect(fig, x0, y1 - 0.4, str(point_amt))


def add_column_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None, point_supply=None
):
    if x_color is None:
        x_color = purple_str()
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    if point_supply is None:
        add_ch_xx_rect(fig, x0, y0, display_str)
    if point_supply is not None:
        point_percent = f"{display_str} {int(((y0 - y1) * 12.5))}%"
        add_ch_xx_rect(fig, x0, y0, str(point_percent))
        point_amt = round((((y0 - y1) * 12.5) / 100) * point_supply)
        add_ch_xx_rect(fig, x0, y0 - 0.2, str(point_amt))


def add_river_row(fig, cares_dict: dict, point_amt, row_x0, row_x1, y0, color=None):
    row_len = row_x1 - row_x0
    cares_sum = sum(cares_dict.values())
    ratio_dict = {careee: grax / cares_sum for careee, grax in cares_dict.items()}
    for careee in cares_dict:
        new_x1 = row_x0 + row_len * ratio_dict.get(careee)
        add_keep_river_rect(fig, row_x0, y0, new_x1, y0 + 1, careee, color, point_amt)
        row_x0 = new_x1


def add_river_point_col(fig, num_dict: dict, point_amt, x0, y0, c_len):
    row_y0 = y0
    row_y1 = row_y0 - c_len
    row_len = row_y1 - row_y0
    num_sum = sum(num_dict.values())
    ratio_dict = {
        contact_name: contactx / num_sum for contact_name, contactx in num_dict.items()
    }
    for careee in num_dict:
        new_y1 = row_y0 + row_len * ratio_dict.get(careee)
        add_column_rect(fig, x0, row_y0, x0 + 1, new_y1, careee, None, point_amt)
        row_y0 = new_y1


def add_cares_top(fig, cares_dict: dict, t_y0: int, healer_name, point_amt):
    cares_str = f"{healer_name} Cares"
    dy0 = t_y0 - 1.2
    dy1 = t_y0 - 1.6
    dy2 = t_y0 - 2.2
    dy3 = t_y0 - 3
    ey0 = t_y0 - 0.8
    ey1 = t_y0 - 1.2
    add_keep_river_rect(fig, 1.0, t_y0 - 1, 2.0, t_y0, cares_str, green_str())
    add_river_row(fig, cares_dict, point_amt, 1, 9, t_y0 - 4)
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 7.4,{dy2} 9,{dy3}", color=blue_str())
    add_2_curve(fig, path=f"M 1.75,{dy0} C 2,{dy1} 1.2,{dy2} 1,{dy3}", color=blue_str())
    add_rect2_arrow(fig, 1.75, ey1, 1.5, ey0, blue_str())


def add_needs_bottom(fig, needs_dict, b_y0: int, healer_name: str, point_amt: int):
    needs_str = f"{healer_name} Needs"
    cy0 = b_y0 + 1.2
    cy1 = b_y0 + 1.6
    cy2 = b_y0 + 2.2
    cy3 = b_y0 + 3
    ay0 = b_y0 + 0.8
    ay1 = b_y0 + 1.2
    add_keep_river_rect(fig, 1.0, b_y0, 2.0, b_y0 + 1, needs_str, darkred_str())
    add_river_row(fig, needs_dict, point_amt, 1, 9, y0=b_y0 + 3, color=purple_str())
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 7.4,{cy2} 9,{cy3}", color=red_str())
    add_2_curve(fig, path=f"M 1.75,{cy0} C 2,{cy1} 1.2,{cy2} 1,{cy3}", color=red_str())
    add_rect2_arrow(fig, 1.5, ay0, 1.75, ay1, red_str())


def add_needs_column(
    fig,
    needs_dict,
    b_x0: int,
    b_y0: int,
    healer_name: str,
    point_amt: int,
    col_y0: float,
    col_len: float,
):
    needs_str = f"{healer_name} Needs"
    cx0 = b_x0 - 0.2
    cx1 = b_x0 - 0.8
    cx2 = b_x0 - 0.4
    cy1 = col_y0 - col_len
    cy2 = cy1 + 2
    cy4 = b_y0 - 1
    cy5 = cy4 - 1
    cy6 = col_y0 + 1
    add_keep_river_rect(fig, b_x0, b_y0 - 1, b_x0 + 1, b_y0, needs_str, darkred_str())
    add_river_point_col(fig, needs_dict, point_amt, b_x0, col_y0, c_len=col_len)
    z1_path = f"M {cx0},{cy4} C {cx2},{cy5} {cx2},{cy6} {b_x0},{col_y0}"
    z2_path = f"M {cx0},{cy4} C {cx1},{cy5} {cx1},{cy2} {b_x0},{cy1}"
    add_2_curve(fig, path=z1_path, color=red_str())
    add_2_curve(fig, path=z2_path, color=red_str())
    ax0 = b_x0 + 0.05
    ax1 = b_x0 - 0.2
    ay0 = b_y0 - 0.7
    add_rect2_arrow(fig, ax0, ay0, ax1, cy4, red_str())


def add_rivercycle(fig: plotly_Figure, x0, y0, x1, y1, display_str):
    line_dict = dict(color=get_light_sea_green_str(), width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_ch_xx_rect(fig, x0, y1, display_str)


def add_keep2_rect(
    fig: plotly_Figure,
    x0,
    y0,
    x1,
    y1,
    text1=None,
    text2=None,
    text3=None,
    text4=None,
    color=None,
):
    if color is None:
        color = get_light_sea_green_str()
    y0 -= 0.3
    y1 += 0.3
    line_dict = dict(color=color, width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    mid_x0 = x0 + ((x1 - x0) / 2)
    add_keep_str(fig, mid_x0, y1 - 0.2, text1)
    add_keep_str(fig, mid_x0, y1 - 0.5, text2)
    add_keep_str(fig, mid_x0, y1 - 0.8, text3)
    add_keep_str(fig, mid_x0, y1 - 1.1, text4)


def add_keep_str(fig, x0, y0, text):
    fig.add_annotation(x=x0, y=y0, text=text, showarrow=False, align="left")


def add_ch_xx_rect(fig, x0, y0, text):
    x_margin = 0.3
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_rect2_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None, width=None):
    if color is None:
        color = black_str()
    if width is None:
        width = 3
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # no title
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=width,
        arrowcolor=color,
    )


def get_keep_graphic_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def cares1_dict() -> dict:
    return {
        ben_str(): 2.2 - 1.0,
        buz_str(): 3.0 - 2.2,
        car_str(): 4.6 - 3.0,
        ric_str(): 5.2 - 4.6,
        sue_str(): 6.6 - 5.2,
        xio_str(): 7.2 - 6.6,
        yao_str(): 8.0 - 7.2,
        zia_str(): 9.0 - 8.0,
    }


def needs1_dict() -> dict:
    return {
        joc_str(): 100,
        luc_str(): 100,
        ell_str(): 55,
        ric_str(): 60,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 100,
        zia_str(): 100,
    }


def rivercycle1_dict() -> dict:
    return {
        ben_str(): 60,
        joc_str(): 200,
        luc_str(): 55,
        ell_str(): 66,
        sue_str(): 76,
        xio_str(): 130,
        yao_str(): 50,
        zia_str(): 70,
    }


def rivercycle2_dict() -> dict:
    return {
        ben_str(): 8,
        joc_str(): 13,
        ell_str(): 1,
        sue_str(): 1,
    }


def rivercycle3_dict() -> dict:
    return {
        ben_str(): 60,
        joc_str(): 200,
        luc_str(): 55,
        xio_str(): 130,
        yao_str(): 50,
        zia_str(): 70,
    }


def rivercycle4_dict() -> dict:
    return {ben_str(): 60, joc_str(): 200}


def add_cycle_to_need_arrows(fig, cx_src, cx0, cx1, cy1, cy2, cy3, coor_dict):
    for coor_value in coor_dict.values():
        y0 = coor_value.get("y0")
        x2 = coor_value.get("x2")
        z_path = f"M {cx0},{y0} C {cx1},{cy1} {x2},{cy2} {x2+1},{cy3}"
        add_2_curve(fig, path=z_path, color=red_str())
        add_rect2_arrow(fig, cx_src, y0, cx0, y0, red_str(), 2)


def get_protect_structures0_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        m_y1 = -3
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )
        add_needs_bottom(fig, needs1_dict(), m_y1, healer_name=sue_str(), point_amt=mm)
        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )

        conditional_fig_show(fig, graphics_bool)


def get_protect_structures1_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        m_y1 = -5
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )
        add_needs_bottom(fig, needs1_dict(), m_y1, healer_name=sue_str(), point_amt=mm)

        y_mid = m_y1 + (m_y0 - m_y1) / 2
        add_rect2_arrow(fig, 2, y_mid - 1.5, 2, y_mid + 1.5, green_str())
        add_rect2_arrow(fig, 5, y_mid - 1.5, 5, y_mid + 1.5, green_str())
        add_rect2_arrow(fig, 8, y_mid - 1.5, 8, y_mid + 1.5, green_str())

        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )
        conditional_fig_show(fig, graphics_bool)


def get_protect_structures2_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        m_y1 = -7
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )
        col_y0 = 4
        col_len = 11
        add_needs_column(fig, needs1_dict(), -1, 8, sue_str(), mm, col_y0, col_len)
        add_river_row(fig, rivercycle1_dict(), mm, 1, 9, 0, black_str())

        ay0 = 3.88
        ay1 = ay0 - 2.6
        ben_src = 2
        buz_src = 2.75
        car_src = 3.25
        ric_src = 4.75
        sue_src = 5.5
        xio_src = 6.7
        yao_src = 7.3
        zia_src = 8.5
        ben_dst = 1.3
        joc_dst = 2.5
        luc_dst = 4.25
        mar_dst = 4.75
        sue_dst = 5.6
        xio_dst = 6.7
        yao_dst = 7.3
        zia_dst = 8.5
        add_rect2_arrow(fig, ben_dst, ay1, ben_src, ay0, green_str(), 2)
        add_rect2_arrow(fig, luc_dst, ay1, ben_src, ay0, green_str(), 2)
        add_rect2_arrow(fig, sue_dst, ay1, ben_src, ay0, green_str(), 2)
        add_rect2_arrow(fig, joc_dst, ay1, buz_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, luc_dst, ay1, buz_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, joc_dst, ay1, car_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, mar_dst, ay1, car_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, luc_dst, ay1, car_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, mar_dst, ay1, ric_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, luc_dst, ay1, sue_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, joc_dst, ay1, sue_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, yao_dst, ay1, sue_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, zia_dst, ay1, sue_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, luc_dst, ay1, xio_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, joc_dst, ay1, xio_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, xio_dst, ay1, yao_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, joc_dst, ay1, yao_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, xio_dst, ay1, zia_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, joc_dst, ay1, zia_src, ay0, green_str(), 1)
        add_rect2_arrow(fig, zia_src, ay1, zia_src, ay0, green_str(), 1)

        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        add_keep2_rect(fig, -1.9, m_y1, 0.3, m_y0, "", "", "", "")
        add_keep2_rect(fig, -1.2, 7, 2.2, 8.7, sue_str(), "", "", "", color=black_str())
        fig.update_yaxes(range=[-8, 10])
        fig.update_xaxes(range=[-3, 10])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )
        conditional_fig_show(fig, graphics_bool)


def get_protect_structures3_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        m_y1 = -7
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )
        col_y0 = 2
        col_len = 9
        add_needs_column(fig, needs1_dict(), -1, 8, sue_str(), mm, col_y0, col_len)
        ry0 = 0
        add_river_row(fig, rivercycle1_dict(), mm, 1, 9, ry0, black_str())

        ry1 = m_y0 - 4
        y_mid = ry0 + (ry1 - ry0 + 1) / 2
        add_rect2_arrow(fig, 2, y_mid - 1, 2, y_mid + 1, green_str())
        add_rect2_arrow(fig, 5, y_mid - 1, 5, y_mid + 1, green_str())
        add_rect2_arrow(fig, 8, y_mid - 1, 8, y_mid + 1, green_str())

        cx_src = 0
        cx0 = cx_src + 0.3
        cx1 = cx0 + 1
        joc_x2 = cx1 + 0.2
        joc_y0 = 1.5
        cy1 = -1
        cy2 = -0.6
        cy3 = 0
        luc_y0 = 0
        luc_x2 = 3.3
        mar_y0 = -0.8
        mar_x2 = 4.0
        sue_y0 = -2.3
        sue_x2 = 4.6
        xio_y0 = -3.3
        xio_x2 = 5.8
        yao_y0 = -5
        yao_x2 = 6.8
        zia_y0 = -6.2
        zia_x2 = 7.7
        coor_dict = {
            1: {"y0": joc_y0, "x2": joc_x2},
            2: {"y0": luc_y0, "x2": luc_x2},
            3: {"y0": mar_y0, "x2": mar_x2},
            4: {"y0": sue_y0, "x2": sue_x2},
            5: {"y0": xio_y0, "x2": xio_x2},
            6: {"y0": yao_y0, "x2": yao_x2},
            7: {"y0": zia_y0, "x2": zia_x2},
        }

        add_cycle_to_need_arrows(fig, cx_src, cx0, cx1, cy1, cy2, cy3, coor_dict)

        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        add_keep2_rect(fig, -1.2, 7, 2.2, 8.7, sue_str(), "", "", "", color=black_str())
        # fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
        fig.update_yaxes(range=[-8, 10])
        fig.update_xaxes(range=[-3, 10])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )
        conditional_fig_show(fig, graphics_bool)


def get_protect_structures4_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        m_y1 = -7
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )
        need_x0 = -1
        col_y0 = 2
        col_len = 9
        add_needs_column(fig, needs1_dict(), need_x0, 8, sue_str(), mm, col_y0, col_len)
        ry0 = 0
        add_river_row(fig, rivercycle1_dict(), mm, 1, 9, ry0, black_str())
        add_rect2_arrow(
            fig, need_x0 + 1.1, ry0 + 0.5, need_x0 + 2, ry0 + 0.5, red_str(), 5
        )
        add_river_row(
            fig, rivercycle2_dict(), mm, 1, 4, ry0 - 3, get_light_sea_green_str()
        )

        ry1 = m_y0 - 4
        y_mid = ry0 + (ry1 - ry0 + 1) / 2
        add_rect2_arrow(fig, 2, y_mid - 1, 2, y_mid + 1, green_str())
        add_rect2_arrow(fig, 5, y_mid - 1, 5, y_mid + 1, green_str())
        add_rect2_arrow(fig, 8, y_mid - 1, 8, y_mid + 1, green_str())

        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        add_keep2_rect(fig, -1.2, 7, 2.2, 8.7, sue_str(), "", "", "", color=black_str())
        # fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
        fig.update_yaxes(range=[-8, 10])
        fig.update_xaxes(range=[-3, 10])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )
        conditional_fig_show(fig, graphics_bool)


def get_protect_structures5_fig(graphics_bool: bool) -> plotly_Figure:
    if graphics_bool:
        fig = get_keep_graphic_base_fig()

        mm = default_point_magnitude()
        sue1_p1 = f"Healer = {sue_str()} "
        sue1_p2 = "Problem = problem1"
        sue1_p3 = "Keep = keep1"
        sue1_p4 = f"Point = {mm} "

        m_y0 = 8
        add_cares_top(
            fig, cares1_dict(), t_y0=m_y0, healer_name=sue_str(), point_amt=mm
        )

        need_x0 = -1
        col_y0 = 4
        col_len = 10
        add_needs_column(fig, needs1_dict(), need_x0, 8, sue_str(), mm, col_y0, col_len)
        cycle1_y0 = 2
        ry1 = m_y0 - 4
        y_mid = cycle1_y0 + (ry1 - cycle1_y0 + 1) / 2
        add_rect2_arrow(fig, 2, y_mid - 0.5, 2, y_mid + 0.5, green_str())
        add_rect2_arrow(fig, 5, y_mid - 0.5, 5, y_mid + 0.5, green_str())
        add_rect2_arrow(fig, 8, y_mid - 0.5, 8, y_mid + 0.5, green_str())
        add_river_row(fig, rivercycle1_dict(), mm, 1, 9, cycle1_y0, black_str())
        red_a1_x0 = cycle1_y0 + 0.5
        add_rect2_arrow(
            fig, need_x0 + 1.1, red_a1_x0, need_x0 + 2, red_a1_x0, red_str(), 3
        )
        need1_y0 = cycle1_y0 - 1
        add_river_row(
            fig, rivercycle2_dict(), mm, 1, 4, need1_y0, get_light_sea_green_str()
        )

        cycle2_y0 = cycle1_y0 - 3
        add_river_row(fig, rivercycle3_dict(), mm, 1, 4, cycle2_y0, black_str())
        a2y_mid = cycle2_y0 + (cycle1_y0 - cycle2_y0) / 2
        add_rect2_arrow(fig, 1.3, a2y_mid - 0.5, 1.3, a2y_mid + 0.5, green_str())
        add_rect2_arrow(fig, 2.5, a2y_mid - 0.5, 2.5, a2y_mid + 0.5, green_str())
        add_rect2_arrow(fig, 3.7, a2y_mid - 0.5, 3.7, a2y_mid + 0.5, green_str())
        red_a2_y0 = cycle2_y0 + 0.5
        needy0 = cycle2_y0 - 1
        add_rect2_arrow(
            fig, need_x0 + 1.1, red_a2_y0, need_x0 + 2, red_a2_y0, red_str(), 3
        )
        add_river_row(
            fig, rivercycle4_dict(), mm, 1, 2, needy0, get_light_sea_green_str()
        )

        cycle3_y0 = cycle2_y0 - 3
        add_river_row(fig, rivercycle4_dict(), mm, 1, 2, cycle3_y0, black_str())
        a3y_mid = cycle3_y0 + (cycle2_y0 - cycle3_y0) / 2
        add_rect2_arrow(fig, 1.2, a3y_mid - 0.5, 1.2, a3y_mid + 0.5, green_str())
        add_rect2_arrow(fig, 1.8, a3y_mid - 0.5, 1.8, a3y_mid + 0.5, green_str())
        red_a3_y0 = cycle3_y0 + 0.5
        add_rect2_arrow(
            fig, need_x0 + 1.1, red_a3_y0, need_x0 + 2, red_a3_y0, red_str(), 3
        )

        m_y1 = -7
        add_keep2_rect(fig, 0.7, m_y1, 9.3, m_y0, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
        add_keep2_rect(fig, -1.2, 7, 2.2, 8.7, sue_str(), "", "", "", color=black_str())
        # fig.update_yaxes(range=[m_y1 - 1, m_y0 + 3])
        fig.update_yaxes(range=[-8, 10])
        fig.update_xaxes(range=[-3, 10])
        fig.add_trace(
            plotly_Scatter(
                x=[5.0, 5.0, 5.0],
                y=[m_y0 + 1.5, m_y0 + 1, m_y0 + 0.5],
                text=[
                    "Keep Point Structure",
                    "Circulation of Point to Contacts",
                    "Point starts as cares from Healer. Needs are point coming back to healer.",
                ],
                mode="text",
            )
        )
        conditional_fig_show(fig, graphics_bool)
