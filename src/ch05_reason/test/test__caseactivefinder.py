from ch00_py.csv_toolbox import open_csv_with_types
from ch00_py.plotly_toolbox import conditional_fig_show
from ch05_reason.reason_main import CaseActiveFinder, caseactivefinder_shop
from dataclasses import dataclass
from plotly.graph_objects import Figure as plotly_figure, Scatter as plotly_Scatter
from pytest import raises as pytest_raises
from ref.keywords import Ch05Keywords as kw, ExampleStrs as exx


def test_CaseActiveFinder_Exists():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 1
    x_reason_divisor = 1
    x_fact_lower_full = 1
    x_fact_upper_full = 1

    # WHEN
    x_csf = CaseActiveFinder(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.reason_lower == x_reason_lower
    assert x_csf.reason_upper == x_reason_upper
    assert x_csf.reason_divisor == x_reason_divisor
    assert x_csf.fact_lower_full == x_fact_lower_full
    assert x_csf.fact_upper_full == x_fact_upper_full


def test_caseactivefinder_shop_ReturnsObj():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 1
    x_reason_divisor = 1
    x_fact_lower_full = 1
    x_fact_upper_full = 1

    # WHEN
    x_csf = caseactivefinder_shop(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.reason_lower == x_reason_lower
    assert x_csf.reason_upper == x_reason_upper
    assert x_csf.reason_divisor == x_reason_divisor
    assert x_csf.fact_lower_full == x_fact_lower_full
    assert x_csf.fact_upper_full == x_fact_upper_full


def test_CaseActiveFinder_check_attr_RaisesError_Scenario0():
    # ESTABLISH / WHEN
    with pytest_raises(Exception) as excinfo_1:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=None,
            reason_divisor=1,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assert str(excinfo_1.value) == "No parameter can be None"


def test_CaseActiveFinder_check_attr_RaisesError_Scenario1():
    # ESTABLISH
    x_fact_lower_full = 2
    x_fact_upper_full = 1

    # WHEN
    with pytest_raises(Exception) as excinfo_2:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=1,
            reason_divisor=1,
            fact_lower_full=x_fact_lower_full,
            fact_upper_full=x_fact_upper_full,
        )

    # THEN
    assertion_fail_str = f"self.fact_lower_full={x_fact_lower_full} cannot be greater than self.fact_upper_full={x_fact_upper_full}"
    assert str(excinfo_2.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario2():
    # ESTABLISH
    x_reason_divisor = -1

    # WHEN
    with pytest_raises(Exception) as excinfo_3:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=1,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = (
        f"self.reason_divisor={x_reason_divisor} cannot be less/equal to zero"
    )
    assert str(excinfo_3.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario3():
    # ESTABLISH
    x_reason_divisor = 1
    x_reason_lower = -1

    # WHEN
    with pytest_raises(Exception) as excinfo_4:
        caseactivefinder_shop(
            reason_lower=x_reason_lower,
            reason_upper=1,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = f"self.reason_lower={x_reason_lower} cannot be less than zero or greater than self.reason_divisor={x_reason_divisor}"
    assert str(excinfo_4.value) == assertion_fail_str


def test_CaseActiveFinder_check_attr_RaisesError_Scenario4():
    # ESTABLISH
    x_reason_divisor = 1
    x_reason_upper = 2

    # WHEN
    with pytest_raises(Exception) as excinfo_5:
        caseactivefinder_shop(
            reason_lower=1,
            reason_upper=x_reason_upper,
            reason_divisor=x_reason_divisor,
            fact_lower_full=1,
            fact_upper_full=1,
        )

    # THEN
    assertion_fail_str = f"self.reason_upper={x_reason_upper} cannot be less than zero or greater than self.reason_divisor={x_reason_divisor}"
    assert str(excinfo_5.value) == assertion_fail_str


def test_CaseActiveFinder_get_fact_lower_remainder_ReturnsObj():
    # ESTABLISH
    x_reason_lower = 1
    x_reason_upper = 2
    x_reason_divisor = 3
    x_fact_lower_full = 4
    x_fact_upper_full = 5

    # WHEN
    x_csf = caseactivefinder_shop(
        x_reason_lower,
        x_reason_upper,
        x_reason_divisor,
        x_fact_lower_full,
        x_fact_upper_full,
    )

    # THEN
    assert x_csf.get_fact_lower_remainder() == x_fact_lower_full % x_reason_divisor
    assert x_csf.get_fact_upper_remainder() == x_fact_upper_full % x_reason_divisor


# for CaseActiveFinder tests
def add_trace(
    fig: plotly_figure,
    x_int: int,
    x_end: int,
    y_int: int,
    trace_name: str,
    x_color: str = None,
    showlegend: bool = False,
    case_str: str = "",
    expect_str: str = "",
    expect_case_task_str: str = "",
    reason_divisor: float = 0,
) -> plotly_figure:
    x_end = x_int if x_end is None else x_end
    x_color = "Black" if x_color is None else x_color
    x_marker_size = 12 if x_color == "Blue" else 10
    fig.add_trace(
        plotly_Scatter(
            x=[x_int, x_end],
            y=[y_int, y_int],
            marker_size=x_marker_size,
            name=trace_name,
            marker_color=x_color,
            showlegend=showlegend,
        )
    )
    fig.add_annotation(
        x=reason_divisor + 0.15, y=y_int, text=expect_str, showarrow=False
    )
    fig.add_annotation(
        x=reason_divisor + 0.4, y=y_int, text=expect_case_task_str, showarrow=False
    )
    fig.add_annotation(x=-0.1, y=y_int, text=case_str, showarrow=False)


# for CaseActiveFinder tests
def add_traces(
    fig: plotly_figure,
    x_csf: CaseActiveFinder,
    y_int: int,
    showlegend: bool = False,
    case_str: str = "",
    expect_str: str = "",
    expect_case_task_str: str = "",
    reason_divisor: float = 1,
) -> plotly_figure:
    fact_str = "FactUnit range"
    pink_str = "Pink"
    sl = showlegend

    if x_csf.reason_lower <= x_csf.reason_upper:
        add_trace(
            fig, x_csf.reason_lower, x_csf.reason_upper, y_int, case_str, exx.blue, sl
        )
    else:
        add_trace(fig, 0, x_csf.reason_upper, y_int, case_str, exx.blue, sl)
        add_trace(
            fig,
            x_csf.reason_lower,
            x_csf.reason_divisor,
            y_int,
            case_str,
            exx.blue,
            sl,
        )

    if x_csf.get_fact_lower_remainder() <= x_csf.get_fact_upper_remainder():
        x_int = x_csf.get_fact_lower_remainder()
        x_end = x_csf.get_fact_upper_remainder()
        if x_csf.fact_upper_full == x_csf.reason_divisor:
            x_end = x_csf.reason_divisor
        add_trace(
            fig,
            x_int,
            x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            expect_str=expect_str,
            expect_case_task_str=expect_case_task_str,
            reason_divisor=reason_divisor,
        )
    else:
        trace1_x_int = 0
        trace1_x_end = x_csf.get_fact_upper_remainder()
        trace2_x_int = x_csf.get_fact_lower_remainder()
        trace2_x_end = x_csf.reason_divisor

        add_trace(
            fig,
            trace1_x_int,
            trace1_x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
            case_str=case_str,
            expect_str=expect_str,
            expect_case_task_str=expect_case_task_str,
            reason_divisor=reason_divisor,
        )
        add_trace(
            fig,
            trace2_x_int,
            trace2_x_end,
            y_int,
            fact_str,
            pink_str,
            sl,
        )


# for CaseActiveFinder tests
def show_x(
    expect_active: bool,
    expect_case_task_bool: bool,
    x_csf: CaseActiveFinder,
    fig: plotly_figure,
    trace_y: float,
    case_str: str,
    showlegend: bool = False,
    graphics_bool: bool = False,
) -> float:
    if not graphics_bool:
        return
    expect_str = "TRUE" if expect_active else "FALSE"
    expect_case_task_str = "TRUE" if expect_case_task_bool else "FALSE"
    add_traces(
        fig, x_csf, trace_y, showlegend, case_str, expect_str, expect_case_task_str, 1
    )
    if (
        x_csf.get_active_bool() != expect_active
        or x_csf.get_case_task_bool() != expect_case_task_bool
    ):
        fig.show()
    return 0.1


# for CaseActiveFinder tests
def get_fig(pd: float, graphics_bool: bool) -> plotly_figure:
    if not graphics_bool:
        return None
    fig = plotly_figure()
    add_trace(
        fig=fig,
        x_int=0.0,
        x_end=pd,
        y_int=0.0,
        trace_name="reason_divisor Range",
        x_color=None,
        showlegend=True,
        case_str="Scenario",
        expect_str="case_active",
        expect_case_task_str="case_task Bool",
        reason_divisor=pd,
    )
    fig_label = "Given Fact Range and Case Range assert expected Case.case_active, Case.case_task Bools."
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=True, showticklabels=False)
    fig.update_layout(plot_bgcolor="white", title=fig_label, title_font_size=20)
    return fig


@dataclass
class ExpectedCaseAttrs:
    caseactivefinder: CaseActiveFinder
    expected_active: bool
    expected_case_task: bool
    add_to_line: float
    description: str = None


def eca_shop(
    caseactivefinder: CaseActiveFinder,
    add_to_line: float,
    expected_active: bool,
    expected_case_task: bool,
    description: str = None,
) -> ExpectedCaseAttrs:
    return ExpectedCaseAttrs(
        caseactivefinder, expected_active, expected_case_task, add_to_line, description
    )


def check_case(
    linel: float,
    expectedcaseattrs: ExpectedCaseAttrs,
    fig: plotly_figure,
    graphics_bool: bool,
    case_desc: str,
):
    linel += expectedcaseattrs.add_to_line
    show_legend = linel == 0.1
    if expectedcaseattrs.description:
        case_desc = expectedcaseattrs.description
    # case = c_tuple[0]
    # expected_active = c_tuple[1]
    # expected_case_task = c_tuple[2]
    x_caseactivefinder = expectedcaseattrs.caseactivefinder
    show_x(
        expectedcaseattrs.expected_active,
        expectedcaseattrs.expected_case_task,
        x_caseactivefinder,
        fig,
        linel,
        case_desc,
        show_legend,
        graphics_bool,
    )
    assert x_caseactivefinder.get_active_bool() == expectedcaseattrs.expected_active
    assert (
        x_caseactivefinder.get_case_task_bool() == expectedcaseattrs.expected_case_task
    )
    return linel


def caf_shop(
    reason_lower, reason_upper, reason_divisor, fact_lower_full, fact_upper_full
) -> CaseActiveFinder:
    """made to shorten function name in only one test"""
    return caseactivefinder_shop(
        reason_lower, reason_upper, reason_divisor, fact_lower_full, fact_upper_full
    )


def check_show_caseactivefinder_scenarios(graphics_bool: bool):
    graph_b = graphics_bool
    grb = graphics_bool
    pd = 1  # reason_divisor
    fig = get_fig(pd, graphics_bool)
    linel = 0
    test_cases_csv_path = "src/ch05_reason/test/caseactivefinder_test_cases.csv"
    test_cases_types = {
        "case_desc": "TEXT",
        kw.reason_lower: "REAL",
        kw.reason_upper: "REAL",
        kw.reason_divisor: "REAL",
        f"{kw.fact_lower}_full": "REAL",
        f"{kw.fact_upper}_full": "REAL",
        "linl_add": "REAL",
        "expected_active": "BOOLEAN",
        f"expected_{kw.case_task}": "BOOLEAN",
    }
    test_cases = open_csv_with_types(test_cases_csv_path, test_cases_types)
    header = None
    for test_case in test_cases:
        if not header:
            header = test_case
        else:
            case_desc = test_case[0]
            reason_lower = test_case[1]
            reason_upper = test_case[2]
            reason_divisor = test_case[3]
            fact_lower_full = test_case[4]
            fact_upper_full = test_case[5]
            linl_add = test_case[6]
            expected_active = test_case[7]
            expected_case_task = test_case[8]
            x_caseactivefinder = caseactivefinder_shop(
                reason_lower,
                reason_upper,
                reason_divisor,
                fact_lower_full,
                fact_upper_full,
            )
            x_eca = eca_shop(
                x_caseactivefinder,
                linl_add,
                expected_active,
                expected_case_task,
                case_desc,
            )
            linel = check_case(linel, x_eca, fig, grb, None)

    # Bottom reason_divisor line
    _add_last_trace_and_show(fig, pd, linel, graph_b)


def test_CaseActiveFinder_get_active_get_case_task_bool_ReturnsObj_Scenari0_fact_range(
    graphics_bool,
):
    # # ESTABLISH / WHEN / THEN
    """Check Scenarios CaseUnit.active. Plotly graph can be used to identify problems."""
    # # Scenario A
    assert caf_shop(0.3, 0.7, 1, 0.1, 1.2).get_active_bool()

    # # Scenario B1
    check_show_caseactivefinder_scenarios(graphics_bool)


def _add_last_trace_and_show(fig: plotly_figure, pd, linel, graphics_bool: bool):
    if graphics_bool:
        add_trace(fig, 0.0, pd, linel - 0.2, "reason_divisor Range", None)
        conditional_fig_show(fig, graphics_bool)


def test_CaseActiveFinder_get_active_get_case_task_bool_ReturnsObj_Scenario1_Seperated_reason_range_Inside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=20000,
        fact_upper_full=29000,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    x_str2 = f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    x_str3 = f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    print(x_str2)
    print(x_str3)
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_case_task_bool()=}")
    # assert segr_obj.fact_range_len == 9000
    # assert segr_obj.get_fact_upper_mod_div() == 200

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_case_task_bool()


def test_CaseActiveFinder_get_active_get_case_task_bool_ReturnsObj_Scenario2_reason_range_Inside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=1300,
        fact_upper_full=1400,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_case_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_case_task_bool()


def test_CaseActiveFinder_get_active_get_case_task_bool_ReturnsObj_Scenario3_reason_range_Outside_fact_range():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=1305.0,
        reason_upper=1305.0,
        reason_divisor=1440,
        fact_lower_full=1300,
        fact_upper_full=1300,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_case_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool() is False
    assert segr_obj.get_case_task_bool() is False


def test_CaseActiveFinder_get_active_get_case_task_bool_ReturnsObj_Scenario4_fact_range_Equals_divisor():
    # ESTABLISH
    segr_obj = caseactivefinder_shop(
        reason_lower=600.0,
        reason_upper=690.0,
        reason_divisor=1440,
        fact_lower_full=0,
        fact_upper_full=1440,
    )
    print(f"----\n  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=}")
    print(
        f"  {segr_obj.reason_lower=}  {segr_obj.reason_upper=}  {segr_obj.reason_divisor=}"
    )
    print(
        f"  {segr_obj.fact_lower_full=}  {segr_obj.fact_upper_full=} \tdifference:{segr_obj.fact_upper_full-segr_obj.fact_lower_full}"
    )
    print(f"  {segr_obj.get_active_bool()=}  {segr_obj.get_case_task_bool()=}")

    # WHEN / THEN
    assert segr_obj.get_active_bool()
    assert segr_obj.get_case_task_bool()
