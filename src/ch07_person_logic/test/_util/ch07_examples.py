from enum import Enum
from src.ch00_py.file_toolbox import open_json
from src.ch03_workforce.workforce import workforceunit_shop
from src.ch04_rope.rope import RopeTerm, create_rope
from src.ch05_reason.reason_main import factunit_shop, reasonunit_shop
from src.ch06_plan.plan import planunit_shop
from src.ch07_person_logic.person_main import (
    PersonUnit,
    get_personunit_from_dict,
    personunit_shop,
)
from src.ref.keywords import ExampleStrs as exx

# from src.ch00_py.file_toolbox import save_file
# from src.ch07_person_logic.test._util.ch07_env import get_person_examples_dir as env_dir
# from src.ch07_person_logic.test._util.example_persons import personunit_v001, personunit_v002

# save_json(env_dir(), "example_person3.json", personunit_v001().to_dict())
# save_json(env_dir(), "example_person4.json", personunit_v002().to_dict())


def personunit_v001() -> PersonUnit:
    person1_path = "src/ch07_person_logic/test/_util/example_person1.json"
    return get_personunit_from_dict(open_json(person1_path))


def personunit_v001_with_large_agenda() -> PersonUnit:
    yao_person = personunit_v001()
    jour_minute_rope = yao_person.make_l1_rope("jour_minute")
    month_wk_rope = yao_person.make_l1_rope("month_wk")
    nations_rope = yao_person.make_l1_rope("Nation-States")
    mood_rope = yao_person.make_l1_rope("Moods")
    aaron_rope = yao_person.make_l1_rope("Aaron Donald objects effected by him")
    yr_month_rope = yao_person.make_l1_rope("yr_month")
    season_rope = yao_person.make_l1_rope("Seasons")
    ced_wk_rope = yao_person.make_l1_rope("ced_wk")
    sem_jours_rope = yao_person.make_l1_rope("sem_jours")

    yao_person.add_fact(aaron_rope, aaron_rope)
    yao_person.add_fact(ced_wk_rope, ced_wk_rope, fact_lower=0, fact_upper=53)
    yao_person.add_fact(jour_minute_rope, jour_minute_rope, 0, 1399)
    # yao_person.add_fact(websites, websites)
    yao_person.add_fact(month_wk_rope, month_wk_rope, fact_lower=0, fact_upper=5)
    yao_person.add_fact(mood_rope, mood_rope)
    # yao_person.add_fact(movie, movie)
    yao_person.add_fact(nations_rope, nations_rope)
    yao_person.add_fact(season_rope, season_rope)
    yao_person.add_fact(yr_month_rope, yr_month_rope, fact_lower=0, fact_upper=12)
    # yao_person.add_fact(water, water)
    yao_person.add_fact(sem_jours_rope, sem_jours_rope)
    return yao_person


def personunit_v002() -> PersonUnit:
    person2_path = "src/ch07_person_logic/test/_util/example_person2.json"
    return get_personunit_from_dict(open_json(person2_path))


def get_personunit_with_4_levels() -> PersonUnit:
    # sourcery skip: extract-duplicate-method
    sue_person = personunit_shop("Sue", exx.a23)
    sue_person.set_l1_plan(planunit_shop(exx.casa, star=30, pledge=True))
    cat_str = "cat have dinner"
    sue_person.set_l1_plan(planunit_shop(cat_str, star=30, pledge=True))

    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    plan_kid_sem_jours = planunit_shop(wk_str, star=40)
    sue_person.set_l1_plan(plan_kid_sem_jours)
    sun_str = "Sun"
    mon_str = "Mon"
    tue_str = "Tue"
    thu_str = "Thur"
    fri_str = "Fri"
    sat_str = "Sat"
    sue_person.set_plan_obj(planunit_shop(sun_str, star=20), wk_rope)
    sue_person.set_plan_obj(planunit_shop(mon_str, star=20), wk_rope)
    sue_person.set_plan_obj(planunit_shop(tue_str, star=20), wk_rope)
    sue_person.set_plan_obj(planunit_shop(exx.wed, star=20), wk_rope)
    sue_person.set_plan_obj(planunit_shop(thu_str, star=30), wk_rope)
    sue_person.set_plan_obj(planunit_shop(fri_str, star=40), wk_rope)
    sue_person.set_plan_obj(planunit_shop(sat_str, star=50), wk_rope)

    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    plan_kid_nation = planunit_shop(nation_str, star=30)
    sue_person.set_l1_plan(plan_kid_nation)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    france_str = "France"
    brazil_str = "Brazil"
    plan_grandkid_usa = planunit_shop(usa_str, star=50)
    plan_grandkid_france = planunit_shop(france_str, star=50)
    plan_grandkid_brazil = planunit_shop(brazil_str, star=50)
    sue_person.set_plan_obj(plan_grandkid_france, nation_rope)
    sue_person.set_plan_obj(plan_grandkid_brazil, nation_rope)
    sue_person.set_plan_obj(plan_grandkid_usa, nation_rope)
    texas_str = "Texas"
    oregon_str = "Oregon"
    plan_grandgrandkid_usa_texas = planunit_shop(texas_str, star=50)
    plan_grandgrandkid_usa_oregon = planunit_shop(oregon_str, star=50)
    sue_person.set_plan_obj(plan_grandgrandkid_usa_texas, usa_rope)
    sue_person.set_plan_obj(plan_grandgrandkid_usa_oregon, usa_rope)
    return sue_person


def get_personunit_with_4_levels_and_2reasons() -> PersonUnit:
    # sourcery skip: extract-duplicate-method
    sue_person = get_personunit_with_4_levels()
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    wed_rope = sue_person.make_rope(wk_rope, exx.wed)
    wk_reason = reasonunit_shop(wk_rope)
    wk_reason.set_case(wed_rope)

    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    nation_reason = reasonunit_shop(nation_rope)
    nation_reason.set_case(usa_rope)

    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.edit_plan_attr(casa_rope, reason=wk_reason)
    sue_person.edit_plan_attr(casa_rope, reason=nation_reason)
    return sue_person


def get_personunit_with_4_levels_and_2reasons_2facts() -> PersonUnit:
    sue_person = get_personunit_with_4_levels_and_2reasons()
    wk_str = "sem_jours"
    wk_rope = sue_person.make_l1_rope(wk_str)
    wed_rope = sue_person.make_rope(wk_rope, exx.wed)
    nation_str = "nation"
    nation_rope = sue_person.make_l1_rope(nation_str)
    usa_str = "USA"
    usa_rope = sue_person.make_rope(nation_rope, usa_str)
    sue_person.add_fact(fact_context=wk_rope, fact_state=wed_rope)
    sue_person.add_fact(fact_context=nation_rope, fact_state=usa_rope)
    return sue_person


def get_personunit_with7am_clean_table_reason() -> PersonUnit:
    sue_person = get_personunit_with_4_levels_and_2reasons_2facts()

    ziet_str = "ziettech"
    ziet_rope = sue_person.make_l1_rope(ziet_str)
    ziet_plan = planunit_shop(ziet_str)

    x24hr_str = "24hr"
    x24hr_rope = sue_person.make_rope(ziet_rope, x24hr_str)
    x24hr_plan = planunit_shop(x24hr_str, begin=0.0, close=24.0)

    am_str = "am"
    am_rope = sue_person.make_rope(x24hr_rope, am_str)
    pm_str = "pm"
    n1_str = "1"
    n2_str = "2"
    n3_str = "3"
    am_plan = planunit_shop(am_str, gogo_want=0, stop_want=12)
    pm_plan = planunit_shop(pm_str, gogo_want=12, stop_want=24)
    n1_plan = planunit_shop(n1_str, gogo_want=1, stop_want=2)
    n2_plan = planunit_shop(n2_str, gogo_want=2, stop_want=3)
    n3_plan = planunit_shop(n3_str, gogo_want=3, stop_want=4)

    sue_person.set_l1_plan(ziet_plan)
    sue_person.set_plan_obj(x24hr_plan, ziet_rope)
    sue_person.set_plan_obj(am_plan, x24hr_rope)
    sue_person.set_plan_obj(pm_plan, x24hr_rope)
    sue_person.set_plan_obj(n1_plan, am_rope)  # plan_am
    sue_person.set_plan_obj(n2_plan, am_rope)  # plan_am
    sue_person.set_plan_obj(n3_plan, am_rope)  # plan_am

    house_str = "houseadministration"
    house_rope = sue_person.make_l1_rope(house_str)
    clean_str = "clean table"
    clean_rope = sue_person.make_rope(house_rope, clean_str)
    dish_str = "remove dishs"
    soap_str = "get soap"
    soap_rope = sue_person.make_rope(clean_rope, soap_str)
    grab_str = "grab soap"
    grab_rope = sue_person.make_rope(soap_rope, grab_str)
    house_plan = planunit_shop(house_str)
    clean_plan = planunit_shop(clean_str, pledge=True)
    dish_plan = planunit_shop(dish_str, pledge=True)
    soap_plan = planunit_shop(soap_str, pledge=True)
    grab_plan = planunit_shop(grab_str, pledge=True)

    sue_person.set_l1_plan(house_plan)
    sue_person.set_plan_obj(clean_plan, house_rope)
    sue_person.set_plan_obj(dish_plan, clean_rope)
    sue_person.set_plan_obj(soap_plan, clean_rope)
    sue_person.set_plan_obj(grab_plan, soap_rope)

    clean_table_7am_reason_context = x24hr_rope
    clean_table_7am_case_rope = x24hr_rope
    clean_table_7am_reason_lower = 7.0
    clean_table_7am_reason_upper = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_reason_context)
    clean_table_7am_reason.set_case(
        case=clean_table_7am_case_rope,
        reason_lower=clean_table_7am_reason_lower,
        reason_upper=clean_table_7am_reason_upper,
    )
    sue_person.edit_plan_attr(clean_rope, reason=clean_table_7am_reason)
    casa_rope = sue_person.make_l1_rope(exx.casa)
    sue_person.edit_plan_attr(casa_rope, reason=clean_table_7am_reason)
    return sue_person


def get_personunit_1case_task_1ceo_minutes_reason_1fact() -> PersonUnit:
    yao_person = personunit_shop("Yao")
    hr_min_str = "hr"
    hr_min_plan = planunit_shop(hr_min_str)
    hr_rope = yao_person.make_l1_rope(hr_min_str)
    hr_reasonunit = reasonunit_shop(hr_rope)
    hr_reasonunit.set_case(hr_rope, reason_lower=80, reason_upper=90)
    yao_person.set_l1_plan(hr_min_plan)
    yao_person.add_fact(hr_rope, hr_rope, 85, 95)
    mail_str = "obtain mail"
    mail_rope = yao_person.make_l1_rope(mail_str)
    mail_plan = planunit_shop(mail_str, pledge=True)
    yao_person.set_l1_plan(mail_plan)
    yao_person.edit_plan_attr(mail_rope, reason=hr_reasonunit)
    return yao_person


def get_personunit_x1_3levels_1reason_1facts() -> PersonUnit:
    tiger_rope = create_rope("tiger")
    zia_person = personunit_shop("Zia", tiger_rope)
    shave_str = "shave"
    shave_rope = zia_person.make_l1_rope(shave_str)
    plan_kid_shave = planunit_shop(shave_str, star=30, pledge=True)
    zia_person.set_l1_plan(plan_kid_shave)
    wk_str = "sem_jours"
    wk_rope = zia_person.make_l1_rope(wk_str)
    wk_plan = planunit_shop(wk_str, star=40)
    zia_person.set_l1_plan(wk_plan)

    sun_str = "Sun"
    sun_rope = zia_person.make_rope(wk_rope, sun_str)
    church_str = "Church"
    church_rope = zia_person.make_rope(sun_rope, church_str)
    mon_str = "Mon"
    mon_rope = zia_person.make_rope(wk_rope, mon_str)
    plan_grandkidU = planunit_shop(sun_str, star=20)
    plan_grandkidM = planunit_shop(mon_str, star=20)
    zia_person.set_plan_obj(plan_grandkidU, wk_rope)
    zia_person.set_plan_obj(plan_grandkidM, wk_rope)

    shave_reason = reasonunit_shop(wk_rope)
    shave_reason.set_case(mon_rope)

    zia_person.edit_plan_attr(shave_rope, reason=shave_reason)
    zia_person.add_fact(fact_context=wk_rope, fact_state=sun_rope)
    x_factunit = factunit_shop(fact_context=wk_rope, fact_state=church_rope)
    zia_person.edit_plan_attr(shave_rope, factunit=x_factunit)
    return zia_person


def get_personunit_reason_context_ziet_example() -> PersonUnit:
    sue_person = personunit_shop("Sue")
    sue_person.set_l1_plan(planunit_shop("casa"))
    return sue_person


def get_personunit_irrational_example() -> PersonUnit:
    # sourcery skip: extract-duplicate-method
    # this person has no definitive agenda because 2 pledge plans are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken.plan_active is True, egg.plan_active is set to False
    # Step 1: if egg.plan_active is False, chicken.plan_active is set to False
    # Step 2: if chicken.plan_active is False, egg.plan_active is set to True
    # Step 3: if egg.plan_active is True, chicken.plan_active is set to True
    # Step 4: back to step 0.
    # after hatter_person.conpute these should be true:
    # 1. hatter_person._irrational is True
    # 2. hatter_person.tree_traverse_count = hatter_person.max_tree_traverse

    hatter_person = personunit_shop("Mad Hatter")
    hatter_person.set_max_tree_traverse(3)

    egg_str = "egg first"
    egg_rope = hatter_person.make_l1_rope(egg_str)
    hatter_person.set_l1_plan(planunit_shop(egg_str))

    chicken_str = "chicken first"
    chicken_rope = hatter_person.make_l1_rope(chicken_str)
    hatter_person.set_l1_plan(planunit_shop(chicken_str))

    # set egg pledge is True when chicken first is False
    hatter_person.edit_plan_attr(
        egg_rope,
        pledge=True,
        reason_context=chicken_rope,
        reason_requisite_active=True,
    )

    # set chick pledge is True when egg first is False
    hatter_person.edit_plan_attr(
        chicken_rope,
        pledge=True,
        reason_context=egg_rope,
        reason_requisite_active=False,
    )

    return hatter_person


def get_mop_with_reason_personunit_example1():
    sue_person = personunit_shop("Sue")
    casa_rope = sue_person.make_l1_rope(exx.casa)
    floor_str = "mop floor"
    floor_rope = sue_person.make_rope(casa_rope, floor_str)
    floor_plan = planunit_shop(floor_str, pledge=True)
    sue_person.set_plan_obj(floor_plan, casa_rope)
    sue_person.set_l1_plan(planunit_shop("unimportant"))

    situation_str = "cleaniness situation"
    situation_rope = sue_person.make_rope(casa_rope, situation_str)
    sue_person.set_plan_obj(planunit_shop(situation_str), casa_rope)

    clean_rope = sue_person.make_rope(situation_rope, exx.clean)
    sue_person.set_plan_obj(planunit_shop(exx.clean), situation_rope)
    sue_person.set_plan_obj(planunit_shop("very_much"), clean_rope)
    sue_person.set_plan_obj(planunit_shop("moderately"), clean_rope)
    sue_person.set_plan_obj(planunit_shop("dirty"), situation_rope)

    floor_reason = reasonunit_shop(situation_rope)
    floor_reason.set_case(case=situation_rope)
    sue_person.edit_plan_attr(floor_rope, reason=floor_reason)
    return sue_person


def get_personunit_laundry_example1() -> PersonUnit:
    yao_person = personunit_shop(exx.yao)
    cali_str = "Cali"
    yao_person.add_partnerunit(exx.yao)
    yao_person.add_partnerunit(cali_str)

    basket_str = "laundry basket situation"
    b_full_str = "full"
    b_smel_str = "smelly"
    b_bare_str = "bare"
    b_fine_str = "fine"
    b_half_str = "half full"
    do_laundry_str = "do_laundry"
    casa_rope = yao_person.make_l1_rope(exx.casa)
    basket_rope = yao_person.make_rope(casa_rope, basket_str)
    b_full_rope = yao_person.make_rope(basket_rope, b_full_str)
    b_smel_rope = yao_person.make_rope(basket_rope, b_smel_str)
    laundry_plan_task_rope = yao_person.make_rope(casa_rope, do_laundry_str)
    yao_person.set_l1_plan(planunit_shop(exx.casa))
    yao_person.set_plan_obj(planunit_shop(basket_str), casa_rope)
    yao_person.set_plan_obj(planunit_shop(b_full_str), basket_rope)
    yao_person.set_plan_obj(planunit_shop(b_smel_str), basket_rope)
    yao_person.set_plan_obj(planunit_shop(b_bare_str), basket_rope)
    yao_person.set_plan_obj(planunit_shop(b_fine_str), basket_rope)
    yao_person.set_plan_obj(planunit_shop(b_half_str), basket_rope)
    yao_person.set_plan_obj(planunit_shop(do_laundry_str, pledge=True), casa_rope)

    # laundry requirement
    yao_person.edit_plan_attr(
        laundry_plan_task_rope, reason_context=basket_rope, reason_case=b_full_rope
    )
    # laundry requirement
    yao_person.edit_plan_attr(
        laundry_plan_task_rope, reason_context=basket_rope, reason_case=b_smel_rope
    )
    cali_workforceunit = workforceunit_shop()
    cali_workforceunit.add_labor(cali_str)
    yao_person.edit_plan_attr(laundry_plan_task_rope, workforceunit=cali_workforceunit)
    yao_person.add_fact(fact_context=basket_rope, fact_state=b_full_rope)

    return yao_person


def from_list_get_active(
    rope: RopeTerm, plan_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_plan = None

    active_true_count = 0
    active_false_count = 0
    for plan in plan_dict.values():
        if plan.get_plan_rope() == rope:
            temp_plan = plan
            print(
                f"s for PlanUnit {temp_plan.get_plan_rope()}  {temp_plan.plan_active=}"
            )

        if plan.plan_active:
            active_true_count += 1
        elif plan.plan_active is False:
            active_false_count += 1

    active = temp_plan.plan_active
    print(
        f"Set active: {plan.plan_label=} {active} {active_true_count=} {active_false_count=}"
    )

    return active
