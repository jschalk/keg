**ALL CHAPTER SUMMARIES WRITTEN BY AI
*This summary is authored by AI 5-26-2026.*

---

## Chapter 00 — `ch00_py`
**"Standard Python Toolbox — the foundation everything else is built on"**

**Prompt used to build this** *(from `ch00_ref.json`)*:
> "Create some standard tools for files, python dictionaries, databases, and other basic programming objects."

**Summary of previous relevant chapters:**
None. This is chapter zero — the base of the inductive stack. It imports only from the Python standard library and a small set of third-party packages (`compact_json`, `pathlib`, `shutil`, etc.). Nothing in `keg` precedes it.

**What this chapter does:**
`ch00_py` provides purely utilitarian helper functions used throughout every subsequent chapter. It has no domain logic and no philosophical content — the author's own ref note says *"there is nothing philosophically interesting here."* It is organized into four toolboxes:

- `dict_toolbox.py` — safe null-handling helpers (`get_0_if_None`, `get_empty_dict_if_None`), nested dict operations (get, set, delete by key path), JSON serialization, CSV-to-dict conversion, and normalization utilities.
- `file_toolbox.py` — OS-level path construction (`create_path`), directory creation/deletion/copying, file open/save, JSON file read/write, and path validity checks.
- `csv_toolbox.py` — CSV reading with type coercion, CSV-to-SQLite bridging.
- `plotly_toolbox.py` — minimal Plotly charting wrappers.

The chapter establishes the project's coding style: highly defensive null handling, consistent type aliasing, and thin wrappers around standard library calls with explicit, understandable names.


*This summary is authored by AI 5-26-2026.*

## Chapter 01 — `ch01_keyword`
**"Keyword Glossary Engine — gives every chapter a shared controlled vocabulary"**

**Prompt used to build this** *(from `ch01_ref.json`)*:
> "Create Keyword Enum classes for use in testing files."

**Summary of previous relevant chapters:**
Imports directly from `ch00_py` — specifically `file_toolbox` for `create_path`, `open_json`, and `save_file`. It relies on `ch00`'s file I/O to read two source JSON configs (`keywords_src.json` and `example_strs.json`) that define the full vocabulary of the project.

**What this chapter does:**
`ch01_keyword` is the project's glossary engine. It reads a master list of keyword strings (stored in `ch99_glossary/keywords_src.json`) where each keyword is tagged with a `valid_ch` field indicating which chapters it belongs to. From this, the chapter dynamically generates Python `Enum` classes — one per chapter — so that every chapter has a type-safe, auto-documented set of domain terms available for use in tests and code.

Key mechanics:
- `chapter_desc_main.py` scans the `src/` directory using `ch00`'s `get_level1_dirs` to discover all chapter folders and extract their numbers.
- `keyword_class_builder.py` parses the `valid_ch` range syntax (e.g. `"3:"` means "all chapters from 3 onwards"), builds cumulative keyword sets per chapter, and generates `Enum` class source code strings like `C03Keywords`, `C07Keywords`, etc.
- It also produces a human-understandable `keywords_by_chapter.md` markdown file listing which keywords are introduced in each chapter.

The effect is that all later chapters can reference domain terms as strongly-typed enum values rather than raw strings, making the codebase self-documenting and test-able at the vocabulary level.


*This summary is authored by AI 5-26-2026.*

## Chapter 02 — `ch02_allot`
**"Allotment Engine — defines how a finite pool of value is divided across a weighted ledger"**

**Prompt used to build this** *(from `ch02_ref.json`)*:
> "Defines tools for allotment of a large number (called a pool) to a ledger (a list of things with a weighted value to represent their importance)."

**Summary of previous relevant chapters:**
Imports from `ch00_py` only — `dict_toolbox` for null-safe helpers (`get_0_if_None`, `get_1_if_None`) and `file_toolbox` for `create_path`, `open_json`, `save_json`. It does not use `ch01_keyword`. This chapter introduces its own semantic type aliases in `ch02_semantic_types.py` (`GrainNum`, `PoolNum`, `WeightNum`) which are thin subclasses of `float` used to make function signatures self-describing.

**What this chapter does:**
`ch02_allot` solves the problem of fairly distributing a discrete pool of value (e.g. a resource pool) across a set of competing claims that have relative weights. The author's ref note says plainly: *"When things have to be divided, such as currency, this defines how."*

Three semantic types anchor the logic:
- `PoolNum` — the total number to distribute.
- `WeightNum` — the unnormalized relative importance of each ledger entry.
- `GrainNum` — the smallest indivisible unit (like a cent in currency).

The core function `allot_scale(ledger, scale_number, grain_unit)` takes a weighted dictionary, a total to distribute, and a grain size, and returns a new dictionary where each key receives a share proportional to its weight — guaranteed to sum exactly to `scale_number` with no floating-point remainder. A careful residual-distribution algorithm handles the rounding leftover by assigning extra grain units to the highest-weighted entries first.

`allot_nested_scale` extends this to hierarchical ledgers stored as directory trees of JSON files, recursively allotting a parent's share down to its children up to a configurable depth. This foreshadows the tree-structured logic that appears in later chapters.


*This summary is authored by AI 5-26-2026.*


## Chapter 03 — `ch03_contact`
**"A Contact, A Group, and A Membership — the first core philosophical definitions in keg"**

**Prompt used to build this** *(from `ch03_ref.json`)*:
> "Defines a contact, and its group memberships. Groups will be produced from memberships."

**Summary of previous relevant chapters:**
- From `ch00_py`: `get_0_if_None`, `get_1_if_None`, `get_None_if_nan` for safe null handling.
- From `ch02_allot`: `allot_scale` and `default_grain_num_if_None` — used directly to distribute a contact's creditor/debtor pool proportionally across its group memberships. The semantic types `GrainNum`, `PoolNum`, `WeightNum` are re-exported through `ch03_semantic_types.py`.

**What this chapter does:**
This is where `keg`'s philosophical content starts. The author's ref note calls these *"keg's first core philosophical definitions."* The chapter defines the social actors of the system and how they relate to one another through credit and debt.

**`ContactUnit`** is the fundamental social actor — a named individual. Each contact carries:
- `contact_cred_mass` and `contact_debt_mass`: how much credit and debt the surrounding system assigns to this contact.
- `memberships`: a dictionary of `MemberShip` objects, each linking the contact to a `GroupTitle`.
- Calculated fields like `fund_give`, `fund_take`, `fund_agenda_give`, `fund_agenda_take`, and their ratios — populated later by the "thinkout" process in higher chapters.

**`MemberShip`** links a contact to a group with its own `group_cred_mass` and `group_debt_mass` weights. When a contact's `credor_pool` or `debtor_pool` is set, `allot_scale` (from `ch02`) distributes that pool proportionally across all of the contact's memberships.

**`GroupUnit`** is derived from memberships rather than declared directly. It aggregates the memberships of multiple contactunits and, using `allot_scale`, distributes its `fund_give` and `fund_take` values back down to individual members. This give/take accounting is the core mechanism by which the system tracks flows of obligation and resource.

**`AwardUnit`**, **`AwardHeir`**, and **`AwardLine`** form a parallel hierarchy representing explicit awards of `give_force` and `take_force` to groups — used later assign relevance to specific groups.

The semantic types introduced here (`ContactName`, `GroupTitle`, `GroupMark`, `NameTerm`, `FundNum`, `RespectNum`) are inherited by all subsequent chapters via `ch03_semantic_types.py`. The `GroupMark` (defaulting to `";"`) is the separator character that distinguishes a group title from a contact name — a contact name cannot contain it, while a group title can.


*This summary is authored by AI 5-26-2026.*


## Chapter 04 — `ch04_workforce`
**"Workforce and Labor — assigning who is responsible for tasks"**

**Prompt used to build this** *(from `ch04_ref.json`)*:
> "Introduces Workforce concept: How tasks are assigned."

**Summary of previous relevant chapters:**
- From `ch00_py`: `get_empty_dict_if_None`, `get_False_if_None` for safe initialization.
- From `ch03_contact`: `ContactName`, `GroupTitle`, `GroupUnit` — workforce assignment is expressed entirely in terms of the group and contact structures defined in ch03. `ch04_semantic_types.py` simply re-exports all of ch03's semantic types wholesale, nothing new of its own.

**What this chapter does:**
`ch04_workforce` is a focused, relatively small chapter that introduces the concept of *labor* — which groups or a contact are designated as responsible for carrying out a task.

**`LaborUnit`** is a simple dataclass pairing a `GroupTitle` with an optional `solo` boolean flag. When `solo=True`, the labor is restricted to a single contact rather than any member of the group.

**`WorkforceUnit`** is a container of `LaborUnit` objects — essentially a named set of groupunits/contactunits that are eligible to perform a task. It supports add, delete, and existence checks for individual labor entries.

**`LaborHeir`** and **`WorkforceHeir`** are the "inherited" counterparts used when a task inherits workforce constraints from a parent task in a tree. `WorkforceHeir.set_labors()` implements the inheritance logic: if the parent has no workforce defined, the child's own workforce is used; if the child has no workforce, the parent's is inherited; if both have workforce definitions, the parent's takes precedence and the child's is only added if not already present. `WorkforceHeir.get_person_name_is_workforce_bool()` then checks whether a specific contact (by `ContactName`) is a member of any of the heir's labor groups, determining if that person is eligible to carry out the task.

This chapter establishes the workforce inheritance pattern that will be applied recursively across a tree in later chapters.

# ch05_rope — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 05 — `ch05_rope`**
**"Ropes and Knots — a path-based identity system for navigating a tree of concepts"**

---

## 2. Prompt Used to Build This

From `ch05_ref.json`:
> "Defines what a Rope is and required format for groups names and individual names."

Ontology note from the ref:
> "Ropes, Knots delineate reality into totalities using letters. From the nothing root all ropes ever branch out."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `is_path_valid` from `file_toolbox` is used to check whether a rope can map to a valid OS directory path.
- **ch02_allot**: `GrainNum`, `PoolNum`, `WeightNum` re-exported through `ch05_semantic_types.py`.
- **ch03_contact**: All of ch03's semantic types (`ContactName`, `GroupTitle`, `GroupMark`, `NameTerm`, `BreakTerm`, `FundNum`, `RespectNum`, etc.) are re-exported, making ch05 the new semantic type accumulation point for all downstream chapters.

Ch05 introduces no new numeric types, only new string-based structural types.

---

## 4. Summary of What This Chapter Does

`ch05_rope` defines the **address system** used throughout keg to identify any node in a tree. The core concept: reality is organized as a hierarchy of named nodes, and any node can be uniquely addressed by its path from the root — this path is called a `RopeTerm`.

**New semantic types introduced:**
- `KnotTerm` — the delimiter character that separates labels within a rope (defaults to `";"`). This directly parallels `GroupMark` from ch03, which used the same default separator to distinguish group names from contact names. In ch05 the concept is generalized into the tree-path domain.
- `LabelTerm` — a single node name; must not contain the `KnotTerm`.
- `RopeTerm` — a full path string composed of `LabelTerm`s joined by `KnotTerm`s, always starts and ends with the knot (e.g. `";root;tasks;cooking;"`).
- `FirstLabel` — the top-level label in a rope, the root of a subtree.

**Key functions in `rope.py`:**
- `create_rope(parent_rope, tail_label, knot)` — constructs a new rope by appending a label to an existing rope.
- `get_all_rope_labels(rope, knot)` — splits a rope into its constituent labels.
- `get_parent_rope(rope)` / `get_tail_label(rope)` — navigate up and down the tree.
- `get_ancestor_ropes(rope)` — returns the full list of ancestor paths from root to the given rope.
- `is_sub_rope(ref_rope, sub_rope)` / `is_heir_rope(src, heir)` — test hierarchical containment relationships.
- `rebuild_rope(subj_rope, old_rope, new_rope)` / `replace_knot(rope, old_knot, new_knot)` — support structural reorganization of the tree.
- `get_unique_short_ropes(ropes_set, knot)` — produces the shortest unambiguous label suffix for each rope in a set (useful for display).
- `rope_is_valid_dir_path(rope, knot)` — checks if a rope can be mapped to a valid OS file path, enabling the file-system-backed persistence used in later chapters.

The rope system is the backbone of every subsequent chapter. A tree structure navigations can/will be done entirely through rope operations.

# ch06_reason — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 06 — `ch06_reason`**
**"Reasons and Facts — the logic engine that decides whether a Reason is active"**

---

## 2. Prompt Used to Build This

From `ch06_ref.json`:
> "Describes what a reason and a fact is; if the reasons match the facts, the Reason.reason_active = True"

Ontology note:
> "ReasonUnits mated to FactUnits produce justifications. If a task must be justified the Reasons and Facts must match."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_empty_dict_if_None` for safe initialization of cases dictionaries.
- **ch05_rope**: `RopeTerm`, `KnotTerm`, `default_knot_if_None`, `is_heir_rope`, `rebuild_rope`, `replace_knot`, `find_replace_rope_key_dict` — all rope operations are central here. Both `FactUnit` and `ReasonUnit` use `RopeTerm` as their identity keys (`fact_context`, `reason_context`). The `is_in_lineage` check in `CaseUnit` uses `is_heir_rope` to test whether a fact's state rope is an ancestor or descendant of the case's required state rope.
- **ch02_allot**, **ch03_contact** semantic types are re-exported through `ch06_semantic_types.py`. Two new float subtypes are introduced: `ReasonNum` and `FactNum`.

---

## 4. Summary of What This Chapter Does

`ch06_reason` implements the **conditional activation logic** of keg — the mechanism by which a node object declares what conditions must be true for it to be considered active.

**`FactUnit` / `FactHeir` / `FactCore`**
A `FactUnit` is a statement about the world: it says that a context (identified by a `RopeTerm` called `fact_context`) is currently in a particular state (`fact_state`), optionally within a numeric range (`fact_lower` to `fact_upper`). Facts are supplied externally to the person and flow down a tree as `FactHeir` objects. A `FactHeir` can be further narrowed by child `FactUnit` moldations as it propagates.

**`CaseUnit`**
A `CaseUnit` is a single condition within a reason. It specifies:
- `reason_state`: the rope state that must be active for this case to pass.
- Optionally `reason_lower` / `reason_upper`: a numeric range the fact must be within.
- Optionally `reason_divisor`: enables **cyclic/modular reasoning** — the fact value is taken modulo the divisor before comparing to the range. This allows conditions like "every 7 rotations of the earth" or "every quarter."

`CaseUnit.set_case_active(factheir)` evaluates whether the supplied fact satisfies this case's condition, setting both `case_active` and `case_task` (whether the case indicates there is still work remaining within the range).

**`CaseActiveFinder`**
A helper dataclass that handles the complex modular arithmetic for cyclic range checks. It computes remainders of fact bounds against the divisor and tests multiple overlap scenarios to determine whether the cyclic condition is currently satisfied.

**`ReasonUnit` / `ReasonHeir`**
A `ReasonUnit` groups one or more `CaseUnit`s under a shared `reason_context` rope. It can also carry `active_requisite` — a boolean that, if set, requires the *parent node's active state* to match before this reason counts. `ReasonHeir.set_reason_active(factheirs)` evaluates all cases against the current fact set and sets `reason_active = True` if any case passes (or if `active_requisite` is satisfied). It also computes `reason_task` to indicate whether the node is not yet fully complete within the fact's range.

This chapter delivers the core inference engine: given a set of real-world facts and a set of declared conditions, it determines what is currently true and what still needs to be done.

# ch07_plan — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 07 — `ch07_plan`**
**"PlanUnit — the most complex concept in keg, a hierarchical node carrying reasoning, funding, workforce, and pledge logic"**

---

## 2. Prompt Used to Build This

From `ch07_ref.json`:
> "Defines PlanUnits. Plans are complicated. A plan can have sub plans, define itself as a pledge, define Awardees, assigned Workforce, required Reasons, etc."

Ontology note:
> "PlanUnits are the most complicated concepts in Keg2. Plans are hierarchical with child plans and a parent plan (unless its a root). Data in a plan can be sourced from the Parent Plan (Heirs) or the Child Plan (Lines). Plans distribute funds to Awardees. There is a lot."

---

## 3. Summary of Previous Relevant Chapters

`ch07_plan` is the first chapter to draw on every prior chapter simultaneously:

- **ch00_py**: null-safe helpers (`get_0_if_None`, `get_1_if_None`, `get_empty_dict_if_None`, `get_False_if_None`, `get_positive_int`).
- **ch02_allot**: `allot_scale` and `default_grain_num_if_None` — used to distribute a plan's fund pool proportionally among its child plans (via their `poynt` weights) and to distribute award funds among `AwardUnit`s.
- **ch03_contact**: `AwardUnit`, `AwardHeir`, `AwardLine`, `GroupUnit` — the award system from ch03 is embedded into each `PlanUnit`. Groups receive fund flows via award structures.
- **ch04_workforce**: `WorkforceUnit`, `WorkforceHeir` — each plan can declare which groups/contactunits are responsible for carrying it out; these inherit down the tree.
- **ch05_rope**: `RopeTerm`, `create_rope`, `rebuild_rope`, `is_sub_rope`, `find_replace_rope_key_dict`, `all_ropes_between` — the plan tree is entirely organized by rope paths. Every plan has a `parent_rope` and a `plan_label`, and its full identity is its rope.
- **ch06_reason**: `ReasonUnit`, `ReasonHeir`, `FactUnit`, `FactHeir` — each plan can declare conditions (`reasonunits`) and local facts (`factunits`). These are evaluated to determine `plan_active`.

Ch07 also introduces `HealerUnit` (in `healer.py`) and `RangeUnit` (in `range_toolbox.py`) as supporting structures.

---

## 4. Summary of What This Chapter Does

`ch07_plan` defines `PlanUnit` — the central data structure of keg. A `PlanUnit` is a node in a tree of plans rooted at a single root. Each node can be:

- A **container** (`kids: dict[LabelTerm, PlanUnit]`) that groups sub-plans.
- A **pledge** (`pledge: True`) — a declared commitment that can be active or inactive.
- A **fact source** (`factunits`) — a local regulator of incoming facts.
- A **reason-gated plan** (`reasonunits`) — only active if its conditions are met.
- A **funded node** — receives a slice of the parent's fund pool proportional to its `poynt` weight, tracked via `fund_onset` and `fund_cease`.
- A **ranged plan** (`begin`, `close`, `addin`, `numor`, `denom`, `morph`) — can represent a numeric interval that can be inherited and morphed by children.
- A **problem** (`problem_bool`) with designated **healers** (`healerunit`) — plans that flag issues and point to responsible remediation plans.

**Key computed ("heir") attrs** that flow down from parent to child:
- `factheirs` — facts inherited and possibly narrowed by local `factunits`.
- `reasonheirs` — reasons inherited from parent and evaluated against `factheirs`.
- `workforceheir` — inherited workforce assignment.
- `awardheirs` / `awardlines` — fund flow directions inherited and accumulated from children.

**`PlanAttrHolder`** is a parameter-object pattern used to batch-set attrs on a `PlanUnit` without requiring positional arguments for every field — a clean API for the large number of settable properties.

The plan tree is the structural core of keg. Every subsequent chapter either populates this tree, tracks changes to it, or reads from it to produce outputs such as reports.

# ch08_person_logic — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 08 — `ch08_person_logic`**
**"PersonUnit — a complete belief system: one person's plan tree, contacts, and the thinkout engine that brings it all to life"**

---

## 2. Prompt Used to Build This

From `ch08_ref.json`:
> "A person is a personunit, made of contacts and plans. All plans are connected to the planroot, which is given all the funds in a personunit."

Ontology note:
> "A PersonUnit is a single planroot and Contacts. thinkout awards fund debts and creds to Contacts and defines the PersonUnit's agenda."

---

## 3. Summary of Previous Relevant Chapters

Ch08 is the first full integration chapter — it imports from every prior chapter:

- **ch00_py**: null-safe helpers, dict/file utilities.
- **ch02_allot**: `allot_scale`, `valid_allotment_ratio`, `validate_pool_num` — the fund pool and respect pools are allotted across contacts using these tools.
- **ch03_contact**: `ContactUnit`, `contactunit_shop`, `GroupUnit`, `groupunit_shop`, `membership_shop`, `AwardUnit` — contacts and groups are first-class members of `PersonUnit`.
- **ch04_workforce**: `WorkforceUnit` — plans within the person carry workforce assignments.
- **ch05_rope**: All rope navigation functions — `create_rope`, `get_ancestor_ropes`, `get_parent_rope`, `get_forefather_ropes`, `is_sub_rope`, etc. — used to traverse and manage the plan tree.
- **ch06_reason**: `FactUnit`, `ReasonUnit` — facts and reasons are set on plans within the person.
- **ch07_plan**: `PlanUnit`, `PlanAttrHolder`, `planunit_shop` — the plan tree is the core data structure of the person. The `PersonUnit.planroot` is a `PlanUnit`.

A new semantic type is introduced in `ch08_semantic_types.py`: `PersonName` (a `NameTerm`) and `ManaGrain` (a float subtype for mana grain sizing).

---

## 4. Summary of What This Chapter Does

`ch08_person_logic` defines `PersonUnit` — the top-level object representing a single participant in the keg system. A person is the union of:

- **`planroot`**: A single `PlanUnit` that is the root of the entire plan tree. All fund flows begin here.
- **`contacts`**: A dictionary of `ContactUnit`s representing the people this person relates to.
- **Grain and pool parameters**: `fund_pool`, `fund_grain`, `respect_grain`, `mana_grain`, `credor_respect`, `debtor_respect` — the numeric resolution and scale of the person's economy.

**The `thinkout()` method** is the computational core of `PersonUnit`. It is a multi-phase engine that resolves the entire person's state:

1. **Clear and rebuild the plan dict** — flattens the plan tree into a `_plan_dict` keyed by rope.
2. **Set range attrs** — evaluates numeric range inheritance for ranged plans.
3. **Set contact/group respect ledgers** — builds credit and debit ledgers across contacts and groups.
4. **Clear fund attrs** — resets all fund tracking fields.
5. **Set factheirs, workforceheirs, awardheirs** — propagates inherited attrs down the plan tree.
6. **Iterative plan-active loop** — repeatedly traverses the plan tree setting `plan_active` for each plan based on its reasons and facts, until no more changes occur (the system reaches a `rational` constant state, or `max_tree_traverse` is reached).
7. **Set fund attrs** — distributes the `fund_pool` down the tree proportionally by `poynt` weights using `allot_scale`, assigning each plan its `fund_onset` and `fund_cease`.
8. **Set contact/group fund flows** — propagates fund give/take from plan award structures back to contacts and groups.
9. **Set keep attrs** — identifies "keep" plans (healer-designated plans) for some kind of tracking.

**`get_agenda_dict()`** returns the subset of plans that are active pledges with a qualifying reason context — this is the person's current to-do list.

This chapter is the largest in the codebase (~1.4MB) and is the computational core of keg. All subsequent chapters either transform `PersonUnit` data or use it to produce outputs (reports, world coordination, other things to be defined).

# ch09_person_atom — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 09 — `ch09_person_atom`**
**"PersonAtom — the irreducible unit of change for a PersonUnit, enabling versioning and delta-based updates"**

---

## 2. Prompt Used to Build This

From `ch09_ref.json`:
> "Defines PersonAtoms: Irreducible units of change for a PersonUnit."

Ontology note:
> "Any difference between PersonUnits can be expressed as AtomUnits."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_empty_dict_if_None` for safe dict initialization.
- **ch03_contact**: `contactunit_shop`, `awardunit_shop` — atom execution reconstructs or modifies contacts and awards.
- **ch05_rope**: `create_rope`, `get_parent_rope`, `get_tail_label` — rope operations reconstruct plan paths from atom key arguments.
- **ch06_reason**: `factunit_shop` — fact atoms reconstruct fact objects.
- **ch07_plan**: `planunit_shop` — plan atoms reconstruct plan nodes.
- **ch08_person_logic**: `PersonUnit` is the object that atoms are applied to. `person_attr_exists` and `person_get_obj` (from `person_tool.py`) are used during atom execution to check and retrieve the current state before applying a change.

Ch09's `ch09_semantic_types.py` re-exports types from ch03, ch05, ch06 with no additions of its own — it is a pass-through semantic layer.

---

## 4. Summary of What This Chapter Does

`ch09_person_atom` defines `PersonAtom` — a minimal, self-describing record of a single create, update, or delete operation on a `PersonUnit`. The concept is analogous to a database transaction log entry or a git commit diff at the finest granularity.

**`PersonAtom` structure:**
- `dimen` — the "dimension" or table being modified. Valid dimensions (defined in `atom_config.json`) include: `personunit`, `person_contactunit`, `person_contact_membership`, `person_planunit`, `person_plan_awardunit`, `person_plan_factunit`, `person_plan_reasonunit`, `person_plan_reason_caseunit`, `person_plan_healerunit`, `person_plan_laborunit`.
- `crud_str` — one of `"INSERT"`, `"UPDATE"`, `"DELETE"`.
- `jkeys` — the primary key fields that identify the focus object (e.g. `plan_rope` for a plan, `contact_name` for a contact).
- `jvalues` — the attribute fields being set or changed.
- `atom_order` — an integer determining the correct application order (e.g. a plan must exist before its reasons can be inserted).

**Validation:** `is_valid()` checks that `crud_str` is legal, `jkeys` matches the schema for the given `dimen`, and `jvalues` is a subset of the allowed value fields.

**`modify_person_with_personatom(person, atom)`** is the execution function. It dispatches by `dimen` to the appropriate low-level modification function (e.g. `_modify_person_insert_planunit`, `_modify_person_delete_contactunit`), which directly calls the relevant `PersonUnit` setter methods.

**`jvalues_different(dimen, x_obj, y_obj)`** compares two objects of a given dimension to determine what atom(s) would need to be generated to transform one into the other — the basis for diff-generation between two `PersonUnit` states.

Together, `PersonAtom`s form a complete, ordered, reversible description of any transformation between two `PersonUnit` states. This chapter is the foundation for future chapters that use PersonAtoms to communicate indivisible data.

# ch10_person_lesson — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 10 — `ch10_person_lesson`**
**"LessonUnit and PersonDelta — packaging PersonAtoms into named, ordered change sets that express what was learned"**

---

## 2. Prompt Used to Build This

From `ch10_ref.json`:
> "Tools for the creation and organization of lessons, which are collections of personunit atoms for building complex personunits."

Ontology note:
> "Any PersonUnit change implies something has been learned. The LessonUnit that was learned is made of AtomUnits."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: File I/O (`create_path`, `open_json`, `save_json`, `get_json_filename`) used by `lesson_filehandler.py` to persist lessons to disk.
- **ch03_contact**: `ContactUnit`, `MemberShip` — compared field-by-field in `PersonDelta` when generating contact-level atoms.
- **ch05_rope**: `RopeTerm` — used as keys in nested `PersonDelta` structures, particularly for plan-level atom tracking.
- **ch06_reason**: `FactUnit`, `ReasonUnit` — compared in `PersonDelta` when generating reason and fact atoms.
- **ch07_plan**: `PlanUnit` — compared plan-by-plan in `PersonDelta.add_personatoms_plans`.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the before/after objects that `PersonDelta` diffs.
- **ch09_person_atom**: `PersonAtom`, `personatom_shop`, `modify_person_with_personatom`, `jvalues_different`, `sift_personatom` — the atom building blocks that `PersonDelta` organizes and applies.

New semantic types introduced in `ch10_semantic_types.py`:
- `FaceName` (a `NameTerm`) — identifies the source of outside data, the external "face" from which a lesson arrives.
- `MomentRope` (a `RopeTerm`) — the rope address of a Moment, the temporal/contextual location where lessons accumulate.

---

## 4. Summary of What This Chapter Does

`ch10_person_lesson` builds two layered abstractions on top of ch09's atoms: the **delta** (a structured collection of atoms) and the **lesson** (a delta attributed to a face and moment).

**`PersonDelta`** is the workhorse. It holds a nested dictionary of `PersonAtom`s organized by `crud_str → dimen → jkeys`. Its key capabilities:

- `add_all_different_personatoms(before_person, after_person)` — the diff engine. It calls `thinkout()` on both persons, then walks contacts and plans field-by-field, generating INSERT/UPDATE/DELETE atoms for every difference found. This is a complete, schema-aware diff of two `PersonUnit` states.
- `get_sorted_personatoms()` — returns atoms in the correct application order (respecting `atom_order` so that e.g. a plan exists before its reasons are inserted).
- `get_atom_edited_person(before_person)` — applies the delta to a copy of a person, producing the after state.
- `get_minimal_persondelta(delta, person)` — filters a delta to only atoms that would actually change the focus person, eliminating no-ops.

**`LessonUnit`** wraps a `PersonDelta` with provenance metadata:
- `spark_face` (`FaceName`) — who the lesson came from.
- `moment_rope` (`MomentRope`) — where in the temporal/moment structure this lesson belongs.
- `person_name` — who is having their belief system updated.
- `spark_num` — the ordinal position of this lesson within a moment's sequence.
- `lesson_id` / `delta_start` — for sequencing and resuming lesson application.

**`LassoUnit`** (in `lasso.py`) is a small path-construction helper that converts a `MomentRope` into an OS directory path — bridging the rope addressing system to the file system layout used for persisting lesson and gut files.

**`legible.py`** (not read in full) provides human-understandable representations of deltas and atoms for debugging and reporting.

Together, ch10 establishes the full change-tracking and persistence layer: any transformation of a `PersonUnit` can be expressed as a named, ordered, file-backed `LessonUnit` attributed to a specific face and moment.

# ch11_person_listen — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 11 — `ch11_person_listen`**
**"Listening — how one PersonUnit takes in another's agenda and facts, implementing keg's core Levinasian ethic in code"**

---

## 2. Prompt Used to Build This

From `ch11_ref.json`:
> "These tools describe how one personunit listens to another."

Ontology note:
> "To truly listen one must consider the other's perspective. This chapter contains tools that do just that. The listener takes the speaker's PersonUnit, changes the person_name to their own and takes the agenda into their own PersonUnit."

---

## 3. Summary of Previous Relevant Chapters

- **ch02_allot**: `allot_scale` — used in `generate_ingest_list` to distribute the listener's `debtor_respect` pool across the speaker's agenda plans proportionally by their `poynt` weights.
- **ch05_rope**: `get_ancestor_ropes`, `get_first_label_from_rope` — used when ingesting plans to create any missing ancestor plans in the listener's tree.
- **ch07_plan**: `PlanUnit` — the unit of exchange between speaker and listener.
- **ch08_person_logic**: `PersonUnit`, `ContactUnit` — the listener and speaker objects. `create_empty_person_from_person` and `create_listen_basis` (in `basis_person.py`) create clean shells of a person preserving grain/pool parameters.
- **ch10_person_lesson**: `LassoUnit`, `lassounit_shop`, `LessonFileHandler`, `open_gut_file` — used to load speaker gut files from disk when running the full multi-speaker listening pipeline.

`ch11_semantic_types.py` is a pass-through re-export with no new types.

---

## 4. Summary of What This Chapter Does

This is the philosophical center of keg, implemented as code. The `listen_to_speaker_agenda` function embodies the Levinasian concept that genuine listening means taking the other person's perspective seriously and incorporating it into your own understanding.

**`get_perspective_person(speaker, listener_person_name)`** (from `keep_tool.py`) — creates a version of the speaker's `PersonUnit` re-evaluated from the listener's perspective. Facts on the speaker's plan root are reset so the listener can independently assess which of the speaker's pledges are currently active from their own vantage point.

**`listen_to_speaker_agenda(listener, speaker)`** — the core function:
1. Checks the listener has the speaker as a contact (a prerequisite — you can only listen to someone you've acknowledged).
2. Gets the perspective person.
3. If the speaker's belief system is irrational (didn't converge), marks the full speaker `contact_debt_mass` as `irrational_contact_debt_mass` — the listener notes the speaker couldn't provide a coherent agenda.
4. If the speaker has no agenda items, marks the debt as `inallocable_contact_debt_mass`.
5. Otherwise, generates the agenda, scales each plan's `poynt` by `allot_scale` against the listener's `debtor_respect`, and ingests each plan into the listener's tree via `_ingest_single_planunit`.

**`listen_to_speaker_fact(listener, speaker)`** — fills in missing facts in the listener's plan tree by borrowing matching facts from the speaker. This allows the listener to become aware of real-world state they couldn't observe themselves.

**`listen_to_agendas_create_init_job_from_guts`** and **`listen_to_agendas_jobs_into_job`** — orchestrate multi-speaker listening pipelines: for each contact in the listener's debtor roll, load that contact's gut (or job) file and call `listen_to_speaker_agenda`. The distinction between "gut" (a person's own belief system) and "job" (a person's synthesized listening output) is introduced here.

**`create_listen_basis`** (in `basis_person.py`) — creates a fresh `PersonUnit` shell that carries over the grain/pool parameters and contact list from the gut, but with a blank plan tree and reset listen-tracking fields — the starting state for each new listening cycle.

The `irrational` and `inallocable` debt tracking from ch03's `ContactUnit` is here put to use: failed listening is not silently dropped, it is accounted for, maintaining the integrity of the credit/debit ledger.

# ch12_bud — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 12 — `ch12_bud`**
**"BudUnit and TranBook — time-stamped fund distributions and the transaction ledger that records them"**

---

## 2. Prompt Used to Build This

From `ch12_ref.json`:
> "Defines a budget and the tools necessary to create one. Budgets are created when a personunit is given funds that must be distributed."

Ontology note:
> "Defines Budget that distribute funds."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: Nested dict utilities (`get_from_nested_dict`, `set_in_nested_dict`, `del_in_nested_dict`, `exists_in_nested_dict`, `create_csv`) — used to manage the three-level nested structure of `TranBook.tranunits` (`person_name → contact_name → tran_time → amount`).
- **ch02_allot**: `default_pool_num()` — provides the default `quota` value for a `BudUnit`.
- **ch10_person_lesson**: `MomentRope` — `TranBook` is scoped to a moment rope, tying transactions to a specific temporal/contextual location.

New semantic types introduced in `ch12_semantic_types.py`:
- `TimeNum` (an `int`) — represents an instant on the time number line (absolute minutes from a zero-minute).
- `SparkInt` (an `int`) — describes the ordinal position of a data ingestion event (a "spark").

---

## 4. Summary of What This Chapter Does

`ch12_bud` introduces the **time dimension** to keg's fund-flow system. Where ch03 defined how funds are distributed across contacts within a single `PersonUnit` evaluation, ch12 defines how these distributions are recorded as time-stamped transactions and aggregated across time.

**`TranUnit`** is the atomic fund record: a transfer of `amount` (`FundNum`) from a source person (`src`) to a destination contact (`dst`) at a specific `tran_time` (`TimeNum`). It is keg's equivalent of a double-entry ledger line.

**`TranBook`** aggregates `TranUnit`s into a three-level nested dictionary: `person_name → contact_name → tran_time → amount`. It tracks a `moment_rope` scope and provides:
- `add_tranunit` — validates against blocked times and a maximum time ceiling before inserting.
- `get_person_contacts_net` — calculates the net fund position for each `(person_name, contact_name)` pair across all recorded transactions.
- `get_tran_times` — retrieves all distinct transaction times.
- Export to nested dicts and CSV for reporting.

**`BudUnit`** is a scheduled distribution event: at a given `bud_time`, a `quota` of funds is to be distributed. The `celldepth` parameter (default 2) controls how many layers of the listening hierarchy participate in distributing that quota. `calc_magnitude()` verifies that the net of `bud_contact_nets` (positive credits and negative debits) sums to zero — enforcing conservation of funds.

**`PersonBudHistory`** is a person's full history of `BudUnit`s keyed by `bud_time`. It tracks summary statistics: total quota committed, net contact balances, and time range.

**`cell_main.py`** and **`weighted_facts_tool.py`** (not read in full) implement the cell-based distribution logic — the mechanism by which a `BudUnit`'s quota is recursively divided among listening participants up to `celldepth` levels deep, weighted by the contact cred_mass/debt_mass values established in ch03.

Ch12 is the first chapter to introduce `TimeNum` as a first-class type, setting up the time numbers for later.
# ch13_keep — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 13 — `ch13_keep`**
**"RiverCycle and RiverRun — simulating how effectively a healer earns credit by caring for their community"**

---

## 2. Prompt Used to Build This

From `ch13_ref.json`:
> "Builds a simulation that describes how much credit a healer has earned."

Ontology note:
> "Challenging Ch, describes how effective a healer so does not take is."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_0_if_None`, `get_empty_dict_if_None` for safe initialization.
- **ch02_allot**: `allot_scale`, `default_grain_num_if_None`, `validate_pool_num` — the core mechanism by which `mana` (care credit) is distributed across contacts in each river cycle.
- **ch08_person_logic**: `PersonUnit` — `get_patientledger` and `get_doctorledger` extract credit_mass/debt_mass dictionaries directly from a person's contacts.
- **ch12_bud**: `TimeNum`, `SparkInt` — imported via ch13's semantic types, tying the river simulation to the time/transaction layer.

New semantic type introduced in `ch13_semantic_types.py`:
- `ManaNum` (a `float`) — represents a unit of care credit ("mana"), the currency of the river cycle simulation. Distinct from `FundNum` to semantically separate the healer-care economy from the general fund economy.

---

## 4. Summary of What This Chapter Does

`ch13_keep` implements keg's **healer accountability simulation** — a mechanism for evaluating how much care credit a healer has genuinely earned through their keep (their designated responsibility zone).

The metaphor is a river: mana flows from healers to patients and circulates through the community across multiple cycles, accumulating to form a picture of who has given and received care.

**`get_patientledger(person)`** — extracts a ledger of `contact_name → contact_cred_mass` for all contacts with positive credit_mass. These are the people the person cares about (their "patients").

**`get_doctorledger(person)`** — extracts `contact_name → contact_debt_mass` for contacts with positive debt_mass. These are the people who owe care to this person (their "doctors").

**`RiverBook`** — a single person's mana distribution record within one cycle. Given a patient ledger and a total `book_point_amount`, it uses `allot_scale` to distribute the mana proportionally across patients.

**`RiverCycle`** — one full cycle of the river simulation for a healer. It holds `keep_patientledgers` (the patient ledgers of all persons in the healer's keep) and iterates through them, creating a `RiverBook` for each, then aggregates via `create_cylceledger()` — a merged ledger summing all care flows across all river books in the cycle. This cycle ledger becomes the input mana distribution for the next cycle.

**`riverrun.py`** (not read in full) orchestrates multiple `RiverCycle`s in sequence — running the river through N cycles to reach a static distribution. The convergence of the cycle ledger across runs indicates how much each person in the keep has earned relative to their declared responsibilities.

The river metaphor directly operationalizes the Levinasian ethic: a healer's credit is not self-declared but emerges from actual cycles of caring — how much mana flows through them toward others over time.

# ch14_time — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 14 — `ch14_time`**
**"Epoch and Calendar — mapping arbitrary human time structures onto the absolute TimeNum line using plan trees"**

---

## 2. Prompt Used to Build This

From `ch14_ref.json`:
> "Allows arbitrary calendars to be defined for each personunit with minimal configuration."

Ontology note:
> "Keg's ontological structure of time: absolute day minutes length, c400_cycle, variable months, weeks, hours."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path`, `open_json` — used to load `c400_constants.json`, the Gregorian calendar constants file.
- **ch05_rope**: `create_rope`, `get_first_label_from_rope`, `is_sub_rope` — epoch plan trees are organized and navigated using rope paths.
- **ch06_reason**: `CaseUnit`, `FactUnit`, `ReasonUnit` — `epoch_reason.py` generates reason/case structures on a person's plan tree to express time-based conditions (e.g. "active during Monday 8am–10am").
- **ch07_plan**: `PlanUnit`, `planunit_shop`, `all_plans_between`, `get_rangeunit_from_lineage_of_plans` — the epoch calendar is built as a tree of `PlanUnit`s with `denom` and `morph` attrs that encode calendar arithmetic.
- **ch08_person_logic**: `PersonUnit`, `add_frame_to_personunit`, `person_planunit_exists`, `person_planunit_get_obj` — epoch plans are inserted into a person's plan tree and queried.
- **ch12_bud**: `TimeNum` — the absolute integer minute value that the epoch system converts to and from human calendar positions.
- **ch13_keep**: `ManaNum` — re-exported through ch14's semantic types, accumulating the full type chain.

New semantic type: `EpochLabel` (a `LabelTerm`) — identifies a specific epoch unit (e.g. `"hr"`, `"day"`, `"week"`, `"month"`, `"year"`).

---

## 4. Summary of What This Chapter Does

`ch14_time` solves a fundamental problem: keg's reasoning engine operates on abstract numeric ranges (`fact_lower`, `fact_upper`, `reason_lower`, `reason_upper`) but humans think in calendars. This chapter bridges the two.

**The C400 system.** Time in keg is measured in absolute minutes from an epoch. The Gregorian calendar repeats exactly every 400 years (a "c400 cycle" of 210,379,680 minutes). `c400_constants.json` encodes the precise minute-lengths of leap years, non-leap centuries, 4-year cycles, and individual years. These constants are loaded into `C400Constants` and used to build standard `PlanUnit`s with `denom` and `morph` attrs that perform the modular calendar arithmetic.

**Epoch plan trees.** A calendar is represented as a hierarchy of `PlanUnit`s (e.g. `c400_leap → c100 → yr4_leap → year → month → week → day → hour`) where each node's `denom` encodes the number of minutes in that unit relative to its parent's cycle. The `morph=True` flag instructs the plan tree to inherit and transform parent numeric ranges — enabling a `TimeNum` value to be correctly positioned within any calendar level by propagating the range arithmetic down the tree.

**`epoch_reason.py`** provides functions that take a human-understandable time specification (e.g. "Monday, 8am to 10am, weekly") and make `ReasonUnit`/`CaseUnit` structures on a specific plan in the person's tree, using modular arithmetic against the day/week denominators. This is how a person declares "this pledge is active every Monday morning" — expressed as a case with a `reason_divisor` equal to the week length in minutes.

**`epoch_main.py`** provides helpers like `get_day_rope`, `get_week_rope`, `get_year_rope` — pre-built rope paths for standard calendar nodes — and `stan_c400_leap_planunit()` etc. — creation functions for the standard Gregorian plan units.

**`calendar_markdown.py`** generates human-understandable calendar output from a person's plan tree for display and reporting.

In summary, ch14 makes keg's belief system time-aware: a person's plan tree can now express not just what they want to accomplish, but *when* — using any calendar structure they choose, mapped faithfully onto the absolute `TimeNum` line.

# ch15_moment — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 15 — `ch15_moment`**
**"MomentUnit — the full coordination hub: a shared time system, person histories, fund ledger, and multi-pipeline listening orchestrator"**

---

## 2. Prompt Used to Build This

From `ch15_ref.json`:
> "A MomentUnit is a Moment system with the basic requirements: common system of time, contact transactions ledger, etc. Importantly a Moment system must know the state of a person's personunit at any time in the past."

Ontology note:
> "Defines MomentUnits: common time tech, ledger, ContactNames, history of PersonUnits."

---

## 3. Summary of Previous Relevant Chapters

Ch15 is the first true integration chapter — it imports from every prior chapter simultaneously:

- **ch00_py**: File I/O, path creation, directory management.
- **ch02_allot**: `default_grain_num_if_None` for grain initialization.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the core object managed by the moment.
- **ch10_person_lesson**: `LassoUnit`, `lassounit_shop`, `LessonFileHandler`, `open_gut_file`, `save_gut_file` — lesson/gut file management.
- **ch11_person_listen**: `create_listen_basis`, `listen_to_agendas_create_init_job_from_guts`, `listen_to_debtors_roll_jobs_into_job`, `open_job_file`, `save_job_file`, `save_duty_person`, `create_treasury_db_file` — the full listening pipeline.
- **ch12_bud**: `BudUnit`, `PersonBudHistory`, `TranBook`, `TranUnit`, `cellunit_shop`, `cellunit_save_to_dir` — the budget and transaction system.
- **ch14_time**: `EpochUnit`, `add_epoch_planunit`, `epochunit_shop` — the calendar system embedded in each person's gut.

`ch15_semantic_types.py` re-exports the full accumulated type chain with no additions — it is the most complete semantic accumulation point so far.

---

## 4. Summary of What This Chapter Does

`ch15_moment` defines `MomentUnit` — the top-level coordination object for a single keg community. A moment represents a shared context (identified by `moment_rope`) within which multiple persons interact, share beliefs, exchange funds, and track time together.

**`MomentUnit` fields:**
- `moment_rope` — the rope address that scopes this moment (e.g. `";TexasMusic;"`).
- `moment_mstr_dir` — the root directory where all moment data is persisted.
- `epoch` — the shared `EpochUnit` (calendar system) all persons in this moment use.
- `personbudhistorys` — a dictionary of `PersonBudHistory` per person, tracking all scheduled fund distributions.
- `ceckbook` — a `TranBook` recording all fund transactions within the moment.
- `offi_times` — the set of official time points at which distributions have been processed.
- Grain parameters (`fund_grain`, `respect_grain`, `mana_grain`) — shared resolution settings applied when creating new persons.

**The seven pipelines** (documented in the class docstring):
1. `lessons → gut` — apply incoming lesson atoms to a person's core belief file.
2. `gut → dutys` — from a person's gut, derive duty files for each healer they reference.
3. `duty → vision` — from duty files, produce vision files (a healer's synthesized view).
4. `vision → job` — from vision files, produce the job file (what a person will actually do).
5. `gut → job` (direct) — skip vision, build job directly from guts.
6. `gut → vision → job` — full pipeline through visions.
7. `lessons → job` — end-to-end pipeline.

**Key orchestration methods:**
- `create_gut_file_if_none(person_name)` — bootstraps a new person into the moment with an empty gut file.
- `create_init_job_from_guts(person_name)` — loads the person's gut, creates a listen basis, runs the initial job-from-guts listen pass, and saves the job file.
- `rotate_job(person_name)` — loads the current job, runs `thinkout()`, then re-listens to all debtors' job files to produce an updated job. Called repeatedly to converge the community's collective understanding.
- `generate_all_jobs()` — runs the full job-generation cycle for all persons: first creates initial jobs from guts, then rotates `job_listen_rotations` times to let the listening converge.
- `add_epoch_to_guts()` — injects the shared epoch (calendar) plan into all persons' gut files, ensuring everyone operates on the same time system.

`MomentUnit` is the highest-level object in keg's operational stack — it is where individual belief systems (ch08), change tracking (ch09–ch10), listening (ch11), fund flows (ch12–ch13), and time (ch14) all come together into a running community simulation.

# ch16_nabu — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 16 — `ch16_nabu`**
**"NabuUnit — numeric translation layer that converts external time values into the internal TimeNum coordinate system"**

---

## 2. Prompt Used to Build This

From `ch16_ref.json`:
> "A tool that interprets numbers from outside accounting to inside accounting."

Ontology note:
> "Numeric translation is different from word translation, it has to be done after the non-numeric translations."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `set_modular_dict_values` from `dict_toolbox` — applies modular arithmetic to the `otx2inx` mapping, enforcing that epoch differences wrap correctly within the cycle length.
- **ch10_person_lesson**: `FaceName`, `MomentRope` — a `NabuTime` is attributed to a specific face and spark number, matching the lesson provenance model from ch10.
- **ch12_bud**: `TimeNum`, `SparkInt` — the numeric types being converted. The "nabuable" args (`bud_time`, `fact_lower`, `fact_upper`, `reason_lower`, `reason_upper`, `tran_time`, `offi_time`) are all time-related numeric fields from ch12 and ch06.
- **ch14_time**: `EpochLabel` — epoch cycle lengths are the denominators used in the modular translation arithmetic.

`ch16_semantic_types.py` re-exports the full chain through ch14 with no new additions. The chapter introduces no new semantic types of its own.

---

## 4. Summary of What This Chapter Does

`ch16_nabu` addresses a problem that arises in any multi-party system: different participants may use different time reference points. An external face might report times relative to their own epoch (e.g. "day 5 of my calendar") while the internal system tracks absolute `TimeNum` minutes. Nabu is the translation bridge.

The name "Nabu" is the ancient Mesopotamian god of writing and wisdom — an appropriate name for a chapter that interprets and transcribes numeric values across reference frames.

**`NabuTime`** is the core object, keyed by `(spark_face, spark_num)` — the same provenance identifiers used in lessons. It holds an `otx2inx` dictionary mapping:
- Key: `otx_epoch_length` — the cycle length of the external time system (e.g. 525,600 minutes = 1 year).
- Value: `inx_epoch_diff` — the offset (in minutes) to add when converting from external to internal time.

The mapping is stored modularly: `set_modular_dict_values` applies `value % key` to each entry, ensuring differences are always within one cycle. This handles cases like "the external calendar is 3 months ahead of the internal one."

**`reveal_inx(otx_epoch_length, otx_value)`** is the translation function: it adds the stored `inx_epoch_diff` to the external value, then takes it modulo the epoch length — producing the correct internal `TimeNum` position within the cycle.

**`nabu_config.py`** defines which argument fields are "nabuable" — they carry raw external time values that need translation before being used internally:
- `bud_time`, `tran_time`, `offi_time` — scheduling and transaction times.
- `fact_lower`, `fact_upper`, `reason_lower`, `reason_upper` — the numeric bounds in fact and reason conditions.

The config also defines the `nabu_timenum` dimension for atom-style CRUD operations, and `set_nabuable_otx_inx_args` which expands nabuable field names into their `_otx` / `_inx` variants — used downstream when storing both the external and converted versions of a value side by side.

**`inherit_timenabu(new, old)`** enforces that newer `NabuTime` objects (higher `spark_num`) from the same face supersede older ones — maintaining the same ordered-inheritance pattern established in ch10's lesson sequencing.

Ch16 completes the "outside → inside" translation infrastructure. Ch17 handles word/string translation; ch16 handles number/time translation. Together they ensure that external data from any face can be faithfully and consistently interpreted in the internal coordinate system.

# ch17_translate — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 17 — `ch17_translate`**
**"TranslateUnit — string-level translation layer mapping external (otx) terms to internal (inx) terms across all string types"**

---

## 2. Prompt Used to Build This

From `ch17_ref.json`:
> "A tool that translates persons from outside language to inside language."

Ontology note:
> "Demonstrates Ontological structure of translation of LabelTerms, RopeTerms, NameTerms, GroupTerms."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `dict_toolbox` string-search utilities (`str_in_dict`, `str_in_dict_keys`, `str_in_dict_values`, `get_str_in_sub_dict`) — used in `MapCore` to validate that the `unknown_str` sentinel does not appear in translation mappings.
- **ch05_rope**: `create_rope`, `create_rope_from_labels`, `get_all_rope_labels`, `get_parent_rope`, `get_tail_label` — `RopeMap` uses these to translate ropes label-by-label, applying the `LabelMap` to each segment of a path.
- **ch10_person_lesson**: `FaceName` — each map and `TranslateUnit` is attributed to a specific face and `spark_num`, maintaining provenance.
- **ch12_bud**: `SparkInt` — the ordering integer for inheritance resolution.

`ch17_semantic_types.py` re-exports through ch12/ch10 with no new types. The chapter introduces one configuration constant: `unknown_str` (default `"UNKNOWN"`) — the sentinel value used when a translation mapping cannot be found.

---

## 4. Summary of What This Chapter Does

`ch17_translate` implements the **string translation system** — the counterpart to ch16's numeric translation. Where ch16 converts external time numbers to internal `TimeNum` values, ch17 converts external string terms (names, labels, rope paths, group titles) to their internal equivalents.

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

**`TranslateUnit`** composes all four maps into a single per-face translation object. It exposes unified methods (`set_titleterm`, `set_nameterm`, `set_labelterm`, `set_ropeterm`) and a `get_mapunit(obj_type)` dispatcher. It also holds top-level `otx_knot`/`inx_knot` and `unknown_str` settings that are propagated to all child maps via `_check_all_core_attrs_match`.

**`inherit_*` functions** (`inherit_labelmap`, `inherit_namemap`, etc.) merge an older map into a newer one — the same ordered-inheritance pattern used in ch10 lessons and ch16 nabu, ensuring that more recent translations from the same face supersede older ones.

Together ch16 (numeric translation) and ch17 (string translation) form the complete "outside-to-inside" interface layer. All data arriving from external faces passes through these two chapters before being processed by the internal keg machinery.

# ch18_db_tool — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 18 — `ch18_db_tool`**
**"Database Toolbox — SQLite helper utilities for creating tables, inserting CSVs, and querying keg data from relational storage"**

---

## 2. Prompt Used to Build This

From `ch18_ref.json`:
> "Create some standard tools for creating sqlite sql statements. Some are complicated."

Ontology note:
> "Beginning of a mapping from objects to relational databases."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `ch18_db_tool` is structurally parallel to ch00 — it is a pure utility chapter with no domain logic, just as ch00 provided Python/file toolboxes. The main difference is ch18 uses SQLite rather than the file system.
- All prior semantic types are re-exported through `ch18_semantic_types.py` (the full chain through ch14) — but ch18's own code imports only from Python's `sqlite3`, `csv`, `pandas`, `re`, and `dataclasses` standard/third-party libraries. It does not import from any prior keg chapter in `db_toolbox.py` itself.

This is a deliberate design: ch18 is a low-level database infrastructure chapter — like ch00, it intentionally avoids domain dependencies so it can be used freely by all higher chapters.

---

## 4. Summary of What This Chapter Does

`ch18_db_tool` provides two files of SQLite utility functions that later chapters use to persist and query keg data in relational databases.

**`db_toolbox.py`** — the main utility library:

- **Type conversion**: `sqlite_obj_str(x_obj, sqlite_datatype)` converts Python objects (including booleans, None) to properly quoted SQLite literal strings. `sqlite_to_python(query_value)` converts SQLite results back to Python values. These handle the type-mapping quirks between Python's type system and SQLite's loose typing.

- **Table introspection**: `get_db_tables(conn)` lists all tables in a database; `get_db_columns(conn)` returns column names and types; `get_table_columns(conn, tablename)` retrieves column names for a specific table. `db_table_exists(conn, tablename)` checks for table existence before operations.

- **Table creation**: `create_table_from_columns(conn, tablename, columns_list, column_types)` generates and executes a `CREATE TABLE` statement. `create_table_from_csv(csv_file_path, conn, table_name, column_types)` reads a CSV header and creates a matching table automatically.

- **Data insertion**: `insert_csv(csv_file_path, conn, table_name)` bulk-inserts CSV rows into a table, handling type coercion and NULL conversion. `create_table2table_agg_insert_query(...)` builds a complex aggregation INSERT query that copies and aggregates data from one table into another — used for producing summary/rollup tables.

- **Data quality**: `get_nonconvertible_columns(row_dict, col_types)` identifies cells that cannot be coerced to their expected type. `delete_all_duplicate_rows(conn, tablename, key_columns)` removes duplicate rows while keeping one copy. `create_select_inconsistency_query(conn, tablename, focus_columns, exclude_columns)` generates a GROUP BY/HAVING query that finds rows where non-key columns disagree across identical key groups — useful for detecting data inconsistencies in ledger tables.

- **Column utilities**: `get_sorted_cols_only_list(existing_columns, sorting_columns)` returns an intersection of columns in a specified order — used to produce consistently-ordered SELECT lists.

**`notebook_toolbox.py`** provides Jupyter-notebook-oriented utilities — helpers for displaying query results and database state in an interactive analysis context.

Ch18 is the "ch00 of persistence" — a deliberately dependency-free utility layer. It carries the full semantic type chain in its `_ref` file as preparation for the ETL chapters that will use both these database tools and the domain objects to build the full data pipeline.

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
- **ch18_db_tool**: `get_sorted_cols_only_list` — used to enforce consistent column ordering across all brick DataFrames.

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

# ch22_etl_config — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 22 — `ch22_etl_config`**
**"ETL Configuration — dimension abbreviations, stage-type ordering, SQL generation, and Excel brick collection for the full data pipeline"**

---

## 2. Prompt Used to Build This

From `ch22_ref.json`:
> "All the tools used by WorldDirs to create MomentUnits."

Ontology note:
> "Defines the tools that move data through pipelines."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path`, `open_json` — config files are loaded via file toolbox.
- **ch09_person_atom**: `get_delete_key_name` — used when constructing DELETE-type SQL stage queries to identify the correct key column.
- **ch16_nabu**: `get_context_nabuable_args`, `set_nabuable_otx_inx_args` — ETL config expands nabuable columns into `_otx`/`_inx` pairs in SQL table definitions.
- **ch17_translate**: `set_translateable_otx_inx_args` — same expansion for translateable string columns.
- **ch18_db_tool**: `get_create_table_sqlstr` — used to generate CREATE TABLE statements for each pipeline stage.
- **ch20_brick**: `get_brick_config_dict`, `get_brick_sqlite_types`, `get_default_sorted_list`, `get_brick_types`, `get_quick_bricks_column_ref` — all brick schema information flows through ch22.

---

## 4. Summary of What This Chapter Does

`ch22_etl_config` is the configuration and orchestration backbone of the ETL pipeline — it defines the stage ordering, dimension abbreviations, SQL generation utilities, and Excel file collection tools that the actual ETL execution chapters consume.

**`etl_config.py`** — the core configuration module:

- `ALL_DIMEN_ABBV7` and `ALL_DIMEN_ABBV2` — two abbreviation sets for all 23 dimension types (e.g. `"moment_ceckbook"` → `"MMTCECK"` / `"MP"`). These abbreviated names are used as table name prefixes throughout the SQLite ETL database.
- `get_dimen_abbv7(dimen)` and `get_dimen_abbv2(dimen)` — dispatch functions mapping full dimension names to abbreviations.
- `get_etl_stage_types_config_dict()` — loads `etl_stage_types_config.json`, which defines the ordered sequence of ETL stages (e.g. `b_raw` → `b_agg` → `b_vld` → `s_raw` → `s_agg` → `s_vld` → `h_raw` → ...). Each stage has a `stage_type_order` integer determining its position in the pipeline.
- `get_stage_create_table_sqlstr(dimen, stage_type)` — generates the `CREATE TABLE` SQL for a specific dimension at a specific pipeline stage, incorporating `_otx`/`_inx` column expansions for translated and nabu fields.

**`brick_collector.py`** — Excel discovery and sheet reordering:

- `BrickFileRef` — a dataclass identifying a specific brick sheet within an Excel file: `file_dir`, `filename`, `sheet_name`, `brick_type`.
- `get_all_brickfilerefs(dir)` — scans a directory for `.xlsx` files, finds all sheets with names that contain a known `brick_type`, validates that the sheet has the required columns, and returns a list of `BrickFileRef` objects ready for ETL loading.
- `reorder_etl_db_sheets(filepath)` — reorders sheets in an Excel output file to match the canonical stage-type ordering defined in `etl_stage_types_config.json`.

**`etl_sqlstr.py`** — SQL string generation for sound and heard tables:

- `create_prime_tablename(dimen, stage, crud)` — constructs table names like `"PRNPLAN_s_raw_put"` or `"MMTBUDD_s_raw"` following the `ABBV7_stage_crud` naming convention.
- `create_sound_and_heard_tables(cursor)` — iterates all dimensions and all stage types, generating and executing `CREATE TABLE IF NOT EXISTS` statements for every table in the full pipeline.

**`etl_csv.py`** provides CSV export utilities for pipeline stage tables.

The chapter has no new semantic types of its own — `ch22_semantic_types.py` re-exports through ch20. Ch22's role is purely infrastructural: it defines the names, shapes, and ordering of every table in the ETL database before any data flows through it.

# ch23_idea_src — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 23 — `ch23_idea_src`**
**"Idea Source — the first ETL stage: reading raw Excel idea sheets, running fission transforms, and writing validated brick DataFrames"**

---

## 2. Prompt Used to Build This

From `ch23_ref.json`:
> "Defines the 'Idea Src' process. Where valid 'Idea' data is sparked and moved to Bricks."

Ontology note:
> "Source Ideas are validated some and then converted to Bricks."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `delete_dir`, `set_dir` — idea output directories are wiped and recreated on each run.
- **ch05_rope**: `default_knot_if_None` — used in `fission_add_ancestor_rope_rows` to parse rope paths and infer missing ancestor plan rows.
- **ch20_brick**: `create_brick_df_from_file`, `save_sheet`, `_sort_dataframe` — bricks are read from and written to Excel via ch20 tooling.
- **ch22_etl_config**: `get_etl_stage_types_config_dict` — used to determine valid stage type names during idea processing.
- **ch99_glossary**: `get_keg_elements_sort_order` — column sort order is enforced via the master glossary.

`ch23_semantic_types.py` re-exports through ch20 with no additions.

---

## 4. Summary of What This Chapter Does

`ch23_idea_src` is the **entry point of the ETL pipeline** — where raw human-authored Excel data ("ideas") is first read, lightly transformed, and written out as structured brick DataFrames ready for validation in later chapters.

**`fission_step.py`** — data transformation functions applied to raw idea DataFrames before they become bricks. Each function is a pure DataFrame → DataFrame transform:

- `fission_add_ancestor_rope_rows(df)` — inspects all `plan_rope` values in the DataFrame; for any rope that references an ancestor path not already present as a row, it inserts synthetic ancestor rows (with `pledge=0`, `poynt=None`). This ensures the plan tree is complete before it reaches the person object.
- `fission_set_pledge_to_one(df)` — sets all `pledge` values to 1 (marking all rows as active pledges).
- `fission_set_plan_rope_from_health_label(df)` — constructs `plan_rope` values by combining `moment_rope` and `health_label` columns, with strict null validation raising `ValueError` on missing values.
- `fission_set_moment_rope_from_moment_label(df)` — constructs `moment_rope` from a `moment_label` column.
- `run_fission_steps(df, fission_config)` — dispatches the configured sequence of fission steps for a given brick type, as specified in `idea_config.json`.

**`idea2brick.py`** — the main orchestration layer:

- `get_spark_faces_from_df(df)` / `get_spark_faces_from_files(directory)` — extract the set of distinct `spark_face` values present in idea files, used to validate provenance before loading.
- `get_max_spark_num_from_files(directory)` — finds the highest `spark_num` across all idea files, used to sequence the next ingestion spark.
- The main pipeline function (not fully read) reads each Excel idea file, applies fission steps per sheet, validates column presence against the brick schema, and writes valid rows to brick-format CSV/Excel outputs.

**`idea_config.json`** defines per-brick-type fission step sequences — which transforms to apply and in which order when converting a given idea sheet type to its corresponding brick format.

The "idea → brick" boundary is keg's human-computer interface: ideas are loosely structured, human-friendly spreadsheets; bricks are precisely schema-validated tabular records. Ch23 bridges the two.

# ch24_etl_brick — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 24 — `ch24_etl_brick`**
**"ETL Brick — the multi-stage SQLite pipeline that validates brick data from raw through aggregated, validated, and sound-ready tables"**

---

## 2. Prompt Used to Build This

From `ch24_ref.json`:
> "Defines the 'Etl Bricks' process. Where valid 'Brick' data is translated into clean 'Sound' data."

Ontology note:
> "Bricks have data type validations and then are turned into Sound data."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `create_path` for file path construction.
- **ch18_db_tool**: `create_insert_into_clause_str`, `create_select_query`, `create_table_from_columns`, `create_type_reference_insert_sqlstr`, `db_table_exists`, `delete_all_duplicate_rows`, `get_create_table_sqlstr`, `get_db_tables`, `get_grouping_with_all_values_equal_sql_query`, `get_nonconvertible_columns`, `get_table_columns` — ch24 is the primary consumer of ch18's full SQL utility library.
- **ch20_brick**: `get_brick_format_filename`, `get_brick_sqlite_types`, `get_brick_types`, `get_brickref_from_file`, `get_brickref_obj`, `create_brick_df_from_file`, `create_brick_sorted_table`, `get_default_sorted_list` — all brick schema operations.
- **ch22_etl_config**: `BrickFileRef`, `get_all_brickfilerefs`, `create_prime_tablename`, `create_sound_and_heard_tables`, `etl_sqlstr` — stage naming and table creation helper tools.

`ch24_semantic_types.py` adds `SheetName` from ch20 to the full accumulated type chain.

---

## 4. Summary of What This Chapter Does

`ch24_etl_brick` executes the **four-stage brick validation pipeline** entirely within SQLite, transforming raw Excel brick data into clean, validated "sound" tables ready for person/moment reconstruction.

**Stage 1 — `etl_brick_dfs_to_brixk_raw_tables(cursor, bricks_src_dir)`**
Discovers all brick Excel files in the source directory via `get_all_brickfilerefs`, reads each sheet into a DataFrame, sorts columns to the canonical order, prepends `file_dir`/`filename`/`sheet_name` provenance columns, creates a `{brick_type}_b_raw` SQLite table, and inserts each row. On insertion, `get_nonconvertible_columns` checks every cell against the expected SQLite type — any row with type errors has the offending columns nulled and an `error_message` written. Duplicate rows are deleted at the end.

**Stage 2 — `etl_brixk_raw_tables_to_brixk_agg_tables(conn)`**
For each `_b_raw` table, produces a `{brick_type}_b_agg` table. Uses `get_grouping_with_all_values_equal_sql_query` (from ch18) to GROUP BY the brick's key columns and filter to only rows where all value columns are consistent across duplicates — i.e. rows where the same key has conflicting values are excluded. Only rows with no `error_message` from stage 1 are considered. This is the **deduplication and consistency check** stage.

**Stage 3 — Spark validation (`etl_brixk_agg_tables_to_sparks_b_agg_table` + `etl_sparks_b_agg_table_to_sparks_b_vld_table`)**
Aggregates all `spark_num`/`spark_face` pairs from every `_b_agg` table into a `sparks_b_agg` table. Flags any `spark_num` that maps to more than one `spark_face` as invalid (a spark number must belong to exactly one face). Valid sparks are written to `sparks_b_vld`. This enforces the provenance rule: a single spark event cannot be attributed to two different faces.

**Stage 4 — `etl_brixk_agg_tables_to_brixk_vld_tables(conn)`**
Produces `{brick_type}_b_vld` by JOINing the `_b_agg` table against `sparks_b_vld` — only rows with validated `spark_num` pass through. This is the final validated brick layer.

**Stage 5 — `etl_brixk_vld_tables_to_sound_raw_tables(cursor)`**
Maps validated brick rows into "sound" dimension tables (`{ABBV7}_s_raw_put` / `{ABBV7}_s_raw_del`) by intersecting the brick's columns with the focus sound table's columns and inserting the common fields. The `brick_type` column is prepended to each inserted row for traceability. This produces the `s_raw` tables that downstream chapters will aggregate into `s_agg`, validate into `s_vld`, and ultimately use to reconstruct `PersonUnit` and `MomentUnit` objects.

The table naming convention throughout: `{brick_type}_b_{stage}` for brick-level tables, `{ABBV7}_s_{stage}_{crud}` for sound-level tables.

# ch25_sound — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 25 — `ch25_sound`**
**"Sound — the ETL stage where validated brick data is aggregated, inconsistency-checked, and translated from otx to inx before becoming heard data"**

---

## 2. Prompt Used to Build This

From `ch25_ref.json`:
> "Defines the 'Sound' process. Where valid 'Brick' data is translated into clean 'Heard' data."

Ontology note:
> "Bricks are turned into Sound concepts, Translation is applied and produces Heard data."

---

## 3. Summary of Previous Relevant Chapters

- **ch05_rope**: `default_knot_if_None` — used when validating that label/name/rope columns in sound-agg tables do not contain the knot character.
- **ch17_translate**: `get_translate_labelterm_args`, `get_translate_nameterm_args`, `get_translate_ropeterm_args`, `get_translate_titleterm_args`, `get_translates_column_ref`, `default_unknown_str_if_None` — the full translation type registry drives which sound-agg columns need knot-error checking and which need `otx → inx` resolution.
- **ch18_db_tool**: `create_update_inconsistency_error_query`, `delete_all_duplicate_rows`, `get_table_columns` — SQL-level data quality tools.
- **ch20_brick**: `get_brick_dimen_ref` — the master brick dimension registry drives which `s_raw` and `s_agg` tables exist and need processing.
- **ch22_etl_config**: `etl_sqlstr` — nearly all SQL strings used in ch25 are generated by ch22's SQL-string generation functions. Ch25 is the executor; ch22 is the generator.

`ch25_semantic_types.py` re-exports through ch20 with no additions.

---

## 4. Summary of What This Chapter Does

`ch25_sound` advances data through three sound stages (`s_raw → s_agg → s_vld`) and then into the first heard stage (`h_raw`), applying translation on the way.

**`etl_sound_raw_tables_to_sound_agg_tables(cursor)`** — two steps:
1. `set_sound_raw_tables_error_message` — for each dimension, runs an inconsistency-detection query against its `s_raw` table; any row where non-key columns conflict across identical key groups gets an `error_message`.
2. `insert_sound_raw_selects_into_sound_agg_tables` — copies error-free rows from `s_raw` into `s_agg`, deduplicating afterward.

**Translation pipeline** (`etl_translate_sound_agg_tables_to_translate_sound_vld_tables`):
This is the most complex function in ch25. It processes the four translation dimensions (`trlname`, `trltitl`, `trllabe`, `trlrope`) plus the shared `trlcore` (which holds `otx_knot`, `inx_knot`, `unknown_str` per face) through their own `s_raw → s_agg → s_vld` cycle:
1. Aggregates all four translate dimensions' `s_agg` rows into a unified `trlcore_s_raw` table.
2. Flags inconsistencies (same `spark_face` with conflicting `otx_knot`/`inx_knot`) in `trlcore_s_raw`.
3. Promotes consistent rows to `trlcore_s_agg` (MAX aggregation on knot/unknown columns per face).
4. Promotes to `trlcore_s_vld`, filtering on valid knot/unknown_str values.
5. Fills in `trlcore_s_vld` entries for any `spark_face` that appears in moment/person sound-agg tables but has no explicit translation core — assigning default knot and unknown values.
6. Runs knot-error checks on each translation dimension's `s_agg` table — flagging rows where the `otx` value contains the knot character (which would make it an invalid label/name).
7. Promotes valid rows from each translate `s_agg` to `s_vld`.

**`etl_sound_agg_tables_to_sound_vld_tables(cursor)`** — promotes all moment/person dimension rows from `s_agg` to `s_vld` by running the pre-generated `get_insert_into_sound_vld_sqlstrs` queries and deduplicating.

**`etl_sound_vld_tables_to_heard_raw_tables(cursor)`** — the final step of ch25: copies `s_vld` rows into `h_raw` tables, using `exclude_postfix="_inx"` in deduplication so that `_inx` columns (not yet populated) don't trigger false duplicate detection. The `_inx` columns are populated by later steps.

The sound layer is where the data first becomes semantically trustworthy — type-validated in ch24, consistency-checked and translation-prepared in ch25.

# ch26_heard — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 26 — `ch26_heard`**
**"Heard — applying otx→inx string translation and TimeNum conversion to produce fully resolved heard tables, then reconstructing MomentUnit JSON from them"**

---

## 2. Prompt Used to Build This

From `ch26_ref.json`:
> "Defines the 'Heard' process. Where valid 'Sound' data is aggregated into clean 'lego' data."

Ontology note:
> "Sounds are turned into trusted concepts, Nabu interpreted (time conversion included) and produces Moment and Person objects."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `set_in_nested_dict`, `get_level1_dirs`, `save_file`, `save_json` — moment JSON files are assembled from query results using nested dict helpers and persisted to disk.
- **ch05_rope**: `create_rope` — used when constructing `LassoUnit` objects to navigate moment directory paths.
- **ch10_person_lesson**: `create_moment_json_path`, `create_moments_dir_path`, `LassoUnit`, `lassounit_shop` — the moment file system layout is defined in ch10 path helpers.
- **ch12_bud**: `MomentRope` — scopes all heard table queries.
- **ch17_translate**: `get_translate_args_obj_types`, `translateable_obj_types` — drives which `h_raw` columns need `_inx` values populated via translation lookups.
- **ch18_db_tool**: `delete_all_duplicate_rows`, `get_row_count`, `get_table_columns` — SQL utilities.
- **ch22_etl_config**: `etl_sqlstr` functions — `create_update_heard_raw_empty_inx_col_sqlstr`, `create_update_heard_raw_existing_inx_col_sqlstr`, `get_insert_heard_agg_sqlstrs`, `get_insert_heard_vld_sqlstrs`, `update_heard_agg_timenum_columns`, `get_moment_heard_select1_sqlstrs`, `get_person_heard_vld_tablenames`, `save_to_split_csvs` — all SQL generation delegated to ch22.

---

## 4. Summary of What This Chapter Does

`ch26_heard` is the final ETL stage before data becomes usable `PersonUnit` and `MomentUnit` objects. It advances data through `h_raw → h_agg → h_vld` and then reconstructs structured files from the validated heard tables.

**`etl_heard_raw_tables_to_heard_agg_tables(cursor)`** — three steps:
1. `set_all_heard_raw_inx_columns` — for every `_otx`-suffixed column in every `h_raw` table, determines the translation type (`NameTerm`, `TitleTerm`, `LabelTerm`, or `RopeTerm`) from the ch17 translate-args registry. If the column's base type is translateable, runs an UPDATE query that JOINs against the validated `trl{type}_s_vld` table to fill in the `_inx` value. For rows where no translation mapping exists, goes back to copying the `_otx` value into `_inx` directly (pass-through for untranslated terms).
2. INSERT into `h_agg` tables from `h_raw`, deduplicating while excluding `_inx` columns from duplicate comparison.
3. `update_heard_agg_timenum_columns` — applies NabuTime conversion to all time-numeric columns (`bud_time`, `fact_lower`, `fact_upper`, `reason_lower`, `reason_upper`, `tran_time`, `offi_time`) in `h_agg` tables: reads the `_otx` value, applies the epoch-length modular offset from the validated nabu table, and writes the result to the `_inx` column. This is where ch16's numeric translation is finally executed against real data.

**`etl_heard_agg_tables_to_heard_vld_tables(cursor)`** — promotes `h_agg` rows to `h_vld` via pre-generated INSERT/SELECT queries, deduplicating.

**`get_moment_dict_from_heard_tables(cursor, moment_rope)`** — the reconstruction function. Runs a series of SELECT queries against the fully validated `h_vld` tables for a given `moment_rope` and assembles a nested Python dict representing the complete `MomentUnit` state: `momentunit` row for top-level attributes, `moment_ceckbook` rows for `TranUnit`s (nested `person_name → contact_name → tran_time → amount`), `moment_budunit` rows for `BudUnit`s, and epoch configuration rows (hours, months, weekdays, offi_times).

**`etl_heard_vld_tables_to_mind_moment_jsons(cursor, moment_mstr_dir)`** — iterates all `moment_rope`s from `momentunit_h_vld`, calls `get_moment_dict_from_heard_tables` for each, and writes the result as a `moment.json` file to the appropriate directory. The inline comment notes a known architectural tension: using rope-based file paths is idiomatic but problematic when `moment_rope` contains characters that don't translate to valid OS paths — a hash-based directory scheme is suggested as an alternative.

**`etl_heard_raw_tables_to_lego_moment_ote1_agg`** — builds the `moment_ote1_agg` table: a mapping of `(moment_rope, person_name, spark_num) → bud_time`, which tells later chapters which spark to apply at which budget time.

**`etl_heard_vld_to_lego_spark_person_csvs`** — splits validated `h_vld` person dimension tables into per-moment/per-person/per-spark CSV files on disk, organized as `moments/{moment}/persons/{person}/sparks/{spark_num}/{dimen_h_vld_put.csv}`. These CSVs are the raw material later chapters convert into `LessonUnit`s.

# ch27_lego — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 27 — `ch27_lego`**
**"Lego — the final ETL stage: assembling PersonAtoms from heard CSVs into LessonUnits, applying them cumulatively to produce gut files, running the listening pipeline, and loading job PersonUnits into the database"**

---

## 2. Prompt Used to Build This

From `ch27_ref.json`:
> "Defines the lego stage of data. Source of Job Persons, complete Moment data."

Ontology note:
> "The most static and clear of all etl stages. Everything has been calculated except for audience idea."

---

## 3. Summary of Previous Relevant Chapters

Ch27 is the final integration point of the entire ETL pipeline. It imports from more chapters than any other single file:

- **ch00_py**: File I/O, path, directory walking.
- **ch05_rope**: `create_rope` for moment rope construction.
- **ch08_person_logic**: `PersonUnit`, `personunit_shop` — the object being reconstructed.
- **ch09_person_atom**: `get_person_dimens`, `personatom_shop` — atoms are reconstructed from CSV rows.
- **ch10_person_lesson**: `get_minimal_persondelta`, `LassoUnit`, `lassounit_shop`, `LessonUnit`, `get_lessonunit_from_dict`, `lessonunit_shop`, path helpers — lessons are the vehicle for applying deltas.
- **ch11_person_listen**: `open_job_file` — job files are loaded for DB insertion.
- **ch12_bud**: Path helpers, `TranBook`, `collect_person_spark_dir_sets`, `get_persons_downhill_spark_nums`, `open_person_file`.
- **ch15_moment**: `create_moment_persons_cell_trees`, `set_cell_tree_cell_mandates`, `set_cell_trees_decrees`, `set_cell_trees_found_facts`, `create_bud_mandate_ledgers`, `open_moment_file`.
- **ch18_db_tool**: `delete_all_duplicate_rows`, `get_db_tables`.
- **ch20_brick**: `get_brick_sqlite_types` for type-aware CSV parsing.
- **ch22_etl_config**: Path helpers, `create_job_tables`, `create_prime_tablename`, `save_to_split_csvs`.
- **ch27_lego.lego_job2db**: `insert_job_obj` — inserts a fully evaluated job `PersonUnit` into all job-tracking SQLite tables.

---

## 4. Summary of What This Chapter Does

`ch27_lego` is where all ETL threads converge into running `PersonUnit` and `MomentUnit` objects.

**`etl_moment_ote1_agg_csvs_to_jsons`** — converts the `moment_ote1_agg` CSVs (from ch26) into JSON dicts mapping `person_name → bud_time → spark_num`, creating the lookup table that tells the system which spark to apply at each budget time.

**`etl_lego_spark_person_csvs_to_lesson_json`** — walks the `moments/{moment}/persons/{person}/sparks/{spark_num}/` directory tree (written by ch26) and for each spark directory, reads all `h_vld_put` and `h_vld_del` CSVs, reconstructs `PersonAtom`s row by row (skipping provenance columns `spark_face`, `spark_num`, `moment_rope`, `person_name`), assembles them into a `LessonUnit`'s `PersonDelta`, and saves the result as `spark_all_lesson.json`.

**`etl_lego_spark_lesson_json_to_spark_inherited_personunits`** — the cumulative application loop. For each person across all moments, it walks sparks in order. For each spark:
1. Loads the previous spark's `PersonUnit` from disk (or creates an empty one for spark 0).
2. Loads the current spark's `LessonUnit` from `spark_all_lesson.json`.
3. Calls `get_minimal_persondelta` to strip no-op atoms.
4. Applies the delta to the previous `PersonUnit` to produce the current one.
5. Saves the current `PersonUnit` as `personspark.json`.
6. Saves a minimal `expressed_lesson.json` (only the atoms that actually changed something).

This is the moment when the full atom-based version history from ch09/ch10 is replayed against real data.

**`etl_spark_inherited_personunits_to_mind_gut`** — identifies the max spark number for each person (the most recent state) and copies that `PersonUnit` JSON to the person's `gut` file — their current belief system.

**`add_lego_epoch_to_mind_guts`** — injects the shared epoch into all gut files via `MomentUnit.add_epoch_to_guts()`.

**`etl_mind_guts_to_mind_jobs`** — calls `MomentUnit.generate_all_jobs()` for each moment, running the full listening pipeline (ch11) across all persons to produce job files.

**`etl_mind_job_jsons_to_job_tables`** — loads each person's job `PersonUnit` and inserts it into the SQLite job tables via `lego_job2db.insert_job_obj`, making the final computed state queryable from SQL.

**`calc_moment_bud_contact_mandate_net_ledgers`** — orchestrates the full cell-tree pipeline from ch15: builds root cells from `ote1` data, creates cell trees, propagates found facts, computes decrees, sets mandates, and generates bud mandate ledgers — the fund-distribution calculation for each budget time point.

**`create_last_run_metrics_json`** — records the max `spark_num` seen across all `b_agg` tables, providing a aguamark for the next ETL run.

`lego_job2db.py` provides `insert_job_obj` which calls `thinkout()` on the job `PersonUnit` and inserts the resulting contacts, memberships, plans, reasons, facts, and fund metrics into dedicated `_job` SQLite tables — making the fully evaluated, post-listening state of every person queryable.

# ch30_idea_dst — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 30 — `ch30_idea_dst`**
**"Idea Destination — exporting the fully processed world state back to human-understandable Excel idea files for external audiences"**

---

## 2. Prompt Used to Build This

From `ch30_ref.json`:
> "Defines how ideas for outside audiences are created."

Ontology note:
> "Tools for creating ideax_dst files with for-audience translation."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `delete_column_from_csv_string`, `replace_csv_column_from_string` — used to strip or replace `spark_num`/`spark_face` columns before writing output files.
- **ch05_rope**: `create_rope`, `default_knot_if_None` — moment ropes are constructed when walking the moment directory tree.
- **ch10_person_lesson**: `create_moments_dir_path`, `lassounit_shop` — path navigation for the moment file system.
- **ch12_bud**: `open_person_file` — gut and job `PersonUnit` JSON files are loaded for export.
- **ch15_moment**: `open_moment_file` — `MomentUnit` objects are loaded for export.
- **ch20_brick**: `csv_dict_to_excel`, `prettify_excel_file`, `remove_empty_sheets` — the final output is an Excel file with one sheet per brick/idea type.
- **ch22_etl_config**: `create_moment_mstr_path`, `create_world_db_path`, `create_prime_tablename`, `create_sound_and_heard_tables` — path helpers and SQL table names for loading translation data.
- **ch23_idea_src**: `add_momentunit_to_idea_csv_strs`, `add_personunit_to_idea_csv_strs`, `create_init_idea_csv_strs` — the idea CSV structure from the source chapter is reused for the destination output.

New semantic type: none. `ch30_semantic_types.py` re-exports through ch22.

---

## 4. Summary of What This Chapter Does

Ch30 is the **output inverse of ch23** — where ch23 reads human-authored idea sheets and converts them into bricks for ingestion, ch30 takes the fully processed world state and writes it back out as idea-format Excel files for human consumption.

**`collect_full_world_idea_csv_strs(world_dir)`** — the main data-collection function:
1. Walks all moment directories, loads each `MomentUnit` via `open_moment_file`, and calls `add_momentunit_to_idea_csv_strs` to serialize moment-level fields (budget units, epoch config, ceckbook, offi_times) into the idea CSV string dict.
2. For each person within each moment, loads the **gut** `PersonUnit` (the person's own belief system, not the job) and calls `add_personunit_to_idea_csv_strs` to serialize their full plan tree, contacts, reasons, facts, etc.
3. Opens the world SQLite database, creates sound/heard tables if absent, then calls `add_translate_rows_to_idea_csv_strs` to append validated translation mappings (from `trltitl_s_vld`, `trlname_s_vld`, `trllabe_s_vld`, `trlrope_s_vld` joined with `trlcore_s_vld`) into the four translation idea sheets (`ii00142`–`ii00145`).

**`create_lego0001_file(world_dir, output_dir, world_name)`** — produces the **world-level** output Excel:
- Calls `collect_full_world_idea_csv_strs`.
- Replaces the `spark_face` column value with `world_name` on every sheet (re-attributing all data to the world as author for the audience).
- Deletes the `spark_num` column (internal provenance not relevant to the audience).
- Writes the result as `lego0001.xlsx` and optionally prettifies it.

**`create_lego0002_file(world_dir, output_dir, person_name)`** — produces a **person-level** output Excel:
- Collects only the moments and **job** `PersonUnit`s (the post-listening state) for the specified person.
- Strips both `spark_face` and `spark_num` columns entirely.
- Writes as `{person_name}_ideas.xlsx`, removes empty sheets, and prettifies.

The distinction between `lego0001` (gut-based, world-attributed) and `lego0002` (job-based, person-scoped) reflects the gut/job duality established in ch11: the world sees raw belief systems; a person sees their listening-synthesized agenda.

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
- **ch18_db_tool**: `db_table_exists`, `get_db_tables` — KPI tables are checked before creation.
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

# ch32_world — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 32 — `ch32_world`**
**"WorldDir — the top-level orchestrator: a single entry point that runs the complete ETL pipeline from idea sheets to lego output and KPIs"**

---

## 2. Prompt Used to Build This

From `ch32_ref.json`:
> "WorldDirs create and admin MomentUnits."

Ontology note:
> "WorldUnits can hold multiple disjoint MomentUnits, because every moment is independent."

---

## 3. Summary of Previous Relevant Chapters

Ch32 imports from every ETL chapter (ch23–ch31) simultaneously — it is the conductor:

- **ch20_brick**: `export_db_to_excel` — full database export to Excel.
- **ch22_etl_config**: `reorder_etl_db_sheets`, path helpers.
- **ch23_idea_src**: `ideas_sheets_to_brick_sheets` — idea → brick conversion.
- **ch24_etl_brick**: All six brick ETL stage functions.
- **ch25_sound**: All four sound ETL stage functions.
- **ch26_heard**: All seven heard ETL stage functions.
- **ch27_lego**: All eleven lego ETL stage functions.
- **ch30_idea_dst**: `create_lego0001_file` — world-level idea export.
- **ch31_kpi**: `create_calendar_markdown_files`, `populate_kpi_bundle`, `lego_to_person_gcal_day_punchs`, `copy_person_day_punches_to_dst_dir`, `get_day_punchs_persons`.

New semantic type: `WorldName` (a `str`) — identifies a world, the top-level container for one or more disjoint `MomentUnit`s.

---

## 4. Summary of What This Chapter Does

`ch32_world` defines `WorldDir` and its generation function `worlddir_shop` — the user-facing entry point for the entire keg system.

**`WorldDir`** is a dataclass holding the directory layout for one world:
- `world_name` / `worlds_dir` — the name and parent directory of this world.
- `world_dir` — computed as `worlds_dir/world_name`.
- `db_path` — the SQLite database at `world_dir/world.db`.
- `moment_mstr_dir` — the moment master directory at `world_dir/moment_mstr`.
- `bricks_src_dir` — where brick Excel files are staged.
- `ideas_src_dir` — where human-authored idea Excel files are placed.
- `output_dir` — where output Excel files and CSVs are written.

**`brick_sheets_to_lego_with_cursor(cursor, bricks_src_dir, moment_mstr_dir)`** — the complete ordered ETL pipeline as a single function. Called with an open SQLite cursor, it executes all ~20 ETL stage functions in sequence:
1. `etl_brick_dfs_to_brixk_raw_tables` through `etl_brixk_vld_tables_to_sound_raw_tables` (ch24 — brick validation).
2. `etl_sound_raw_tables_to_sound_agg_tables` through `etl_sound_vld_tables_to_heard_raw_tables` (ch25 — sound/translation).
3. `etl_heard_raw_tables_to_heard_agg_tables` through `etl_heard_vld_to_lego_spark_person_csvs` (ch26 — heard/reconstruction).
4. `etl_lego_spark_person_csvs_to_lesson_json` through `calc_moment_bud_contact_mandate_net_ledgers` (ch27 — lego/listening).
5. `etl_mind_job_jsons_to_job_tables` + `etl_moment_json_contact_nets_to_moment_tranbook_nets_table` (ch27 — DB population).
6. `populate_kpi_bundle` + `create_last_run_metrics_json` (ch31/ch27 — analytics).

**`brick_sheets_to_lego_mstr(worlddir)`** — wraps the above in a `sqlite3_connect` context manager, commits, and optionally exports the full database to a formatted Excel file via `save_and_reformat_db_export`.

**`idea_sheets_to_lego_mstr(worlddir)`** — the end-to-end user-facing pipeline:
1. Reads the current `max_b_agg_spark_num` from the existing database (to avoid re-processing already-ingested sparks).
2. Calls `ideas_sheets_to_brick_sheets` (ch23) to convert idea sheets to brick sheets.
3. Calls `brick_sheets_to_lego_mstr`.

**`idea_sheets_to_gcal_day_punchs(worlddir, person_names, day)`** — runs `idea_sheets_to_lego_mstr` then generates Google Calendar day-punch files for each named person for the given day.

**`create_today_punchs`** — convenience wrapper that calls `idea_sheets_to_gcal_day_punchs` with `datetime.now()`.

`WorldDir` is what a user or operator instantiates to run keg. All other chapters are internal machinery; this is the interface.

# ch33_pitch — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 33 — `ch33_pitch`**
**"PitchUnit — a stub for structured negotiation between persons, representing gift/request/offer idea exchanges"**

---

## 2. Prompt Used to Build This

From `ch33_ref.json`:
> "Defines Pitch Tools for gifts, World Scenarios."

Ontology note:
> "Future tools that handle scenarios of different worlds. To be used for negotiation: here are the possible Worlds..."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `get_0_if_None` — used in `validate_spark_nums` to default None spark nums to 0.
- **ch10_person_lesson**: `LessonUnit` — a pitch carries lessons as its exchange medium.
- **ch23_idea_src**: `PromiseBook` — the data container for each of the three pitch components (gift, request, offer).
- **ch32_world**: `WorldName` — imported but not yet used in the current stub implementation.

`ch33_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

Ch33 is an **early-stage design stub** — its ref file's `chapter_blurb` is incomplete ("Defines Finance Tools for "), and `pitch.py` consists of a dataclass, a generation function, and inline design notes rather than a working implementation.

**`PitchUnit`** is the dataclass representing a negotiation between two persons:
- `pitcher_name` / `peer_name` — the two parties.
- `pitch_id` / `pitch_active` — identifier and current status of the negotiation.
- Three `PromiseBook` slots with associated `SparkInt` sequence numbers:
  - `gift_ideabook` / `gift_spark_num` — ideas the pitcher is committing to (already bricked).
  - `request_ideabook` / `request_spark_num` — ideas the pitcher is asking the peer to commit to.
  - `offer_ideabook` / `offer_spark_num` — ideas the pitcher is offering conditionally (if the request is accepted).

**`validate_spark_nums()`** enforces the sequencing constraint: `gift_spark_num < request_spark_num < offer_spark_num`. The gift must be established first (it's already committed), the request comes next, and the offer is the final conditional commitment. If `gift_spark_num` is None and either of the others is set, validation fails.

The inline design comments in `pitch.py` reveal the intended model:
- A pitch begins with a gift — concrete ideas the pitcher vows to make into bricks, demonstrating good faith.
- The pitch then describes possible future gifts from both parties.
- If accepted, the deal (explicitly noted as "needs to be added here so the word isn't used anywhere else") translates the offer ideabook into bricks.

The `pitchunit_shop` function is a placeholder — it accepts all parameters but currently only sets `pitcher_name`. The chapter represents keg's planned mechanism for structured peer-to-peer negotiation, grounding agreement in concrete idea commitments rather than verbal promises. The ontology note's phrase "here are the possible Worlds" indicates this chapter is also intended to support scenario comparison across different `WorldDir` configurations.

# ch34_finance — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 34 — `ch34_finance`**
**"Finance — an empty stub; reserved for financial modeling tools over PitchUnit scenarios"**

---

## 2. Prompt Used to Build This

From `ch34_ref.json`:
> "Defines Finance Tools for financial modeling."

Ontology note:
> "Tools for measuring PitchUnits that hold different possible worlds."

---

## 3. Summary of Previous Relevant Chapters

N/A — the chapter contains only `__init__.py` with no imports and no implementation.

---

## 4. Summary of What This Chapter Does

Ch34 is an **empty stub**. The `src/ch34_finance/` directory contains only `__init__.py` (which passes) and a `_ref/` directory. There are no `.py` implementation files, no functions, and no classes.

The ref file and ontology note indicate the intended purpose: financial modeling tools that operate over `PitchUnit`s (ch33) — specifically measuring the financial implications of different world scenarios represented by competing `WorldDir` configurations. This would close the loop between the negotiation layer (ch33) and quantified financial outcomes.

As of the cloned repository state on 5-26-2026, this chapter has not been implemented. It is a reserved chapter number in the inductive chain, positioned after the negotiation chapter (ch33) and before the person viewer web app in future chapters.

# ch35_person_viewer — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 35 — `ch35_person_viewer`**
**"Person Viewer — a Flask web app that renders a PersonUnit's plan tree and contacts as an interactive, checkbox-driven HTML visualization"**

---

## 2. Prompt Used to Build This

From `ch35_ref.json`:
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

`ch35_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

`ch35_person_viewer` provides two outputs: a Python dict representation of a `PersonUnit` suitable for JSON serialization (`person_viewer_tool.py`) and a Flask web application that renders that dict as an interactive HTML page (`person_viewer_app.py`).

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





# ch90_puncher_app — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 50 — `ch90_puncher_app`**
**"Puncher App — a tkinter desktop GUI that wraps the full ETL pipeline, letting non-developers run keg from an Excel-file interface"**

---

## 2. Prompt Used to Build This

From `ch90_ref.json`:
> "Simple ETL app to create a world database from excel files."

Ontology note:
> "The entry point for most excel savvy users."

---

## 3. Summary of Previous Relevant Chapters

- **ch08_person_logic**: `personunit_shop` — used in `puncher_tool.py` to construct example `PersonUnit`s for the bundled starter idea files.
- **ch14_time**: `get_creg_config`, `get_five_config`, `epochunit_shop` — the "El Paso" and "TeamFive" example templates use real epoch configurations.
- **ch15_moment**: `momentunit_shop` — moment objects are built for example templates.
- **ch20_brick**: `csv_dict_to_excel`, `prettify_excel_file`, `remove_empty_sheets`, `prettify_excel_files` — all Excel output formatting is delegated to ch20.
- **ch23_idea_src**: `add_momentunits_to_idea_csv_strs`, `add_personunit_to_idea_csv_strs`, `create_init_idea_csv_strs` — example idea files are generated using the same CSV machinery as the ETL source layer.
- **ch30_idea_dst**: `create_lego0002_file` — person-level idea export is triggered from the GUI.
- **ch32_world**: `worlddir_shop`, `create_today_punchs` — the entire ETL pipeline is invoked via ch32's `WorldDir` entry point.

New semantic type: none. `ch90_semantic_types.py` re-exports through ch22.

---

## 4. Summary of What This Chapter Does

`ch90_puncher_app` is the **desktop application layer** of keg — the product that end users interact with directly.

**`puncher_tool.py`** contains three categories of logic:

*App settings and defaults:*
- `ETLAppSettings` — a dataclass holding all UI theming values (dark background `#1a1a1f`, accent yellow `#e8c547`, monospace fonts, etc.) with platform-specific font selection (Courier New on Windows, Menlo on macOS/Linux).
- `get_app_default_dir()` — returns `C:/keg/worlds` on Windows, `~/keg/worlds` on macOS/Linux.
- `get_app_default_dirs()` — builds the full `WorldDir` path layout for the default world (`hope1`).
- `get_app_default_me_personname()` / `get_app_default_you_personname()` — returns `"Emmanuel"` and `"Steve"` as starter person names, a deliberate reference to Levinas.

*Starter idea file generators:*
Eight named example generators build `PersonUnit`s and `MomentUnit`s programmatically and serialize them to idea-format Excel files, providing ready-made starting points:
- `create_simple_1m2p2pledges_idea_file` — 1 moment, 2 persons, 2 pledges.
- `create_simple_1m2p5pledges_idea_file` — 1 moment, 2 persons, 5 pledges (household tasks with baking soda — a recurring example throughout the codebase).
- `create_simple_2m2p5pledges_idea_file` — 2 moments (home + sport/dance), 2 persons.
- `create_emmanuel_lovemaking_idea_file` — 1 moment called "loving moment", 2 persons.
- `create_five_time_config_file` — a moment with the "Five" epoch (a custom 5-unit time system).
- `create_elpaso_time_config_file` — a moment with the standard Gregorian epoch, set in El Paso.
- Several `pass`-bodied stubs (`create_emmanuel_idea_file`, `create_example_moment_ledger_file`, `create_example_moment_budget_file`, `create_monopoly_idea_file`) reserved for future examples.

*Utility:*
- `fill_spark_face_in_directory(directory, face_name)` — fills empty `spark_face` cells in all Excel files in a directory with the provided face name. Used before running the pipeline when a user has authored idea sheets without attributing them to a face.
- `get_option_table_options()` — returns a dict mapping human-understandable option names to their generator functions, used to populate the GUI's dropdown/table of example actions.

**`puncher_app.py`** — the tkinter GUI:
- A dark-themed desktop window with labeled entry fields for `world_name`, `worlds_dir`, `me_name`, `you_name`, and `output_dir`.
- A scrollable option table listing the example generator functions from `get_option_table_options`.
- A "Run ETL" button that calls `create_today_punchs` (ch32) — the end-to-end pipeline from ideas to Google Calendar day punches — with a live log output pane showing stdout.
- A "Create Person Ideas" button that calls `create_lego0002_file` (ch30) to produce a person-scoped idea Excel for the named person.
- Settings are persisted to a local JSON config file between sessions.

ch96 pass
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

# ch98_linter — Chapter Summary

*This summary is authored by AI 5-26-2026.*

## 1. Title and Summary Declaration

**Chapter 98 — `ch98_linter`**
**"Linter — AST-based style enforcement, chapter-move tooling, and line counting for the keg repository"**

---

## 2. Prompt Used to Build This

From `ch98_ref.json`:
> "Linter for repo."

Ontology note:
> "All chapters get checked for following style rules."

---

## 3. Summary of Previous Relevant Chapters

- **ch00_py**: `is_camel_case`, `uppercase_in_str` from `dict_toolbox`; `create_path`, `get_dir_filenames`, `open_file` from `file_toolbox` — file traversal and string utilities.
- **ch01_keyword**: `get_example_strs_config` — the linter validates that example strings in test files match the registered example string configurations.
- **ch97_docs_builder**: `get_chapter_desc_prefix`, `get_chapter_descs`, `get_func_names_and_class_bases_from_file` — chapter directory discovery and AST-based function name extraction are reused from ch97.

`ch98_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

`ch98_linter` enforces keg's coding conventions across the repository. Because it needs to import from ch97 (which imports from nearly all chapters), it is positioned at 98 — only ch99 is later in the inductive chain.

**`style.py`** — the core linter:

- `filename_style_is_correct(filename)` — enforces two rules: no uppercase characters in `.py` or `.json` filenames; no Python files ending in `s.py` (plural module names are disallowed).
- `get_filenames_with_wrong_style(filenames)` — returns the set of violating filenames.
- An `ast.NodeVisitor` subclass traverses each Python file's AST, checking:
  - Function names must be `snake_case` (no camelCase via `is_camel_case`).
  - Import statements must not import from chapters higher than the current chapter's number (enforcing the inductive import rule: a chapter may only import from earlier chapters).
  - Functions must have docstrings if they exceed a minimum line count threshold.
  - Class names must be `PascalCase`.
- `get_func_names_and_class_bases_from_file` from ch97 is used to cross-check declared class hierarchies against style expectations.

**`line_counter.py`** — counts lines of code per chapter and per file, used to track codebase growth and identify chapters with unusually large files.

**`ch_move1.py`** / **`ch_move_many.py`** / **`chapter_move_tool.py`** — utilities for renumbering chapters. When a chapter needs to be renumbered (e.g. inserting a new chapter between existing ones), these tools:
  - Update all import statements across the entire `src/` tree that reference the old chapter number.
  - Rename the chapter directory itself.
  - Update `_ref/chXX_ref.json` chapter number fields.
  - Update test file paths and any hardcoded chapter references.
  `ch_move_many` extends this to batch-renumber a range of chapters simultaneously.

**`paths_change.py`** — finds and replaces path strings across the repo when directory structures change.

**`create_notebook.py`** — generates Jupyter notebook helper library for a chapter's test suite, enabling interactive exploration of chapter functionality.

The linter's placement at 98 means it can validate the import-ordering rule across the entire codebase — it has the highest chapter number of any functional chapter, and can therefore check that nothing in chapters 0–97 imports from chapters higher than themselves.
