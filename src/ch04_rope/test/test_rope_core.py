from dataclasses import dataclass
from pytest import mark as pytest_mark, raises as pytest_raises
from src.ch04_rope._ref.ch04_semantic_types import default_knot_if_None
from src.ch04_rope.rope import (
    RopeTerm,
    all_ropes_between,
    create_rope,
    create_rope_from_labels,
    default_knot_if_None,
    find_replace_rope_key_dict,
    get_all_rope_labels,
    get_ancestor_ropes,
    get_default_rope,
    get_first_label_from_rope,
    get_forefather_ropes,
    get_parent_rope,
    get_tail_label,
    is_heir_rope,
    is_labelterm,
    is_sub_rope,
    rebuild_rope,
    remove_knot_ends,
    replace_knot,
    rope_is_valid_dir_path,
    to_rope,
    validate_labelterm,
)
from src.ref.keywords import ExampleStrs as exx


def test_get_default_rope_ReturnsObj_Scenario0_NoKnotTerm():
    # ESTABLISH
    x_knot = default_knot_if_None()

    # WHEN / THEN
    assert get_default_rope() == f"{x_knot}YY{x_knot}"


def test_get_default_rope_ReturnsObj_Scenario1_WithKnotTerm():
    # ESTABLISH
    x_knot = "/"
    assert x_knot != default_knot_if_None()

    # WHEN / THEN
    assert get_default_rope(x_knot) == f"{x_knot}YY{x_knot}"


def root_rope() -> str:
    return create_rope(get_default_rope())


def test_to_rope_ReturnsObj_WithDefault_knot():
    # ESTABLISH
    x_label = "run"
    x_knot = default_knot_if_None()

    # WHEN / THEN
    assert to_rope(x_label) == f"{x_knot}{x_label}{x_knot}"
    assert to_rope(f"{x_knot}{x_label}") == f"{x_knot}{x_label}{x_knot}"
    two_knot_in_front_one_back = f"{x_knot}{x_knot}{x_label}{x_knot}"
    assert to_rope(f"{x_knot}{x_knot}{x_label}") == two_knot_in_front_one_back
    assert to_rope(x_knot) == x_knot
    assert to_rope("", x_knot) == x_knot
    assert to_rope(None) == x_knot


def test_to_rope_ReturnsObj_WithParameter_knot():
    # ESTABLISH
    x_label = "run"
    s_knot = "/"

    # WHEN / THEN
    assert to_rope(x_label, s_knot) == f"{s_knot}{x_label}{s_knot}"
    assert to_rope(f"{s_knot}{x_label}", s_knot) == f"{s_knot}{x_label}{s_knot}"
    assert (
        to_rope(f"{s_knot}{s_knot}{x_label}", s_knot)
        == f"{s_knot}{s_knot}{x_label}{s_knot}"
    )
    assert to_rope(s_knot, s_knot) == s_knot
    assert to_rope(None, s_knot) == s_knot


def test_create_rope_Scenario0_RaisesErrorIfKnotNotAtPostionZeroOf_parent_rope():
    # ESTABLISH
    tulip_str = "tulip"
    semicolon_knot = ";"
    knot_tulip_rope = f"{semicolon_knot}{tulip_str}"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_rope("YY", tulip_str, auto_add_first_knot=False) == knot_tulip_rope
    exception_str = (
        f"Parent rope must have knot '{semicolon_knot}' at position 0 in string"
    )
    assert str(excinfo.value) == exception_str


def test_create_rope_Scenario1_DoesNotRaiseError():
    # ESTABLISH
    tulip_str = "tulip"

    # WHEN / THEN
    assert create_rope("YY", tulip_str)


def test_create_rope_ReturnsObj_Scenario3():
    # ESTABLISH
    tulip_str = "tulip"
    semicolon_knot = ";"
    assert semicolon_knot == default_knot_if_None()
    semicolon_knot_tulip_rope = f"{root_rope()}{tulip_str}{semicolon_knot}"
    print(f"{semicolon_knot_tulip_rope=}")

    # WHEN / THEN
    assert create_rope(root_rope(), tulip_str) == semicolon_knot_tulip_rope


def test_create_rope_ReturnsObj_Scenario4():
    # ESTABLISH
    tulip_str = "tulip"
    slash_knot = "/"
    slash_knot_tulip_rope = (
        f"{slash_knot}{get_default_rope()}{slash_knot}{tulip_str}{slash_knot}"
    )

    # WHEN
    generated_tulip_rope = create_rope(get_default_rope(), tulip_str, knot=slash_knot)
    # THEN
    assert generated_tulip_rope == slash_knot_tulip_rope


def test_rope_create_rope_ReturnsObj_Scenario5():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_rope = f"{root_rope()}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}"
    tulips_str = "tulips"
    tulips_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}{tulips_str}{x_s}"

    # WHEN / THEN
    assert create_rope(None, "YY") == root_rope()
    assert create_rope("", "YY") == root_rope()
    assert create_rope(root_rope(), exx.casa) == casa_rope
    assert create_rope(casa_rope, bloomers_str) == bloomers_rope
    assert create_rope(bloomers_rope, tulips_str) == tulips_rope
    assert create_rope(tulips_rope, None) == tulips_rope


def test_rope_is_sub_rope_ReturnsObj_Scenario0_WhenNone_default_knot_if_None():
    # ESTABLISH / WHEN
    casa_rope = f"{root_rope()}{default_knot_if_None()}{exx.casa}"
    cleaning_str = "cleaning"
    cleaning_rope = f"{casa_rope}{default_knot_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    laundrys_rope = f"{cleaning_rope}{default_knot_if_None()}{laundrys_str}"
    print(f"{cleaning_rope=}")
    print(f"{laundrys_rope=}")

    # WHEN / THEN
    assert is_sub_rope(cleaning_rope, cleaning_rope)
    assert is_sub_rope(laundrys_rope, cleaning_rope)
    assert is_sub_rope(cleaning_rope, laundrys_rope) is False


def test_rope_is_sub_rope_ReturnsObj_Scenario1_WhenNone_default_knot_if_None():
    # ESTABLISH / WHEN
    casa_rope = f"{root_rope()}{exx.slash}{exx.casa}"
    cleaning_str = "cleaning"
    slash_cleaning_rope = f"{casa_rope}{exx.slash}{cleaning_str}"
    default_cleaning_rope = f"{casa_rope}{default_knot_if_None()}{cleaning_str}"
    laundrys_str = "laundrys"
    slash_laundrys_rope = f"{slash_cleaning_rope}{exx.slash}{laundrys_str}"
    default_laundrys_rope = f"{default_cleaning_rope}{exx.slash}{laundrys_str}"
    print(f"{slash_cleaning_rope=}")
    print(f"{slash_laundrys_rope=}")
    print(f"{default_cleaning_rope=}")
    print(f"{default_laundrys_rope=}")

    # WHEN / THEN
    assert is_sub_rope(slash_cleaning_rope, slash_cleaning_rope)
    assert is_sub_rope(slash_laundrys_rope, slash_cleaning_rope)
    assert is_sub_rope(slash_cleaning_rope, slash_laundrys_rope) is False
    assert is_sub_rope(slash_cleaning_rope, default_cleaning_rope) is False
    assert is_sub_rope(slash_laundrys_rope, default_cleaning_rope) is False
    assert is_sub_rope(slash_cleaning_rope, default_laundrys_rope) is False


def test_rope_rebuild_rope_ReturnsRopeTerm():
    # ESTABLISH
    casa_rope = create_rope(root_rope(), exx.casa)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    greenery_str = "greenery"
    greenery_rope = create_rope(casa_rope, greenery_str)
    tulips_str = "tulips"
    old_tulips_rope = create_rope(bloomers_rope, tulips_str)
    new_tulips_rope = create_rope(greenery_rope, tulips_str)

    print(f"{rebuild_rope(old_tulips_rope, bloomers_rope, greenery_rope)}")

    # WHEN / THEN
    assert rebuild_rope(bloomers_rope, bloomers_rope, bloomers_rope) == bloomers_rope
    assert (
        rebuild_rope(old_tulips_rope, bloomers_rope, greenery_rope) == new_tulips_rope
    )
    assert rebuild_rope(old_tulips_rope, "random_str", greenery_rope) == old_tulips_rope


def test_rope_get_all_rope_labels_ReturnsObj_Scenario0_KnotIsSingleCharacter():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_rope = f"{root_rope()}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}"
    tulips_str = "tulips"
    tulips_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}{tulips_str}{x_s}"

    # WHEN / THENs
    root_list = ["YY"]
    assert get_all_rope_labels(rope=root_rope()) == root_list
    casa_list = ["YY", exx.casa]
    assert get_all_rope_labels(rope=casa_rope) == casa_list
    bloomers_list = ["YY", exx.casa, bloomers_str]
    assert get_all_rope_labels(rope=bloomers_rope) == bloomers_list
    tulips_list = ["YY", exx.casa, bloomers_str, tulips_str]
    assert get_all_rope_labels(rope=tulips_rope) == tulips_list


def test_rope_get_all_rope_labels_ReturnsObj_Scenario1_KnotIsLongerThanSingleCharacter():
    # ESTABLISH
    knot = "&&%"
    assert len(knot) > 1
    bloomers_str = "bloomers"
    tulips_str = "tulips"

    # WHEN / THENs
    s1_rope = f"{knot}{exx.casa}{knot}"
    assert get_all_rope_labels(s1_rope, knot) == [exx.casa]
    s2_rope = f"{knot}{exx.casa}{knot}{bloomers_str}{knot}"
    assert get_all_rope_labels(s2_rope, knot) == [exx.casa, bloomers_str]
    s3_rope = f"{knot}{exx.casa}{knot}{bloomers_str}{knot}{tulips_str}{knot}"
    assert get_all_rope_labels(s3_rope, knot) == [exx.casa, bloomers_str, tulips_str]


def test_rope_get_tail_label_ReturnsLabelTerm():
    # ESTABLISH
    x_s = default_knot_if_None()
    casa_rope = f"{root_rope()}{x_s}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{x_s}{bloomers_str}{x_s}"
    tulips_str = "tulips"
    tulips_rope = f"{bloomers_rope}{x_s}{tulips_str}{x_s}"

    # WHEN / THENs
    assert get_tail_label(rope=root_rope()) == "YY"
    assert get_tail_label(rope=casa_rope) == exx.casa
    assert get_tail_label(rope=bloomers_rope) == bloomers_str
    assert get_tail_label(rope=tulips_rope) == tulips_str
    assert get_tail_label(rope="") == ""


def test_rope_get_tail_label_ReturnsLabelTermWhenNonDefaultknot():
    # ESTABLISH
    bloomers_str = "bloomers"
    tulips_str = "tulips"
    slash_casa_rope = f"{exx.slash}{"YY"}{exx.slash}{exx.casa}{exx.slash}"
    slash_bloomers_rope = f"{slash_casa_rope}{bloomers_str}{exx.slash}"
    slash_tulips_rope = f"{slash_bloomers_rope}{tulips_str}{exx.slash}"

    # WHEN / THENs
    assert get_tail_label(slash_casa_rope, exx.slash) == exx.casa
    assert get_tail_label(slash_bloomers_rope, exx.slash) == bloomers_str
    assert get_tail_label(slash_tulips_rope, exx.slash) == tulips_str


def test_rope_get_first_label_from_rope_ReturnsLabelTerm():
    # ESTABLISH
    casa_rope = create_rope(root_rope(), exx.casa)
    bloomers_str = "bloomers"
    bloomers_rope = create_rope(casa_rope, bloomers_str)
    tulips_str = "tulips"
    tulips_rope = create_rope(exx.casa, tulips_str)

    # WHEN / THENs
    assert get_first_label_from_rope(root_rope()) == "YY"
    assert get_first_label_from_rope(casa_rope) == "YY"
    assert get_first_label_from_rope(bloomers_rope) == "YY"
    assert get_first_label_from_rope(tulips_rope) == exx.casa


def test_rope_get_parent_rope_ReturnsObj_Scenario0():
    # ESTABLISH
    x_s = default_knot_if_None()
    expected_root_rope = f"{x_s}{"YY"}{x_s}"
    casa_rope = f"{expected_root_rope}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{bloomers_str}{x_s}"
    tulips_str = "tulips"
    tulips_rope = f"{bloomers_rope}{tulips_str}{x_s}"

    # WHEN / THENs
    assert get_parent_rope(root_rope(), x_s) == ""
    assert get_parent_rope(casa_rope, x_s) == expected_root_rope
    assert get_parent_rope(bloomers_rope, x_s) == casa_rope
    assert get_parent_rope(tulips_rope, x_s) == bloomers_rope


def test_rope_get_parent_rope_ReturnsObj_Scenario1():
    # ESTABLISH
    x_s = "/"
    expected_root_rope = f"{x_s}{"YY"}{x_s}"
    casa_rope = f"{expected_root_rope}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{casa_rope}{bloomers_str}{x_s}"
    tulips_str = "tulips"
    tulips_rope = f"{bloomers_rope}{tulips_str}{x_s}"

    # WHEN / THENs
    assert get_parent_rope(expected_root_rope, x_s) == ""
    assert get_parent_rope(casa_rope, x_s) == expected_root_rope
    assert get_parent_rope(bloomers_rope, x_s) == casa_rope
    assert get_parent_rope(tulips_rope, x_s) == bloomers_rope


@dataclass
class TempFindReplaceRopeObj:
    x_rope: RopeTerm = ""

    def find_replace_rope(self, old_rope, new_rope):
        self.x_rope = rebuild_rope(self.x_rope, old_rope=old_rope, new_rope=new_rope)

    def get_obj_key(self) -> RopeTerm:
        return self.x_rope


def test_rope_find_replace_rope_key_dict_ReturnsDict_Scenario1():
    # ESTABLISH
    x_s = default_knot_if_None()
    old_seasons_rope = f"{root_rope()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_rope: TempFindReplaceRopeObj(old_seasons_rope)}
    assert old_dict_x.get(old_seasons_rope) is not None

    # WHEN
    new_seasons_rope = f"{root_rope()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_rope_key_dict(
        dict_x=old_dict_x, old_rope=old_seasons_rope, new_rope=new_seasons_rope
    )

    # THEN
    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_rope) is not None
    assert new_dict_x.get(old_seasons_rope) is None


def test_rope_get_ancestor_ropes_ReturnsObj_Scenario0_default_knot():
    # ESTABLISH
    x_s = default_knot_if_None()
    nation_str = "nation"
    nation_rope = f"{root_rope()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    texas_anc_ropes = get_ancestor_ropes(rope=texas_rope)

    # THEN
    print(f"     {texas_rope=}")
    print(f"{texas_anc_ropes=}")
    assert texas_anc_ropes is not None
    texas_ancestor_ropes = [
        texas_rope,
        usa_rope,
        nation_rope,
        root_rope(),
    ]
    assert texas_anc_ropes == texas_ancestor_ropes

    # WHEN
    assert get_ancestor_ropes(None) == []
    assert get_ancestor_ropes("") == []
    assert get_ancestor_ropes(root_rope()) == [root_rope()]


def test_rope_get_ancestor_ropes_ReturnsObj_Scenario1_nondefault_knot():
    # ESTABLISH
    x_s = "/"
    expected_root_rope = f"{x_s}amy23{x_s}"
    nation_str = "nation"
    nation_rope = f"{expected_root_rope}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    texas_anc_ropes = get_ancestor_ropes(rope=texas_rope, knot=x_s)

    # THEN
    print(f"     {texas_rope=}")
    print(f"{texas_anc_ropes=}")
    assert texas_anc_ropes is not None
    texas_ancestor_ropes = [
        texas_rope,
        usa_rope,
        nation_rope,
        expected_root_rope,
    ]
    assert texas_anc_ropes == texas_ancestor_ropes


def test_rope_get_forefather_ropes_ReturnsAncestorRopeTermsWithoutClean():
    # ESTABLISH
    x_s = default_knot_if_None()
    nation_str = "nation"
    nation_rope = f"{root_rope()}{nation_str}{x_s}"
    usa_str = "USA"
    usa_rope = f"{nation_rope}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"

    # WHEN
    x_ropes = get_forefather_ropes(rope=texas_rope)

    # THEN
    print(f"{texas_rope=}")
    assert x_ropes is not None
    texas_forefather_ropes = {
        nation_rope: None,
        usa_rope: None,
        root_rope(): None,
    }
    assert x_ropes == texas_forefather_ropes


def test_rope_create_rope_from_labels_ReturnsObj():
    # ESTABLISH
    x_s = default_knot_if_None()
    root_list = get_all_rope_labels(root_rope())
    casa_rope = f"{root_rope()}{exx.casa}{x_s}"
    casa_list = get_all_rope_labels(casa_rope)
    bloomers_str = "bloomers"
    bloomers_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}"
    bloomers_list = get_all_rope_labels(bloomers_rope)
    tulips_str = "tulips"
    tulips_rope = f"{root_rope()}{exx.casa}{x_s}{bloomers_str}{x_s}{tulips_str}{x_s}"
    tulips_list = get_all_rope_labels(tulips_rope)

    # WHEN / THEN
    assert root_rope() == create_rope_from_labels(root_list)
    assert casa_rope == create_rope_from_labels(casa_list)
    assert bloomers_rope == create_rope_from_labels(bloomers_list)
    assert tulips_rope == create_rope_from_labels(tulips_list)


def test_is_labelterm_ReturnsObj():
    # ESTABLISH
    x_s = default_knot_if_None()

    # WHEN / THEN
    assert is_labelterm("", x_knot=x_s) is False
    assert is_labelterm("casa", x_knot=x_s)
    assert not is_labelterm(f"ZZ{x_s}casa", x_s)
    assert not is_labelterm(RopeTerm(f"ZZ{x_s}casa"), x_s)
    assert is_labelterm(RopeTerm("YY"), x_s)


def test_is_heir_rope_IdentifiesHeirs():
    # ESTABLISH
    x_s = default_knot_if_None()
    usa_str = "USA"
    usa_rope = f"{root_rope()}Nation-States{x_s}{usa_str}{x_s}"
    texas_str = "Texas"
    texas_rope = f"{usa_rope}{texas_str}{x_s}"
    # earth_str = "earth"
    # earth_rope = f"{earth_str}"
    # sea_str = "sea"
    # sea_rope = f"{earth_rope}{x_s}{sea_str}"
    # seaside_str = "seaside"
    # seaside_rope = f"{earth_rope}{x_s}{seaside_str}"

    # WHEN / THEN
    assert is_heir_rope(src=usa_rope, heir=usa_rope)
    assert is_heir_rope(src=usa_rope, heir=texas_rope)
    assert (
        is_heir_rope(f"earth{x_s}sea{x_s}", f"earth{x_s}seaside{x_s}beach{x_s}")
        is False
    )
    assert (
        is_heir_rope(src=f"earth{x_s}sea{x_s}", heir=f"earth{x_s}seaside{x_s}") is False
    )


def test_replace_knot_ReturnsNewObj():
    # ESTABLISH
    first_label = "YY"
    gen_casa_rope = create_rope(first_label, exx.casa)
    semicolon_knot = default_knot_if_None()
    semicolon_knot_casa_rope = (
        f"{semicolon_knot}{first_label}{semicolon_knot}{exx.casa}{semicolon_knot}"
    )
    assert semicolon_knot == ";"
    assert gen_casa_rope == semicolon_knot_casa_rope

    # WHEN
    slash_knot = "/"
    gen_casa_rope = replace_knot(
        gen_casa_rope, old_knot=semicolon_knot, new_knot=slash_knot
    )

    # THEN
    slash_knot_casa_rope = (
        f"{slash_knot}{first_label}{slash_knot}{exx.casa}{slash_knot}"
    )
    assert gen_casa_rope == slash_knot_casa_rope


def test_replace_knot_RaisesError():
    # ESTABLISH
    cleaner_str = "cuisine/cleaner"
    gen_cleaner_rope = create_rope(root_rope(), cleaner_str)
    semicolon_knot = default_knot_if_None()
    semicolon_knot_cleaner_rope = f"{root_rope()}{cleaner_str}{semicolon_knot}"
    assert semicolon_knot == ";"
    assert gen_cleaner_rope == semicolon_knot_cleaner_rope

    # WHEN / THEN
    slash_knot = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cleaner_rope = replace_knot(
            gen_cleaner_rope,
            old_knot=semicolon_knot,
            new_knot=slash_knot,
        )
    assertion_failure_str = f"Cannot replace_knot '{semicolon_knot}' with '{slash_knot}' because the new one exists in rope '{gen_cleaner_rope}'."
    assert str(excinfo.value) == assertion_failure_str


def test_replace_knot_WhenNewknotIsFirstInRopeTermRaisesError():
    # ESTABLISH
    cuisine_slash_str = "/cuisine"
    cleaner_str = "cleaner"
    semicolon_knot = default_knot_if_None()
    semicolon_knot_cleaner_rope = f"{cuisine_slash_str}{semicolon_knot}{cleaner_str}"
    assert semicolon_knot == ";"

    # WHEN / THEN
    slash_knot = "/"
    with pytest_raises(Exception) as excinfo:
        semicolon_knot_cleaner_rope = replace_knot(
            semicolon_knot_cleaner_rope,
            old_knot=semicolon_knot,
            new_knot=slash_knot,
        )
    assertion_failure_str = f"Cannot replace_knot '{semicolon_knot}' with '{slash_knot}' because the new one exists in rope '{semicolon_knot_cleaner_rope}'."
    assert str(excinfo.value) == assertion_failure_str


def test_validate_labelterm_Scenario0_RaisesErrorWhenNotLabelTerm():
    # ESTABLISH
    bob_str = "Bob, Tom"
    assert bob_str == validate_labelterm(bob_str, x_knot=exx.slash)

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        validate_labelterm(bob_str, x_knot=comma_str)

    # THEN
    assertion_failure_str = (
        f"'{bob_str}' must be a LabelTerm. Cannot contain knot: '{comma_str}'"
    )
    assert str(excinfo.value) == assertion_failure_str


def test_validate_labelterm_Scenario1_RaisesErrorWhenLabelTerm():
    # ESTABLISH
    bob_str = f"Bob{exx.slash}Tom"
    assert bob_str == validate_labelterm(
        bob_str, x_knot=exx.slash, ropeterm_required=True
    )

    # WHEN
    comma_str = ","
    with pytest_raises(Exception) as excinfo:
        validate_labelterm(bob_str, x_knot=comma_str, ropeterm_required=True)

    # THEN
    assertion_failure_str = (
        f"'{bob_str}' must not be a LabelTerm. Must contain knot: '{comma_str}'"
    )
    assert str(excinfo.value) == assertion_failure_str


@pytest_mark.skip_on_linux
def test_rope_is_valid_dir_path_ReturnsObj_Scenario0_simple_knot():
    # ESTABLISH
    comma_str = ","
    # WHEN / THEN
    assert rope_is_valid_dir_path(",run,", knot=comma_str)
    assert rope_is_valid_dir_path(",run,sport,", knot=comma_str)
    assert not rope_is_valid_dir_path("run,sport?,", comma_str)


@pytest_mark.skip_on_linux
def test_rope_is_valid_dir_path_ReturnsObj_Scenario1_complicated_knot():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run,"
    lap_str = "lap"
    sport_rope = create_rope(sport_str, knot=question_str)
    print(f"{sport_rope=}")
    run_rope = create_rope(sport_rope, run_str, knot=question_str)
    lap_rope = create_rope(run_rope, lap_str, knot=question_str)
    assert lap_rope == f"{sport_rope}{run_str}?{lap_str}?"

    # WHEN / THEN
    assert rope_is_valid_dir_path(sport_rope, knot=question_str)
    assert rope_is_valid_dir_path(run_rope, knot=question_str)
    assert rope_is_valid_dir_path(lap_rope, knot=question_str)
    assert rope_is_valid_dir_path(lap_rope, knot=",") is False


def test_rope_is_valid_dir_path_ReturnsObj_Scenario2_WhereSlashNotknotEdgeSituations():
    # ESTABLISH
    question_str = "?"
    sport_str = "sport"
    run_str = "run/bowl"
    lap_str = "lap"
    sport_rope = create_rope(sport_str, knot=question_str)
    run_rope = create_rope(sport_rope, run_str, knot=question_str)
    lap_rope = create_rope(run_rope, lap_str, knot=question_str)
    assert lap_rope == f"{sport_rope}{run_str}?{lap_str}?"

    # WHEN / THEN
    assert rope_is_valid_dir_path(sport_rope, knot=question_str)
    assert rope_is_valid_dir_path(run_rope, knot=question_str) is False
    assert rope_is_valid_dir_path(lap_rope, knot=question_str) is False
    assert rope_is_valid_dir_path(lap_rope, knot=",") is False


def test_all_ropes_between_ReturnsObj_Scenario0_Default_knot():
    # ESTABLISH
    sport_str = "sport"
    run_str = "run/bowl"
    lap_str = "lap"
    sport_rope = create_rope(exx.casa, sport_str)
    run_rope = create_rope(sport_rope, run_str)
    lap_rope = create_rope(run_rope, lap_str)

    # WHEN / THEN
    assert all_ropes_between(sport_rope, sport_rope) == [sport_rope]
    assert all_ropes_between(sport_rope, run_rope) == [sport_rope, run_rope]
    assert all_ropes_between(sport_rope, lap_rope) == [
        sport_rope,
        run_rope,
        lap_rope,
    ]


def test_all_ropes_between_ReturnsObj_Scenario1_NonDefault_knot():
    # ESTABLISH
    sport_str = "sport"
    run_str = "run,bowl"
    lap_str = "lap"
    sport_rope = create_rope(exx.casa, sport_str, knot=exx.slash)
    run_rope = create_rope(sport_rope, run_str, knot=exx.slash)
    lap_rope = create_rope(run_rope, lap_str, knot=exx.slash)

    # WHEN / THEN
    assert all_ropes_between(sport_rope, sport_rope, exx.slash) == [sport_rope]
    assert all_ropes_between(sport_rope, run_rope, exx.slash) == [
        sport_rope,
        run_rope,
    ]
    assert all_ropes_between(sport_rope, lap_rope, exx.slash) == [
        sport_rope,
        run_rope,
        lap_rope,
    ]


def test_remove_knot_ends_ReturnsObj():
    # ESTABLISH
    x_s = default_knot_if_None()
    root_str = "root"
    root_rode = to_rope(root_str, x_s)
    casa_rope = f"{x_s}{root_rope()}{x_s}{exx.casa}{x_s}"
    bloomers_str = "bloomers"
    bloomers_rope = f"{exx.casa}{x_s}{bloomers_str}{x_s}"

    # WHEN / THENs
    assert remove_knot_ends(root_str, x_s) == root_str
    assert remove_knot_ends(root_rode, x_s) == root_str
    assert remove_knot_ends(casa_rope, x_s) == f"{root_rope()}{x_s}{exx.casa}"
    assert remove_knot_ends(bloomers_rope, x_s) == f"{exx.casa}{x_s}{bloomers_str}"
    assert remove_knot_ends(x_rope="", knot=x_s) == ""
