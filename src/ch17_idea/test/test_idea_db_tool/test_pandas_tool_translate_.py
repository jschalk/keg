from copy import deepcopy as copy_deepcopy
from pandas import DataFrame
from pandas.testing import assert_frame_equal as pandas_assert_frame_equal
from src.ch04_rope.rope import create_rope, to_rope
from src.ch16_translate.map_term import namemap_shop
from src.ch16_translate.test._util.ch16_examples import (
    get_casa_maison_rope_inx_dt,
    get_casa_maison_rope_otx_dt,
    get_casa_maison_translateunit_set_by_label,
    get_casa_maison_translateunit_set_by_otx2inx,
)
from src.ch16_translate.translate_main import translateunit_shop
from src.ch17_idea.idea_db_tool import (
    get_dataframe_translateable_columns,
    translate_all_columns_dataframe,
    translate_single_column_dataframe,
)
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_get_dataframe_translateable_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    x_dt = DataFrame()
    assert get_dataframe_translateable_columns(x_dt) == set()
    x_dt = DataFrame(columns=[kw.partner_name])
    assert get_dataframe_translateable_columns(x_dt) == {kw.partner_name}
    x_dt = DataFrame(columns=[kw.partner_name, kw.partner_cred_lumen])
    assert get_dataframe_translateable_columns(x_dt) == {kw.partner_name}
    x_dt = DataFrame(
        columns=[kw.reason_context, kw.partner_name, kw.partner_cred_lumen]
    )
    assert get_dataframe_translateable_columns(x_dt) == {
        kw.partner_name,
        kw.reason_context,
    }
    x_dt = DataFrame(columns=["calc_swim", kw.partner_name, kw.partner_cred_lumen])
    assert get_dataframe_translateable_columns(x_dt) == {kw.partner_name}


def test_translate_single_column_dataframe_ReturnsObj_Scenario0_PartnerName_EmptyDataFrame():
    # ESTABLISH
    partner_name_mapunit = namemap_shop()
    empty_dt = DataFrame(columns=[kw.partner_name])

    # WHEN
    gen_dt = translate_single_column_dataframe(
        empty_dt, partner_name_mapunit, kw.partner_name
    )

    # THEN
    pandas_assert_frame_equal(gen_dt, empty_dt)


def test_translate_single_column_dataframe_SetsParameterAttrs_Scenario0_PartnerName_5rows():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    partner_name_mapunit = namemap_shop()
    partner_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    partner_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    partner_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.partner_name])
    otx_dt.loc[0] = [zia_otx]
    otx_dt.loc[1] = [sue_otx]
    otx_dt.loc[2] = [bob_otx]
    otx_dt.loc[3] = [xio_otx]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_single_column_dataframe(otx_dt, partner_name_mapunit, kw.partner_name)

    # THEN
    assert otx_dt.iloc[0][kw.partner_name] == zia_otx
    assert otx_dt.iloc[1][kw.partner_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.partner_name])
    inx_dt.loc[0] = zia_otx
    inx_dt.loc[1] = sue_inx
    inx_dt.loc[2] = bob_inx
    inx_dt.loc[3] = xio_inx
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    pandas_assert_frame_equal(otx_dt, inx_dt)
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_translate_single_column_dataframe_SetsParameterAttrs_Scenario1_PartnerName_5rowsMultipleColumns():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    partner_name_mapunit = namemap_shop()
    partner_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    partner_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    partner_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_single_column_dataframe(otx_dt, partner_name_mapunit, kw.partner_name)

    # THEN
    assert otx_dt.iloc[0][kw.partner_name] == zia_otx
    assert otx_dt.iloc[1][kw.partner_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_inx, 12]
    inx_dt.loc[2] = [exx.a23, bob_inx, 12]
    inx_dt.loc[3] = [exx.a23, xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario0_PartnerName():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, None)

    # THEN
    assert otx_dt.iloc[0][kw.partner_name] == zia_otx
    assert otx_dt.iloc[1][kw.partner_name] == sue_otx
    pandas_assert_frame_equal(otx_dt, old_otx_dt)
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_otx, 12]
    inx_dt.loc[2] = [exx.a23, bob_otx, 12]
    inx_dt.loc[3] = [exx.a23, xio_otx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario1_PartnerName():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    yao_translateunit = translateunit_shop(exx.yao)
    yao_translateunit.set_otx2inx(kw.NameTerm, xio_otx, xio_inx)
    yao_translateunit.set_otx2inx(kw.NameTerm, sue_otx, sue_inx)
    yao_translateunit.set_otx2inx(kw.NameTerm, bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    otx_dt.loc[0] = [exx.a23, zia_otx, 12]
    otx_dt.loc[1] = [exx.a23, sue_otx, 12]
    otx_dt.loc[2] = [exx.a23, bob_otx, 12]
    otx_dt.loc[3] = [exx.a23, xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_translateunit)

    # THEN
    assert otx_dt.iloc[0][kw.partner_name] == zia_otx
    assert otx_dt.iloc[1][kw.partner_name] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[kw.moment_rope, kw.partner_name, kw.partner_cred_lumen])
    inx_dt.loc[0] = [exx.a23, zia_otx, 12]
    inx_dt.loc[1] = [exx.a23, sue_inx, 12]
    inx_dt.loc[2] = [exx.a23, bob_inx, 12]
    inx_dt.loc[3] = [exx.a23, xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario2_RodeUnit_get_casa_maison_translateunit_set_by_otx2inx():
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
    yao_translateunit = get_casa_maison_translateunit_set_by_otx2inx()
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][kw.reason_context] == otx_amy45_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_otx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_otx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_otx_rope
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_translateunit)

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


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario3_RodeUnit_get_casa_maison_translateunit_set_by_label():
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
    yao_translateunit = get_casa_maison_translateunit_set_by_label()
    # print(f"{yao_translateunit=}")
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][kw.reason_context] == otx_amy45_rope
    assert otx_dt.iloc[1][kw.reason_context] == casa_otx_rope
    assert otx_dt.iloc[2][kw.reason_context] == clean_otx_rope
    assert otx_dt.iloc[3][kw.reason_context] == sweep_otx_rope
    print(f"Before {otx_dt=}")
    print("")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_translateunit)

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
