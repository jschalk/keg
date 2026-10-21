# from ch18_speech.test._util.ch17_examples import (
#     get_bowl_titleyap,
#     get_clean_labelyap,
#     get_clean_ropeyap,
#     get_suita_nameyap,
# )
# from ch18_speech.speech_main import inherit_speechunit, speechunit_shop
# from ch99_glossary.ch_keyword import Ch18Keywords as kw, ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario0_EmptySpeechUnits():
#     # ESTABLISH
#     old_speechunit = speechunit_shop(exx.sue, 0)
#     new_speechunit = speechunit_shop(exx.sue, 1)

#     # WHEN
#     merged_speechunit = inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert merged_speechunit
#     assert merged_speechunit == new_speechunit


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_speechunit = speechunit_shop(exx.sue, 0, iux_knot=slash_iux_knot)
#     new_speechunit = speechunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_speechunit = speechunit_shop(exx.sue, 0, aux_knot=slash_iux_knot)
#     new_speechunit = speechunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_flare_audie():
#     # ESTABLISH
#     old_speechunit = speechunit_shop(exx.sue, 0)
#     new_speechunit = speechunit_shop(exx.bob, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
#     # ESTABLISH
#     old_speechunit = speechunit_shop(exx.sue, 5)
#     new_speechunit = speechunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert str(excinfo.value) == "older speechunit is not older"


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario6_nameyap_Inherited():
#     # ESTABLISH
#     spark1 = 1
#     old_speechunit = speechunit_shop(exx.sue, 0)
#     old_speechunit.set_nameyap(get_suita_nameyap())
#     old_speechunit.set_titleyap(get_bowl_titleyap())
#     old_speechunit.set_labelyap(get_clean_labelyap())
#     old_speechunit.set_ropeyap(get_clean_ropeyap())
#     new_speechunit = speechunit_shop(exx.sue, spark1)
#     assert new_speechunit.nameyap != get_suita_nameyap()

#     # WHEN
#     merged_speechunit = inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert merged_speechunit
#     merged_contactbridge = get_suita_nameyap()
#     merged_contactbridge.spark_num = spark1
#     assert merged_speechunit.nameyap == merged_contactbridge
#     merged_groupbridge = get_bowl_titleyap()
#     merged_groupbridge.spark_num = spark1
#     assert merged_speechunit.titleyap == merged_groupbridge
#     merged_labelbridge = get_clean_labelyap()
#     merged_labelbridge.spark_num = spark1
#     assert merged_speechunit.labelyap == merged_labelbridge
#     merged_ropebridge = get_clean_ropeyap()
#     merged_ropebridge.spark_num = spark1
#     merged_ropebridge.labelyap = merged_labelbridge
#     assert merged_speechunit.ropeyap == merged_ropebridge


# def test_SpeechUnit_inherit_speechunit_ReturnsObj_Scenario7_nameyap_Inherited():
#     # ESTABLISH
#     spark1 = 1
#     old_speechunit = speechunit_shop(exx.sue, 0)
#     old_speechunit.set_nameyap(get_suita_nameyap())
#     old_speechunit.set_titleyap(get_bowl_titleyap())
#     new_speechunit = speechunit_shop(exx.sue, spark1)
#     bob_iux = "Bob"
#     bob_aux = "Bobby"
#     new_speechunit.set_iux2aux(kw.NameTerm, bob_iux, bob_aux)
#     assert new_speechunit.nameyap != get_suita_nameyap()
#     assert new_speechunit.nameterm_exists(bob_iux, bob_aux)

#     # WHEN
#     merged_speechunit = inherit_speechunit(old_speechunit, new_speechunit)

#     # THEN
#     assert merged_speechunit
#     assert new_speechunit.nameterm_exists(bob_iux, bob_aux)
#     merged_contactbridge = get_suita_nameyap()
#     merged_contactbridge.spark_num = spark1
#     merged_contactbridge.set_iux2aux(bob_iux, bob_aux)
#     assert merged_speechunit.nameyap == merged_contactbridge
#     merged_groupbridge = get_bowl_titleyap()
#     merged_groupbridge.spark_num = spark1
#     assert merged_speechunit.titleyap == merged_groupbridge
