# ch31_kpi — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 31 — `ch31_kpi`**
**"KPI and Calendar — analytics tables over job data, calendar markdown output, and Google Calendar day-punch generation"**

---

## 2. Prompt Used to Build This

From `ch31_ref.json`:
> "Defines the analytics outcomes of completed MomentUnits."

Ontology note:
> "Tools for getting KPIs and do not change ETL core data."

---

## 3. Summary of Previous Relevant Chapters

- **ch03_contact**: `ContactUnit` — contacts are examined when building day-punch schedules.
- **ch05_rope**: `create_rope`, `is_sub_rope` — used in `gcalendar.py` to check whether a plan is within a focus subtree.
- **ch06_reason**: `ReasonHeir` — plan reasons are inspected to extract time-based conditions for calendar generation.
- **ch07_plan**: `PlanUnit` — plan trees are walked to find active pledges.
- **ch08_person_logic**: `PersonUnit`, `get_sorted_plan_list` — the job `PersonUnit` is the data source for all KPI and calendar output.
- **ch10_person_lesson**: Path helpers for moments dir, `lassounit_shop`.
- **ch11_person_listen**: `open_job_file` — job files are the input for calendar and KPI computations.
- **ch14_time**: `TimeShoe`, `add_epoch_planunit`, `get_default_epoch_config_dict`, `get_epoch_min_from_dt`, `get_epoch_rope`, `timeshoe_shop`, `set_epoch_fact` — the epoch system is used to evaluate which plans are active at a specific real-world datetime.
- **ch15_moment**: `open_moment_file`, `get_moment_timeshoe` — the moment's epoch configuration drives the time coordinate system.
- **ch19_db_tool**: `db_table_exists`, `get_db_tables` — KPI tables are checked before creation.
- **ch20_brick**: `save_table_to_csv` — KPI tables are exported to CSV.
- **ch22_etl_config**: `create_moment_mstr_path`, `create_world_db_path` — path helpers.

New semantic types: none beyond the accumulated chain.

---

## 4. Summary of What This Chapter Does

Ch31 is the **analytics and reporting layer** — it reads from the fully computed job state (produced by ch27) and produces human-consumable outputs without modifying any ETL data.

**KPI tables (`kpi_mstr.py` + `kpi_sqlstr.py`)**

Two KPIs are currently defined, both implemented as `CREATE TABLE AS SELECT` SQL statements against the job tables populated in ch27:

- `moment_kpi001_contact_nets` — joins `moment_tranbook_nets` (net fund flows per person) with `person_planunit_job` (plan counts) to produce: `moment_rope`, `person_name`, `net_funds`, `fund_rank` (RANK window function over net amount), `pledges_count` (count of active pledge plans). This gives a ranked leaderboard of who has given and received the most funds relative to their plan commitments.

- `moment_kpi002_person_pledges` — a filtered view of `person_planunit_job` returning only rows where `pledge=1` AND `plan_active=1`. This is the current active to-do list across all persons and moments.

`populate_kpi_bundle(cursor)` runs both KPIs; `create_kpi_csvs(db_path, dst_dir)` exports all `kpi`-prefixed tables to CSV files.

**Calendar markdown (`kpi_mstr.py`)**

`create_calendar_markdown_files(moment_mstr_dir, output_dir)` — for each moment, loads the `MomentUnit`, calls `get_moment_timeshoe` to get the epoch's time-shoe (the mapping from `TimeNum` to calendar position), then calls ch14's `get_calendarmarkdown_str` to produce a human-understandable markdown calendar showing the epoch structure. Written to `output_dir`.

**Google Calendar day-punches (`gcalendar.py`)**

`lego_to_person_gcal_day_punchs(world_dir, person_name, day, focus_group_title)` — the most operationally complex function in ch31:
1. Loads the person's job `PersonUnit` from disk.
2. Calls `add_epoch_planunit` and `set_epoch_fact` (from ch14) to inject the current datetime's `TimeNum` as a fact into the person's plan tree.
3. Runs `thinkout()` to re-evaluate plan activation at that specific point in time.
4. Walks the plan tree looking for active pledges with `ReasonHeir` references to a time-based fact context (using `is_sub_rope` to check against the epoch rope).
5. For each such plan, if it is under `focus_group_title`'s workforce scope, writes a "day punch" text file — a plain-text record of the plan rope, active status, and time bounds suitable for importing into Google Calendar.

`get_day_punchs_persons` and `copy_person_day_punches_to_dst_dir` handle multi-person orchestration and file copying. The day-punch output is the most direct link between keg's belief system and a person's real-world schedule.
