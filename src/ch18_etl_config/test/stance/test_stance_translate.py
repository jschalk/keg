from sqlite3 import Cursor, connect as sqlite3_connect
from src.ch17_idea.idea_csv_tool import create_init_stance_idea_csv_strs
from src.ch18_etl_config.etl_sqlstr import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from src.ch18_etl_config.stance_tool import (
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
    add_translate_rows_to_stance_csv_strs,
)
from src.ref.keywords import Ch18Keywords as kw, ExampleStrs as exx


def test_add_to_br00042_csv_ReturnsObj(cursor0: Cursor):
    # ESTABLISH database with translate data
    # - [`br00042`](ideas/br00042.md): spark_num, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    create_sound_and_heard_tables(cursor0)
    trltitl_dimen = kw.translate_title
    trltitl_s_vld_tablename = prime_tbl(trltitl_dimen, kw.s_vld)
    insert_trltitl_sqlstr = f"""INSERT INTO {trltitl_s_vld_tablename}
    ({kw.spark_num}, {kw.face_name}, {kw.otx_title}, {kw.inx_title})
    VALUES
      ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
    ;
    """
    cursor0.execute(insert_trltitl_sqlstr)

    trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
    insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
    ({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
    VALUES
      ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
    , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
    ;
    """
    cursor0.execute(insert_trlcore_sqlstr)

    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    header_only_csv = x_ideas.get("br00042")
    print(f"{header_only_csv=}")
    expected_header_only_csv = f"{kw.spark_num},{kw.face_name},{kw.otx_title},{kw.inx_title},{kw.otx_knot},{kw.inx_knot},{kw.unknown_str}\n"
    assert header_only_csv == expected_header_only_csv

    # WHEN
    gen_csv = add_to_br00042_csv(header_only_csv, cursor0, csv_delimiter)

    # THEN
    sue_row = f",{sue_otx},{sue_otx},{sue_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
    bob_row = f",{bob_otx},{bob_otx},{bob_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
    expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
    print(f"     {gen_csv=}")
    print(f"{expected_csv=}")
    assert gen_csv == expected_csv


def test_add_to_br00043_csv_ReturnsObj(cursor0: Cursor):
    # ESTABLISH database with translate data
    # - [`br00043`](ideas/br00043.md): spark_num, face_name, otx_name, inx_name, otx_knot, inx_knot, unknown_str
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    create_sound_and_heard_tables(cursor0)
    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, kw.s_vld)
    insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
VALUES
  ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
    cursor0.execute(insert_trlname_sqlstr)

    trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
    insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)

    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    header_only_csv = x_ideas.get("br00043")
    print(f"{header_only_csv=}")
    expected_header_only_csv = f"{kw.spark_num},{kw.face_name},{kw.otx_name},{kw.inx_name},{kw.otx_knot},{kw.inx_knot},{kw.unknown_str}\n"
    assert header_only_csv == expected_header_only_csv

    # WHEN
    gen_csv = add_to_br00043_csv(header_only_csv, cursor0, csv_delimiter)

    # THEN
    sue_row = f",{sue_otx},{sue_otx},{sue_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
    bob_row = f",{bob_otx},{bob_otx},{bob_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
    expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
    print(f"     {gen_csv=}")
    print(f"{expected_csv=}")
    assert gen_csv == expected_csv


def test_add_to_br00044_csv_ReturnsObj(cursor0: Cursor):
    # ESTABLISH database with translate data
    # - [`br00044`](ideas/br00044.md): spark_num, face_name, otx_label, inx_label, otx_knot, inx_knot, unknown_str
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_clean_otx = "clean"
    sue_clean_inx = "limpia"
    bob_clean_otx = "very clean"
    bob_clean_inx = "very limpia"
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    create_sound_and_heard_tables(cursor0)
    trllabe_dimen = kw.translate_label
    trllabe_s_vld_tablename = prime_tbl(trllabe_dimen, kw.s_vld)
    insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_label}, {kw.inx_label})
VALUES
  ({spark1}, '{exx.sue}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{exx.bob}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
    cursor0.execute(insert_trllabe_sqlstr)

    trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
    insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{exx.sue}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{exx.bob}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)

    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    header_only_csv = x_ideas.get("br00044")
    print(f"{header_only_csv=}")
    expected_header_only_csv = f"{kw.spark_num},{kw.face_name},{kw.otx_label},{kw.inx_label},{kw.otx_knot},{kw.inx_knot},{kw.unknown_str}\n"
    assert header_only_csv == expected_header_only_csv

    # WHEN
    gen_csv = add_to_br00044_csv(header_only_csv, cursor0, csv_delimiter)

    # THEN
    sue_row = f",{exx.sue},{sue_clean_otx},{sue_clean_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
    bob_row = f",{exx.bob},{bob_clean_otx},{bob_clean_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
    expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
    print(f"     {gen_csv=}")
    print(f"{expected_csv=}")
    assert gen_csv == expected_csv


def test_add_to_br00045_csv_ReturnsObj(cursor0: Cursor):
    # ESTABLISH database with translate data
    # - [`br00045`](ideas/br00045.md): spark_num, face_name, otx_rope, inx_rope, otx_knot, inx_knot, unknown_str
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_clean_otx = "?casa?clean?"
    sue_clean_inx = ".casa.limpia."
    bob_clean_otx = ";casa;very clean;"
    bob_clean_inx = "/casa/very limpia/"
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    create_sound_and_heard_tables(cursor0)
    trlrope_dimen = kw.translate_rope
    trlrope_s_vld_tablename = prime_tbl(trlrope_dimen, kw.s_vld)
    insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_rope}, {kw.inx_rope})
VALUES
  ({spark1}, '{exx.sue}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{exx.bob}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
    cursor0.execute(insert_trlrope_sqlstr)

    trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
    insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
VALUES
  ('{exx.sue}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{exx.bob}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
    cursor0.execute(insert_trlcore_sqlstr)

    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    header_only_csv = x_ideas.get("br00045")
    print(f"{header_only_csv=}")
    expected_header_only_csv = f"{kw.spark_num},{kw.face_name},{kw.otx_rope},{kw.inx_rope},{kw.otx_knot},{kw.inx_knot},{kw.unknown_str}\n"
    assert header_only_csv == expected_header_only_csv

    # WHEN
    gen_csv = add_to_br00045_csv(header_only_csv, cursor0, csv_delimiter)

    # THEN
    sue_row = f",{exx.sue},{sue_clean_otx},{sue_clean_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
    bob_row = f",{exx.bob},{bob_clean_otx},{bob_clean_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
    expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
    print(f"     {gen_csv=}")
    print(f"{expected_csv=}")
    assert gen_csv == expected_csv


def test_add_translate_rows_to_stance_csv_strs_ReturnsObj(cursor0: Cursor):
    # ESTABLISH database with translate data
    # - [`br00042`](ideas/br00042.md): spark_num, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    create_sound_and_heard_tables(cursor0)

    # insert translate_title records
    trltitl_dimen = kw.translate_title
    trltitl_s_vld_tablename = prime_tbl(trltitl_dimen, kw.s_vld)
    insert_trltitl_sqlstr = f"""INSERT INTO {trltitl_s_vld_tablename}
    ({kw.spark_num}, {kw.face_name}, {kw.otx_title}, {kw.inx_title})
    VALUES
      ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
    , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
    ;
    """
    cursor0.execute(insert_trltitl_sqlstr)

    # insert translate_name records
    trlname_dimen = kw.translate_name
    trlname_s_vld_tablename = prime_tbl(trlname_dimen, kw.s_vld)
    insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_name}, {kw.inx_name})
VALUES
  ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
    cursor0.execute(insert_trlname_sqlstr)

    # insert translate_label records
    sue_clean_otx = "clean"
    sue_clean_inx = "limpia"
    bob_clean_otx = "very clean"
    bob_clean_inx = "very limpia"
    trllabe_dimen = kw.translate_label
    trllabe_s_vld_tablename = prime_tbl(trllabe_dimen, kw.s_vld)
    insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_label}, {kw.inx_label})
VALUES
  ({spark1}, '{exx.sue}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{exx.bob}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
    cursor0.execute(insert_trllabe_sqlstr)

    # insert translate_rope records
    sue_clean_otx = "?casa?clean?"
    sue_clean_inx = ".casa.limpia."
    bob_clean_otx = ";casa;very clean;"
    bob_clean_inx = "/casa/very limpia/"
    trlrope_dimen = kw.translate_rope
    trlrope_s_vld_tablename = prime_tbl(trlrope_dimen, kw.s_vld)
    insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_vld_tablename}
({kw.spark_num}, {kw.face_name}, {kw.otx_rope}, {kw.inx_rope})
VALUES
  ({spark1}, '{exx.sue}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{exx.bob}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
    cursor0.execute(insert_trlrope_sqlstr)

    # insert translate_core records
    trlcore_s_vld_tablename = prime_tbl("TRLCORE", kw.s_vld)
    insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
    ({kw.face_name}, {kw.otx_knot}, {kw.inx_knot}, {kw.unknown_str})
    VALUES
      ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
    , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
    ;
    """
    cursor0.execute(insert_trlcore_sqlstr)

    csv_delimiter = ","
    x_ideas = create_init_stance_idea_csv_strs()
    br00042_header = x_ideas.get("br00042")
    br00043_header = x_ideas.get("br00043")
    br00044_header = x_ideas.get("br00044")
    br00045_header = x_ideas.get("br00045")

    # WHEN
    add_translate_rows_to_stance_csv_strs(cursor0, x_ideas, csv_delimiter)

    # THEN
    assert x_ideas.get("br00042") != br00042_header
    assert x_ideas.get("br00043") != br00043_header
    assert x_ideas.get("br00044") != br00044_header
    assert x_ideas.get("br00045") != br00045_header
