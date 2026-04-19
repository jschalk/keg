from ch07_person_logic.person_main import personunit_shop
from ch09_person_lesson.lasso import lassounit_shop
from ch09_person_lesson.lesson_filehandler import open_gut_file, save_gut_file
from ch13_time.epoch_main import epochunit_shop, get_default_epoch_config_dict
from ch13_time.test._util.ch13_examples import get_five_config
from ch14_moment.moment_main import momentunit_shop
from ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_MomentUnit_get_epoch_config_ReturnsObj_Scenario0(temp3_dir):
    # ESTABLISH
    moment_mstr_dir = temp3_dir
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)

    # WHEN
    a23_epoch_config = a23_moment.get_epoch_config()

    # THEN
    assert a23_epoch_config == a23_moment.epoch.to_dict()
    assert a23_epoch_config == get_default_epoch_config_dict()
    assert a23_epoch_config.get(kw.epoch_label) == "creg"


def test_MomentUnit_get_epoch_config_ReturnsObj_Scenario1(temp3_dir):
    # ESTABLISH
    moment_mstr_dir = temp3_dir
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())

    # WHEN
    a23_epoch_config = a23_moment.get_epoch_config()

    # THEN
    assert a23_epoch_config == a23_moment.epoch.to_dict()
    assert a23_epoch_config == get_five_config()
    assert a23_epoch_config.get(kw.epoch_label) == "five"


def test_MomentUnit_add_epoch_to_gut_SetsFile_Scenario0(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    init_sue_gut = personunit_shop(exx.sue, exx.a23)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_epoch_to_gut(exx.sue)

    # THEN
    a23_lasso = lassounit_shop(exx.a23)
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_lasso, exx.sue)
    assert post_sue_gut.plan_exists(five_rope)


def test_MomentUnit_add_epoch_to_guts_SetsFiles_Scenario0(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    init_sue_gut = personunit_shop(exx.sue, exx.a23)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    a23_moment.add_epoch_to_guts()

    # THEN
    a23_lasso = lassounit_shop(exx.a23)
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_lasso, exx.sue)
    assert post_sue_gut.plan_exists(five_rope)
