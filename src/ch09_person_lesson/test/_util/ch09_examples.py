from src.ch04_rope.rope import RopeTerm, create_rope, create_rope_from_labels
from src.ch08_person_atom.atom_main import PersonAtom, personatom_shop
from src.ch09_person_lesson._ref.ch09_semantic_types import LabelTerm, MomentRope
from src.ch09_person_lesson.delta import PersonDelta, persondelta_shop
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_main import LessonUnit, lessonunit_shop
from src.ref.keywords import Ch09Keywords as kw, ExampleStrs as exx


def get_ch09_example_moment_rope() -> str:
    return ";FizzBuzz2;"


def get_ch09_example_person_lasso() -> LassoUnit:
    return lassounit_shop(get_ch09_example_moment_rope())


def get_texas_rope() -> RopeTerm:
    moment_rope = get_ch09_example_moment_rope()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_rope, nation_str, usa_str, texas_str])


def get_atom_example_factunit_knee(first_label: LabelTerm = None) -> PersonAtom:
    if not first_label:
        first_label = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(first_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(first_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = kw.person_plan_factunit
    insert_factunit_personatom = personatom_shop(x_dimen, kw.INSERT)
    insert_factunit_personatom.set_jkey(kw.plan_rope, ball_rope)
    insert_factunit_personatom.set_jkey(kw.fact_context, knee_rope)
    insert_factunit_personatom.set_jvalue(kw.fact_lower, knee_fact_lower)
    insert_factunit_personatom.set_jvalue(kw.fact_upper, knee_fact_upper)
    return insert_factunit_personatom


def get_atom_example_planunit_sports(moment_rope: MomentRope = None) -> PersonAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    insert_planunit_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    insert_planunit_personatom.set_jkey(kw.plan_rope, sports_rope)
    return insert_planunit_personatom


def get_atom_example_planunit_ball(moment_rope: MomentRope = None) -> PersonAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_personatom = personatom_shop(kw.person_planunit, kw.INSERT)
    insert_planunit_personatom.set_jkey(kw.plan_rope, ball_rope)
    return insert_planunit_personatom


def get_atom_example_planunit_knee(moment_rope: MomentRope = None) -> PersonAtom:
    if not moment_rope:
        moment_rope = exx.a23
    sports_str = "sports"
    sports_rope = create_rope(moment_rope, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_personatom = personatom_shop(kw.person_planunit, crud_str=kw.INSERT)
    insert_planunit_personatom.set_jkey(kw.plan_rope, knee_rope)
    insert_planunit_personatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_personatom.set_jvalue(close_str, knee_close)
    return insert_planunit_personatom


def get_persondelta_sue_example() -> PersonDelta:
    sue_persondelta = persondelta_shop()

    pool_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    pool_attribute = kw.credor_respect
    pool_personatom.set_jvalue(pool_attribute, 77)
    sue_persondelta.set_personatom(pool_personatom)

    dimen = kw.person_partnerunit
    sue_personatom = personatom_shop(dimen, kw.DELETE)
    sue_personatom.set_jkey(kw.partner_name, exx.sue)
    sue_persondelta.set_personatom(sue_personatom)
    return sue_persondelta


def get_persondelta_example1() -> PersonDelta:
    sue_persondelta = persondelta_shop()

    x_personatom = personatom_shop(kw.personunit, kw.UPDATE)
    x_personatom.set_jvalue(kw.max_tree_traverse, 66)
    x_personatom.set_jvalue(kw.credor_respect, 77)
    x_personatom.set_jvalue(kw.debtor_respect, 88)
    sue_persondelta.set_personatom(x_personatom)

    x_personatom = personatom_shop(dimen=kw.person_partnerunit, crud_str=kw.DELETE)
    x_personatom.set_jkey(kw.partner_name, exx.zia)
    sue_persondelta.set_personatom(x_personatom)
    return sue_persondelta


def get_sue_lessonunit() -> LessonUnit:
    return lessonunit_shop(person_name="Sue", lesson_id=37, face_name="Yao")


def sue_1personatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(person_name="Sue", lesson_id=53, face_name="Yao")
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_sports())
    return x_lessonunit


def sue_2personatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(person_name="Sue", lesson_id=53, face_name="Yao")
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_knee())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_sports())
    return x_lessonunit


def sue_3personatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(person_name="Sue", lesson_id=37, face_name="Yao")
    x_lessonunit.persondelta.set_personatom(get_atom_example_factunit_knee())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_ball())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_knee())
    return x_lessonunit


def sue_4personatoms_lessonunit() -> LessonUnit:
    x_lessonunit = lessonunit_shop(person_name="Sue", lesson_id=47, face_name="Yao")
    x_lessonunit.persondelta.set_personatom(get_atom_example_factunit_knee())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_ball())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_knee())
    x_lessonunit.persondelta.set_personatom(get_atom_example_planunit_sports())
    return x_lessonunit
