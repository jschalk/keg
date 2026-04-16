from src.linter.style import find_matching_tests


def test_matches_any_function_name_with_same_scenario():
    tests = {
        "test_alpha_ReturnsObj_Scenario1_valid",
        "test_alpha_ReturnsObj_Scenario1_invalid",
        "test_beta_ReturnsObj_Scenario1_valid",  # different func → ignore
        "test_alpha_ReturnsObj_Scenario2_valid",  # single → ignore
    }

    result = find_matching_tests(tests)

    assert set(result) == {
        "test_alpha_ReturnsObj_Scenario1_valid",
        "test_alpha_ReturnsObj_Scenario1_invalid",
    }


def test_separates_different_functions_same_scenario():
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }

    result = find_matching_tests(tests)

    assert set(result) == {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }


def test_ignores_non_returnsobj_tests():
    tests = {
        "test_alpha_Scenario1_a",
        "test_alpha_Scenario1_b",
    }

    result = find_matching_tests(tests)

    assert result == []


def test_ignores_missing_scenario():
    tests = {
        "test_alpha_ReturnsObj_valid",
        "test_alpha_ReturnsObj_invalid",
    }

    result = find_matching_tests(tests)

    assert result == []


def test_requires_duplicates_per_function_and_scenario():
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_a",
    }

    result = find_matching_tests(tests)

    assert result == []


def test_multiple_valid_groups():
    tests = {
        "test_alpha_ReturnsObj_Scenario1_a",
        "test_alpha_ReturnsObj_Scenario1_b",
        "test_alpha_ReturnsObj_Scenario2_a",
        "test_alpha_ReturnsObj_Scenario2_b",
        "test_beta_ReturnsObj_Scenario1_a",
        "test_beta_ReturnsObj_Scenario1_b",
    }

    result = find_matching_tests(tests)

    assert set(result) == tests
