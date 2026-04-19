from ch00_py.plotly_toolbox import conditional_fig_show
from ch14_moment.moment_report import (
    get_moment_guts_agenda_dataframe,
    get_moment_guts_agenda_plotly_fig,
    get_moment_guts_contacts_dataframe,
    get_moment_guts_contacts_plotly_fig,
    get_moment_jobs_agenda_dataframe,
    get_moment_jobs_agenda_plotly_fig,
    get_moment_jobs_contacts_dataframe,
    get_moment_jobs_contacts_plotly_fig,
)
from ch14_moment.test._util.ch14_examples import (
    create_example_moment2,
    create_example_moment3,
    create_example_moment4,
)
from ref.keywords import Ch14Keywords as kw, ExampleStrs as exx


def test_get_moment_guts_contacts_dataframe_ReturnsObj(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment2(str(temp3_fs))

    # WHEN
    x_df = get_moment_guts_contacts_dataframe(amy_moment)

    # THEN
    contactunit_colums = {
        kw.person_name,
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
        kw.memberships,
        kw.fund_give,
        kw.fund_take,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == contactunit_colums
    assert x_df.shape[0] == 8


def test_get_moment_guts_contacts_plotly_fig_DisplaysInfo(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment2(str(temp3_fs))

    # WHEN
    x_fig = get_moment_guts_contacts_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_jobs_contacts_dataframe_ReturnsObj(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment2(str(temp3_fs))
    amy_moment.generate_all_jobs()

    # WHEN
    x_df = get_moment_jobs_contacts_dataframe(amy_moment)

    # THEN
    contactunit_colums = {
        kw.person_name,
        kw.contact_name,
        kw.contact_cred_lumen,
        kw.contact_debt_lumen,
        kw.memberships,
        kw.fund_give,
        kw.fund_take,
        kw.fund_agenda_give,
        kw.fund_agenda_take,
        kw.fund_agenda_ratio_give,
        kw.fund_agenda_ratio_take,
        kw.inallocable_contact_debt_lumen,
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert x_df.shape[0] == 8
    assert set(x_df.columns) == contactunit_colums


def test_get_moment_jobs_contacts_plotly_fig_DisplaysInfo(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment2(str(temp3_fs))
    amy_moment.generate_all_jobs()

    # WHEN
    x_fig = get_moment_jobs_contacts_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_guts_agenda_dataframe_ReturnsObj(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment3(str(temp3_fs))

    # WHEN
    x_df = get_moment_guts_agenda_dataframe(amy_moment)

    # THEN
    agenda_colums = {
        kw.person_name,
        kw.fund_ratio,
        kw.plan_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] == 8


def test_get_moment_guts_agenda_plotly_fig_DisplaysInfo(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment3(str(temp3_fs))

    # WHEN
    x_fig = get_moment_guts_agenda_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)


def test_get_moment_jobs_agenda_dataframe_ReturnsObj(temp3_fs):
    # ESTABLISH
    amy_moment = create_example_moment4(str(temp3_fs))
    amy_moment.generate_all_jobs()

    # WHEN
    x_df = get_moment_jobs_agenda_dataframe(amy_moment)

    # THEN
    agenda_colums = {
        kw.person_name,
        kw.fund_ratio,
        kw.plan_label,
        kw.parent_rope,
        kw.begin,
        kw.close,
        kw.addin,
        kw.denom,
        kw.numor,
        kw.morph,
    }
    print(f"{set(x_df.columns)=}")
    print(x_df)

    assert set(x_df.columns) == agenda_colums
    assert x_df.shape[0] in [8, 9]


def test_get_moment_jobs_agenda_plotly_fig_DisplaysInfo(temp3_fs, graphics_bool):
    # ESTABLISH
    amy_moment = create_example_moment4(str(temp3_fs))
    amy_moment.generate_all_jobs()

    # WHEN
    x_fig = get_moment_jobs_agenda_plotly_fig(amy_moment)

    # THEN
    conditional_fig_show(x_fig, graphics_bool)
