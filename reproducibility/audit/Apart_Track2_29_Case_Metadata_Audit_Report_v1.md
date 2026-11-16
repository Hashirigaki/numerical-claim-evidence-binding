# Apart AI × Epistemics Sprint, Track 2
## 29 flagged outcomes: second-pass metadata audit (v1)

- **Audit date:** 2026-11-15 (JST)
- **Scope:** 24 wrong/unjustified links from Simple Matching plus five over-abstentions from Attribute-Aware Matching; 29 **method-level outcomes**, involving **27 distinct claims**.
- **Status:** Review of **frozen, normalized evidence CSV, frozen predictions, gold-audit CSV, and matcher source code**. This is **not** independent verification of the saved original BLS HTML and is **not** exhaustive discovery of alternative valid proof sets.
- **Integrity:** Four original inputs retain the SHA-256 values in `Apart_Epistemics_Audit_Changelog_v1.md`. Re-running `compare_matchers.py` with the frozen original claim and evidence CSV yielded **88 prediction rows, byte-for-byte identical** to the original `matcher_predictions.csv` (`SHA-256 49D99550F084602072F271AA06C90E02B981C77FB68FBE94BCD890A2321CDEDB`). No original input, prediction, or gold record was modified.

### 1. Corrected failure categories

The `failure_category` column of the existing scored audit CSV was produced by a short heuristic in `audit_and_rescore.py`; it is **not** a semantic explanation of every failure. This review uses a *mutually exclusive primary cause*, retaining secondary complexities in the case notes.

| Method | Primary cause | Count | Claim IDs |
|---|---|---:|---|
| Simple | Wrong statistic, indicator, row, or unit | 14 | 012, 022, 023, 025, 027, 030, 031, 033, 034, 039, 040, 041, 043, 051 |
| Simple | Wrong reporting period | 7 | 005, 006, 008, 011, 045, 047, 048 |
| Simple | Incomplete evidence/proof set | 2 | 044, 046 |
| Simple | Cannot establish complete claim from permitted tables | 1 | 004 |
| **Simple total** | | **24** | |
| Attribute-Aware | Deliberately unsupported cross-edition calculation, with early abstention rule | 4 | 020, 022, 028, 051 |
| Attribute-Aware | Missing semantic mapping from prose concept to table label | 1 | 013 |
| **Attribute-Aware total** | | **5** | |

**Interpretation of the categories:** These are predominant causes, not exhaustive features. For example, several wrong-statistic links also omit required arithmetic or use a wrong period. No failure was assigned primarily to seasonal-adjustment mismatch because the selected predicted cells were already filtered to `SA` by the implementation.

### 2. Result of inspecting all 24 Simple Matching links

- **22/24** predicted evidence IDs have **zero overlap** with the accepted evidence IDs in the audited gold CSV. This includes one out-of-corpus claim for which the gold reference set is empty. Their period, statistic, unit, or claim-level proof scope is inconsistent with the corresponding numerical claim under the declared evaluation rules.
- **2/24 (CLAIM-044 and CLAIM-046)** are **valid partial members** of a gold proof set. For CLAIM-044, the prediction is the October hourly wage endpoint **$32.75**, but omits September **$32.63**, which is needed to check the rise of 12 cents (and the rounded 0.4%). For CLAIM-046, the prediction is September manufacturing workweek **40.5 hours**, but omits October **40.5 hours** required to establish "unchanged." These are **incomplete proofs**, not entirely unrelated citations.
- Based on the recorded table-cell metadata, **none of these 24 singleton links provides a complete accepted proof for its full numerical claim**. That conclusion is **conditional on the currently enumerated accepted proof sets and numerical-only scoring rubric**. It does **not** establish that all plausible alternative proofs have been exhaustively considered.

### 3. Result of inspecting all five Attribute-Aware abstentions

- **CLAIM-013:** Long-term unemployed share 27.6% exists in `cps_empsit_a09:R18:C10` under **"27 weeks and over"** in a **percentage distribution** section. The mapper does not bridge the paraphrase **"long-term unemployed"** and the table label, so it abstains.
- **CLAIM-020/022/028:** Average monthly gains over the preceding 12 months require endpoint-level subtraction across **2026-10-02 and 2026-11-06 releases**, then division by 12. The explicit guard `if 'average monthly gain' in x` returns `[]` before candidate search.
- **CLAIM-051:** Combined revisions require four cells across two releases: `(186,000 - 133,000) + (60,000 - 29,000) = 84,000`. The explicit `higher than previously reported` guard returns `[]` before candidate search.
- **Separate implementation constraint:** `compare_matchers.py` line 17 filters evidence to **2026-11-06 only** and to **seasonally adjusted numeric cells**. Thus the four cross-edition cases are **out of reach by design** even if the early text guards were removed. They are linkable under the later *gold convention*, but not within the matcher’s implemented search space.

The numerical calculations for CLAIM-020, -022, -028 and -051 were recomputed from the frozen normalized cell values. The three annual-average calculations remain **provisional cross-vintage reconstructions**, not independently authenticated historical series values.

### 4. Examples worth retaining in the report

| Claim | Observation | Trust-infrastructure implication |
|---|---|---|
| 005 | 3.9% occurs for adult men in September **and** October; Simple picks September | Matching number and indicator does not establish correct reporting period |
| 012 | Simple picks 2,000,000 people unemployed for **less than 5 weeks** instead of **27+ weeks** (1,963,000 rounded to 2.0 million) | Unit/quantity resemblance cannot substitute for cohort identity |
| 043 | Simple picks **3.1 hours** of manufacturing overtime, while claim is **3.1%** increase in average hourly earnings requiring two wage levels | Unit and derivation must be validated together |
| 044 | Simple picks the correct **$32.75 endpoint** but omits the **$32.63** comparison value | A relevant evidence cell is not necessarily a complete proof |
| 051 | Simple picks an unrelated 84,000 employment level; Attribute-Aware abstains due to an explicit rule; the numerical claim requires four revision cells | Version provenance and multi-source arithmetic must be represented explicitly |

### 5. Checks performed and not performed

**Performed:**

1. Loaded and enumerated all 29 flagged outcomes from the **audited** scored CSV.
2. Resolved every predicted and accepted evidence ID against the 12,852-row frozen normalized evidence catalog.
3. Inspected the predicted and accepted row labels, publication editions, periods, units, seasonality tags and canonical values; compared them with the claim text.
4. Checked set membership, including the two genuine partial-proof matches, and recomputed the cited multi-cell arithmetic.
5. Read matcher logic and verified explicit abstention patterns and the November-only evidence filter.
6. Re-ran the frozen code and verified its 88 predictions were byte-identical to original output.

**Not performed:**

1. Independent check of the saved, original BLS HTML or its extraction fidelity (not included in these two ZIPs).
2. Exhaustive search for *every* mathematically or semantically equivalent alternative proof set, or independent expert adjudication of gold labels.
3. Blind, newly held-out source evaluation, ablation studies or a claim of generalization.

### 6. Implications for the report revision

- Replace the existing heuristic `failure_category` count with the table in Section 1, clearly noting that categories identify the **primary observed cause** and may overlap causally.
- Describe **24 false or unjustified complete links**, while noting that **two are valid partial evidence**. Do not call every selected source wholly unrelated.
- Describe Attribute-Aware’s four cross-edition abstentions as **deliberately unsupported** by its current rule set and **ineligible under its evidence filter**, not merely as failures of an unrestricted general-purpose evidence search.
- Keep the gold audit conditional: the matcher was evaluated in sample; full HTML provenance and alternative proofs remain to be checked. The 35 correct / 0 wrong in-sample result must not be presented as evidence of accuracy on future releases.
- Next stage is an original-source audit of the most consequential evidence cells, and explicit review of alternative accepted proof sets. Preserve the current predicted CSV and gold labels; record any later annotation changes with separate versioned outputs.

### 7. Supporting files

- `Apart_Track2_29_Case_Metadata_Audit_v1.csv`: one row for each of 29 method-level outcomes, including the actual predicted and accepted evidence IDs and full normalized cell details; cause, explanation, and limits of this audit.
- `review_29_cases.py`: deterministic reconstruction of the case ledger from the already saved *Working Bundle* and *Review Package*. Its per-ID primary-cause interpretation is explicitly curated and should **not** be described as an automatically discovered cause model.
- Primary source archives and original predictions remain in existing bundles. **They were not altered.**
