from dataclasses import dataclass
from drawsvg import (
    Circle as drawsvg_Circle,
    Drawing,
    Line as drawsvg_Line,
    Lines as drawsvg_Lines,
    Path as drawsvg_Path,
    Rectangle as drawsvg_Rectangle,
    Text as drawsvg_Text,
)
from math import cos as math_cos, pi as math_pi, sin as math_sin
from pathlib import Path


def add_title_to_drawing(d: Drawing, title_txt: str, title_font_size: int, margin: int):
    # Get the directory containing this script
    d.append(
        drawsvg_Text(
            title_txt,
            title_font_size,
            d.width / 2,
            margin + title_font_size,
            center=True,
            fill="black",
            font_weight="bold",
        )
    )


def add_footer_to_drawing(d: Drawing, footer_txt: str, margin: int):
    d.append(
        drawsvg_Text(
            footer_txt,
            12,
            d.width - margin,
            d.height - margin,
            center=False,
            text_anchor="end",
            fill="black",
        )
    )


def save_to_images_dir(d: Drawing, filebasename: str = "theory"):
    # Get the directory containing this script
    project_dir = Path(__file__).resolve().parent
    # Save the SVG
    output_file_path = project_dir / "images" / f"{filebasename}.svg"
    d.save_svg(str(output_file_path))
    return output_file_path


def draw_contact_circle(
    d: Drawing,
    cx: int,
    cy: int,
    radius: int,
    contact_name: str,
    face_status: str,
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    font_size=14,
    status_font_size=18,
):
    # Draw the circle
    circle = drawsvg_Circle(
        cx,
        cy,
        radius,
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )
    d.append(circle)

    is_face = face_status == "Face"
    status_size = status_font_size if is_face else font_size

    # Two lines of text: contact_name on top, face_status below.
    # face_status is drawn larger and bold when it reads "Face".
    name_line_height = font_size * 1.2
    status_line_height = status_size * 1.2
    total_height = name_line_height + status_line_height

    name_y = cy - total_height / 2 + font_size
    status_y = cy - total_height / 2 + name_line_height + status_size

    d.append(
        drawsvg_Text(
            contact_name,
            font_size,
            cx,
            name_y,
            center=True,
            fill="black",
        )
    )

    d.append(
        drawsvg_Text(
            face_status,
            status_size,
            cx,
            status_y,
            center=True,
            fill="black",
            font_weight="bold" if is_face else "normal",
        )
    )

    return {
        "cx": cx,
        "cy": cy,
        "radius": radius,
    }


def _required_radius(
    contact_name: str,
    face_status: str,
    font_size: int,
    status_font_size: int,
    padding: int = 12,
) -> int:
    """
    Estimate the minimum circle radius needed so that both lines of text
    (contact_name and, when applicable, the larger/bold face_status) fit
    inside the circle.
    """
    avg_char_width = font_size * 0.6
    is_face = face_status == "Face"
    status_size = status_font_size if is_face else font_size
    # Bold text runs a bit wider than normal text.
    avg_status_char_width = status_size * (0.65 if is_face else 0.6)

    name_width = len(contact_name) * avg_char_width
    status_width = len(face_status) * avg_status_char_width
    text_width = max(name_width, status_width)

    name_line_height = font_size * 1.2
    status_line_height = status_size * 1.2
    text_block_height = name_line_height + status_line_height

    # The circle must contain a rectangle of size (text_width x text_block_height):
    # radius >= sqrt((text_width/2)^2 + (text_block_height/2)^2)
    half_w = text_width / 2
    half_h = text_block_height / 2
    min_radius = (half_w**2 + half_h**2) ** 0.5

    return int(min_radius) + padding


def draw_contacts_row(
    contacts: list,
    font_size: int = 14,
    status_font_size: int = 18,
    gap: int = 20,
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    margin: int = 20,
) -> Drawing:
    """
    Draws a horizontal, non-overlapping row of same-sized circles, one per
    contact. Each contact is a dict-like object with 'contact_name' and
    'face_status'.

    All circles share a single radius, computed as the largest radius
    required to fit any contact's text, so every circle is the same size.
    Circles are spaced with `gap` pixels of empty space between neighboring
    edges to guarantee no overlap.
    """
    # Find the one radius big enough to fit every contact's text.
    radius = 0
    for contact in contacts:
        r = _required_radius(
            contact["contact_name"],
            contact["face_status"],
            font_size,
            status_font_size,
        )
        radius = max(radius, r)

    center_y = margin + radius

    total_width = 2 * margin
    if contacts:
        total_width += 2 * radius * len(contacts) + gap * (len(contacts) - 1)

    total_height = 2 * margin + 2 * radius

    d = Drawing(total_width, total_height, origin=(0, 0))

    cursor_x = margin
    for contact in contacts:
        cx = cursor_x + radius
        cy = center_y
        draw_contact_circle(
            d,
            cx,
            cy,
            radius,
            contact["contact_name"],
            contact["face_status"],
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            font_size=font_size,
            status_font_size=status_font_size,
        )
        cursor_x += 2 * radius + gap

    return d


def _required_loop_radius(text: str, font_size: int, padding: int = 8) -> int:
    """
    Estimate the minimum radius of a single infinity "loop" needed to fit
    one line of text (a single word/label, not two stacked lines).
    """
    avg_char_width = font_size * 0.6
    text_width = len(text) * avg_char_width
    text_height = font_size * 1.2

    half_w = text_width / 2
    half_h = text_height / 2
    min_radius = (half_w**2 + half_h**2) ** 0.5

    return int(min_radius) + padding


def draw_infinity_contact(
    d: Drawing,
    x0: int,
    y0: int,
    contact_name: str,
    face_status: str = "need",
    fill="#E9F0E9",
    stroke="#DEF0DE",
    stroke_width=17,
    font_size=14,
    face_font_size=18,
    face_bold=True,
    num_points=120,
):
    """
    Draws an infinity (figure-eight) shape centered at (cx, cy). The left
    loop contains `contact_name`, the right loop contains `face_status`
    (defaults to "Face", drawn larger/bold to match the circle style).

    `radius` is the horizontal half-width of the whole infinity shape (i.e.
    the curve reaches cx - radius on the left and cx + radius on the right).
    Each loop behaves like a circle of roughly radius/2, centered at
    cx -/+ radius/2.
    """
    # Lemniscate of Gerono: x = a*cos(t), y = (a/2)*sin(2t)
    # Self-intersects at the center, so filling with the evenodd rule
    # produces two solid, symmetric loops -- the classic infinity shape.
    contact_name = f"{contact_name}'s"
    loop_radius = max(
        _required_loop_radius(contact_name, font_size),
        _required_loop_radius(face_status, face_font_size),
    )
    radius = loop_radius * 2
    cx = x0 + radius
    cy = y0 + radius / 2

    path = drawsvg_Path(
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
        fill_rule="evenodd",
    )

    for i in range(num_points + 1):
        t = 2 * math_pi * i / num_points
        x = cx + radius * math_cos(t)
        taper = 1 - 0.45 * math_cos(t) ** 2  # softens amplitude near the tips
        y = cy + (radius * 0.4) * math_sin(2 * t) * taper
        if i == 0:
            path.M(x, y)
        else:
            path.L(x, y)
    path.Z()
    d.append(path)

    # Loop centers: left loop bulges toward cx - radius/2, right loop
    # bulges toward cx + radius/2.
    left_x = cx - radius / 2
    right_x = cx + radius / 2

    is_face = face_status == "Face" and face_bold
    status_size = face_font_size if is_face else font_size

    d.append(
        drawsvg_Text(
            face_status,
            status_size,
            right_x,
            cy,
            center=True,
            fill="black",
            font_weight="bold" if is_face else "normal",
        )
    )

    d.append(
        drawsvg_Text(
            contact_name,
            font_size,
            left_x,
            cy,
            center=True,
            fill="black",
        )
    )

    return {
        "cx": cx,
        "cy": cy,
        "radius": radius,
    }


def _required_rect_width(
    contact_name: str, status: str, font_size: int, padding: int = 16
) -> int:
    """
    Estimate the minimum rectangle width needed so both lines of text
    (contact_name and status) fit inside the rectangle.
    """
    avg_char_width = font_size * 0.6
    longest_line = max(contact_name, status, key=len)
    text_width = len(longest_line) * avg_char_width
    return int(text_width) + padding * 2


def draw_contact_rectangle(
    d: Drawing,
    x: int,
    y: int,
    width: int,
    height: int,
    contact_name: str,
    status: str = "needs",
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    font_size=14,
):
    """
    Draws a single rectangle at (x, y) with the given width/height,
    containing `contact_name` on top and `status` below, both centered.
    """
    rect = drawsvg_Rectangle(
        x,
        y,
        width,
        height,
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )
    d.append(rect)

    lines = [f"{contact_name}'s", status]
    line_height = font_size * 1.2
    total_height = len(lines) * line_height
    start_y = y + height / 2 - total_height / 2 + font_size

    for i, line in enumerate(lines):
        d.append(
            drawsvg_Text(
                line,
                font_size,
                x + width / 2,
                start_y + i * line_height,
                center=True,
                fill="black",
            )
        )

    return {"x": x, "y": y, "width": width, "height": height}


def draw_contact_rows(
    drawing: Drawing,
    rows: list,
    cred_scale: int = 8,
    base_width: int = 60,
    height: int = 60,
    font_size: int = 14,
    gap: int = 5,
    row_gap: int = 5,
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    x0: int = 20,
    y0: int = 20,
) -> Drawing:
    """
    Draws stacked rows of non-overlapping rectangles. Each row is a list of
    contact tuples: (contact_name, cred, status) or (contact_name, cred) --
    status defaults to "need" when omitted. `cred` widens the rectangle
    (width = max(text-driven minimum, base_width + cred * cred_scale)).
    Rows stack vertilly; rectangles within a row are placed left-to-right
    with `gap` pixels between them.
    """
    normalized_rows = []
    for row in rows:
        normalized_row = []
        for contact in row:
            if len(contact) == 3:
                name, cred, status = contact
            else:
                name, cred = contact
                status = "needs"
            normalized_row.append((name, cred, status))
        normalized_rows.append(normalized_row)

    row_widths = []
    for row in normalized_rows:
        widths = []
        for name, cred, status in row:
            min_width = _required_rect_width(name, status, font_size)
            width = max(min_width, base_width + cred * cred_scale)
            widths.append(width)
        row_widths.append(widths)

    cursor_y = y0
    for row, widths in zip(normalized_rows, row_widths):
        cursor_x = x0
        for (name, cred, status), width in zip(row, widths):
            draw_contact_rectangle(
                drawing,
                cursor_x,
                cursor_y,
                width,
                height,
                name,
                status,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                font_size=font_size,
            )
            cursor_x += width + gap
        cursor_y += height + row_gap

    return drawing


def draw_curved_dotted_line(
    d: Drawing,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    curvature: float = 0.3,
    stroke="black",
    stroke_width=2,
    dash_array="4,4",
):
    """
    Draws a curved dotted line from (x1, y1) to (x2, y2).

    `curvature` controls how much the line bows out, as a fraction of the
    straight-line distance between the two points. Positive bows one way,
    negative bows the other way. 0 draws a straight (still dotted) line.
    """
    # Midpoint of the straight line.
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Perpendicular offset from the midpoint, scaled by curvature.
    dx = x2 - x1
    dy = y2 - y1
    length = (dx**2 + dy**2) ** 0.5 or 1  # avoid div-by-zero for identical points

    # Perpendicular unit vector.
    perp_x = -dy / length
    perp_y = dx / length

    offset = length * curvature
    control_x = mid_x + perp_x * offset
    control_y = mid_y + perp_y * offset

    path = drawsvg_Path(
        fill="none",
        stroke=stroke,
        stroke_width=stroke_width,
        stroke_dasharray=dash_array,
    )
    path.M(x1, y1)
    path.Q(control_x, control_y, x2, y2)
    d.append(path)

    return {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "control_x": control_x,
        "control_y": control_y,
    }


def draw_trapezoid_shape(
    d: Drawing,
    x: int,
    y: int,
    bottom_length: int,
    family_title: str,
    height=None,
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    font_size=18,
):

    # Calculate dimensions
    top_length = bottom_length * 0.8
    if not height:
        height = top_length

    # Horizontal inset
    inset = (bottom_length - top_length) / 2

    # Points
    top_left = (x + inset, y)
    top_right = (x + inset + top_length, y)

    bottom_left = (x, y + height)
    bottom_right = (x + bottom_length, y + height)

    # Draw trapezoid
    trapezoid = drawsvg_Lines(
        top_left[0],
        top_left[1],
        top_right[0],
        top_right[1],
        bottom_right[0],
        bottom_right[1],
        bottom_left[0],
        bottom_left[1],
        close=True,
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )

    d.append(trapezoid)

    # Add centered label
    lines = family_title.split("\n")
    line_height = font_size * 1.2

    total_height = len(lines) * line_height
    start_y = y + height / 2 - total_height / 2 + font_size

    for i, line in enumerate(lines):
        d.append(
            drawsvg_Text(
                line,
                font_size,
                x + bottom_length / 2,
                start_y + i * line_height,
                center=True,
                fill="black",
            )
        )

    return {
        "x": x,
        "y": y,
        "width": bottom_length,
        "height": height,
        "top_width": top_length,
    }


def draw_land(
    d: Drawing,
    y: float,
    label: str = "Land",
    stroke: str = "black",
    stroke_width: float = 2,
    font_size: float = 14,
    label_gap: float = 6,
) -> dict:
    """
    Draw a horizontal line representing land with a centered label beneath it.

    (x, y) is the left endpoint of the line.
    """
    length = d.width * 0.8
    x = (d.width - length) / 2

    # Draw the line.
    d.append(
        drawsvg_Line(
            x,
            y,
            x + length,
            y,
            stroke=stroke,
            stroke_width=stroke_width,
        )
    )

    # Draw the label.
    d.append(
        drawsvg_Text(
            label,
            font_size,
            x=x + length / 2,
            y=y + label_gap + font_size,
            center=True,
        )
    )

    return {
        "x": x,
        "y": y,
        "length": length,
        "label_x": x + length / 2,
        "label_y": y + label_gap + font_size,
    }


def draw_tower_land(fig_obj: Drawing, tower0_y0: int, tower_height: int, desc_str: str):
    l_y0 = tower0_y0 + tower_height + 10
    draw_land(fig_obj, l_y0, "Land", stroke_width=4, font_size=20)


def draw_tower_fig(fig_obj: Drawing, family_desc: str, t_descs: list[str]):
    towers_count = len(t_descs)
    family_y0 = 90
    family_height = 50
    tower_height = 170
    fig_width = fig_obj.width

    tower_width = (fig_width / 3) - 40
    family_width = (tower_width * towers_count) - 40
    family_x0 = (fig_width - family_width) / 2
    tower0_x0 = (fig_width / 2) - tower_width - 10
    tower1_x0 = (fig_width / 2) + 10
    tower0_y0 = family_y0 + family_height + 10
    tower1_y0 = family_y0 + family_height + 10
    trapunits = [
        TrapeziodUnit(family_x0, family_y0, family_width, family_desc, family_height),
        TrapeziodUnit(tower0_x0, tower0_y0, tower_width, t_descs[0], tower_height),
        TrapeziodUnit(tower1_x0, tower1_y0, tower_width, t_descs[1], tower_height),
    ]
    draw_trapezoid_stack(fig_obj, trapunits)
    draw_tower_land(fig_obj, tower0_y0, tower_height, "Land")


@dataclass
class TrapeziodUnit:
    x0: int = None
    y0: int = None
    bottom_length: int = None
    family_title: str = None
    height: int = None


def draw_trapezoid_stack(
    d: Drawing,
    trapunits: list[TrapeziodUnit],
    fill="#D9F2D9",
    stroke="black",
    stroke_width=2,
    font_size=18,
):
    for trapunit in trapunits:
        draw_trapezoid_shape(
            d=d,
            x=trapunit.x0,
            y=trapunit.y0,
            bottom_length=trapunit.bottom_length,
            height=trapunit.height,
            family_title=trapunit.family_title,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            font_size=font_size,
        )


XMX = 20
XFX = 12


def get_standard_drawing(width: int = 800, height: int = 600) -> Drawing:
    d = Drawing(width, height, origin='top-left')
    d.append(drawsvg_Rectangle(0, 0, 800, 600, fill='white'))
    return d


def get_wheel_fig(fig_dict: dict[str,]) -> Drawing:
    fig_width = fig_dict.get("fig_width")
    if fig_width is None:
        fig_width = 600
    fig_height = fig_dict.get("fig_height")
    if fig_height is None:
        fig_height = 400
    tx_str = fig_dict.get("fig_title_str")
    tx_font_size = fig_dict.get("fig_title_font_size")
    if tx_font_size is None:
        tx_font_size = 30
    tx_margin = fig_dict.get("fig_title_margin")
    if tx_margin is None:
        tx_margin = 10

    foot_str = fig_dict.get("footer_str")

    fig = get_standard_drawing(fig_width, fig_height)
    if fig_dict.get("infinity_contacts"):
        for infinity_contact_dict in fig_dict.get("infinity_contacts").values():
            i_x0 = infinity_contact_dict.get("x0")
            i_y0 = infinity_contact_dict.get("y0")
            i_name = infinity_contact_dict.get("contact_name")
            i_status = infinity_contact_dict.get("face_status")
            draw_infinity_contact(fig, i_x0, i_y0, i_name, i_status)
    if fig_dict.get("contact_rows_objs"):
        c_rows_x0 = fig_dict.get("contact_rows_x0")
        c_rows_y0 = fig_dict.get("contact_rows_y0")
        c_rows_objs = fig_dict.get("contact_rows_objs")
        draw_contact_rows(fig, c_rows_objs, x0=c_rows_x0, y0=c_rows_y0)
    if fig_dict.get("curved_lines"):
        for curved_line_dict in fig_dict.get("curved_lines"):
            cur_x1 = curved_line_dict.get("x1")
            cur_y1 = curved_line_dict.get("y1")
            cur_x2 = curved_line_dict.get("x2")
            cur_y2 = curved_line_dict.get("y2")
            curvature = curved_line_dict.get("curvature")
            draw_curved_dotted_line(fig, cur_x1, cur_y1, cur_x2, cur_y2, curvature)
    if fig_dict.get("trapunits"):
        draw_trapezoid_stack(fig, fig_dict.get("trapunits"))
    if fig_dict.get("land_y0"):
        land_y0 = fig_dict.get("land_y0")
        draw_land(fig, land_y0, "Land", stroke_width=4, font_size=20)
    if fig_dict.get("sub_title_str"):
        sub_title_str = fig_dict.get("sub_title_str")
        sub_title_margin = fig_dict.get("sub_title_margin")
        font_size = fig_dict.get("sub_title_font_size")
        if font_size is None:
            font_size = 16
        add_title_to_drawing(fig, sub_title_str, font_size, sub_title_margin)
    if fig_dict.get("tower_attrs"):
        tower_attrs_dict = fig_dict.get("tower_attrs")
        family_desc = tower_attrs_dict.get("family_desc")
        tower_descs = tower_attrs_dict.get("tower_descs")
        draw_tower_fig(fig, family_desc, tower_descs)
    add_title_to_drawing(fig, tx_str, tx_font_size, tx_margin)
    add_footer_to_drawing(fig, foot_str, XMX)
    return fig


def get_markdown_wheel_theory_drawings() -> dict[str, Drawing]:
    t_str = "am i a good father?"
    low_trust_str = "Families on the Land"
    fig0_0_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "fig_title_margin": 20,
        "footer_str": "fig0_0",
        "fig_width": 370,
        "fig_height": 180,
        "infinity_contacts": {
            0: {"x0": 120, "y0": 70, "contact_name": "son", "face_status": "Face"}
        },
    }
    fig0_1_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_1",
        "fig_height": 180,
        "infinity_contacts": {
            0: {"x0": 70, "y0": 50, "contact_name": "son     ", "face_status": "Face"},
            1: {"x0": 330, "y0": 50, "contact_name": "daughter", "face_status": "Face"},
        },
    }
    fig0_2_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_2",
        "fig_height": 300,
        "infinity_contacts": {
            0: {"x0": 70, "y0": 50, "contact_name": "son     ", "face_status": "Face"},
            1: {"x0": 330, "y0": 70, "contact_name": "daughter", "face_status": "Face"},
            2: {
                "x0": 170,
                "y0": 180,
                "contact_name": "wife    ",
                "face_status": "Face",
            },
        },
    }
    fig0_3_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_3",
        "fig_width": 700,
        "fig_height": 300,
        "infinity_contacts": {
            0: {"x0": 70, "y0": 50, "contact_name": "son     ", "face_status": "Face"},
        },
        "contact_rows_x0": 300,
        "contact_rows_y0": 90,
        "contact_rows_objs": [
            [("daughter", 15)],
            [("wife", 12, "needs"), ("brother", 2, "needs")],
        ],
    }
    fig0_4_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_4",
        "fig_width": 700,
        "fig_height": 300,
        "infinity_contacts": {
            0: {"x0": 70, "y0": 50, "contact_name": "son     ", "face_status": "Face"},
        },
        "contact_rows_x0": 300,
        "contact_rows_y0": 90,
        "contact_rows_objs": [
            [("son", 8), ("daughter", 12)],
            [("wife", 12, "needs"), ("brother", 2, "needs")],
        ],
    }
    fig0_5_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_5",
        "fig_width": 700,
        "fig_height": 300,
        "contact_rows_x0": 50,
        "contact_rows_y0": 50,
        "contact_rows_objs": [
            [("son", 8), ("daughter", 12)],
            [("wife", 12, "needs"), ("brother", 2, "needs")],
            [("cousin", 5, "needs"), ("brother #2", 6, "needs"), ("uncle", 6, "needs")],
        ],
    }
    fig0_6_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_6",
        "fig_width": 700,
        "fig_height": 360,
        "contact_rows_x0": 50,
        "contact_rows_y0": 50,
        "contact_rows_objs": [
            [("son", 8), ("daughter", 12), ("neighbor", 2), ("friend #2", 6)],
            [("wife", 12, "needs"), ("brother", 2, "needs"), ("friend #1", 6)],
            [
                ("cousin", 5, "needs"),
                ("brother #2", 6, "needs"),
                ("uncle", 6, "needs"),
                ("friend #5", 4),
            ],
            [
                ("kid friend B1 dad", 5, "needs"),
                ("kid friend B2 mom", 6, "needs"),
                ("co-worker #2", 6, "needs"),
                ("supervisor #1", 10),
            ],
        ],
    }
    fig0_7_dict = {
        "curved_lines": [
            {"x1": 40, "y1": 40, "x2": 40, "y2": 320, "curvature": 0.1},
            {"x1": 40, "y1": 40, "x2": 350, "y2": 40, "curvature": -0.1},
            {"x1": 320, "y1": 140, "x2": 350, "y2": 40, "curvature": 0.3},
            {"x1": 320, "y1": 140, "x2": 370, "y2": 230, "curvature": -0.3},
            {"x1": 260, "y1": 260, "x2": 370, "y2": 230, "curvature": 0.2},
            {"x1": 260, "y1": 260, "x2": 200, "y2": 320, "curvature": -0.2},
            {"x1": 40, "y1": 320, "x2": 200, "y2": 320, "curvature": 0.15},
        ],
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_7",
        "fig_width": 700,
        "fig_height": 360,
        "contact_rows_x0": 50,
        "contact_rows_y0": 50,
        "contact_rows_objs": [
            [("son", 8), ("daughter", 12), ("neighbor", 2), ("friend #2", 6)],
            [("wife", 12, "needs"), ("brother", 2, "needs"), ("friend #1", 6)],
            [
                ("cousin", 5, "needs"),
                ("brother #2", 6, "needs"),
                ("uncle", 6, "needs"),
                ("friend #5", 4),
            ],
            [
                ("kid friend B1 dad", 5, "needs"),
                ("kid friend B2 mom", 6, "needs"),
                ("co-worker #2", 6, "needs"),
                ("supervisor #1", 10),
            ],
        ],
    }
    fig0_8_dict = {
        "fig_title_str": t_str,
        "fig_title_font_size": 18,
        "footer_str": "fig0_8",
        "fig_width": 700,
        "fig_height": 160,
        "contact_rows_x0": 180,
        "contact_rows_y0": 60,
        "contact_rows_objs": [[("Family", 12), ("Everyone Else", 12)]],
    }
    fig1_00_dict = {
        "fig_title_str": low_trust_str,
        "footer_str": "fig1_00",
        "fig_height": 250,
        "trapunits": [
            TrapeziodUnit(120, 100, 90, "Smiths"),
            TrapeziodUnit(220, 100, 90, "Duvals"),
            TrapeziodUnit(340, 100, 150, "Gomezs", 72),
        ],
        "land_y0": 180,
    }
    fig1_01_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": "The Smiths and the Duvals lift up the Gomezs",
        "sub_title_margin": 50,
        "footer_str": "fig1_01",
        "fig_height": 350,
        "trapunits": [
            TrapeziodUnit(120, 190, 90, "Smiths"),
            TrapeziodUnit(220, 190, 90, "Duvals", 72),
            TrapeziodUnit(170, 110, 110, "Gomezs", 72),
        ],
        "land_y0": 270,
    }
    smiths_str = "Smiths"
    duvals_str = "Duvals"
    gomezs_str = "Gomezs"
    flores_str = "Fabelas"
    fig1_02_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": "Flores lifts up the Gomezs and drags themselves down",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_02",
        "fig_width": 700,
        "fig_height": 450,
        "trapunits": [
            TrapeziodUnit(170, 130, 100, flores_str, 72),
            TrapeziodUnit(140, 210, 150, gomezs_str, 72),
            TrapeziodUnit(120, 290, 90, smiths_str),
            TrapeziodUnit(220, 290, 90, duvals_str, 72),
            TrapeziodUnit(470, 130, 100, gomezs_str, 72),
            TrapeziodUnit(440, 210, 150, flores_str, 72),
            TrapeziodUnit(420, 290, 90, smiths_str),
            TrapeziodUnit(520, 290, 90, duvals_str, 72),
        ],
        "land_y0": 370,
    }
    fig1_03_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": f"""{gomezs_str} is lifted up because {flores_str} thinks things will be better""",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_03",
        "fig_width": 800,
        "fig_height": 550,
        "trapunits": [
            TrapeziodUnit(170, 160, 100, flores_str, 72),
            TrapeziodUnit(140, 240, 150, gomezs_str, 72),
            TrapeziodUnit(120, 320, 90, smiths_str),
            TrapeziodUnit(220, 320, 90, duvals_str, 72),
            TrapeziodUnit(470, 120, 150, gomezs_str, 85),
            TrapeziodUnit(440, 215, 210, flores_str, 85),
            TrapeziodUnit(400, 310, 140, smiths_str, 85),
            TrapeziodUnit(550, 310, 140, duvals_str, 85),
        ],
        "land_y0": 410,
    }
    fam01 = "F1"
    fam02 = "F2"
    fam03 = "F3"
    fam04 = "F4"
    fam05 = "F5"
    fam06 = "F6"
    fam07 = "F7"
    fam08 = "F8"
    fam09 = "F9"
    fig1_04_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": """F1 is lifted up by F2, F3. Doesn't know the rest.""",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_04",
        "trapunits": [
            TrapeziodUnit(230, 90, 100, fam01, 50),
            TrapeziodUnit(200, 150, 80, fam02, 50),
            TrapeziodUnit(300, 150, 80, fam03, 50),
            TrapeziodUnit(160, 210, 90, fam04, 50),
            TrapeziodUnit(260, 210, 150, fam05, 50),
            TrapeziodUnit(270, 270, 100, fam06, 50),
            TrapeziodUnit(130, 270, 60, fam07, 50),
            TrapeziodUnit(380, 270, 60, fam08, 50),
            TrapeziodUnit(200, 270, 60, fam09, 50),
        ],
        "land_y0": 330,
    }
    fig1_05_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": """F1 is lifted up by F2, F3. Doesn't know the rest.""",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_05",
        "trapunits": [
            TrapeziodUnit(230, 90, 100, "F1", 50),
            TrapeziodUnit(190, 150, 180, "Lifting F1", 170),
        ],
        "land_y0": 330,
    }
    fig1_06_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": """F1 is lifted up by the Tower under it. Doesn't know the rest.""",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_06",
        "trapunits": [
            TrapeziodUnit(230, 90, 100, "F1", 50),
            TrapeziodUnit(190, 150, 180, "Tower", 170),
        ],
        "land_y0": 330,
    }
    fig1_07_dict = {
        "fig_title_str": low_trust_str,
        "sub_title_str": "F1 is lifted up by the Towers under it. Doesn't know the rest.",
        "sub_title_margin": 50,
        "sub_title_font_size": 20,
        "footer_str": "fig1_07",
        "tower_attrs": {"family_desc": "Family1", "tower_descs": ["Tower0", "Tower1"]},
    }
    fig1_08_dict = {
        "fig_title_str": low_trust_str,
        "footer_str": "fig1_08",
    }
    fig1_09_dict = {
        "fig_title_str": low_trust_str,
        "footer_str": "fig1_08",
    }
    fig1_10_dict = {
        "fig_title_str": low_trust_str,
        "footer_str": "fig1_08",
    }
    return {
        "wheel_fig0_0": get_wheel_fig(fig0_0_dict),
        "wheel_fig0_1": get_wheel_fig(fig0_1_dict),
        "wheel_fig0_2": get_wheel_fig(fig0_2_dict),
        "wheel_fig0_3": get_wheel_fig(fig0_3_dict),
        "wheel_fig0_4": get_wheel_fig(fig0_4_dict),
        "wheel_fig0_5": get_wheel_fig(fig0_5_dict),
        "wheel_fig0_6": get_wheel_fig(fig0_6_dict),
        "wheel_fig0_7": get_wheel_fig(fig0_7_dict),
        "wheel_fig0_8": get_wheel_fig(fig0_8_dict),
        "wheel_fig1_00": get_wheel_fig(fig1_00_dict),
        "wheel_fig1_01": get_wheel_fig(fig1_01_dict),
        "wheel_fig1_02": get_wheel_fig(fig1_02_dict),
        "wheel_fig1_03": get_wheel_fig(fig1_03_dict),
        "wheel_fig1_04": get_wheel_fig(fig1_04_dict),
        "wheel_fig1_05": get_wheel_fig(fig1_05_dict),
        "wheel_fig1_06": get_wheel_fig(fig1_06_dict),
        "wheel_fig1_07": get_wheel_fig(fig1_07_dict),
        "wheel_fig1_08": get_wheel_fig(fig1_08_dict),
        "wheel_fig1_09": get_wheel_fig(fig1_09_dict),
        "wheel_fig1_10": get_wheel_fig(fig1_10_dict),
    }


def rebuild_markdown_wheel_theory_images() -> list[str]:
    image_file_paths = []
    for filebasename, drawing in get_markdown_wheel_theory_drawings().items():
        image_file_path = save_to_images_dir(drawing, filebasename)
        image_file_paths.append(image_file_path)
    return image_file_paths
