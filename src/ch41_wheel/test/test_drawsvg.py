from ch41_wheel.wheel_builder import (
    draw_trapezoid_shape,
    draw_trapezoid_stack,
    draw_contacts_row,
    draw_infinity_contact,
    draw_contact_rows,
    get_standard_drawing,
    save_to_images_dir,
    rebuild_markdown_wheel_theory_images,
    get_markdown_wheel_theory_drawings,
    TrapeziodUnit,
    draw_land,
)
from drawsvg import Drawing
from copy import deepcopy as copy_deepcopy
from pathlib import Path
from os.path import exists as os_path_exists
from re import compile as re_compile, Match as re_Match


def _get_elements_count(d: Drawing) -> int:
    return len(d.__dict__.get("elements"))


def save_example_image(d: Drawing, filebasename: str = "theory"):
    # Save the SVG
    output_file_path = save_to_images_dir(d, filebasename)
    print(f"Saved SVG to: {output_file_path}")


def test_draw_contacts_row_SetsAttr_Scenario0_4People():
    # ESTABLISH
    contacts = [
        {"contact_name": "Alice", "face_status": "Face"},
        {"contact_name": "Bob", "face_status": "needs"},
        {"contact_name": "Christopher", "face_status": "needs"},
        {"contact_name": "Dee", "face_status": "Face"},
    ]

    # WHEN
    drawing = draw_contacts_row(contacts)

    # THEN
    assert drawing
    # save_example_image(drawing)


def test_draw_infinity_contact_SetsAttr_Scenario0_ContactWithFace(rebuild_docs):
    # ESTABLISH
    # drawing = Drawing(2 * x_margin + 2 * radius, 2 * y_margin + radius, origin=(0, 0))
    drawing = get_standard_drawing()
    contact_name = "Doug Something of Someplace"
    face_status = "Face"
    font_size = 14
    face_font_size = 18
    x0 = 55
    y0 = 20
    d0_old = copy_deepcopy(drawing)
    assert drawing.__dict__ == d0_old.__dict__

    # WHEN
    draw_infinity_contact(
        d=drawing,
        x0=x0,
        y0=y0,
        font_size=font_size,
        face_font_size=face_font_size,
        contact_name=contact_name,
        face_status=face_status,
    )

    # THEN
    assert drawing.__dict__ != d0_old.__dict__
    # if rebuild_docs:
    #     save_example_image(drawing)


def test_draw_trapezoid_shape_SetsAttr_Scenario0_No_height():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_shape(d0, 50, 50, 50, "test2")

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    elements_str = "elements"
    print(f"{d0_old.__dict__.get(elements_str)=}")
    print(f"    {d0.__dict__.get(elements_str)=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)


def test_draw_trapezoid_shape_SetsAttr_Scenario1_height_Passed():
    # ESTABLISH
    d0 = get_standard_drawing()
    d0_old = copy_deepcopy(d0)
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_shape(d0, 50, 50, 50, "test2", height=80)

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    elements_str = "elements"
    print(f"{d0_old.__dict__.get(elements_str)=}")
    print(f"    {d0.__dict__.get(elements_str)=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_TrapeziodUnit_Exists():
    # ESTABLISH / WHEN
    trapunit = TrapeziodUnit()
    # THEN
    assert not trapunit.x0
    assert not trapunit.y0
    assert not trapunit.bottom_length
    assert not trapunit.family_title
    assert not trapunit.height


# def test_draw_trapezoid_row_SetsAttr_Scenario0_1Element():
#     # ESTABLISH
#     d0 = get_standard_drawing()
#     d0_old = copy_deepcopy(d0)
#     assert d0.__dict__ == d0_old.__dict__

#     # WHEN
#     draw_trapezoid_row(d0, 50, 50, 50, ["test2"])

#     # THEN
#     assert d0.__dict__ != d0_old.__dict__
#     elements_str = "elements"
#     print(f"{d0_old.__dict__.get(elements_str)=}")
#     print(f"    {d0.__dict__.get(elements_str)=}")
#     assert _get_elements_count(d0) != _get_elements_count(d0_old)
#     # save_example_image(d0)


# def test_draw_trapezoid_row_SetsAttr_Scenario1_3Elements():
#     # ESTABLISH
#     d0 = get_standard_drawing()
#     d0_old = copy_deepcopy(d0)
#     assert d0.__dict__ == d0_old.__dict__

#     # WHEN
#     draw_trapezoid_row(d0, 50, 50, 50, ["test0", "test1", "test2"])

#     # THEN
#     assert d0.__dict__ != d0_old.__dict__
#     elements_str = "elements"
#     print(f"{d0_old.__dict__.get(elements_str)=}")
#     print(f"    {d0.__dict__.get(elements_str)=}")
#     assert _get_elements_count(d0) != _get_elements_count(d0_old)
#     # save_example_image(d0)


def test_draw_trapezoid_stack_SetsAttr_Scenario0_3Elements():
    # ESTABLISH
    d0 = get_standard_drawing(350, 150)
    d0_old = copy_deepcopy(d0)
    fam0_trapunit = TrapeziodUnit(20, 30, 80, "Fam0")
    fam1_trapunit = TrapeziodUnit(120, 30, 80, "Fam1")
    fam2_trapunit = TrapeziodUnit(220, 30, 80, "Fam2")
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_stack(d0, [fam0_trapunit, fam1_trapunit, fam2_trapunit])

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    elements_str = "elements"
    # print(f"{d0_old.__dict__.get(elements_str)=}")
    # print(f"    {d0.__dict__.get(elements_str)=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    # save_example_image(d0)


def test_draw_trapezoid_stack_SetsAttr_Scenario1_7Elements():
    # ESTABLISH
    d0 = get_standard_drawing(400, 440)
    d0_old = copy_deepcopy(d0)
    fam0_trapunit = TrapeziodUnit(40, 130, 80, "Fam0")
    fam1_trapunit = TrapeziodUnit(130, 130, 80, "Fam1")
    fam2_trapunit = TrapeziodUnit(220, 130, 80, "Fam2")
    fam3_trapunit = TrapeziodUnit(180, 200, 160, "Fam3", 80)
    fam4_trapunit = TrapeziodUnit(20, 200, 160, "Fam4", 140)
    fam5_trapunit = TrapeziodUnit(190, 290, 175, "Fam5", 50)
    fam6_trapunit = TrapeziodUnit(70, 90, 195, "Fam6", 35)
    trapunits = [
        fam0_trapunit,
        fam1_trapunit,
        fam2_trapunit,
        fam3_trapunit,
        fam4_trapunit,
        fam5_trapunit,
        fam6_trapunit,
    ]
    assert d0.__dict__ == d0_old.__dict__

    # WHEN
    draw_trapezoid_stack(d0, trapunits)

    # THEN
    assert d0.__dict__ != d0_old.__dict__
    elements_str = "elements"
    # print(f"{d0_old.__dict__.get(elements_str)=}")
    # print(f"    {d0.__dict__.get(elements_str)=}")
    assert _get_elements_count(d0) != _get_elements_count(d0_old)
    draw_land(d0, 10, 350, 370, "Land", stroke_width=6)
    # save_example_image(d0)


def test_draw_contact_rows_SetsAttr_Scenario0_2Rows():
    # ESTABLISH
    rows = [
        [("Alice", 5, "need"), ("Bob", 20)],
        [("Sue", 12, "need"), ("Christopher", 2, "need")],
    ]
    d0_curr = get_standard_drawing()
    d0_old = copy_deepcopy(d0_curr)
    assert d0_curr.__dict__ == d0_old.__dict__

    # WHEN
    draw_contact_rows(d0_curr, rows)

    # THEN
    assert d0_curr.__dict__ != d0_old.__dict__
    assert _get_elements_count(d0_curr) != _get_elements_count(d0_old)
    # save_example_image(drawing)


def test_rebuild_markdown_wheel_theory_images_SpecialCreateImages(rebuild_docs):
    # ESTABLISH / WHEN / THEN
    # sourcery skip: no-conditionals-in-tests
    if rebuild_docs:
        svg_image_paths = rebuild_markdown_wheel_theory_images()
        for svg_image_path in svg_image_paths:
            print(f"Saved {svg_image_path}")
        # assert False, f"Special Images Rebuilt {len(svg_image_paths)} images built."


_NUMBER_RE = re_compile(r"-?\d+\.\d+")


def normalize_svg(svg: str, decimals: int = 8) -> str:
    def repl(match: re_Match[str]) -> str:
        return f"{float(match.group()):.{decimals}f}"

    return _NUMBER_RE.sub(repl, svg)


def test_get_markdown_wheel_theory_drawings_ReturnsObj_HasExpectedKeys():
    # ESTABLISH / WHEN
    wheel_theory_filebasenames = set(get_markdown_wheel_theory_drawings().keys())
    # THEN
    print(wheel_theory_filebasenames)
    expected_wheel_theory_filebasenames = {
        'wheel_fig0_0',
        'wheel_fig0_1',
        'wheel_fig0_2',
        'wheel_fig0_3',
        'wheel_fig0_4',
        'wheel_fig0_5',
        'wheel_fig0_6',
        'wheel_fig0_7',
        'wheel_fig0_8',
        "wheel_fig1_00",
        "wheel_fig1_01",
        "wheel_fig1_02",
        "wheel_fig1_03",
        "wheel_fig1_04",
        "wheel_fig1_05",
        "wheel_fig1_06",
        "wheel_fig1_07",
        "wheel_fig1_08",
        "wheel_fig1_09",
        "wheel_fig1_10",
    }
    assert wheel_theory_filebasenames == expected_wheel_theory_filebasenames


def test_get_markdown_wheel_theory_drawings_ReturnsObj_MatcheStaticFiles():
    # ESTABLISH
    for filebasename, drawing in get_markdown_wheel_theory_drawings().items():
        project_dir = Path(__file__).resolve().parent.parent
        # Save the SVG
        output_file_path = project_dir / "images" / f"{filebasename}.svg"
        assert os_path_exists(output_file_path)

        # WHEN
        curr_svg_text = output_file_path.read_text()

        # THEN
        assert normalize_svg(curr_svg_text) == normalize_svg(drawing.as_svg())
        print(f"{output_file_path=}")
