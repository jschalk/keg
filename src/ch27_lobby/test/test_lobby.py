from ch27_lobby.lobby import LobbyUnit, lobbyunit_shop


def test_LobbyUnit_Exists():
    # ESTABLISH / WHEN
    x_lobbyunit = LobbyUnit()

    # THEN
    assert not x_lobbyunit.lobby_id
    assert not x_lobbyunit.option_lessons
    assert not x_lobbyunit.selected_lesson
    assert not x_lobbyunit.worlds


def test_lobbyunit_shop_ReturnsObj():
    # ESTABLISH
    d456_str = "d456"

    # WHEN
    d456_lobbyunit = lobbyunit_shop(d456_str)

    # THEN
    assert d456_lobbyunit.lobby_id
    assert not d456_lobbyunit.option_lessons
    assert not d456_lobbyunit.selected_lesson
    assert not d456_lobbyunit.worlds


# def test_LobbyUnit_CreateOptionLessons():
