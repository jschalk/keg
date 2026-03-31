from os.path import exists as os_path_exists
from src.ch00_py.file_toolbox import delete_dir
from src.ch10_person_listen._ref.ch10_path import create_keep_grade_path
from src.ch12_keep.riverrun import riverrun_shop
from src.ch12_keep.test._util.ch12_examples import get_nation_texas_rope
from src.ref.keywords import ExampleStrs as exx


def test_RiverRun_save_rivergrade_file_SavesFile(temp3_fs):
    # ESTABLISH / WHEN
    mstr_dir = str(temp3_fs)
    texas_rope = get_nation_texas_rope()
    yao_partner_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao, texas_rope)
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    x_riverrun.set_need_dues({exx.yao: 1})
    x_riverrun.calc_metrics()
    yao_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        person_name=x_riverrun.person_name,
        moment_rope=x_riverrun.moment_rope,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_person_name=exx.yao,
    )
    print(f"{yao_keep_grade_path=}")
    assert os_path_exists(yao_keep_grade_path) is False

    # WHEN
    x_riverrun._save_rivergrade_file(exx.yao)

    # THEN
    assert os_path_exists(yao_keep_grade_path)


def test_RiverRun_save_rivergrade_files_SavesFile(temp3_fs):
    # ESTABLISH / WHEN
    delete_dir(str(temp3_fs))
    github_error_path1 = "src\\ch12_keep\\test\\_util\\moment_mstr\\moments/moments/ex_keep04/persons/Yao/keeps/nation/usa/texas/grades/Yao.json"
    assert os_path_exists(github_error_path1) is False
    mstr_dir = str(temp3_fs)
    texas_rope = get_nation_texas_rope()
    yao_partner_cred_lumen = 500
    x_riverrun = riverrun_shop(mstr_dir, exx.a23, exx.yao, texas_rope)
    yao_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        person_name=x_riverrun.person_name,
        moment_rope=x_riverrun.moment_rope,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_person_name=exx.yao,
    )
    bob_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        person_name=x_riverrun.person_name,
        moment_rope=x_riverrun.moment_rope,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_person_name=exx.bob,
    )
    sue_keep_grade_path = create_keep_grade_path(
        moment_mstr_dir=x_riverrun.moment_mstr_dir,
        person_name=x_riverrun.person_name,
        moment_rope=x_riverrun.moment_rope,
        keep_rope=x_riverrun.keep_rope,
        knot=x_riverrun.knot,
        grade_person_name=exx.sue,
    )
    x_riverrun.set_keep_patientledger(exx.yao, exx.yao, yao_partner_cred_lumen)
    x_riverrun.set_keep_patientledger(exx.yao, exx.bob, 1)
    x_riverrun.set_need_dues({exx.yao: 1, exx.sue: 1})
    x_riverrun.calc_metrics()
    assert os_path_exists(yao_keep_grade_path) is False
    assert os_path_exists(bob_keep_grade_path) is False
    assert os_path_exists(sue_keep_grade_path) is False

    # WHEN
    x_riverrun.save_rivergrade_files()

    # THEN
    assert os_path_exists(yao_keep_grade_path)
    assert os_path_exists(bob_keep_grade_path)
    # assert os_path_exists(x_riverrun.grade_path(exx.sue))
