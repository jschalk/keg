from pandas import DataFrame, concat as pandas_concat
from plotly.graph_objects import Figure as plotly_Figure, Table as plotly_Table
from src.ch07_person_logic.person_report import (
    get_person_agenda_dataframe,
    get_person_partnerunits_dataframe,
)
from src.ch09_person_lesson.lasso import lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import open_gut_file
from src.ch10_person_listen.keep_tool import open_job_file
from src.ch14_moment.moment_main import MomentUnit


def get_moment_guts_partners_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all person paths
    moment_person_names = x_moment._get_person_dir_names()
    # for all persons get gut
    gut_dfs = []
    for person_name in moment_person_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope)
        gut_person = open_gut_file(x_moment.moment_mstr_dir, moment_lasso, person_name)
        gut_person.conpute()
        df = get_person_partnerunits_dataframe(gut_person)
        df.insert(0, "person_name", gut_person.person_name)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_partners_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "person_name",
        "partner_name",
        "partner_cred_lumen",
        "partner_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
    ]
    df = get_moment_guts_partners_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.person_name,
                df.partner_name,
                df.partner_cred_lumen,
                df.partner_debt_lumen,
                df.fund_give,
                df.fund_take,
                df.fund_agenda_give,
                df.fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', gut partners metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)

    return fig


def get_moment_jobs_partners_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all person paths
    moment_person_names = x_moment._get_person_dir_names()
    # for all persons get gut
    job_dfs = []
    for person_name in moment_person_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        job = open_job_file(x_moment.moment_mstr_dir, moment_lasso, person_name)
        job.conpute()
        job_df = get_person_partnerunits_dataframe(job)
        job_df.insert(0, "person_name", job.person_name)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_partners_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "person_name",
        "partner_name",
        "partner_cred_lumen",
        "partner_debt_lumen",
        "fund_give",
        "fund_take",
        "fund_agenda_give",
        "fund_agenda_take",
    ]
    df = get_moment_jobs_partners_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.person_name,
                df.partner_name,
                df.partner_cred_lumen,
                df.partner_debt_lumen,
                df.fund_give,
                df.fund_take,
                df.fund_agenda_give,
                df.fund_agenda_take,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', job partners metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_guts_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all person paths
    moment_person_names = x_moment._get_person_dir_names()
    # for all persons get gut
    gut_dfs = []
    for person_name in moment_person_names:
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        gut_person = open_gut_file(x_moment.moment_mstr_dir, moment_lasso, person_name)
        gut_person.conpute()
        df = get_person_agenda_dataframe(gut_person)
        gut_dfs.append(df)
    return pandas_concat(gut_dfs, ignore_index=True)


def get_moment_guts_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "person_name",
        "fund_ratio",
        "plan_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_moment_guts_agenda_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.person_name,
                df.fund_ratio,
                df.plan_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', gut agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


def get_moment_jobs_agenda_dataframe(x_moment: MomentUnit) -> DataFrame:
    # get list of all person paths
    job_dfs = []
    for x_person_name in x_moment._get_person_dir_names():
        moment_lasso = lassounit_shop(x_moment.moment_rope, x_moment.knot)
        job = open_job_file(x_moment.moment_mstr_dir, moment_lasso, x_person_name)
        job.conpute()
        job_df = get_person_agenda_dataframe(job)
        job_dfs.append(job_df)
    return pandas_concat(job_dfs, ignore_index=True)


def get_moment_jobs_agenda_plotly_fig(x_moment: MomentUnit) -> plotly_Figure:
    column_header_list = [
        "person_name",
        "fund_ratio",
        "plan_label",
        "parent_rope",
        "begin",
        "close",
        "addin",
        "denom",
        "numor",
        "morph",
    ]
    df = get_moment_jobs_agenda_dataframe(x_moment)
    header_dict = dict(values=column_header_list, fill_color="powderblue", align="left")
    x_table = plotly_Table(
        header=header_dict,
        cells=dict(
            values=[
                df.person_name,
                df.fund_ratio,
                df.plan_label,
                df.parent_rope,
                df.begin,
                df.close,
                df.addin,
                df.denom,
                df.numor,
                df.morph,
            ],
            fill_color="lavender",
            align="left",
        ),
    )

    fig = plotly_Figure(data=[x_table])
    fig_label = f"moment '{x_moment.moment_rope}', job agenda metrics"
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig
