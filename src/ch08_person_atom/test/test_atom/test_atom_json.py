from ch04_rope.rope import create_rope
from ch08_person_atom.atom_main import get_personatom_from_dict, personatom_shop
from ref.keywords import Ch08Keywords as kw


def test_PersonAtom_to_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.person_plan_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    insert_factunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    insert_factunit_personatom.set_jkey(kw.plan_rope, ball_rope)
    insert_factunit_personatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_personatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    insert_factunit_personatom.set_jvalue(kw.fact_upper, knee_reason_upper)

    # WHEN
    atom_dict = insert_factunit_personatom.to_dict()

    # THEN
    assert atom_dict == {
        kw.dimen: x_dimen,
        kw.crud: kw.INSERT,
        kw.jkeys: {kw.plan_rope: ball_rope, kw.fact_context: knee_rope},
        kw.jvalues: {
            kw.fact_lower: knee_reason_lower,
            kw.fact_upper: knee_reason_upper,
        },
    }


def test_get_personatom_from_dict_ReturnsObj():
    # ESTABLISH
    sports_str = "sports"
    sports_rope = create_rope("a", sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope("a", knee_str)
    x_dimen = kw.person_plan_factunit
    knee_reason_lower = 7
    knee_reason_upper = 13
    gen_personatom = personatom_shop(x_dimen, kw.INSERT)
    gen_personatom.set_jkey(kw.plan_rope, ball_rope)
    gen_personatom.set_jkey(kw.fact_context, knee_rope)
    gen_personatom.set_jvalue(kw.fact_lower, knee_reason_lower)
    gen_personatom.set_jvalue(kw.fact_upper, knee_reason_upper)
    atom_serializable_dict = gen_personatom.to_dict()

    # WHEN
    gen_personatom = get_personatom_from_dict(atom_serializable_dict)

    # THEN
    assert gen_personatom.dimen == gen_personatom.dimen
    assert gen_personatom.crud_str == gen_personatom.crud_str
    assert gen_personatom.jkeys == gen_personatom.jkeys
    assert gen_personatom.jvalues == gen_personatom.jvalues
    assert gen_personatom == gen_personatom
