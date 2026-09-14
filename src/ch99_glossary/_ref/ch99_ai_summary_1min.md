# ch99_glossary — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 99 — `ch99_glossary`**
**"Glossary — the master vocabulary source: a ranked, structured JSON of all keg terms used by every other chapter for keyword generation, sort ordering, and documentation"**

---

## 2. Prompt Used to Build This

From `ch99_ref.json`:
> "Where keg terms will be defined, described, ranked."

Ontology note:
> "Glossary of kegology terms. Structured and weighted, can be analyzed, critiqued."

---

## 3. Summary of Previous Relevant Chapters

Ch99 is the **most unusual chapter in the inductive chain**: it is numbered 99 and sits at the top, but it is also *imported by ch01* — the second chapter in the chain. This is the one deliberate inversion in the otherwise strict bottom-up import order.

The resolution: ch99 contains only data files and simple utility functions with no imports from any other keg chapter. It is dependency-free despite its high number, making it safe to import from ch01 onward. Ch99 is numbered 99 not because it depends on everything before it, but because it is the *conceptual capstone* — the place where all terms are finally defined, ranked, and described in full.

- **ch01_keyword** imports `keywords_src.json` from ch99 to generate all chapter keyword Enum classes.
- **ch18_db_tool** / **ch20_brick** / **ch22_etl_config** import `get_keg_elements_sort_order` from `sorter.py` to enforce consistent column ordering across all DataFrames and SQL tables.
- **ch97_docs_builder** imports from ch99 for documentation generation.
- **ch98_linter** imports from ch99 indirectly through ch97.

---

## 4. Summary of What This Chapter Does

`ch99_glossary` is the **single source of truth for keg's vocabulary**.

**`keywords_src.json`** — the master keyword registry. Each entry defines:
- `keg_term` — the string identifier (e.g. `"plan_rope"`, `"moment_rope"`, `"spark_face"`).
- `valid_ch` — a range string (e.g. `"5:"`, `"3:8"`) indicating which chapters this term is relevant to.
- `keyword_definition` — a concise human-understandable definition.
- Additional metadata fields used by ch97's exam-question generator.

**`keywords_definitions.json`** — a secondary definitions file, structured for documentation output and kept in sync by `ch97_docs_builder.rebuild_keywords_definitions_contents`.

**`example_strs.json`** — a registry of example string values used in test files across all chapters, allowing the linter (ch98) to validate that test examples match canonical values.

**`sorter.py`** — provides `get_keg_elements_sort_order()`, which returns the canonical ordered list of all brick and person-calc column names used throughout the ETL pipeline. This list (100+ column names) determines the column ordering in every DataFrame, CSV, and SQL table in the system. It is the single authoritative reference for column ordering — any new field added to the system must be registered here.

**`ch_keyword.py`** — provides `get_chapter_keywords(ch_num)`, which reads `keywords_src.json` and returns the set of terms valid for a given chapter number by evaluating the `valid_ch` range expressions. Used by ch01's keyword class builder.

**`derived/`** — a directory of generated files (keyword markdown lists, brick format docs) written by ch97's doc builder. These are outputs, not inputs.

Ch99's architectural role is that of a **shared data layer without code dependencies**. Because it imports nothing from keg, it can be safely used by ch01 (near the bottom of the chain) while also serving as the vocabulary capstone for ch97 and ch98 (near the top). It is the one point in the inductive architecture where the chain intentionally loops back to the beginning — the glossary defines the language in which all the code is written.
