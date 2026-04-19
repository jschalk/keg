from ch13_time.epoch_main import get_first_weekday_index_of_year
from ch13_time.test._util.ch13_examples import get_creg_config, get_five_config
from ref.keywords import Ch13Keywords as kw, ExampleStrs as exx


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario0_creg_epoch_config():
    # ESTABLISH
    weekdays_config = get_creg_config().get(kw.weekdays_config)
    print(f"{weekdays_config=}")
    week_length = len(weekdays_config)

    # WHEN
    x2000_index = get_first_weekday_index_of_year(week_length, 2000)
    x2001_index = get_first_weekday_index_of_year(week_length, 2001)
    x2002_index = get_first_weekday_index_of_year(week_length, 2002)
    x2003_index = get_first_weekday_index_of_year(week_length, 2003)
    x2004_index = get_first_weekday_index_of_year(week_length, 2004)

    # THEN
    print(f"{weekdays_config[x2000_index]=}")
    print(f"{weekdays_config[x2001_index]=}")
    print(f"{weekdays_config[x2002_index]=}")
    print(f"{weekdays_config[x2003_index]=}")
    print(f"{weekdays_config[x2004_index]=}")

    assert weekdays_config[x2000_index] == exx.Wednesday
    assert weekdays_config[x2001_index] == exx.Thursday
    assert weekdays_config[x2002_index] == exx.Friday
    assert weekdays_config[x2003_index] == exx.Saturday
    assert weekdays_config[x2004_index] == exx.Monday


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario1_five_epoch_config():
    # ESTABLISH
    weekdays_config = get_five_config().get(kw.weekdays_config)
    print(f"{weekdays_config=}")
    week_length = len(weekdays_config)

    # WHEN
    x2000_index = get_first_weekday_index_of_year(week_length, 2000)
    x2001_index = get_first_weekday_index_of_year(week_length, 2001)
    x2002_index = get_first_weekday_index_of_year(week_length, 2002)
    x2003_index = get_first_weekday_index_of_year(week_length, 2003)
    x2004_index = get_first_weekday_index_of_year(week_length, 2004)

    # THEN
    print(f"{weekdays_config[x2000_index]=}")
    print(f"{weekdays_config[x2001_index]=}")
    print(f"{weekdays_config[x2002_index]=}")
    print(f"{weekdays_config[x2003_index]=}")
    print(f"{weekdays_config[x2004_index]=}")

    assert weekdays_config[x2000_index] == kw.Anaday
    assert weekdays_config[x2001_index] == kw.Anaday
    assert weekdays_config[x2002_index] == kw.Anaday
    assert weekdays_config[x2003_index] == kw.Anaday
    assert weekdays_config[x2004_index] == kw.Baileyday
