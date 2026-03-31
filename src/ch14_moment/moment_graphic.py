from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch00_py.plotly_toolbox import conditional_fig_show
from src.ch12_keep.keep_graphic import (
    add_keep_str,
    get_light_sea_green_str,
    green_str,
    purple_str,
)


def add_moment_river_rect(
    fig: plotly_Figure, x0, xw, y0, yh, display_str, x_color=None
):
    if x_color is None:
        x_color = get_light_sea_green_str()
    x1 = x0 + xw
    y1 = y0 + yh
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_col_rect(
    fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None, mana_supply=None
):
    if x_color is None:
        x_color = purple_str()
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    if mana_supply is None:
        add_rect_str(fig, x0, y0, display_str)
    if mana_supply is not None:
        mana_percent = f"{display_str} {int(((y0 - y1) * 12.5))}%"
        add_rect_str(fig, x0, y0, str(mana_percent))
        mana_amt = round((((y0 - y1) * 12.5) / 100) * mana_supply)
        add_rect_str(fig, x0, y0 - 0.2, str(mana_amt))


def add_river_mana_col(fig, num_dict: dict, mana_amt, x0, y0, c_len):
    row_y0 = y0
    row_y1 = row_y0 - c_len
    row_len = row_y1 - row_y0
    num_sum = sum(num_dict.values())
    ratio_dict = {
        contact_name: contactx / num_sum for contact_name, contactx in num_dict.items()
    }
    for careee in num_dict:
        new_y1 = row_y0 + row_len * ratio_dict.get(careee)
        add_col_rect(fig, x0, row_y0, x0 + 1, new_y1, careee, None, mana_amt)
        row_y0 = new_y1


def add_moment__rect(
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
    x0 -= 0.3
    x1 += 0.3
    line_dict = dict(color=color, width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    mid_x0 = x0 + ((x1 - x0) / 2)
    add_keep_str(fig, mid_x0, y1 - 0.2, text1)
    add_keep_str(fig, mid_x0, y1 - 0.5, text2)
    add_keep_str(fig, mid_x0, y1 - 0.8, text3)
    add_keep_str(fig, mid_x0, y1 - 1.1, text4)


def add_rect_str(fig, x0, y0, text):
    x_margin = 0.3
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="center"
    )


def get_moment_graphic_base_fig() -> plotly_Figure:
    fig = plotly_Figure()
    fig.update_xaxes(range=[0, 10])
    fig.update_yaxes(range=[0, 10])
    return fig


def get_moment_structures0_fig(graphics_bool: bool = False) -> plotly_Figure:
    fig = get_moment_graphic_base_fig()
    rx0 = 0
    rx1 = 10
    ry0 = 0
    ry1 = 10

    r_xmid = (rx1 - rx0) / 2
    r_ymid = (ry1 - ry0) / 2

    rect_height = 6
    rect_width = 6

    add_moment_river_rect(fig, 3, 5, 2.0, 6, "People gut", green_str())
    # add_moment_river_rect(fig, 1.0, ry1 - 2, 2.0, ry1 - 6, "People gut", green_str())

    sue1_p1 = ""
    sue1_p2 = ""
    sue1_p3 = ""
    sue1_p4 = ""
    add_moment__rect(fig, rx0, ry0, rx1, ry1, sue1_p1, sue1_p2, sue1_p3, sue1_p4)
    fig.update_xaxes(range=[rx0 - 1, rx1 + 1])
    fig.update_yaxes(range=[ry0 - 1, ry1 + 1])
    fig.add_trace(
        plotly_Scatter(
            x=[5.0, 5.0, 5.0],
            y=[ry0 + 1.5, ry0 + 1, ry0 + 0.5],
            text=[
                "momentity Structure",
                "Circulation of guting to Doing",
                "We all have an life where we clam chowder gut. And then there is what we do.",
            ],
            mode="text",
        )
    )
    conditional_fig_show(fig, graphics_bool)
