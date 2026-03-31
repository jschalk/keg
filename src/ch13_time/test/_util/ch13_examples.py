from datetime import datetime
from enum import Enum
from plotly.graph_objects import Figure as plotly_Figure, Scatter as plotly_Scatter
from src.ch00_py.file_toolbox import open_json
from src.ch00_py.plotly_toolbox import conditional_fig_show
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch13_time._ref.ch13_semantic_types import LabelTerm
from src.ch13_time.epoch_main import (
    add_epoch_planunit,
    create_weekday_planunits,
    epochholder_shop,
    get_min_from_dt_offset,
    new_epoch_planunit,
)
from src.ref.keywords import Ch13Keywords as kw, ExampleStrs as exx

DIRTYNESS_STR = "dirtyness"
FIVE_STR = "five"
WK_STR = "wk"
WED_STR = "Wed"

BOB_PERSON = personunit_shop(exx.bob)
MOP_ROPE = BOB_PERSON.make_l1_rope(exx.mop)
SWEEP_ROPE = BOB_PERSON.make_l1_rope(exx.sweep)
SCRUB_ROPE = BOB_PERSON.make_l1_rope(exx.scrub)
CLEAN_ROPE = BOB_PERSON.make_l1_rope(exx.clean)
DIRTYNESS_ROPE = BOB_PERSON.make_rope(CLEAN_ROPE, DIRTYNESS_STR)
TIME_ROPE = BOB_PERSON.make_l1_rope(kw.time)
FIVE_ROPE = BOB_PERSON.make_rope(TIME_ROPE, FIVE_STR)
FIVE_DAY_ROPE = BOB_PERSON.make_rope(FIVE_ROPE, kw.day)
FIVE_DAYS_ROPE = BOB_PERSON.make_rope(FIVE_ROPE, kw.days)
FIVE_WEEK_ROPE = BOB_PERSON.make_rope(FIVE_ROPE, kw.week)
FIVE_WEEKS_ROPE = BOB_PERSON.make_rope(FIVE_ROPE, kw.weeks)

FIVE_C400_LEAP_ROPE = BOB_PERSON.make_rope(FIVE_ROPE, kw.c400_leap)
FIVE_C400_CORE_ROPE = BOB_PERSON.make_rope(FIVE_C400_LEAP_ROPE, kw.c400_core)
FIVE_C100_ROPE = BOB_PERSON.make_rope(FIVE_C400_CORE_ROPE, kw.c100)
FIVE_YR4_LEAP_ROPE = BOB_PERSON.make_rope(FIVE_C100_ROPE, kw.yr4_leap)
FIVE_YR4_CORE_ROPE = BOB_PERSON.make_rope(FIVE_YR4_LEAP_ROPE, kw.yr4_core)
FIVE_YEAR_ROPE = BOB_PERSON.make_rope(FIVE_YR4_CORE_ROPE, kw.year)


class Ch13ExampleStrs(str, Enum):
    Bob = exx.bob
    casa_str = exx.casa
    clean_str = exx.clean
    dirtyness_str = DIRTYNESS_STR
    five_str = FIVE_STR
    mop_str = exx.mop
    wk_str = WK_STR
    wed_str = WED_STR
    root_rope = BOB_PERSON.planroot.get_plan_rope()
    mop_rope = MOP_ROPE
    sweep_str = exx.sweep
    sweep_rope = SWEEP_ROPE
    scrub_str = exx.scrub
    scrub_rope = SCRUB_ROPE
    clean_rope = CLEAN_ROPE
    dirtyness_rope = DIRTYNESS_ROPE
    time_rope = TIME_ROPE
    five_rope = FIVE_ROPE
    day_rope = FIVE_DAY_ROPE
    days_rope = FIVE_DAYS_ROPE
    week_rope = FIVE_WEEK_ROPE
    weeks_rope = FIVE_WEEKS_ROPE
    five_year_rope = FIVE_YEAR_ROPE
    Fredrick = "Fredrick"
    Geo = "Geo"
    Holocene = "Holocene"
    Iguana = "Iguana"
    Jesus = "Jesus"
    Keel = "Keel"
    LeBron = "LeBron"
    Mikayla = "Mikayla"
    Ninon = "Ninon"
    Obama = "Obama"
    Preston = "Preston"
    Quorum = "Quorum"
    RioGrande = "RioGrande"
    Simon = "Simon"
    Trump = "Trump"

    def __str__(self):
        return self.value


def get_bob_five_person() -> PersonUnit:
    """Returns PersonUnit with person_name=Bob, mop as pledge plan, and five_epoch"""
    bob_person = personunit_shop(exx.bob)
    bob_person.add_plan(MOP_ROPE, pledge=True)
    add_epoch_planunit(bob_person, get_five_config())
    return bob_person


def get_example_epoch_config(epoch_label: LabelTerm) -> dict:
    x_dir = "src/ch13_time/test/_util"
    x_filename = f"epoch_config_{epoch_label}.json"
    return open_json(x_dir, x_filename)


def get_five_config() -> dict:
    return get_example_epoch_config(kw.five)


def get_creg_config() -> dict:
    return get_example_epoch_config(kw.creg)


def get_squirt_config() -> dict:
    return get_example_epoch_config("squirt")


def get_lizzy9_config() -> dict:
    return get_example_epoch_config("lizzy9")


def cregtime_planunit() -> PlanUnit:
    c400_number = get_creg_config().get(kw.c400_number)
    return new_epoch_planunit(kw.creg, c400_number)


def get_wed():
    return creg_weekdays_list()[0]


def get_thu():
    return creg_weekdays_list()[1]


def get_fri():
    return creg_weekdays_list()[2]


def get_sat():
    return creg_weekdays_list()[3]


def get_sun():
    return creg_weekdays_list()[4]


def get_mon():
    return creg_weekdays_list()[5]


def get_tue():
    return creg_weekdays_list()[6]


def creg_hours_list() -> list[list[str, int]]:
    return get_creg_config().get(kw.hours_config)


def creg_weekdays_list() -> list[str]:
    return get_creg_config().get(kw.weekdays_config)


def creg_weekday_planunits() -> dict[str, PlanUnit]:
    return create_weekday_planunits(creg_weekdays_list())


def creg_hour_int_label(x_int: int) -> str:
    return creg_hours_list()[x_int][0]


def add_time_creg_planunit(x_personunit: PersonUnit) -> PersonUnit:
    """Add creg epoch planunit to personunit"""
    add_epoch_planunit(x_personunit, get_creg_config())
    return x_personunit


def add_time_five_planunit(x_personunit: PersonUnit) -> PersonUnit:
    """Add five epoch planunit to personunit"""
    add_epoch_planunit(x_personunit, get_five_config())
    return x_personunit


def add_time_squirt_planunit(x_personunit: PersonUnit) -> PersonUnit:
    """Add squirt epoch planunit to personunit"""
    add_epoch_planunit(x_personunit, get_squirt_config())
    return x_personunit


def get_creg_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_creg_config().get(kw.yr1_jan1_offset))


def get_five_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_five_config().get(kw.yr1_jan1_offset))


def get_squirt_min_from_dt(dt: datetime) -> int:
    return get_min_from_dt_offset(dt, get_squirt_config().get(kw.yr1_jan1_offset))


def display_current_creg_five_min(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime.now()
        current_creg = get_creg_min_from_dt(current_datetime)
        current_five = get_five_min_from_dt(current_datetime)

        curr_str = f"year: {current_datetime.year}"
        curr_str += f", month: {current_datetime.month}"
        curr_str += f", day: {current_datetime.day}"
        curr_str += f", hour: {current_datetime.hour}"
        curr_str += f", minute: {current_datetime.minute}"
        curr_str = f"<b>{curr_str}</b>"
        creg_min_str = f"<b>creg epoch min: {current_creg}</b>"
        five_min_str = f"<b>five epoch min: {current_five}</b>"
        curr_list = [curr_str, creg_min_str, five_min_str]
        xp_list = [1, 1, 1]
        yp_list = [3, 2, 1]

        x_fig = plotly_Figure()
        x_fig.update_xaxes(range=[-6, 8])
        x_fig.update_yaxes(range=[0, 5])
        x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
        x_fig.update_layout(font=x_font)
        x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
        x_fig.add_trace(x1_scatter)
        conditional_fig_show(x_fig, graphics_bool)


def display_current_creg_five_time_attrs(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime.now()
        sue_person = personunit_shop("Sue")
        sue_person = add_time_creg_planunit(sue_person)
        sue_person = add_time_five_planunit(sue_person)
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        creg_TimeNum = epochholder_shop(sue_person, kw.creg, creg_min)
        five_TimeNum = epochholder_shop(sue_person, kw.five, five_min)
        creg_TimeNum.calc_epoch()
        five_TimeNum.calc_epoch()
        creg_blurb = f"<b>{creg_TimeNum.get_blurb()}</b>"
        five_blurb = f"<b>{five_TimeNum.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg epoch min: {creg_min}</b>"
        five_min_str = f"<b>five epoch min: {five_min}</b>"
        curr_list = [dt_str, creg_min_str, creg_blurb, five_min_str, five_blurb]
        xp_list = [1, 1, 1, 1, 1]
        yp_list = [7, 5, 4, 2, 1]

        x_fig = plotly_Figure()
        x_fig.update_xaxes(range=[-6, 8])
        x_fig.update_yaxes(range=[0, 10])
        x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
        x_fig.update_layout(font=x_font)
        x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
        x_fig.add_trace(x1_scatter)
        conditional_fig_show(x_fig, graphics_bool)


def display_creg_five_squirt_time_attrs(graphics_bool: bool):
    if graphics_bool:
        current_datetime = datetime(2031, 2, 17, 7, 47)
        sue_person = personunit_shop("Sue")
        sue_person = add_time_creg_planunit(sue_person)
        sue_person = add_time_five_planunit(sue_person)
        sue_person = add_time_squirt_planunit(sue_person)
        time_rope = sue_person.make_l1_rope(kw.time)
        squirt_rope = sue_person.make_rope(time_rope, "squirt")
        creg_min = get_creg_min_from_dt(current_datetime)
        five_min = get_five_min_from_dt(current_datetime)
        squirt_min = get_squirt_min_from_dt(current_datetime)
        creg_TimeNum = epochholder_shop(sue_person, kw.creg, creg_min)
        five_TimeNum = epochholder_shop(sue_person, kw.five, five_min)
        squirt_TimeNum = epochholder_shop(sue_person, "squirt", squirt_min)
        creg_TimeNum.calc_epoch()
        five_TimeNum.calc_epoch()
        squirt_TimeNum.calc_epoch()
        creg_blurb = f"<b>{creg_TimeNum.get_blurb()}</b>"
        five_blurb = f"<b>{five_TimeNum.get_blurb()}</b>"
        squirt_blurb = f"<b>{squirt_TimeNum.get_blurb()}</b>"

        datetime_str = current_datetime.strftime("%H:%M, %A, %d %B, %Y")
        dt_str = f"python : {datetime_str}"
        dt_str = f"<b>{dt_str}</b>"
        creg_min_str = f"<b>creg epoch min: {creg_min}</b>"
        five_min_str = f"<b>five epoch min: {five_min}</b>"
        squirt_min_str = f"<b>squirt epoch min: {squirt_min}</b>"
        curr_list = [
            dt_str,
            creg_min_str,
            creg_blurb,
            five_min_str,
            five_blurb,
            squirt_min_str,
            squirt_blurb,
        ]
        xp_list = [1, 1, 1, 1, 1, 1, 1]
        yp_list = [7, 5, 4, 2, 1, -1, -2]

        x_fig = plotly_Figure()
        x_fig.update_xaxes(range=[-6, 8])
        x_fig.update_yaxes(range=[-5, 10])
        x_font = dict(family="Courier New, monospace", size=45, color="RebeccaPurple")
        x_fig.update_layout(font=x_font)
        x1_scatter = plotly_Scatter(x=xp_list, y=yp_list, text=curr_list, mode="text")
        x_fig.add_trace(x1_scatter)
        conditional_fig_show(x_fig, graphics_bool)


def get_expected_creg_2024_markdown() -> str:
    return """
                               Year 2024                                

       March                     April                      May         
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
             1  2  3       1  2  3  4  5  6  7             1  2  3  4  5
 4  5  6  7  8  9 10       8  9 10 11 12 13 14       6  7  8  9 10 11 12
11 12 13 14 15 16 17      15 16 17 18 19 20 21      13 14 15 16 17 18 19
18 19 20 21 22 23 24      22 23 24 25 26 27 28      20 21 22 23 24 25 26
25 26 27 28 29 30 31      29 30                     27 28 29 30 31      

        June                      July                     August       
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2       1  2  3  4  5  6  7                1  2  3  4
 3  4  5  6  7  8  9       8  9 10 11 12 13 14       5  6  7  8  9 10 11
10 11 12 13 14 15 16      15 16 17 18 19 20 21      12 13 14 15 16 17 18
17 18 19 20 21 22 23      22 23 24 25 26 27 28      19 20 21 22 23 24 25
24 25 26 27 28 29 30      29 30 31                  26 27 28 29 30 31   

     September                  October                   November      
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1          1  2  3  4  5  6                   1  2  3
 2  3  4  5  6  7  8       7  8  9 10 11 12 13       4  5  6  7  8  9 10
 9 10 11 12 13 14 15      14 15 16 17 18 19 20      11 12 13 14 15 16 17
16 17 18 19 20 21 22      21 22 23 24 25 26 27      18 19 20 21 22 23 24
23 24 25 26 27 28 29      28 29 30 31               25 26 27 28 29 30   
30                                                                      

      December               January (2025)           February (2025)   
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1             1  2  3  4  5                      1  2
 2  3  4  5  6  7  8       6  7  8  9 10 11 12       3  4  5  6  7  8  9
 9 10 11 12 13 14 15      13 14 15 16 17 18 19      10 11 12 13 14 15 16
16 17 18 19 20 21 22      20 21 22 23 24 25 26      17 18 19 20 21 22 23
23 24 25 26 27 28 29      27 28 29 30 31            24 25 26 27 28      
30 31                                                                   """


def get_expected_creg_year0_markdown() -> str:
    return """
                                 Year 0                                 

       March                     April                      May         
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
 1  2  3  4  5  6  7                1  2  3  4                      1  2
 8  9 10 11 12 13 14       5  6  7  8  9 10 11       3  4  5  6  7  8  9
15 16 17 18 19 20 21      12 13 14 15 16 17 18      10 11 12 13 14 15 16
22 23 24 25 26 27 28      19 20 21 22 23 24 25      17 18 19 20 21 22 23
29 30 31                  26 27 28 29 30            24 25 26 27 28 29 30
                                                    31                  

        June                      July                     August       
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
    1  2  3  4  5  6                1  2  3  4                         1
 7  8  9 10 11 12 13       5  6  7  8  9 10 11       2  3  4  5  6  7  8
14 15 16 17 18 19 20      12 13 14 15 16 17 18       9 10 11 12 13 14 15
21 22 23 24 25 26 27      19 20 21 22 23 24 25      16 17 18 19 20 21 22
28 29 30                  26 27 28 29 30 31         23 24 25 26 27 28 29
                                                    30 31               

     September                  October                   November      
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
       1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7
 6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14
13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21
20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28
27 28 29 30               25 26 27 28 29 30 31      29 30               

      December                January (1)               February (1)    
We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu      We Th Fr Sa Su Mo Tu
       1  2  3  4  5                      1  2          1  2  3  4  5  6
 6  7  8  9 10 11 12       3  4  5  6  7  8  9       7  8  9 10 11 12 13
13 14 15 16 17 18 19      10 11 12 13 14 15 16      14 15 16 17 18 19 20
20 21 22 23 24 25 26      17 18 19 20 21 22 23      21 22 23 24 25 26 27
27 28 29 30 31            24 25 26 27 28 29 30      28                  
                          31                                            """


def get_expected_five_5524_markdown() -> str:
    return """
                                Year 5224                                 

   Fredrick              Geo               Holocene             Iguana    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Jesus                Keel               LeBron             Mikayla    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Ninon               Obama              Preston              Quorum    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

  RioGrande             Simon               Trump     
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14         
18 19 20 21 22      18 19 20 21 22                    
23 24               23 24                             """
