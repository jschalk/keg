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
- **ch23_idea_src**: `PromiseUnit` — the data container for each of the three pitch components (gift, request, offer).
- **ch32_world**: `WorldName` — imported but not yet used in the current stub implementation.

`ch33_semantic_types.py` re-exports through ch22 with no additions.

---

## 4. Summary of What This Chapter Does

Ch33 is an **early-stage design stub** — its ref file's `chapter_blurb` is incomplete ("Defines Finance Tools for "), and `pitch.py` consists of a dataclass, a generation function, and inline design notes rather than a working implementation.

**`PitchUnit`** is the dataclass representing a negotiation between two persons:
- `pitcher_name` / `peer_name` — the two parties.
- `pitch_id` / `pitch_active` — identifier and current status of the negotiation.
- Three `PromiseUnit` slots with associated `SparkInt` sequence numbers:
  - `gift_promiseunit` / `gift_spark_num` — ideas the pitcher is committing to (already bricked).
  - `request_promiseunit` / `request_spark_num` — ideas the pitcher is asking the peer to commit to.
  - `offer_promiseunit` / `offer_spark_num` — ideas the pitcher is offering conditionally (if the request is accepted).

**`validate_spark_nums()`** enforces the sequencing constraint: `gift_spark_num < request_spark_num < offer_spark_num`. The gift must be established first (it's already committed), the request comes next, and the offer is the final conditional commitment. If `gift_spark_num` is None and either of the others is set, validation fails.

The inline design comments in `pitch.py` reveal the intended model:
- A pitch begins with a gift — concrete ideas the pitcher vows to make into bricks, demonstrating good faith.
- The pitch then describes possible future gifts from both parties.
- If accepted, the deal (explicitly noted as "needs to be added here so the word isn't used anywhere else") translates the offer promiseunit into bricks.

The `pitchunit_shop` function is a placeholder — it accepts all parameters but currently only sets `pitcher_name`. The chapter represents keg's planned mechanism for structured peer-to-peer negotiation, grounding agreement in concrete idea commitments rather than verbal promises. The ontology note's phrase "here are the possible Worlds" indicates this chapter is also intended to support scenario comparison across different `WorldDir` configurations.
