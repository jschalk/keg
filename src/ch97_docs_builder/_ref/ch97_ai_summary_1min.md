# ch97_docs_builder — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 97 — `ch97_docs_builder`**
**"Docs Builder — AST-based documentation generator and glossary ranking system that reads the source tree and writes chapter overviews, brick format docs, and exam questions"**

---

## 2. Prompt Used to Build This

From `ch97_ref.json`:
> "Defines Tools that create documentation."

Ontology note:
> "Documents can be created here where the keywords selection is always largest."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: File I/O (`create_path`, `get_dir_filenames`, `open_json`, `save_file`, `save_json`) — documentation artifacts are written to disk via ch00 utilities.
- **ch01_keyword**: `get_chapter_desc_prefix`, `get_chapter_descs`, `get_keywords_src_config`, `get_ch_int`, `parse_valid_ch_str`, `create_src_keywords_src_path`, `create_src_example_strs_path` — ch97 reads the full keyword glossary and chapter directory structure to build its documentation. The chapter is numbered 97 specifically because it needs access to the complete keyword set, which accumulates through all prior chapters.
- **ch05_rope**: `get_ropeterm_description_md` — a chapter-specific doc-builder helper in `ch05_rope/_ref/ch05_doc_builder.py` that provides the markdown description of the `RopeTerm` concept.
- **ch20_brick**: `get_brick_formats_md`, `get_brick_mds` — generates markdown documentation for all brick format schemas.
- **ch99_glossary**: `get_keg_elements_sort_order` — the canonical sort order is used when listing elements in generated docs.

`ch97_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

`ch97_docs_builder` uses Python's `ast` module to introspect the keg source tree and generate structured documentation artifacts.

**`doc_builder.py`**

- `get_func_names_and_class_bases_from_file(file_path)` — parses a `.py` file using `ast.parse` + `ast.walk`, extracting all top-level function names and all class names with their base class names. This enables documentation of what each module defines without executing it.
- `get_chapter_blurbs_md()` — iterates all chapter directories via `get_chapter_descs`, reads each chapter's `_ref/chXX_ref.json`, and assembles a markdown document listing each chapter number, description, and blurb. This produces the repo's high-level "what does each chapter do" reference.
- `get_ropeterm_description_md()` — delegates to ch05's own doc-builder helper for the RopeTerm concept description.
- `get_brick_formats_md()` / `get_brick_mds()` — produce markdown tables and descriptions of all brick format schemas, pulling from `brick_config.json` and the `brick_formats/` JSON files.
- `rebuild_keywords_definitions_contents()` (from `glossary_definition.py`) — reads `keywords_definitions.json` and rebuilds its contents from the keyword source files, keeping definitions in sync with the glossary.

**`glossary_ranking.py`**

- `QuestionUnit` — a dataclass representing a single study question about a keg term: `keg_term`, `keyword_definition`, `init_ch` (the chapter where the term is first introduced), `question_tier`, `did_you_read_order`, and optionally a `complete_question` arbitary setting.
- `get_keyword_definition_questionunits()` — iterates all keywords in `keywords_src.json`, parses their `valid_ch` range to determine `init_ch`, looks up their definition, and constructs a `QuestionUnit` for each. Default questions follow the pattern: "Did you read that the keyword_definition of '{term}' is '{definition}'."
- `rebuild_keg_exam_questions(dst_path)` — writes all questions to a CSV file, sorted by `did_you_read_order`, suitable for use as flash cards or onboarding material.
- `rebuild_keg_rank_csv(dst_path)` — writes a JSON ranking of all keg terms ordered by chapter of introduction, providing a structured learning path through the system's vocabulary.

The positioning at chapter 97 is deliberate: by being near the end of the inductive chain, ch97 has access to the complete keyword set and all chapter descriptions — making it the only chapter with a full view of the entire codebase's vocabulary and structure.
