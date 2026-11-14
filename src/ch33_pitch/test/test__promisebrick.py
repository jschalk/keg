from ch00_py.file_toolbox import create_path, save_json
from ch20_brick.brick_config import get_brick_config_dict
from ch22_etl_config.etl_config import get_dimen_abbv7, get_etl_category_stages_dict
from ch23_idea_src.idea_config import get_idea_config_dict
from ch33_pitch.promisebrick_main import (
    get_promisebrick_config_dict,
    get_promisebrick_filename,
    promisebrick_config_path,
)
from ch99_glossary.ch_keyword import Ch33Keywords as kw


def test_get_promisebrick_filename_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_promisebrick_filename() == "promisebr_config.json"


def test_promisebrick_config_path_ReturnsObj_Promisebrick() -> str:
    # ESTABLISH / WHEN / THEN
    chapter_dir = create_path(kw.src, "ch33_pitch")
    expected_path = create_path(chapter_dir, get_promisebrick_filename())
    print(f"{promisebrick_config_path()=}")
    print(f"{expected_path=}")
    assert promisebrick_config_path() == expected_path


def test_get_promisebrick_config_dict_ReturnsObj():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH / WHEN
    promisebrick_config = get_promisebrick_config_dict()

    # THEN
    idea_config_dict = get_idea_config_dict()
    brick_config_dict = get_brick_config_dict()
    expected_config = {}
    for bc_key, bc_value in brick_config_dict.items():
        x_abbv7 = get_dimen_abbv7(bc_key)
        x_allowed_crud = bc_value.get("allowed_crud")
        expected_jkeys = {x_key: {} for x_key in bc_value.get(kw.jkeys).keys()}
        expected_jvalues = {x_key: {} for x_key in bc_value.get(kw.jvalues).keys()}
        # print(f"{expected_jkeys=}")
        # print(f"{expected_jvalues=}")
        # print(f"{bc_value.get(brick_category_str)=}")
        if x_allowed_crud in {"delete_insert", "delete_insert_update"}:
            expected_config[f"Prom{x_abbv7}_PutUnit"] = {
                kw.jkeys: expected_jkeys,
                kw.jvalues: expected_jvalues,
            }
            expected_config[f"Prom{x_abbv7}_DelUnit"] = {
                kw.jkeys: expected_jkeys,
                kw.jvalues: {},
            }
        else:
            expected_config[f"Prom{x_abbv7}_Unit"] = {
                kw.jkeys: expected_jkeys,
                kw.jvalues: expected_jvalues,
            }

    # To override currrent file
    # save_json(promisebrick_config_path(), None, expected_config)

    assert promisebrick_config.keys() == expected_config.keys()
    for pb_key, pb_val in promisebrick_config.items():
        expected_dict = expected_config.get(pb_key)
        expected_x_jkeys = expected_dict.get(kw.jkeys)
        expected_x_jvals = expected_dict.get(kw.jvalues)
        assertion_jkeys_fail_str = f"{pb_key} jkeys should have {expected_x_jkeys}"
        assertion_jvals_fail_str = f"{pb_key} jvalues should have {expected_x_jvals}"
        # if pb_val.get(kw.jkeys) != expected_x_jkeys:
        #     print(f""""jkeys": {expected_x_jkeys},""")
        assert pb_val.get(kw.jkeys) == expected_x_jkeys, assertion_jkeys_fail_str
        # if pb_val.get(kw.jvalues) != expected_x_jvals:
        #     print(f""""jvalues": {expected_x_jvals},""")
        assert pb_val.get(kw.jvalues) == expected_x_jvals, assertion_jvals_fail_str
        assert pb_val == expected_dict, "huh"
    assert promisebrick_config == expected_config


# TODO change the config from referencing brick source config to referencing ideas
# TODO create tests for all PromiseBrick classes
