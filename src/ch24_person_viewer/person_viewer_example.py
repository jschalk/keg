from src.ch02_contact.group import awardunit_shop
from src.ch03_workforce.workforce import workforceunit_shop
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch07_person_logic.person_tool import person_plan_reason_caseunit_set_obj
from src.ch07_person_logic.test._util.ch07_examples import (
    get_personunit_irrational_example,
)


def sue2_str() -> str:
    return "Sue"


def bob2_str() -> str:
    return "Bob"


def best_sport_str() -> str:
    return "best sport"


def best_soccer_str() -> str:
    return "The best sport is soccer"


def best_bowl_str() -> str:
    return "The best sport is bowling"


def best_run_str() -> str:
    return "The best sport is running"


def play_str() -> str:
    return "playing"


def play_soccer_str() -> str:
    return "play soccer"


def play_bowl_str() -> str:
    return "play bowling"


def play_run_str() -> str:
    return "play running"


def get_sue_personunit() -> PersonUnit:
    sue_person = personunit_shop(sue2_str(), ";accord23;")
    sue_cred_lumen = 11
    sue_debt_lumen = 13
    bob_cred_lumen = 23
    bob_debt_lumen = 29
    sue_person.add_contactunit(sue2_str(), sue_cred_lumen, sue_debt_lumen)
    sue_person.add_contactunit(bob2_str(), bob_cred_lumen, bob_debt_lumen)
    sue_contact = sue_person.get_contact(sue2_str())
    bowlers_str = ";bowlers"
    team_str = ";Team Administrator"
    sue_contact.add_membership(bowlers_str, 77, 51)
    bob_contact = sue_person.get_contact(bob2_str())
    bob_contact.add_membership(bowlers_str, 12, 37)
    bob_contact.add_membership(team_str, 51, 91)

    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, "clean")
    mop_rope = sue_person.make_rope(clean_rope, "mop")
    mop_fancy_rope = sue_person.make_rope(mop_rope, "use fancy mop")
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    tidi_rope = sue_person.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_person.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_person.make_rope(tidi_rope, "tidy")
    sue_person.add_plan(casa_rope, 3)
    sue_person.add_plan(tidi_rope, 7)
    sue_person.add_plan(dirty_rope, 1)
    sue_person.add_plan(tidy_rope, 3)
    sue_person.add_plan(clean_rope, 3)
    sue_person.add_plan(mop_rope, 3, pledge=True)
    sue_person.add_plan(mop_fancy_rope, 3, pledge=True)
    sue_person.add_plan(sweep_rope, 3, pledge=True)
    sports_rope = sue_person.make_l1_rope("sports")
    best_rope = sue_person.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_person.make_rope(best_rope, best_soccer_str())
    best_bowl_rope = sue_person.make_rope(best_rope, best_bowl_str())
    best_run_rope = sue_person.make_rope(best_rope, best_run_str())
    play_rope = sue_person.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_person.make_rope(play_rope, play_soccer_str())
    play_bowl_rope = sue_person.make_rope(play_rope, play_bowl_str())
    play_run_rope = sue_person.make_rope(play_rope, play_run_str())
    sue_person.add_plan(sports_rope, 5)
    sue_person.add_plan(best_soccer_rope, 23)
    sue_person.add_plan(best_bowl_rope, 2)
    sue_person.add_plan(best_run_rope, 23)
    sue_person.add_plan(play_rope, 2)
    sue_person.add_plan(play_soccer_rope, 11, pledge=True)
    sue_person.add_plan(play_bowl_rope, 55, pledge=True)
    sue_person.add_plan(play_run_rope, 22, pledge=True)

    # Add some award links
    casa_administrator_awardunit = awardunit_shop("Administrator", 0.5, 0.2)
    casa_team_awardunit = awardunit_shop(team_str, 0.3, 0.1)
    casa_devloper_awardunit = awardunit_shop(sue2_str(), 1, 0.8)
    casa_jundevloper_awardunit = awardunit_shop("Bob", 0.7, 0.9)
    root_rope = sue_person.planroot.get_plan_rope()
    sue_person.edit_plan_attr(root_rope, awardunit=casa_administrator_awardunit)
    sue_person.edit_plan_attr(root_rope, awardunit=casa_team_awardunit)
    sue_person.edit_plan_attr(casa_rope, awardunit=casa_devloper_awardunit)
    sue_person.edit_plan_attr(casa_rope, awardunit=casa_jundevloper_awardunit)
    sue_person.conpute()
    return sue_person


def get_sue_person_with_facts_and_reasons() -> PersonUnit:
    sue_person = get_sue_personunit()
    casa_rope = sue_person.make_l1_rope("casa")
    clean_rope = sue_person.make_rope(casa_rope, "clean")
    mop_rope = sue_person.make_rope(clean_rope, "mop")
    sweep_rope = sue_person.make_rope(clean_rope, "sweep")
    tidi_rope = sue_person.make_rope(casa_rope, "tidiness")
    dirty_rope = sue_person.make_rope(tidi_rope, "dirty")
    tidy_rope = sue_person.make_rope(tidi_rope, "tidy")
    sports_rope = sue_person.make_l1_rope("sports")
    best_rope = sue_person.make_rope(sports_rope, best_sport_str())
    best_soccer_rope = sue_person.make_rope(best_rope, best_soccer_str())
    best_bowl_rope = sue_person.make_rope(best_rope, best_bowl_str())
    best_run_rope = sue_person.make_rope(best_rope, best_run_str())
    play_rope = sue_person.make_rope(sports_rope, play_str())
    play_soccer_rope = sue_person.make_rope(play_rope, play_soccer_str())
    play_bowl_rope = sue_person.make_rope(play_rope, play_bowl_str())
    play_run_rope = sue_person.make_rope(play_rope, play_run_str())
    sue_person.add_fact(tidi_rope, dirty_rope, 4, 8)
    sue_person.add_fact(best_rope, best_soccer_rope, 1, 7)
    mop_workforceunit = workforceunit_shop()
    mop_workforceunit.add_labor(sue2_str())
    mop_workforceunit.add_labor(bob2_str(), True)
    sue_person.edit_plan_attr(mop_rope, workforceunit=mop_workforceunit)
    # add reasons to mop_plan, sweep_plan, play_soccer_plan, plan_bowl_plan, play_run_plan
    x_plan = "plan_rope"
    x_context = "reason_context"
    x_state = "reason_state"
    tidi_dirty_jkeys = {x_plan: mop_rope, x_context: tidi_rope, x_state: dirty_rope}
    swwep_dirty_jkeys = {x_plan: sweep_rope, x_context: tidi_rope, x_state: dirty_rope}
    soccer_soccer_jkeys = {
        x_plan: play_soccer_rope,
        x_context: best_rope,
        x_state: best_soccer_rope,
    }
    soccer_run_jkeys = {
        x_plan: play_soccer_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    soccer_tidy_jkeys = {
        x_plan: play_soccer_rope,
        x_context: tidi_rope,
        x_state: tidy_rope,
    }
    bowl_bowl_jkeys = {
        x_plan: play_bowl_rope,
        x_context: best_rope,
        x_state: best_bowl_rope,
    }
    bowl_tidy_jkeys = {x_plan: play_bowl_rope, x_context: tidi_rope, x_state: tidy_rope}
    run_run_jkeys = {
        x_plan: play_run_rope,
        x_context: best_rope,
        x_state: best_run_rope,
    }
    person_plan_reason_caseunit_set_obj(sue_person, tidi_dirty_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, swwep_dirty_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, soccer_soccer_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, soccer_run_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, soccer_tidy_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, bowl_bowl_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, bowl_tidy_jkeys)
    person_plan_reason_caseunit_set_obj(sue_person, run_run_jkeys)
    sue_person.conpute()
    return sue_person
