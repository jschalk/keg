from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import save_json
from src.ch07_person_logic.person_main import personunit_shop
from src.ch09_person_lesson._ref.ch09_path import create_moment_json_path
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_gut_file, save_gut_file
from src.ch13_time.epoch_main import epochunit_shop
from src.ch13_time.test._util.ch13_examples import get_five_config
from src.ch14_moment.moment_main import momentunit_shop
from src.ch19_etl_main.etl_main import add_moment_epoch_to_guts
from src.ref.keywords import Ch19Keywords as kw, ExampleStrs as exx


def test_add_moment_epoch_to_guts_SetsFiles_Scenario0(temp3_fs):
    # ESTABLISH
    moment_mstr_dir = str(temp3_fs)
    a23_lasso = lassounit_shop(exx.a23)
    a23_moment = momentunit_shop(exx.a23, moment_mstr_dir)
    a23_moment.epoch = epochunit_shop(get_five_config())
    moment_json_path = create_moment_json_path(moment_mstr_dir, a23_lasso)
    save_json(moment_json_path, None, a23_moment.to_dict())
    assert os_path_exists(moment_json_path)
    init_sue_gut = personunit_shop(exx.sue, exx.a23)
    time_rope = init_sue_gut.make_l1_rope(kw.time)
    five_rope = init_sue_gut.make_rope(time_rope, kw.five)
    save_gut_file(moment_mstr_dir, init_sue_gut)
    assert not init_sue_gut.plan_exists(five_rope)

    # WHEN
    add_moment_epoch_to_guts(moment_mstr_dir)

    # THEN
    post_sue_gut = open_gut_file(moment_mstr_dir, a23_lasso, exx.sue)
    assert post_sue_gut.plan_exists(five_rope)
