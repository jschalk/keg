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

The name "Nabu" is the ancient Mesopotamian diety of writing and wisdom — an appropriate name for a chapter that interprets and transcribes numeric values across reference frames.

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
