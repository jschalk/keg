from os.path import exists as os_path_exists
from pandas import DataFrame
from src.ch00_py.file_toolbox import create_path, save_json
from src.ch04_rope.rope import create_rope, to_rope
from src.ch16_translate.test._util.ch16_examples import (
    get_casa_maison_rope_inx_dt,
    get_casa_maison_rope_otx_dt,
    get_casa_maison_translateunit_set_by_label,
    get_suita_contact_name_inx_dt,
    get_suita_contact_name_otx_dt,
    get_suita_namemap,
)
from src.ch16_translate.translate_config import get_translate_filename
from src.ch16_translate.translate_main import translateunit_shop
from src.ch17_idea.brick_db_tool import (
    move_otx_csvs_to_translate_inx,
    open_csv,
    save_dataframe_to_csv,
)
from src.ref.keywords import Ch17Keywords as kw, ExampleStrs as exx


def test_move_otx_csvs_to_translate_inx_CreatesTranslateedFiles_Scenario0_SingleFile(
    temp3_fs,
):
    # ESTABLISH
    bob_otx = "Bob"
    sue_otx = "Sue"
    xio_otx = "Xio"
    zia_otx = "Zia"
    bob_inx = "Bobita"
    sue_inx = "Suita"
    xio_inx = "Xioita"
    sue_translateunit = translateunit_shop(sue_otx)
    sue_translateunit.set_namemap(get_suita_namemap())
    sue_dir = create_path(str(temp3_fs), sue_otx)
    translateunit_file_path = create_path(sue_dir, get_translate_filename())
    print(f"{sue_dir=}")
    save_json(sue_dir, get_translate_filename(), sue_translateunit.to_dict())
    sue_otx_dt = get_suita_contact_name_otx_dt()
    sue_inx_dt = get_suita_contact_name_inx_dt()
    otx_dir = create_path(sue_dir, "otx")
    inx_dir = create_path(sue_dir, "inx")

    example_filename = "contact_name_example.csv"
    otx_file_path = create_path(otx_dir, example_filename)
    inx_file_path = create_path(inx_dir, example_filename)
    save_dataframe_to_csv(sue_otx_dt, otx_dir, example_filename)
    assert os_path_exists(translateunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_translate_inx(sue_dir)

    # THEN
    assert os_path_exists(translateunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    gen_inx_dt = open_csv(inx_dir, example_filename)
    assert gen_inx_dt.iloc[0][kw.contact_name] == bob_inx
    assert gen_inx_dt.iloc[3][kw.contact_name] == zia_otx
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    static_inx_dt = DataFrame(columns=[kw.contact_name])
    static_inx_dt.loc[0, kw.contact_name] = bob_inx
    static_inx_dt.loc[1, kw.contact_name] = sue_inx
    static_inx_dt.loc[2, kw.contact_name] = xio_inx
    static_inx_dt.loc[3, kw.contact_name] = zia_otx
    assert gen_inx_dt.iloc[0][kw.contact_name] == static_inx_dt.iloc[0][kw.contact_name]
    assert gen_inx_dt.iloc[1][kw.contact_name] == static_inx_dt.iloc[1][kw.contact_name]
    assert gen_inx_dt.iloc[2][kw.contact_name] == static_inx_dt.iloc[2][kw.contact_name]
    assert gen_inx_dt.iloc[3][kw.contact_name] == static_inx_dt.iloc[3][kw.contact_name]
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(kw.contact_name).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(kw.contact_name).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == static_inx_dt.to_csv()


# save two dataframes to be translateed: two files in otx, two files in inx
def test_move_otx_csvs_to_translate_inx_CreatesTranslateedFiles_Scenario1_SingleFile_RopeTerm(
    temp3_fs,
):
    # ESTABLISH
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_rope, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_rope, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)

    sweep_otx_rope = create_rope(clean_otx_rope, exx.sweep)
    sweep_inx_rope = create_rope(clean_inx_rope, exx.sweep)

    sue_translateunit = get_casa_maison_translateunit_set_by_label()
    sue_dir = create_path(str(temp3_fs), sue_translateunit.spark_face)
    save_json(sue_dir, get_translate_filename(), sue_translateunit.to_dict())
    sue_otx_dt = get_casa_maison_rope_otx_dt()
    sue_inx_dt = get_casa_maison_rope_inx_dt()
    otx_dir = create_path(sue_dir, "otx")
    inx_dir = create_path(sue_dir, "inx")

    example_filename = "rope1_example.csv"
    otx_file_path = create_path(otx_dir, example_filename)
    inx_file_path = create_path(inx_dir, example_filename)
    save_dataframe_to_csv(sue_otx_dt, otx_dir, example_filename)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_translate_inx(sue_dir)

    # THEN
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    print(f"{sue_otx_dt=} \n")
    print(f"{sue_inx_dt=} \n")
    gen_inx_dt = open_csv(inx_dir, example_filename)
    assert gen_inx_dt.iloc[0][kw.reason_context] == inx_amy87_rope
    assert gen_inx_dt.iloc[1][kw.reason_context] == casa_inx_rope
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    assert (
        gen_inx_dt.iloc[0][kw.reason_context] == sue_inx_dt.iloc[0][kw.reason_context]
    )
    assert (
        gen_inx_dt.iloc[1][kw.reason_context] == sue_inx_dt.iloc[1][kw.reason_context]
    )
    assert (
        gen_inx_dt.iloc[2][kw.reason_context] == sue_inx_dt.iloc[2][kw.reason_context]
    )
    assert (
        gen_inx_dt.iloc[3][kw.reason_context] == sue_inx_dt.iloc[3][kw.reason_context]
    )
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(kw.reason_context).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(kw.reason_context).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == sue_inx_dt.to_csv()


# save two dataframes to be translateed: two files in otx, two files in inx
def test_move_otx_csvs_to_translate_inx_CreatesTranslateedFiles_Scenario2_TwoFile(
    temp3_fs,
):
    # ESTABLISH
    sue_translateunit = get_casa_maison_translateunit_set_by_label()
    sue_translateunit.set_namemap(get_suita_namemap())
    sue_dir = create_path(str(temp3_fs), sue_translateunit.spark_face)
    translateunit_file_path = create_path(sue_dir, get_translate_filename())
    print(f"{sue_dir=}")
    save_json(sue_dir, get_translate_filename(), sue_translateunit.to_dict())
    sue_otx_dt = get_suita_contact_name_otx_dt()
    otx_dir = create_path(sue_dir, "otx")
    inx_dir = create_path(sue_dir, "inx")

    contact_name_filename = "contact_name_example.csv"
    contact_name_otx_file_path = create_path(otx_dir, contact_name_filename)
    contact_name_inx_file_path = create_path(inx_dir, contact_name_filename)
    rope1_otx_dt = get_casa_maison_rope_otx_dt()
    rope1_filename = "rope1_example.csv"
    rope1_otx_file_path = create_path(otx_dir, rope1_filename)
    rope1_inx_file_path = create_path(inx_dir, rope1_filename)
    save_dataframe_to_csv(rope1_otx_dt, otx_dir, rope1_filename)
    save_dataframe_to_csv(sue_otx_dt, otx_dir, contact_name_filename)
    assert os_path_exists(rope1_otx_file_path)
    assert os_path_exists(rope1_inx_file_path) is False
    assert os_path_exists(translateunit_file_path)
    assert os_path_exists(contact_name_otx_file_path)
    assert os_path_exists(contact_name_inx_file_path) is False

    # WHEN
    move_otx_csvs_to_translate_inx(sue_dir)

    # THEN
    assert os_path_exists(rope1_otx_file_path)
    assert os_path_exists(rope1_inx_file_path)
    assert os_path_exists(translateunit_file_path)
    assert os_path_exists(contact_name_otx_file_path)
    assert os_path_exists(contact_name_inx_file_path)
    contact_inx_dt = open_csv(inx_dir, contact_name_filename)
    gen_csv = contact_inx_dt.sort_values(kw.contact_name).to_csv(index=False)
    sue_inx_dt = get_suita_contact_name_inx_dt()
    assert gen_csv == sue_inx_dt.sort_values(kw.contact_name).to_csv(index=False)

    gen_rope1_inx_dt = open_csv(inx_dir, rope1_filename)
    rope1_inx_dt = get_casa_maison_rope_inx_dt()
    assert gen_rope1_inx_dt.to_csv() == rope1_inx_dt.to_csv()
