from pytest import raises as pytest_raises
from sqlite3 import Cursor
from src.ch00_py.db_toolbox import get_rowdata
from src.ch04_rope.rope import create_rope
from src.ch08_person_atom.atom_main import get_personatom_from_rowdata, personatom_shop
from src.ch08_person_atom.test._util.ch08_env import cursor0
from src.ref.keywords import Ch08Keywords as kw


def test_PersonAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.person_plan_factunit
    update_disc_personatom = personatom_shop(x_dimen, kw.UPDATE)
    update_disc_personatom.set_jkey("reason_context", knee_rope)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_personatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_dimen}' with is_valid=False."
    )


def test_PersonAtom_get_insert_sqlstr_ReturnsObj_PersonUnitSimpleAttrs():
    # ESTABLISH
    new2_value = 66
    dimen = kw.personunit
    opt_arg2 = kw.max_tree_traverse
    x_personatom = personatom_shop(dimen, kw.UPDATE)
    x_personatom.set_jvalue(opt_arg2, new2_value)
    x_table = "atom_hx"
    example_sqlstr = f"""
INSERT INTO {x_table} (
  {dimen}_{kw.UPDATE}_{opt_arg2}
)
VALUES
  ({new2_value})
;
"""

    # WHEN / THEN
    assert x_personatom.get_insert_sqlstr() == example_sqlstr


def test_PersonAtom_get_insert_sqlstr_ReturnsObj_plan_factunit():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_reason_lower = 7
    x_dimen = kw.person_plan_factunit
    update_disc_personatom = personatom_shop(x_dimen, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_personatom.set_jvalue(kw.fact_lower, knee_reason_lower)

    # WHEN
    generated_sqlstr = update_disc_personatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""
INSERT INTO {kw.atom_hx} (
  {x_dimen}_{kw.INSERT}_{kw.plan_rope}
, {x_dimen}_{kw.INSERT}_{kw.fact_context}
, {x_dimen}_{kw.INSERT}_{kw.fact_lower}
)
VALUES
  ('{ball_rope}', '{knee_rope}', {knee_reason_lower})
;
"""
    print(f"{generated_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_personatom_from_rowdata_ReturnsObj_plan_factunit(cursor0: Cursor):
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    knee_fact_lower = 7
    x_dimen = kw.person_plan_factunit
    x_sqlstr = f"""SELECT
  '{ball_rope}' as {x_dimen}_{kw.INSERT}_{kw.plan_rope}
, '{knee_rope}' as {x_dimen}_{kw.INSERT}_{kw.fact_context}
, {knee_fact_lower} as {x_dimen}_{kw.INSERT}_{kw.fact_lower}
"""
    x_rowdata = get_rowdata(kw.atom_hx, cursor0, x_sqlstr)

    # WHEN
    x_personatom = get_personatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_personatom = personatom_shop(x_dimen, kw.INSERT)
    update_disc_personatom.set_jkey(kw.plan_rope, ball_rope)
    update_disc_personatom.set_jkey(kw.fact_context, knee_rope)
    update_disc_personatom.set_jvalue(kw.fact_lower, knee_fact_lower)
    assert update_disc_personatom.dimen == x_personatom.dimen
    assert update_disc_personatom.crud_str == x_personatom.crud_str
    assert update_disc_personatom.jkeys == x_personatom.jkeys
    assert update_disc_personatom.jvalues == x_personatom.jvalues
