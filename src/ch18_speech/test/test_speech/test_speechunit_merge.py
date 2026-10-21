# from ch17_jargon.test._util.ch17_examples import (
#     get_bowl_titleyap,
#     get_clean_labelyap,
#     get_clean_ropeyap,
#     get_suita_nameyap,
# )
# from ch17_jargon.jargon_main import inherit_jargonunit, jargonunit_shop
# from ch99_glossary.ch_keyword import Ch17Keywords as kw, ExampleStrs as exx
# from pytest import raises as pytest_raises


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario0_EmptyJargonUnits():
#     # ESTABLISH
#     old_jargonunit = jargonunit_shop(exx.sue, 0)
#     new_jargonunit = jargonunit_shop(exx.sue, 1)

#     # WHEN
#     merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert merged_jargonunit
#     assert merged_jargonunit == new_jargonunit


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario1_RaiseErrorWhenDifferent_iux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_jargonunit = jargonunit_shop(exx.sue, 0, iux_knot=slash_iux_knot)
#     new_jargonunit = jargonunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario2_RaiseErrorWhenDifferent_aux_knot():
#     # ESTABLISH
#     slash_iux_knot = "/"
#     old_jargonunit = jargonunit_shop(exx.sue, 0, aux_knot=slash_iux_knot)
#     new_jargonunit = jargonunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario3_RaiseErrorWhenDifferent_x_unknown_str():
#     # ESTABLISH
#     x_unknown_str = "UnknownTerm"
#     old_jargonunit = jargonunit_shop(exx.sue, 0, unknown_str=x_unknown_str)
#     new_jargonunit = jargonunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario4_RaiseErrorWhenDifferent_x_spark_face():
#     # ESTABLISH
#     old_jargonunit = jargonunit_shop(exx.sue, 0)
#     new_jargonunit = jargonunit_shop(exx.bob, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert str(excinfo.value) == "Core attrs in conflict"


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario5_RaiseErrorWhenSparkIntsOutOfOrder():
#     # ESTABLISH
#     old_jargonunit = jargonunit_shop(exx.sue, 5)
#     new_jargonunit = jargonunit_shop(exx.sue, 1)

#     # WHEN
#     with pytest_raises(Exception) as excinfo:
#         inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert str(excinfo.value) == "older jargonunit is not older"


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario6_nameyap_Inherited():
#     # ESTABLISH
#     spark1 = 1
#     old_jargonunit = jargonunit_shop(exx.sue, 0)
#     old_jargonunit.set_nameyap(get_suita_nameyap())
#     old_jargonunit.set_titleyap(get_bowl_titleyap())
#     old_jargonunit.set_labelyap(get_clean_labelyap())
#     old_jargonunit.set_ropeyap(get_clean_ropeyap())
#     new_jargonunit = jargonunit_shop(exx.sue, spark1)
#     assert new_jargonunit.nameyap != get_suita_nameyap()

#     # WHEN
#     merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert merged_jargonunit
#     merged_contactbridge = get_suita_nameyap()
#     merged_contactbridge.spark_num = spark1
#     assert merged_jargonunit.nameyap == merged_contactbridge
#     merged_groupbridge = get_bowl_titleyap()
#     merged_groupbridge.spark_num = spark1
#     assert merged_jargonunit.titleyap == merged_groupbridge
#     merged_labelbridge = get_clean_labelyap()
#     merged_labelbridge.spark_num = spark1
#     assert merged_jargonunit.labelyap == merged_labelbridge
#     merged_ropebridge = get_clean_ropeyap()
#     merged_ropebridge.spark_num = spark1
#     merged_ropebridge.labelyap = merged_labelbridge
#     assert merged_jargonunit.ropeyap == merged_ropebridge


# def test_JargonUnit_inherit_jargonunit_ReturnsObj_Scenario7_nameyap_Inherited():
#     # ESTABLISH
#     spark1 = 1
#     old_jargonunit = jargonunit_shop(exx.sue, 0)
#     old_jargonunit.set_nameyap(get_suita_nameyap())
#     old_jargonunit.set_titleyap(get_bowl_titleyap())
#     new_jargonunit = jargonunit_shop(exx.sue, spark1)
#     bob_iux = "Bob"
#     bob_aux = "Bobby"
#     new_jargonunit.set_iux2aux(kw.NameTerm, bob_iux, bob_aux)
#     assert new_jargonunit.nameyap != get_suita_nameyap()
#     assert new_jargonunit.nameterm_exists(bob_iux, bob_aux)

#     # WHEN
#     merged_jargonunit = inherit_jargonunit(old_jargonunit, new_jargonunit)

#     # THEN
#     assert merged_jargonunit
#     assert new_jargonunit.nameterm_exists(bob_iux, bob_aux)
#     merged_contactbridge = get_suita_nameyap()
#     merged_contactbridge.spark_num = spark1
#     merged_contactbridge.set_iux2aux(bob_iux, bob_aux)
#     assert merged_jargonunit.nameyap == merged_contactbridge
#     merged_groupbridge = get_bowl_titleyap()
#     merged_groupbridge.spark_num = spark1
#     assert merged_jargonunit.titleyap == merged_groupbridge
