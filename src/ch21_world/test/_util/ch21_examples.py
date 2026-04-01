from pandas import DataFrame as pandas_DataFrame
from src.ch04_rope.rope import create_rope, create_rope_from_labels as init_rope
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch13_time.epoch_main import add_epoch_planunit
from src.ref.keywords import Ch21Keywords as kw, ExampleStrs as exx


def br00013_example() -> pandas_DataFrame:
    """All rows valid. pledge=True throughout. Covers varied names."""

    hr_mop = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.mop])
    hr_tools = init_rope(["herenow_red", "family", exx.casa, exx.clean, exx.scrub])
    hb_mop = init_rope(["herenow_blu", "family", exx.casa, exx.clean, exx.mop])
    hb_grocery = init_rope(["herenow_blu", "family", exx.casa, exx.clean, "grocery"])
    hb_brush = init_rope(["herenow_blu", "family", exx.casa, exx.clean, "brush"])

    data = [
        (0, exx.sue, exx.zia, exx.hn_red, hr_mop, 1, True),
        (0, exx.sue, exx.yao, exx.hn_red, hr_tools, 2, True),
        (2, exx.yao, exx.yao, exx.hn_blu, hb_mop, 8, True),
        (3, exx.sue, exx.sue, exx.hn_blu, hb_grocery, 3, True),
        (4, exx.zia, exx.xio, exx.hn_blu, hb_brush, 1, True),
    ]
    cols = [
        kw.spark_num,
        kw.face_name,
        kw.person_name,
        kw.moment_rope,
        kw.plan_rope,
        kw.star,
        kw.pledge,
    ]
    return pandas_DataFrame(data, columns=cols)
