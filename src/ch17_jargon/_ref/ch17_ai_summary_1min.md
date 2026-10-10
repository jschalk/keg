# ch17_jargon — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 17 — `ch17_jargon`**
**"JargonUnit — string-level translation layer mapping external (otx) terms to internal (inx) terms across all string types"**

---

## 2. Prompt Used to Build This

From `ch17_ref.json`:
> "A tool that translates persons from outside language to inside language."

Ontology note:
> "Demonstrates Ontological structure of translation of LabelTerms, RopeTerms, NameTerms, GroupTerms."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `dict_toolbox` string-search utilities (`str_in_dict`, `str_in_dict_keys`, `str_in_dict_values`, `get_str_in_sub_dict`) — used in `MapCore` to validate that the `unknown_str` sentinel does not appear in translation mappings.
- **ch05_rope**: `create_rope`, `create_rope_from_labels`, `get_all_rope_labels`, `get_parent_rope`, `get_tail_label` — `RopeMap` uses these to jargon ropes label-by-label, applying the `LabelMap` to each segment of a path.
- **ch10_person_lesson**: `FaceName` — each map and `JargonUnit` is attributed to a specific face and `spark_num`, maintaining provenance.
- **ch12_bud**: `SparkInt` — the ordering integer for inheritance resolution.

`ch17_semantic_types.py` re-exports through ch12/ch10 with no new types. The chapter introduces one configuration constant: `unknown_str` (default `"UNKNOWN"`) — the sentinel value used when a translation mapping cannot be found.

---

## 4. Summary of What This Chapter Does

`ch17_jargon` implements the **string translation system** — the counterpart to ch16's numeric translation. Where ch16 converts external time numbers to internal `TimeNum` values, ch17 converts external string terms (names, labels, rope paths, group titles) to their internal equivalents.

The "outside" (`otx`) / "inside" (`inx`) distinction is fundamental: an external face might use the name `"Bob"` for a contact that the internal system calls `"Robert_Smith"`, or use a rope path `";work;tasks;"` where the internal system uses `";job;pledges;"`. Translation enables data from any face to be correctly integrated.

**`MapCore`** is the base class for all maps. It holds:
- `otx2inx` — a dictionary from external string to internal string.
- `unknown_str` — the sentinel returned when no mapping exists (prevents silent failures by making untranslated terms visible).
- `otx_knot` / `inx_knot` — the delimiter characters used in external vs internal rope paths (may differ).
- `spark_face` / `spark_num` — provenance, matching the lesson/nabu model.

**Four specialized map classes** cover all string types:
- `NameMap` — translates `NameTerm`s (contact names, person names). Direct `otx → inx` lookup.
- `TitleMap` — translates `TitleTerm`s (group titles). Direct lookup.
- `LabelMap` — translates `LabelTerm`s (single rope node names). Validates that neither `otx` nor `inx` contains the knot character.
- `RopeMap` — translates full `RopeTerm` paths. It splits the external rope into labels, applies `LabelMap` to each label, replaces the `otx_knot` with the `inx_knot`, and reassembles. Backup to `unknown_str` if any label cannot be translated.

**`JargonUnit`** composes all four maps into a single per-face translation object. It exposes unified methods (`set_titleterm`, `set_nameterm`, `set_labelterm`, `set_ropeterm`) and a `get_mapunit(obj_type)` dispatcher. It also holds top-level `otx_knot`/`inx_knot` and `unknown_str` settings that are propagated to all child maps via `_check_all_core_attrs_match`.

**`inherit_*` functions** (`inherit_labelmap`, `inherit_namemap`, etc.) merge an older map into a newer one — the same ordered-inheritance pattern used in ch10 lessons and ch16 nabu, ensuring that more recent translations from the same face supersede older ones.

Together ch16 (numeric translation) and ch17 (string translation) form the complete "outside-to-inside" interface layer. All data arriving from external faces passes through these two chapters before being processed by the internal keg machinery.
