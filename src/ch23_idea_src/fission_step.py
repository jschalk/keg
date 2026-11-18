from ch05_rope.rope import default_knot_if_None
from ch21_brick.brick_dataframe import _sort_dataframe
from ch99_glossary.sorter import get_keg_elements_sort_order
from pandas import DataFrame, concat as pandas_concat


def fission_add_ancestor_rope_rows(df: DataFrame) -> DataFrame:
    knot_str = default_knot_if_None()

    if "plan_rope" not in df.columns:
        return df

    existing_ropes = set(df["plan_rope"].dropna().unique())
    new_rows = []
    for _, row in df.iterrows():
        rope = row["plan_rope"]
        if not isinstance(rope, str):
            continue
        segments = [s for s in rope.split(knot_str) if s]
        for i in range(1, len(segments)):
            ancestor = knot_str + knot_str.join(segments[:i]) + knot_str
            if ancestor not in existing_ropes:
                existing_ropes.add(ancestor)
                new_row = {**row.to_dict(), "plan_rope": ancestor, "pledge": 0}
                new_row["poynt"] = None
                new_rows.append(new_row)

    if not new_rows:
        return df

    return pandas_concat([df, DataFrame(new_rows)], ignore_index=True)


def fission_set_pledge_to_one(df: DataFrame) -> DataFrame:
    df = df.copy()
    df["pledge"] = 1
    return df


def fission_set_plan_rope_from_health_label(df: DataFrame) -> DataFrame:
    if "moment_rope" not in df.columns:
        raise ValueError(
            "fission_set_plan_rope_from_health_label requires a 'moment_rope' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )
    if "health_label" not in df.columns:
        raise ValueError(
            "fission_set_plan_rope_from_health_label requires a 'health_label' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )

    null_moment = df["moment_rope"].isnull()
    if null_moment.any():
        bad_indices = df.index[null_moment].tolist()
        raise ValueError(
            f"fission_set_plan_rope_from_health_label found null values in 'moment_rope' at row indices: {bad_indices}. "
            "Every row must have a valid moment_rope value to construct plan_rope."
        )

    null_health = df["health_label"].isnull()
    if null_health.any():
        bad_indices = df.index[null_health].tolist()
        raise ValueError(
            f"fission_set_plan_rope_from_health_label found null values in 'health_label' at row indices: {bad_indices}. "
            "Every row must have a valid health_label value to construct plan_rope."
        )

    df = df.copy()
    df["plan_rope"] = df["moment_rope"] + "health;" + df["health_label"] + ";"
    return df


def fission_set_moment_rope_from_moment_label(df: DataFrame) -> DataFrame:
    if "moment_label" not in df.columns:
        raise ValueError(
            "fission_set_moment_rope_from_moment_label requires a 'moment_label' column but it was not found. "
            f"Columns present: {list(df.columns)}"
        )

    null_moment_label = df["moment_label"].isnull()
    if null_moment_label.any():
        bad_indices = df.index[null_moment_label].tolist()
        raise ValueError(
            f"fission_set_moment_rope_from_moment_label found null values in 'moment_label' at row indices: {bad_indices}. "
            "Every row must have a valid moment_label value to construct moment_rope."
        )

    df = df.copy()
    df["moment_rope"] = ";" + df["moment_label"] + ";"
    return df


def fission_add_knot_from_rope(df: DataFrame) -> DataFrame:
    if "knot" in df.columns:
        return df

    knot = None

    for col in ["moment_rope", "plan_rope"]:
        if col in df.columns:
            first_valid = None if df[col].dropna().empty else df[col].dropna().iloc[0]
            if first_valid is not None and len(first_valid) > 0:
                knot = first_valid[0]
                break

    if knot is None:
        knot = ";"

    df = df.copy()
    df["knot"] = knot
    return df


def get_all_fission_steps() -> dict[str,]:
    return {
        "fission_add_knot_from_rope": fission_add_knot_from_rope,
        "fission_set_moment_rope_from_moment_label": fission_set_moment_rope_from_moment_label,
        "fission_set_plan_rope_from_health_label": fission_set_plan_rope_from_health_label,
        "fission_set_pledge_to_one": fission_set_pledge_to_one,
        "fission_add_ancestor_rope_rows": fission_add_ancestor_rope_rows,
    }


def run_fission_steps(df: DataFrame, fission_steps: list[str]) -> DataFrame:
    all_fission_steps = get_all_fission_steps()
    allowed_fission_steps = set(all_fission_steps.keys())
    for step_name in fission_steps:
        if step_name not in allowed_fission_steps:
            raise ValueError(
                f"run_fission_steps encountered unknown fission step '{step_name}'. "
                f"Registered steps: {list(all_fission_steps.keys())}"
            )
        df = all_fission_steps[step_name](df)
        ke_sorted = get_keg_elements_sort_order()
        df = df[[c for c in ke_sorted if c in df.columns]]
        df.reset_index(inplace=True)
        df.drop(columns=["index"], inplace=True)
    return df
