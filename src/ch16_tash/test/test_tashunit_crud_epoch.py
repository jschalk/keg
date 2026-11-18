# from ch16_tash.map_epoch import timetash_shop
# from ch99_glossary.keywords import ExampleStrs as exx


# def test_TashUnit_set_timetash_SetsAttr():
#     # ESTABLISH
#     sue_otx_epoch_length = None
#     sue_inx_epoch_diff = 6
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_timetash = timetash_shop(exx.sue, 0)
#     sue_timetash.set_otx2inx(sue_otx_epoch_length, sue_inx_epoch_diff)
#     assert sue_tashunit.timetash != sue_timetash

#     # WHEN
#     sue_tashunit.set_timetash(sue_timetash)

#     # THEN
#     assert sue_tashunit.timetash == sue_timetash


# def test_TashUnit_get_timetash_ReturnsObj():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_otx_time = 9
#     sue_inx_time = 6
#     sue_epoch_diff = sue_otx_time - sue_inx_time
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_timetash = timetash_shop(exx.sue, sue_spark_num, otx2inx)
#     sue_tashunit.set_timetash(static_sue_timetash)

#     # WHEN
#     gen_x_timetash = sue_tashunit.get_timetash()

#     # THEN
#     assert gen_x_timetash == static_sue_timetash


# def test_TashUnit_get_inx_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_spark_num = 31
#     sue_epoch_diff = 10
#     otx2inx = {None: sue_epoch_diff}
#     static_sue_timetash = timetash_shop(exx.sue, sue_spark_num, otx2inx)
#     assert sue_tashunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_tashunit.set_timetash(static_sue_timetash)

#     # THEN
#     assert sue_tashunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_TashUnit_set_epoch_SetsAttr():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_tashunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_tashunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_tashunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_TashUnit_epoch_exists_ReturnsObj():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert not sue_tashunit.epoch_exists(None)

#     # WHEN
#     sue_tashunit.set_epoch(None, sue_epoch_diff)

#     # THEN
#     assert sue_tashunit.epoch_exists(None)


# def test_TashUnit_del_epoch_ReturnsObj():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch1_length = 111
#     sue_epoch1_diff = 11
#     sue_epoch2_length = 222
#     sue_epoch2_diff = 22
#     sue_tashunit.set_epoch(sue_epoch1_length, sue_epoch1_diff)
#     sue_tashunit.set_epoch(sue_epoch2_length, sue_epoch2_diff)
#     assert sue_tashunit.epoch_exists(sue_epoch1_length)
#     assert sue_tashunit.epoch_exists(sue_epoch2_length)

#     # WHEN
#     sue_tashunit.del_epoch(sue_epoch1_length)

#     # THEN
#     assert not sue_tashunit.epoch_exists(sue_epoch1_length)
#     assert sue_tashunit.epoch_exists(sue_epoch2_length)


# from other file

# def test_TashUnit_set_otx2inx_SetsAttr_Scenario3_TimeNum():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch_diff = 10
#     assert sue_tashunit._get_otx_epoch_diff(None) is None

#     # WHEN
#     sue_tashunit.set_otx2inx(kw.TimeNum, None, sue_epoch_diff)

#     # THEN
#     assert sue_tashunit._get_otx_epoch_diff(None) == sue_epoch_diff


# def test_TashUnit_otx2inx_exists_ReturnsObj_Scenario1_TimeNum():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch0_diff)
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch1_diff)

#     # WHEN
#     sue_tashunit.set_otx2inx(kw.TimeNum, None, sue_epoch0_diff)

#     # THEN
#     assert sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch0_diff)
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch1_diff)


# def test_TashUnit_get_inx_value_ReturnsObj_Scenario1_EpochTerm():
#     # ESTABLISH
#     sue_epoch_diff = 10
#     sue_tashunit = tashunit_shop(exx.sue)
#     assert sue_tashunit.get_inx_value(kw.TimeNum, None) != sue_epoch_diff

#     # WHEN
#     sue_tashunit.set_otx2inx(kw.TimeNum, None, sue_epoch_diff)

#     # THEN
#     assert sue_tashunit.get_inx_value(kw.TimeNum, None) == sue_epoch_diff


# def test_TashUnit_del_otx2inx_ReturnsObj_Scenario1_TimeNum():
#     # ESTABLISH
#     sue_tashunit = tashunit_shop(exx.sue)
#     sue_epoch0_diff = 10
#     sue_epoch1_diff = 11
#     sue_tashunit.set_otx2inx(kw.TimeNum, None, sue_epoch0_diff)
#     assert sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch0_diff)
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch1_diff)

#     # WHEN
#     sue_tashunit.del_otx2inx(kw.TimeNum, None)

#     # THEN
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch0_diff)
#     assert not sue_tashunit.otx2inx_exists(kw.TimeNum, None, sue_epoch1_diff)
