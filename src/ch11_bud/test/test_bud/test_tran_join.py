from ch11_bud.bud_main import tranbook_shop, tranunit_shop
from ref.keywords import ExampleStrs as exx


def test_TranBook_join_SetsAttr():
    # ESTABLISH
    m23_tranbook = tranbook_shop(exx.a23)
    t55_t = 5505
    t55_yao_amount = -55
    t66_t = 6606
    t66_yao_amount = -66
    m23_tranbook.set_tranunit(tranunit_shop(exx.sue, exx.yao, t55_t, t55_yao_amount))
    m23_tranbook.set_tranunit(tranunit_shop(exx.sue, exx.yao, t66_t, t66_yao_amount))

    t55_bob_amount = 600
    m24_tranbook = tranbook_shop("amy24")
    m24_tranbook.set_tranunit(tranunit_shop(exx.sue, exx.bob, t55_t, t55_bob_amount))

    assert m23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)
    assert m23_tranbook.tranunit_exists(exx.sue, exx.yao, t66_t)
    assert m23_tranbook.tranunit_exists(exx.sue, exx.bob, t55_t) is False
    assert m24_tranbook.tranunit_exists(exx.sue, exx.bob, t55_t)

    # WHEN
    m23_tranbook.join(m24_tranbook)

    # THEN
    assert m23_tranbook.tranunit_exists(exx.sue, exx.yao, t55_t)
    assert m23_tranbook.tranunit_exists(exx.sue, exx.yao, t66_t)
    assert m23_tranbook.tranunit_exists(exx.sue, exx.bob, t55_t)
    assert m24_tranbook.tranunit_exists(exx.sue, exx.bob, t55_t)
