from ch05_rope.rope import create_rope, to_rope
from ch17_jargon.map_term import namemap_shop
from ch17_jargon.test._util.ch17_examples import (
    get_casa_maison_jargonunit_set_by_label,
    get_casa_maison_jargonunit_set_by_otx2inx,
)
from ch17_jargon.jargon_main import jargonunit_shop
from ch20_brick.brick_db_tool import (
    get_dataframe_jargonable_columns,
    jargon_all_columns_dataframe,
    jargon_single_column_dataframe,
)
from ch20_brick.test._util.ch20_examples import (
    get_casa_maison_rope_inx_dt,
    get_casa_maison_rope_otx_dt,
)
from ch99_glossary.ch_keyword import Ch20Keywords as kw, ExampleStrs as exx
from copy import deepcopy as copy_deepcopy
from pandas import DataFrame
from pandas.testing import assert_frame_equal as pandas_assert_frame_equal


def test_get_dataframe_jargonable_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    x_dt = DataFrame()
    assert get_dataframe_jargonable_columns(x_dt) == set()
    x_dt = DataFrame(columns=[kw.contact_name])
    assert get_dataframe_jargonable_columns(x_dt) == {kw.contact_name}
    x_dt = DataFrame(columns=[kw.contact_name, kw.contact_cred_mass])
    assert get_dataframe_jargonable_columns(x_dt) == {kw.contact_name}
    x_dt = DataFrame(columns=[kw.reason_context, kw.contact_name, kw.contact_cred_mass])
    assert get_dataframe_jargonable_columns(x_dt) == {
        kw.contact_name,
        kw.reason_context,
    }
    x_dt = DataFrame(columns=["calc_bowl", kw.contact_name, kw.contact_cred_mass])
    assert get_dataframe_jargonable_columns(x_dt) == {kw.contact_name}


def test_jargon_single_column_dataframe_ReturnsObj_Scenario0_ContactName_EmptyDataFrame():
    # ESTABLISH
    contact_name_mapunit = namemap_shop()
    empty_dt = DataFrame(columns=[kw.contact_name])

    # WHEN
    gen_dt = jargon_single_column_dataframe(
        empty_dt, contact_name_mapunit, kw.contact_name
    )

    # THEN
    pandas_assert_frame_equal(gen_dt, empty_dt)


def test_jargon_single_column_dataframe_SetsParameterAttrs_Scenario0_ContactName_5rows():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    contact_name_mapunit = namemap_shop()
    contact_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    contact_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    contact_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.contact_name])
    otx_dt.loc[0] = [zia_otx]
    otx_dt.loc[1] = [sue_otx]
    otx_dt.loc[2] = [bob_otx]
    otx_dt.loc[3] = [xio_otx]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    jargon_single_column_dataframe(otx_dt, contact_name_mapunit, kw.contact_name)

    # THEN
    assert otx_dt.iloc[0][kw.contact_name] == zia_otx
    assert otx_dt.iloc[1][kw.contact_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.contact_name])
    inx_dt.loc[0] = zia_otx
    inx_dt.loc[1] = sue_inx
    inx_dt.loc[2] = bob_inx
    inx_dt.loc[3] = xio_inx
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    pandas_assert_frame_equal(otx_dt, inx_dt)
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_jargon_single_column_dataframe_SetsParameterAttrs_Scenario1_ContactName_5rowsMultipleColumns():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    contact_name_mapunit = namemap_shop()
    contact_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    contact_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    contact_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    jargon_single_column_dataframe(otx_dt, contact_name_mapunit, kw.contact_name)

    # THEN
    assert otx_dt.iloc[0][kw.contact_name] == zia_otx
    assert otx_dt.iloc[1][kw.contact_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_inx, 12]
    inx_dt.loc[2] = [exx.a23, bob_inx, 12]
    inx_dt.loc[3] = [exx.a23, xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_jargon_all_columns_dataframe_SetsParameterAttrs_Scenario0_ContactName():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    jargon_all_columns_dataframe(otx_dt, None)

    # THEN
    assert otx_dt.iloc[0][kw.contact_name] == zia_otx
    assert otx_dt.iloc[1][kw.contact_name] == sue_otx
    pandas_assert_frame_equal(otx_dt, old_otx_dt)
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_otx, 12]
    inx_dt.loc[2] = [exx.a23, bob_otx, 12]
    inx_dt.loc[3] = [exx.a23, xio_otx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_jargon_all_columns_dataframe_SetsParameterAttrs_Scenario1_ContactName():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    yao_jargonunit = jargonunit_shop(exx.yao)
    yao_jargonunit.set_otx2inx(kw.NameTerm, xio_otx, xio_inx)
    yao_jargonunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)
    yao_jargonunit.set_otx2inx(kw.NameTerm, bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    jargon_all_columns_dataframe(otx_dt, yao_jargonunit)

    # THEN
    assert otx_dt.iloc[0][kw.contact_name] == zia_otx
    assert otx_dt.iloc[1][kw.contact_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.contact_name, kw.contact_cred_mass])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_inx, 12]
    inx_dt.loc[2] = [exx.a23, bob_inx, 12]
    inx_dt.loc[3] = [exx.a23, xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_jargon_all_columns_dataframe_SetsParameterAttrs_Scenario2_RodeUnit_get_casa_maison_jargonunit_set_by_otx2inx():
    # ESTABLISH
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)
    yao_jargonunit = get_casa_maison_jargonunit_set_by_otx2inx()
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][kw.reason_context] == otx_amy45_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_otx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_otx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_otx_rope
    print(f"{otx_dt=}")

    # WHEN
    jargon_all_columns_dataframe(otx_dt, yao_jargonunit)

    # THEN
    assert otx_dt.iloc[0][kw.reason_context] == inx_amy87_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_inx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_inx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_inx_rope
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_rope_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_jargon_all_columns_dataframe_SetsParameterAttrs_Scenario3_RodeUnit_get_casa_maison_jargonunit_set_by_label():
    # ESTABLISH
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)
    yao_jargonunit = get_casa_maison_jargonunit_set_by_label()
    # print(f"{yao_jargonunit=}")
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][kw.reason_context] == otx_amy45_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_otx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_otx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_otx_rope
    print(f"Before {otx_dt=}")
    print("")

    # WHEN
    jargon_all_columns_dataframe(otx_dt, yao_jargonunit)

    # THEN
    print("")
    print(f"after  {otx_dt=}")
    assert otx_dt.iloc[0][kw.reason_context] == inx_amy87_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_inx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_inx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_inx_rope
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_rope_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)
