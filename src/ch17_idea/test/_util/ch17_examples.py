from pandas import DataFrame
from src.ch04_rope.rope import create_rope
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx

J45_ROPE = create_rope("jeffy45", knot=exx.slash)


def get_ex1_br00000_df() -> DataFrame:
    """br00000_momentunit_v0_0_0
    c400_number,moment_rope,fund_grain,monthday_index,mana_grain,respect_grain,knot,epoch_label,yr1_jan1_offset
    """
    x_df = DataFrame(
        columns=[
            kw.c400_number,
            kw.moment_rope,
            kw.fund_grain,
            kw.monthday_index,
            kw.mana_grain,
            kw.respect_grain,
            kw.knot,
            kw.epoch_label,
            kw.yr1_jan1_offset,
            kw.job_listen_rotations,
        ]
    )
    x_df.loc[0] = [7, exx.a23, 1, 1, 1, 1, ";", "creg", 440640, 7]
    return x_df


def get_ex1_br00001_df() -> DataFrame:
    """br00001_moment_budunit_v0_0_0
    moment_rope,person_name,bud_time,knot,quota,celldepth"""
    x_df = DataFrame(
        columns=[
            kw.moment_rope,
            kw.person_name,
            kw.bud_time,
            kw.knot,
            kw.quota,
            kw.celldepth,
        ]
    )
    x_df.loc[0] = [exx.a23, "Sue", 777, ";", 445, 5]
    return x_df


def get_ex1_br00002_df() -> DataFrame:
    """br00002_moment_paybook_v0_0_0
    contact_name,amount,moment_rope,person_name,tran_time"""
    x_df = DataFrame(
        columns=["contact_name", "amount", kw.moment_rope, kw.person_name, "tran_time"]
    )
    x_df.loc[0] = ["Bob", 888, exx.a23, "Zia", 777]
    return x_df


def get_ex1_br00003_df() -> DataFrame:
    """br00003_moment_epoch_hour_v0_0_0
    cumulative_minute,moment_rope,hour_label"""
    x_df = DataFrame(columns=[kw.moment_rope, "hour_label", "cumulative_minute"])
    x_df.loc[0] = [exx.a23, "12am", 60]
    x_df.loc[1] = [exx.a23, "1am", 120]
    x_df.loc[2] = [exx.a23, "2am", 180]
    x_df.loc[3] = [exx.a23, "3am", 240]
    x_df.loc[4] = [exx.a23, "4am", 300]
    x_df.loc[5] = [exx.a23, "5am", 360]
    x_df.loc[6] = [exx.a23, "6am", 420]
    x_df.loc[7] = [exx.a23, "7am", 480]
    x_df.loc[8] = [exx.a23, "8am", 540]
    x_df.loc[9] = [exx.a23, "9am", 600]
    x_df.loc[10] = [exx.a23, "10am", 660]
    x_df.loc[11] = [exx.a23, "11am", 720]
    x_df.loc[12] = [exx.a23, "12pm", 780]
    x_df.loc[13] = [exx.a23, "1pm", 840]
    x_df.loc[14] = [exx.a23, "2pm", 900]
    x_df.loc[15] = [exx.a23, "3pm", 960]
    x_df.loc[16] = [exx.a23, "4pm", 1020]
    x_df.loc[17] = [exx.a23, "5pm", 1080]
    x_df.loc[18] = [exx.a23, "6pm", 1140]
    x_df.loc[19] = [exx.a23, "7pm", 1200]
    x_df.loc[20] = [exx.a23, "8pm", 1260]
    x_df.loc[21] = [exx.a23, "9pm", 1320]
    x_df.loc[22] = [exx.a23, "10pm", 1380]
    x_df.loc[23] = [exx.a23, "11pm", 1440]
    return x_df


def get_ex1_br00004_df() -> DataFrame:
    """br00004_moment_epoch_month_v0_0_0
    cumulative_day,moment_rope,month_label"""
    x_df = DataFrame(columns=[kw.moment_rope, kw.month_label, "cumulative_day"])
    x_df.loc[0] = [exx.a23, exx.March, 31]
    x_df.loc[1] = [exx.a23, exx.April, 61]
    x_df.loc[2] = [exx.a23, exx.May, 92]
    x_df.loc[3] = [exx.a23, exx.June, 122]
    x_df.loc[4] = [exx.a23, exx.July, 153]
    x_df.loc[5] = [exx.a23, exx.August, 184]
    x_df.loc[6] = [exx.a23, exx.September, 214]
    x_df.loc[7] = [exx.a23, exx.October, 245]
    x_df.loc[8] = [exx.a23, exx.November, 275]
    x_df.loc[9] = [exx.a23, exx.December, 306]
    x_df.loc[10] = [exx.a23, exx.January, 337]
    x_df.loc[11] = [exx.a23, exx.February, 365]
    return x_df


def get_ex1_br00005_df() -> DataFrame:
    """br00005_moment_epoch_weekday_v0_0_0
    moment_rope,weekday_label,weekday_order"""
    x_df = DataFrame(columns=[kw.moment_rope, kw.weekday_label, kw.weekday_order])
    x_df.loc[0] = [exx.a23, exx.Wednesday, 0]
    x_df.loc[1] = [exx.a23, exx.Thursday, 1]
    x_df.loc[2] = [exx.a23, exx.Friday, 2]
    x_df.loc[3] = [exx.a23, exx.Saturday, 3]
    x_df.loc[4] = [exx.a23, exx.Sunday, 4]
    x_df.loc[5] = [exx.a23, exx.Monday, 5]
    x_df.loc[6] = [exx.a23, exx.Tuesday, 6]
    return x_df


def get_ex2_br00000_df() -> DataFrame:
    """br00000_momentunit_v0_0_0
    c400_number,moment_rope,fund_grain,monthday_index,mana_grain,respect_grain,knot,epoch_label,yr1_jan1_offset,job_listen_rotations
    """
    x_df = DataFrame(
        columns=[
            kw.c400_number,
            kw.moment_rope,
            kw.fund_grain,
            kw.monthday_index,
            kw.mana_grain,
            kw.respect_grain,
            kw.knot,
            kw.epoch_label,
            kw.yr1_jan1_offset,
            kw.job_listen_rotations,
        ]
    )
    x_df.loc[0] = [7, exx.a23_slash, 1, 1, 1, 1, exx.slash, "creg", 440640, 4]
    x_df.loc[1] = [25, J45_ROPE, 1, 0, 1, 1, exx.slash, "five", 1683478080, 4]
    return x_df


def get_ex2_br00001_df() -> DataFrame:
    """br00001_moment_budunit_v0_0_0
    moment_rope,person_name,quota,bud_time,knot"""
    x_df = DataFrame(
        columns=[
            kw.moment_rope,
            kw.person_name,
            kw.quota,
            kw.bud_time,
            kw.celldepth,
            kw.knot,
        ]
    )
    x_df.loc[0] = [exx.a23_slash, "Bob", 332, 999, 3, exx.slash]
    x_df.loc[1] = [exx.a23_slash, "Sue", 445, 777, 3, exx.slash]
    x_df.loc[2] = [exx.a23_slash, "Yao", 700, 222, 3, exx.slash]
    x_df.loc[3] = [J45_ROPE, "Xio", 332, 999, 3, exx.slash]
    x_df.loc[4] = [J45_ROPE, "Zia", 700, 222, 3, exx.slash]
    return x_df


def get_ex2_br00002_df() -> DataFrame:
    """br00002_moment_paybook_v0_0_0
    contact_name,amount,moment_rope,person_name,tran_time,knot"""
    x_df = DataFrame(
        columns=[
            kw.contact_name,
            kw.amount,
            kw.moment_rope,
            kw.person_name,
            kw.tran_time,
            kw.knot,
        ]
    )
    x_df.loc[0] = ["Zia", 888, exx.a23_slash, "Bob", 777, exx.slash]
    x_df.loc[1] = ["Zia", 234, exx.a23_slash, "Sue", 999, exx.slash]
    x_df.loc[2] = ["Zia", 234, exx.a23_slash, "Yao", 999, exx.slash]
    x_df.loc[3] = ["Zia", 234, J45_ROPE, "Yao", 999, exx.slash]
    x_df.loc[4] = ["Bob", 888, exx.a23_slash, "Zia", 777, exx.slash]
    return x_df


def get_ex2_br00003_df() -> DataFrame:
    """br00003_moment_epoch_hour_v0_0_0
    cumulative_minute,moment_rope,hour_label,knot"""
    x_df = DataFrame(
        columns=[kw.moment_rope, kw.hour_label, kw.cumulative_minute, kw.knot]
    )
    x_df.loc[0] = [exx.a23_slash, "12am", 60, exx.slash]
    x_df.loc[1] = [exx.a23_slash, "1am", 120, exx.slash]
    x_df.loc[2] = [exx.a23_slash, "2am", 180, exx.slash]
    x_df.loc[3] = [exx.a23_slash, "3am", 240, exx.slash]
    x_df.loc[4] = [exx.a23_slash, "4am", 300, exx.slash]
    x_df.loc[5] = [exx.a23_slash, "5am", 360, exx.slash]
    x_df.loc[6] = [exx.a23_slash, "6am", 420, exx.slash]
    x_df.loc[7] = [exx.a23_slash, "7am", 480, exx.slash]
    x_df.loc[8] = [exx.a23_slash, "8am", 540, exx.slash]
    x_df.loc[9] = [exx.a23_slash, "9am", 600, exx.slash]
    x_df.loc[10] = [exx.a23_slash, "10am", 660, exx.slash]
    x_df.loc[11] = [exx.a23_slash, "11am", 720, exx.slash]
    x_df.loc[12] = [exx.a23_slash, "12pm", 780, exx.slash]
    x_df.loc[13] = [exx.a23_slash, "1pm", 840, exx.slash]
    x_df.loc[14] = [exx.a23_slash, "2pm", 900, exx.slash]
    x_df.loc[15] = [exx.a23_slash, "3pm", 960, exx.slash]
    x_df.loc[16] = [exx.a23_slash, "4pm", 1020, exx.slash]
    x_df.loc[17] = [exx.a23_slash, "5pm", 1080, exx.slash]
    x_df.loc[18] = [exx.a23_slash, "6pm", 1140, exx.slash]
    x_df.loc[19] = [exx.a23_slash, "7pm", 1200, exx.slash]
    x_df.loc[20] = [exx.a23_slash, "8pm", 1260, exx.slash]
    x_df.loc[21] = [exx.a23_slash, "9pm", 1320, exx.slash]
    x_df.loc[22] = [exx.a23_slash, "10pm", 1380, exx.slash]
    x_df.loc[23] = [exx.a23_slash, "11pm", 1440, exx.slash]
    x_df.loc[24] = [J45_ROPE, "0hr", 144, exx.slash]
    x_df.loc[25] = [J45_ROPE, "1hr", 288, exx.slash]
    x_df.loc[26] = [J45_ROPE, "2hr", 432, exx.slash]
    x_df.loc[27] = [J45_ROPE, "3hr", 576, exx.slash]
    x_df.loc[28] = [J45_ROPE, "4hr", 720, exx.slash]
    x_df.loc[29] = [J45_ROPE, "5hr", 864, exx.slash]
    x_df.loc[30] = [J45_ROPE, "6hr", 1008, exx.slash]
    x_df.loc[31] = [J45_ROPE, "7hr", 1152, exx.slash]
    x_df.loc[32] = [J45_ROPE, "8hr", 1296, exx.slash]
    x_df.loc[33] = [J45_ROPE, "9hr", 1440, exx.slash]
    return x_df


def get_ex2_br00004_df() -> DataFrame:
    """br00004_moment_epoch_month_v0_0_0
    cumulative_day,moment_rope,month_label, knot"""
    x_df = DataFrame(
        columns=[kw.moment_rope, kw.month_label, kw.cumulative_day, kw.knot]
    )
    x_df.loc[0] = [exx.a23_slash, "March", 31, exx.slash]
    x_df.loc[1] = [exx.a23_slash, "April", 61, exx.slash]
    x_df.loc[2] = [exx.a23_slash, "May", 92, exx.slash]
    x_df.loc[3] = [exx.a23_slash, "June", 122, exx.slash]
    x_df.loc[4] = [exx.a23_slash, "July", 153, exx.slash]
    x_df.loc[5] = [exx.a23_slash, "August", 184, exx.slash]
    x_df.loc[6] = [exx.a23_slash, "September", 214, exx.slash]
    x_df.loc[7] = [exx.a23_slash, "October", 245, exx.slash]
    x_df.loc[8] = [exx.a23_slash, "November", 275, exx.slash]
    x_df.loc[9] = [exx.a23_slash, "December", 306, exx.slash]
    x_df.loc[10] = [exx.a23_slash, "January", 337, exx.slash]
    x_df.loc[11] = [exx.a23_slash, "February", 365, exx.slash]
    x_df.loc[12] = (J45_ROPE, "Fredrick", 25, exx.slash)
    x_df.loc[13] = (J45_ROPE, "Geo", 50, exx.slash)
    x_df.loc[14] = (J45_ROPE, "Holocene", 75, exx.slash)
    x_df.loc[15] = (J45_ROPE, "Iguana", 100, exx.slash)
    x_df.loc[16] = (J45_ROPE, "Jesus", 125, exx.slash)
    x_df.loc[17] = (J45_ROPE, "Keel", 150, exx.slash)
    x_df.loc[18] = (J45_ROPE, "LeBron", 175, exx.slash)
    x_df.loc[19] = (J45_ROPE, "Mikayla", 200, exx.slash)
    x_df.loc[20] = (J45_ROPE, "Ninon", 225, exx.slash)
    x_df.loc[21] = (J45_ROPE, "Obama", 250, exx.slash)
    x_df.loc[22] = (J45_ROPE, "Preston", 275, exx.slash)
    x_df.loc[23] = (J45_ROPE, "Quorum", 300, exx.slash)
    x_df.loc[24] = (J45_ROPE, "RioGrande", 325, exx.slash)
    x_df.loc[25] = (J45_ROPE, "Simon", 350, exx.slash)
    x_df.loc[26] = [J45_ROPE, "Trump", 365, exx.slash]
    return x_df


def get_ex2_br00005_df() -> DataFrame:
    """br00005_moment_epoch_weekday_v0_0_0
    moment_rope,weekday_label,weekday_order"""
    x_df = DataFrame(
        columns=[kw.moment_rope, kw.weekday_label, kw.weekday_order, kw.knot]
    )
    x_df.loc[0] = [exx.a23_slash, exx.Wednesday, 0, exx.slash]
    x_df.loc[1] = [exx.a23_slash, exx.Thursday, 1, exx.slash]
    x_df.loc[2] = [exx.a23_slash, exx.Friday, 2, exx.slash]
    x_df.loc[3] = [exx.a23_slash, exx.Saturday, 3, exx.slash]
    x_df.loc[4] = [exx.a23_slash, exx.Sunday, 4, exx.slash]
    x_df.loc[5] = [exx.a23_slash, exx.Monday, 5, exx.slash]
    x_df.loc[6] = [exx.a23_slash, exx.Tuesday, 6, exx.slash]
    x_df.loc[7] = [J45_ROPE, kw.Anaday, 0, exx.slash]
    x_df.loc[8] = [J45_ROPE, kw.Baileyday, 1, exx.slash]
    x_df.loc[9] = [J45_ROPE, kw.Chiday, 2, exx.slash]
    x_df.loc[10] = [J45_ROPE, kw.Danceday, 3, exx.slash]
    x_df.loc[11] = [J45_ROPE, kw.Eastday, 4, exx.slash]
    return x_df


# def get_ex2_br00006_df() -> DataFrame:
#     """br00006_moment_timeoffi_v0_0_0
#     moment_rope,offi_time,_offi_time_maxt"""
#     x_df = DataFrame(columns=[kw.moment_rope, "offi_time", "offi_time_max"])
#     x_df.loc[0] = [exx.a23_slash, 100, 300]
#     x_df.loc[1] = [exx.a23_slash, 110, 320]
#     x_df.loc[2] = [exx.a23_slash, 120, 330]
#     x_df.loc[3] = [exx.a23_slash, 130, 340]
#     x_df.loc[4] = [exx.a23_slash, 140, 350]
#     return x_df


def get_small_example01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["Fay"])
    x_dt.loc[0, "Fay"] = "Fay_bob0"
    x_dt.loc[1, "Fay"] = "Fay_bob1"
    x_dt.loc[2, "Fay"] = "Fay_bob2"
    x_dt.loc[3, "Fay"] = "Fay_bob3"
    return x_dt


def get_small_example01_csv() -> str:
    return """Fay
fay_bob0
fay_bob1
fay_bob2
fay_bob3
"""


def get_empty_dataframe() -> DataFrame:
    return DataFrame()


def get_ex01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["fay", "bob", "x_boolean", "count"])
    x_dt.loc[0] = ["fay2", "bob1", False, 10]
    x_dt.loc[1] = ["fay1", "bob2", True, 10]
    x_dt.loc[2] = ["fay0", "bob3", True, 20]
    x_dt.loc[3] = ["fay3", "bob0", False, 20]
    return x_dt


def get_ex01_unordered_csv() -> str:
    return """fay,bob,x_boolean,count
fay2,bob1,False,10
fay1,bob2,True,10
fay0,bob3,True,20
fay3,bob0,False,20
"""


def get_ex01_ordered_by_fay_csv() -> str:
    return """fay,bob,x_boolean,count
fay0,bob3,True,20
fay1,bob2,True,10
fay2,bob1,False,10
fay3,bob0,False,20
"""


def get_ex01_ordered_by_count_csv() -> str:
    return """count,fay,bob,x_boolean
10,fay1,bob2,True
10,fay2,bob1,False
20,fay0,bob3,True
20,fay3,bob0,False
"""


def get_ex01_ordered_by_count_bob_csv() -> str:
    return """count,bob,fay,x_boolean
10,bob1,fay2,False
10,bob2,fay1,True
20,bob0,fay3,False
20,bob3,fay0,True
"""


def get_ex01_ordered_by_count_x_boolean_csv() -> str:
    return """count,x_boolean,fay,bob
10,False,fay2,bob1
10,True,fay1,bob2
20,False,fay3,bob0
20,True,fay0,bob3
"""


def get_ex02_atom_dataframe() -> DataFrame:
    ex02_columns = [
        "healer_name",
        "contact_name",
        "group_title",
        kw.labor_title,
        kw.awardee_title,
        "plan_rope",
    ]
    x_dt = DataFrame(columns=ex02_columns)
    # x_dt.loc[0] = ["Fay2", "Bob1", False, 10]
    # x_dt.loc[1] = ["Fay1", "Bob2", True, 10]
    # x_dt.loc[2] = ["Fay0", "Bob3", True, 20]
    # x_dt.loc[3] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[4] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[5] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[6] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[7] = ["Fay3", "Bob0", False, 20]
    x_dt.loc[0] = [";yao4", "sue2", ";bowl2", ";workforce5", "aw1", "amy45;casa"]
    x_dt.loc[1] = [";yao3", "sue2", ";bowl1", ";workforce4", "aw1", "amy45;casa;clean"]
    x_dt.loc[2] = [";yao4", "sue2", ";bowl1", ";workforce5", "aw1", "amy45;casa"]
    x_dt.loc[3] = [";yao3", "sue2", ";bowl2", ";workforce4", "aw1", "amy45;casa;clean"]
    x_dt.loc[4] = [";yao4", "sue1", ";bowl1", ";workforce5", "aw1", "amy45;casa"]
    x_dt.loc[5] = [";yao3", "sue1", ";bowl1", ";workforce4", "aw1", "amy45;casa;clean"]
    x_dt.loc[6] = [";yao4", "sue1", ";bowl2", ";workforce5", "aw1", "amy45;casa"]
    x_dt.loc[7] = [";yao3", "sue1", ";bowl2", ";workforce4", "aw1", "amy45;casa;clean"]

    return x_dt


def get_ex02_atom_csv() -> str:
    return """contact_name,group_title,plan_rope,labor_title,awardee_title,healer_name
sue1,;bowl1,amy45;casa,;workforce5,aw1,;yao4
sue1,;bowl1,amy45;casa;clean,;workforce4,aw1,;yao3
sue1,;bowl2,amy45;casa,;workforce5,aw1,;yao4
sue1,;bowl2,amy45;casa;clean,;workforce4,aw1,;yao3
sue2,;bowl1,amy45;casa,;workforce5,aw1,;yao4
sue2,;bowl1,amy45;casa;clean,;workforce4,aw1,;yao3
sue2,;bowl2,amy45;casa,;workforce5,aw1,;yao4
sue2,;bowl2,amy45;casa;clean,;workforce4,aw1,;yao3
"""
