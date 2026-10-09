# ch20_brick — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 20 — `ch20_brick`**
**"BrickUnit — a schema-defined tabular data format that carries PersonUnit and MomentUnit data for ETL ingestion"**

---

## 2. Prompt Used to Build This

From `ch20_ref.json`:
> "Bricks are tables of data that build moment systems and the personunits within them."

Ontology note:
> "Bricks are a complicated mix of things that can change Persons or Moment attributes like ledger."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: File I/O, dict utilities, CSV creation.
- **ch08_person_logic**: `PersonUnit` — `create_brick_df` extracts structured DataFrames directly from a `PersonUnit`'s internal state.
- **ch09_person_atom**: `PersonAtom`, `atomrow_shop` — atoms are the unit of record in several brick formats; brick rows map to atom fields.
- **ch10_person_lesson**: `PersonDelta`, `get_dimens_cruds_persondelta` — bricks can represent a full delta of changes.
- **ch14_time**: `epochunit_shop` — epoch plans are a category of brick data.
- **ch15_moment**: `MomentUnit`, `momentunit_shop` — bricks build both persons and moments.
- **ch19_db_tool**: `get_sorted_cols_only_list` — used to enforce consistent column ordering across all brick DataFrames.

New semantic type: `SheetName` (a `str`) — identifies a named sheet within an Excel workbook, since bricks are primarily authored in `.xlsx` files.

---

## 4. Summary of What This Chapter Does

`ch20_brick` defines the **external data format** for keg — the structure through which humans author data that gets loaded into the system.

**`BrickRef`** is the schema object for a single brick type. It holds:
- `brick_name` — e.g. `"br00031"`.
- `dimens` — the list of atom dimensions this brick maps to (e.g. `["person_planunit", "person_plan_awardunit"]`).
- `attributes` — a dict of column names to `{"otx_key": bool}` — marking whether a column is a primary key field (`otx_key=True`) or a value field (`otx_key=False`).

`get_otx_keys_list()` and `get_otx_values_list()` split attributes into the key columns (used for deduplication and joining) and value columns.

**`brick_config.json`** is the master schema registry — a dictionary of all brick types, each with their `brick_category`, `dimens`, and column definitions. Categories include `"person"`, `"moment"`, `"translate"`, `"nabu"`, and `"spark"`.

**`brick_dataframe.py`** provides `create_brick_df(person, brick_name)` — which introspects a `PersonUnit` and extracts a pandas `DataFrame` matching the brick schema. Each row corresponds to one atom-level record (a plan, a contact, a reason, etc.) in the person's current state.

**`brick_db_tool.py`** handles Excel I/O: `get_all_excel_sheet_names` scans a directory for `.xlsx` files and returns all sheet names; `save_sheet` writes a DataFrame to a named sheet; `create_brick_df_from_file` reads a brick sheet back into a DataFrame.

**`translate_toolbox.py`** provides `add_otx_inx_columns` — given a brick DataFrame with `otx`-valued key columns, it appends matching `_otx` and `_inx` column pairs for use by the translation pipeline (ch17).

**`brick_formats/`** is a directory of per-brick JSON schema files (e.g. `br00031.json`), each specifying the `dimens` and `attributes` for that brick type. These are loaded by `get_brickref_from_file`.

The naming convention `br0NNNN` encodes the atom dimensions a brick covers. The brick system is keg's interface layer between human-authored spreadsheets and the internal atom/person/moment object model.
