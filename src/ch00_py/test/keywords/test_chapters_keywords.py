from src.ch00_py._ref.ch00_path import create_keywords_classes_file_path
from src.ch00_py.chapter_desc_main import (
    get_chapter_desc_prefix,
    get_chapter_desc_str_number,
    valid_chapter_numbers,
)
from src.ch00_py.file_toolbox import open_file, save_file
from src.ch00_py.keyword_class_builder import (
    create_all_enum_keyword_classes_str,
    create_examplestrs_class_str,
    create_keywords_enum_class_file_str,
    get_chapter_descs,
    get_cumlative_ch_keywords_dict,
    get_example_strs_config,
    get_keywords_by_chapter,
    get_keywords_src_config,
)


def test_get_chapter_desc_prefix_ReturnsObj():
    # ESTABLISH
    ch_str = "ch"
    # WHEN / THEN
    assert get_chapter_desc_prefix(f"{ch_str}03_") == f"{ch_str}03"
    assert get_chapter_desc_prefix(f"{ch_str}99") == f"{ch_str}99"
    assert get_chapter_desc_prefix(f"{ch_str}03") == f"{ch_str}03"
    assert get_chapter_desc_prefix(f"{ch_str}99") == f"{ch_str}99"
    assert get_chapter_desc_prefix(f"{ch_str}XX") == f"{ch_str}XX"
    assert get_chapter_desc_prefix(f"{ch_str}a01") != f"{ch_str}02"


def test_get_chapter_desc_str_number_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    ch_str = "ch"
    # WHEN / THEN
    assert get_chapter_desc_str_number(f"{ch_str}04") == "04"
    assert get_chapter_desc_str_number(f"{ch_str}99") == "99"
    assert get_chapter_desc_str_number("aXX") != "XX"
    assert get_chapter_desc_str_number("aa01") != "01"
    assert get_chapter_desc_str_number(f"{ch_str}03") == "03"
    assert get_chapter_desc_str_number(f"{ch_str}99") == "99"
    assert get_chapter_desc_str_number(f"{ch_str}XX") == "XX"
    assert get_chapter_desc_str_number(f"{ch_str}a01") != "01"


def test_get_example_strs_config_ReturnsObj():
    # ESTABLISH / WHEN
    example_strs_config = get_example_strs_config()

    # THEN
    assert example_strs_config
    for key_str, key_value in example_strs_config.items():
        assert type(key_str) == type("")
        assert type(key_value) == type("")


def test_get_keywords_src_config_ReturnsObj():
    # ESTABLISH / WHEN
    keywords_config = get_keywords_src_config()

    # THEN
    assert keywords_config
    req_config_keys = {"init_chapter", "semantic_type"}
    for keyword, ref_dict in keywords_config.items():
        ref_keys = set(ref_dict.keys())
        # print(f"{keyword=} {ref_dict=}")
        assert req_config_keys.issuperset(ref_keys), keyword
    example_strs_keys = set(get_example_strs_config().keys())
    keys_in_both = example_strs_keys.intersection(set(keywords_config.keys()))
    assert not keys_in_both


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario0_Empty_keyword_set():
    # ESTABLISH
    ch_str = "ch"
    ch_03_str = f"{ch_str}03"
    ch_03_keywords = {}

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch_03_str, ch_03_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch03{key_str}words(str, Enum):
    pass

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_create_keywords_enum_class_file_str_ReturnsObj_Scenario1_NonEmpty_keyword_set():
    # ESTABLISH
    ch_str = "ch"
    ch_03_str = f"{ch_str}03"
    keywordF = "Funny"
    keywordI = "INSET"
    keywordf = "funny"
    keywordG = "Guppies"
    keywordH = "Heath"
    keywordR = "Risto"
    ch_03_keywords = {
        keywordF,
        keywordI,
        keywordf,
        keywordG,
        keywordH,
        keywordR,
    }

    # WHEN
    file_str = create_keywords_enum_class_file_str(ch_03_str, ch_03_keywords)

    # THEN
    assert file_str
    key_str = "Key"
    expected_file_str = f"""

class Ch03{key_str}words(str, Enum):
    {keywordF} = "{keywordF}"
    {keywordG} = "{keywordG}"
    {keywordH} = "{keywordH}"
    {keywordI} = "{keywordI}"
    {keywordR} = "{keywordR}"
    {keywordf} = "{keywordf}"

    def __str__(self):
        return self.value
"""
    print(file_str)
    print(expected_file_str)
    assert file_str == expected_file_str


def test_create_examplestrs_class_str_ReturnsObj():
    # ESTABLISH
    example_strs_dict = {"sue": "Sue", "yao": "Yao", "bob": "Bob"}

    # WHEN
    x_str = create_examplestrs_class_str(example_strs_dict)

    # THEN
    expected_str = """class ExampleStrs(str, Enum):
    bob = "Bob"
    sue = "Sue"
    yao = "Yao"

    def __str__(self):
        return self.value"""
    assert x_str == expected_str


def test_create_all_enum_keyword_classes_str_ReturnsObj():
    # ESTABLISH
    examples_strs = get_example_strs_config()

    #  WHEN
    classes_str = create_all_enum_keyword_classes_str()

    # THEN
    keywords_by_chapter = get_keywords_by_chapter(get_keywords_src_config())
    cumlative_keywords = get_cumlative_ch_keywords_dict(keywords_by_chapter)
    expected_classes_str = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}
"""
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        ch_prefix = get_chapter_desc_prefix(chapter_desc)
        ch_keywords = cumlative_keywords.get(ch_prefix)
        enum_class_str = create_keywords_enum_class_file_str(ch_prefix, ch_keywords)
        expected_classes_str += enum_class_str
    assert expected_classes_str == classes_str
    two_line_spacing_str = f"""from enum import Enum


{create_examplestrs_class_str(examples_strs)}


class Ch00Key"""
    print(classes_str[:100])
    assert classes_str.find(two_line_spacing_str) == 0


def test_SpecialTestThatBuildsKeywordEnumClasses():
    # ESTABLISH
    chapter_descs = get_chapter_descs()
    assert valid_chapter_numbers(chapter_descs), chapter_descs.keys()
    # save file for all Enum class references
    keywords_classes_file_path = create_keywords_classes_file_path("src")
    enum_classes_str = create_all_enum_keyword_classes_str()
    current_classes_file_str = open_file(keywords_classes_file_path)
    # print(enum_classes_str[:100])
    print(
        "Create and save Enum classes, fail test if there are any changes so changes can apply to next test run. "
    )
    save_file(keywords_classes_file_path, None, enum_classes_str)

    # WHEN / THEN
    prev_and_curr_classes_file_are_same = enum_classes_str == current_classes_file_str
    assertion_failure_str = "Special case: keywords.py was changed. Run test again."
    assert prev_and_curr_classes_file_are_same, assertion_failure_str
