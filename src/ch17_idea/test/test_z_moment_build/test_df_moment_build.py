from src.ch00_py.file_toolbox import create_path
from src.ch04_rope.rope import default_knot_if_None
from src.ch13_time.epoch_main import epochunit_shop, get_default_epoch_config_dict
from src.ch13_time.test._util.ch13_examples import get_five_config
from src.ch14_moment.moment_main import momentunit_shop
from src.ch17_idea.brick_main import moment_build_from_df
from src.ch17_idea.test._util.ch17_examples import (
    J45_ROPE,
    get_ex1_br00000_df,
    get_ex1_br00001_df,
    get_ex1_br00002_df,
    get_ex1_br00003_df,
    get_ex1_br00004_df,
    get_ex1_br00005_df,
    get_ex2_br00000_df,
    get_ex2_br00001_df,
    get_ex2_br00002_df,
    get_ex2_br00003_df,
    get_ex2_br00004_df,
    get_ex2_br00005_df,
)
from src.ref.keywords import ExampleStrs as exx


# ESTABLISH a dataframe, build a moment unit
def test_moment_build_from_df_ReturnsObj_Scenario0_OneMomentRope(
    temp3_fs,
):
    # ESTABLISH
    br00000_df = get_ex1_br00000_df()
    br00001_df = get_ex1_br00001_df()
    br00002_df = get_ex1_br00002_df()
    br00003_df = get_ex1_br00003_df()
    br00004_df = get_ex1_br00004_df()
    br00005_df = get_ex1_br00005_df()
    x_fund_grain = 55
    x_respect_grain = 66
    x_mana_grain = 77
    x_job_listen_rotations = 7
    x_moments_dir = create_path(str(temp3_fs), "Fay")

    # WHEN
    x_momentunits = moment_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )

    # THEN
    assert x_momentunits
    assert x_momentunits.get(exx.a23) != None
    creg_epochunit = epochunit_shop(get_default_epoch_config_dict())
    expected_amy23_momentunit = momentunit_shop(
        moment_rope=exx.a23,
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        mana_grain=x_mana_grain,
        respect_grain=x_respect_grain,
        knot=default_knot_if_None(),
        epoch=creg_epochunit,
        job_listen_rotations=x_job_listen_rotations,
    )
    expected_amy23_momentunit.add_budunit(
        person_name="Sue",
        bud_time=777,
        quota=445,
        allow_prev_to_offi_time_max_entry=True,
        celldepth=5,
    )
    expected_amy23_momentunit.add_paypurchase(
        person_name="Zia",
        contact_name="Bob",
        tran_time=777,
        amount=888,
    )
    gen_momentunit = x_momentunits.get(exx.a23)
    assert gen_momentunit.fund_grain == x_fund_grain
    assert gen_momentunit.respect_grain == x_respect_grain
    assert gen_momentunit.mana_grain == x_mana_grain
    assert gen_momentunit.moment_rope == exx.a23
    assert gen_momentunit.moment_mstr_dir == x_moments_dir
    assert gen_momentunit.epoch == expected_amy23_momentunit.epoch
    expected_personbudhistorys = expected_amy23_momentunit.personbudhistorys
    print(expected_personbudhistorys)
    print(gen_momentunit.personbudhistorys)
    assert gen_momentunit.personbudhistorys == expected_personbudhistorys
    a23_tranunits = expected_amy23_momentunit.paybook.tranunits
    assert gen_momentunit.paybook.tranunits == a23_tranunits
    # print(f"{gen_momentunit.personbudhistorys=}")
    assert len(gen_momentunit.personbudhistorys) == 1
    assert len(gen_momentunit.paybook.tranunits) == 1
    assert gen_momentunit == expected_amy23_momentunit


# ESTABLISH a dataframe, build a moment unit
def test_moment_build_from_df_ReturnsObj_Scenario1_TwoMomentRopes(
    temp3_fs,
):
    # ESTABLISH
    br00000_df = get_ex2_br00000_df()
    br00001_df = get_ex2_br00001_df()
    br00002_df = get_ex2_br00002_df()
    br00003_df = get_ex2_br00003_df()
    br00004_df = get_ex2_br00004_df()
    br00005_df = get_ex2_br00005_df()
    x_fund_grain = 55
    x_respect_grain = 66
    x_mana_grain = 77
    x_moments_dir = create_path(str(temp3_fs), "Fay")

    # WHEN
    x_momentunits = moment_build_from_df(
        br00000_df,
        br00001_df,
        br00002_df,
        br00003_df,
        br00004_df,
        br00005_df,
        x_fund_grain,
        x_respect_grain,
        x_mana_grain,
        x_moments_dir,
    )

    # THEN
    creg_epochunit = epochunit_shop(get_default_epoch_config_dict())
    amy23_momentunit = momentunit_shop(
        moment_rope=exx.a23,
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        mana_grain=x_mana_grain,
        respect_grain=x_respect_grain,
        knot=default_knot_if_None(),
        epoch=creg_epochunit,
    )
    five_epochunit = epochunit_shop(get_five_config())
    jeffy45_momentunit = momentunit_shop(
        moment_rope=J45_ROPE,
        moment_mstr_dir=x_moments_dir,
        fund_grain=x_fund_grain,
        mana_grain=x_mana_grain,
        respect_grain=x_respect_grain,
        knot=exx.slash,
        epoch=five_epochunit,
    )
    assert x_momentunits
    assert x_momentunits.get(exx.a23_slash) != None
    creg_momentunit = x_momentunits.get(exx.a23_slash)
    assert creg_momentunit.fund_grain == x_fund_grain
    assert creg_momentunit.respect_grain == x_respect_grain
    assert creg_momentunit.mana_grain == x_mana_grain
    assert creg_momentunit.moment_rope == exx.a23_slash
    assert creg_momentunit.moment_mstr_dir == x_moments_dir
    assert creg_momentunit.epoch == amy23_momentunit.epoch
    assert len(creg_momentunit.personbudhistorys) == 3
    assert len(creg_momentunit.paybook.tranunits) == 4
    # assert creg_momentunit == amy23_momentunit

    five_momentunit = x_momentunits.get(J45_ROPE)
    assert five_momentunit.fund_grain == x_fund_grain
    assert five_momentunit.respect_grain == x_respect_grain
    assert five_momentunit.mana_grain == x_mana_grain
    assert five_momentunit.moment_rope == J45_ROPE
    assert five_momentunit.moment_mstr_dir == x_moments_dir
    assert len(five_momentunit.personbudhistorys) == 2
    assert len(five_momentunit.paybook.tranunits) == 1
    jeffy45_epoch = jeffy45_momentunit.epoch
    assert five_momentunit.epoch.hours_config == jeffy45_epoch.hours_config
    assert five_momentunit.epoch.weekdays_config == jeffy45_epoch.weekdays_config
    assert five_momentunit.epoch.months_config == jeffy45_epoch.months_config
    assert five_momentunit.epoch == jeffy45_epoch
    # assert five_momentunit == jeffy45_momentunit
