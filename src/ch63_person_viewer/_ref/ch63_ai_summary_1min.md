# ch63_person_viewer — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 63 — `ch63_person_viewer`**
**"Person Viewer — a Flask web app that renders a PersonUnit's plan tree and contacts as an interactive, checkbox-driven HTML visualization"**

---

## 2. Prompt Used to Build This

From `ch63_ref.json`:
> "Tools for Visualizing PersonUnits."

Ontology note:
> "PersonUnits are complicated, graphic tools are useful."

---

## 3. Summary of Previous Relevant Chapters

- **ch03_contact**: `AwardHeir`, `AwardLine`, `AwardUnit` — rendered with human-understandable strings showing `give_force` and `fund_give` values.
- **ch04_workforce**: `LaborHeir`, `LaborUnit` — rendered with solo-flag labeling.
- **ch06_reason**: `CaseUnit`, `FactHeir`, `FactUnit`, `ReasonHeir`, `ReasonUnit` — each type gets its own readable string representation.
- **ch07_plan**: `PlanUnit` — the tree node rendered at every level of the plan hierarchy.
- **ch08_person_logic**: `PersonUnit` — the root object visualized.
- **ch14_time**: `get_fact_state_readable_str`, `get_reason_case_readable_str` — convert numeric time-based fact/reason values into human-understandable calendar strings (e.g. "Monday 8am–10am" rather than raw `TimeNum` integers).

`ch63_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

`ch63_person_viewer` provides two outputs: a Python dict representation of a `PersonUnit` suitable for JSON serialization (`person_viewer_tool.py`) and a Flask web application that renders that dict as an interactive HTML page (`person_viewer_app.py`).

**`person_objs_asdict(obj, current_person, current_reason)`** — the core recursive serialization function in `person_viewer_tool.py`. It walks any keg dataclass using Python's `dataclasses.fields` introspection and converts the full object graph to a nested dict. For each recognized type it appends a `"readable"` key with a human-friendly HTML snippet:
- `PlanUnit` → `set_readable_plan_values` adds fund percentages (`fund_give`/`fund_take` as `readable_percent`), active status, pledge flag, and descendant pledge count.
- `AwardUnit` / `AwardHeir` / `AwardLine` → give/take force and fund amounts.
- `FactUnit` / `FactHeir` → `get_fact_state_readable_str` from ch14 translates `fact_lower`/`fact_upper` into calendar-readable strings.
- `ReasonUnit` / `ReasonHeir` / `CaseUnit` → context rope and case bounds with `get_reason_case_readable_str`.
- `LaborUnit` / `LaborHeir` → workforce title and solo flag.

**`person_viewer_app.py`** — a Flask app exposing a single route that:
1. Instantiates an example `PersonUnit` (from `person_viewer_example.py` — predefined examples including `get_sue_personunit`, `get_sue_person_with_facts_and_reasons`, and `get_personunit_irrational_example`).
2. Calls `thinkout()` and optionally injects an epoch plan.
3. Calls `get_person_view_dict` to serialize the person.
4. Returns the dict as JSON to a self-contained HTML template that renders the plan tree and contacts panel with JavaScript-driven checkbox toggles.

The HTML template is extensive — it renders ~30 checkbox controls for toggling visibility of individual contact fields (`fund_give`, `fund_agenda_ratio_take`, `irrational_contact_debt_mass`, membership details, etc.) and ~20 plan-level fields (`pledge`, `plan_active`, `plan_task`, `descendant_pledge_count`, reason/fact/award/workforce subtrees). A `static/style.css` file handles layout.

This chapter is a debugging and demonstration tool — it makes the complexity of a post-`thinkout()` `PersonUnit` inspectable by a human without reading raw JSON. The calendar-readable strings from ch14 are what make it genuinely useful: instead of seeing `fact_lower=525600`, a user sees "Monday 8:00 AM".
