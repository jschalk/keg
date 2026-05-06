from ch04_rope.rope import create_rope, to_rope
from pandas import DataFrame
from ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


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


def get_suita_contact_name_inx_dt() -> DataFrame:
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    zia_otx = "Zia"
    inx_dt = DataFrame(columns=[kw.contact_name])
    inx_dt.loc[0, kw.contact_name] = xio_inx
    inx_dt.loc[1, kw.contact_name] = sue_inx
    inx_dt.loc[2, kw.contact_name] = bob_inx
    inx_dt.loc[3, kw.contact_name] = zia_otx
    return inx_dt


def get_suita_contact_name_otx_dt() -> DataFrame:
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[kw.contact_name])
    otx_dt.loc[0, kw.contact_name] = zia_otx
    otx_dt.loc[1, kw.contact_name] = sue_otx
    otx_dt.loc[2, kw.contact_name] = bob_otx
    otx_dt.loc[3, kw.contact_name] = xio_otx
    return otx_dt


def get_casa_maison_rope_inx_dt() -> DataFrame:
    inx_amy87_str = "amy87"
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_inx_rope = create_rope(inx_amy87_rope, "maison")
    clean_inx_rope = create_rope(casa_inx_rope, "propre")
    sweep_inx_rope = create_rope(clean_inx_rope, "sweep")
    inx_dt = DataFrame(columns=[kw.reason_context])
    inx_dt.loc[0, kw.reason_context] = inx_amy87_rope
    inx_dt.loc[1, kw.reason_context] = casa_inx_rope
    inx_dt.loc[2, kw.reason_context] = clean_inx_rope
    inx_dt.loc[3, kw.reason_context] = sweep_inx_rope
    return inx_dt


def get_casa_maison_rope_otx_dt() -> DataFrame:
    otx_amy45_str = "amy45"
    otx_amy45_rope = to_rope(otx_amy45_str)
    casa_otx_str = "casa"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    clean_otx_str = "clean"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    otx_dt = DataFrame(columns=[kw.reason_context])
    otx_dt.loc[0, kw.reason_context] = otx_amy45_rope
    otx_dt.loc[1, kw.reason_context] = casa_otx_rope
    otx_dt.loc[2, kw.reason_context] = clean_otx_rope
    otx_dt.loc[3, kw.reason_context] = sweep_otx_rope
    return otx_dt
