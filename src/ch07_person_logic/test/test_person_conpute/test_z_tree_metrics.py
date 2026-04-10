from src.ch02_contact.contact import contactunit_shop
from src.ch02_contact.group import awardunit_shop
from src.ch04_rope.rope import create_rope_from_labels
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import personunit_shop
from src.ch07_person_logic.test._util.ch07_examples import personunit_v001
from src.ref.keywords import ExampleStrs as exx


def test_PersonUnit_get_tree_metrics_Exists():
    # ESTABLISH
    zia_person = personunit_shop(person_name="Zia")

    # WHEN
    zia_person_tree_metrics = zia_person.get_tree_metrics()

    # THEN
    assert zia_person_tree_metrics.label_count is not None
    assert zia_person_tree_metrics.reason_contexts is not None
    assert zia_person_tree_metrics.tree_level_count is not None
    assert zia_person_tree_metrics.awardunits_metrics is not None


def test_PersonUnit_get_tree_metrics_get_plan_plan_uid_max_GetsMaxPlanplan_uid():
    # ESTABLISH
    yao_person = personunit_v001()

    # WHEN
    tree_metrics_x = yao_person.get_tree_metrics()

    # THEN
    assert tree_metrics_x.plan_uid_max == 279
    assert yao_person.get_plan_plan_uid_max() == 279


def test_PersonUnit_get_tree_metrics_SetsBoolean_all_plan_plan_uids_are_unique():
    # ESTABLISH
    yao_person = personunit_v001()

    # WHEN
    tree_metrics_x = yao_person.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_plan_plan_uids_are_unique is False
    assert len(tree_metrics_x.plan_uid_dict) == 219


def test_PersonUnit_get_tree_set_all_plan_plan_uids_unique():
    # ESTABLISH
    yao_person = personunit_v001()
    tree_metrics_before = yao_person.get_tree_metrics()
    assert len(tree_metrics_before.plan_uid_dict) == 219

    # WHEN
    yao_person.set_all_plan_plan_uids_unique()

    # THEN
    tree_metrics_after = yao_person.get_tree_metrics()
    # for plan_uid, plan_uid_count in tree_metrics_after.plan_uid_dict.items():
    #     # print(f"{plan_uid=} {plan_uid_count=} {len(yao_person.get_plan_dict())=}")
    #     print(f"{plan_uid=} {plan_uid_count=} ")
    assert len(tree_metrics_after.plan_uid_dict) == 252
    assert tree_metrics_after.all_plan_plan_uids_are_unique is True


def test_PersonUnit_set_all_plan_plan_uids_unique_Setsplan_uids():
    # ESTABLISH
    zia_person = personunit_shop(person_name=exx.zia)
    sports_str = "sports"
    zia_person.set_l1_plan(planunit_shop(exx.bowl, plan_uid=None))
    zia_person.set_l1_plan(planunit_shop(sports_str, plan_uid=2))
    bowl_rope = zia_person.make_l1_rope(exx.bowl)
    assert zia_person.get_plan_obj(bowl_rope).plan_uid is None

    # WHEN
    zia_person.set_all_plan_plan_uids_unique()

    # THEN
    assert zia_person.get_plan_obj(bowl_rope).plan_uid is not None


def test_PersonUnit_get_tree_metrics_ReturnsANone_pledge_PlanRopeTerm():
    # ESTABLISH
    nia_str = "Nia"
    nia_person = personunit_shop(nia_str)
    wk = "wk"
    nia_person.set_l1_plan(planunit_shop(wk, star=40))
    tree_metrics_before = nia_person.get_tree_metrics()

    # WHEN / THEN
    assert tree_metrics_before.last_evaluated_pledge_plan_rope is None


def test_PersonUnit_get_tree_metrics_Returns_pledge_PlanRopeTerm():
    # ESTABLISH
    yao_person = personunit_v001()
    yao_tree_metrics = yao_person.get_tree_metrics()

    # WHEN / THEN
    traain_rope = create_rope_from_labels(
        [
            yao_person.planroot.plan_label,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Deterrence and Reporting guildlines",
            "Accomplish Fall 2021 traaining",
        ]
    )
    assert yao_tree_metrics.last_evaluated_pledge_plan_rope == traain_rope


def test_PersonUnit_get_tree_metrics_TracksReasonsThatHaveNoFactreason_contexts():
    # ESTABLISH
    yao_personunit = personunit_v001()

    # WHEN
    yao_tree_metrics = yao_personunit.get_tree_metrics()

    # THEN
    print(f"{yao_tree_metrics.tree_level_count=}")
    print(f"{yao_tree_metrics.reason_contexts=}")
    assert yao_tree_metrics is not None
    reason_contexts_x = yao_tree_metrics.reason_contexts
    assert reason_contexts_x is not None
    assert len(reason_contexts_x) > 0


def test_PersonUnit_get_missing_fact_reason_contexts_ReturnsAllreason_contextsNotCoveredByFacts():
    # ESTABLISH
    yao_personunit = personunit_v001()
    missing_reason_contexts = yao_personunit.get_missing_fact_reason_contexts()
    assert missing_reason_contexts is not None
    print(f"{missing_reason_contexts=}")
    print(f"{len(missing_reason_contexts)=}")
    assert len(missing_reason_contexts) == 11

    yao_personunit.add_fact(
        yao_personunit.make_l1_rope("jour_minute"),
        fact_state=yao_personunit.make_l1_rope("jour_minute"),
        fact_lower=0,
        fact_upper=1439,
    )

    # WHEN
    missing_reason_contexts = yao_personunit.get_missing_fact_reason_contexts()

    # THEN
    assert len(missing_reason_contexts) == 11


def test_PersonUnit_3AdvocatesNoplanunit_shop():
    # ESTABLISH

    zia_personunit = personunit_shop("Zia")
    yao_contactunit = contactunit_shop(contact_name=exx.yao)
    sue_contactunit = contactunit_shop(contact_name=exx.sue)
    zia_contactunit = contactunit_shop(contact_name=exx.zia)
    # print(f"{yao=}")
    zia_personunit.set_contactunit(yao_contactunit)
    zia_personunit.set_contactunit(sue_contactunit)
    zia_personunit.set_contactunit(zia_contactunit)
    zia_personunit.planroot.set_awardunit(awardunit_shop(exx.yao, give_force=10))
    zia_personunit.planroot.set_awardunit(awardunit_shop(exx.sue, give_force=10))
    zia_personunit.planroot.set_awardunit(awardunit_shop(exx.zia, give_force=10))

    # WHEN
    assert zia_personunit.get_awardunits_metrics() is not None
    contacts_metrics = zia_personunit.get_awardunits_metrics()

    # THEN
    yao_awardunit = contacts_metrics[exx.yao]
    sue_awardunit = contacts_metrics[exx.sue]
    zia_awardunit = contacts_metrics[exx.zia]
    assert yao_awardunit.awardee_title is not None
    assert sue_awardunit.awardee_title is not None
    assert zia_awardunit.awardee_title is not None
    assert yao_awardunit.awardee_title == exx.yao
    assert sue_awardunit.awardee_title == exx.sue
    assert zia_awardunit.awardee_title == exx.zia
