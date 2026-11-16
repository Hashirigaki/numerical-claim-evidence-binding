# Apart AI x Epistemics Sprint 2026, Track 2
## Author-guided visual source review: separate addendum (2026-11-15 JST)

**Status:** Source-table visual checks completed for the eight selected audit cases; one additional case (CLAIM-008) also checked. This is a directed author review conducted with an AI assistant and source screenshots, **not** a blind independent expert adjudication or an exhaustive alternative-proof search. No frozen source, matcher, prediction, or prior audit file was modified.

### Review selection

The planned eight cases comprised five purposefully selected failures (005, 012, 043, 044, 051) and three from a previously declared fixed-seed selection (004, 027, 039; seed `20261115`). CLAIM-008 was also inspected in the course of table navigation. Because this review was targeted and the report was already under development, no sampling-based statistical claim follows.

### Source-table observations

| Claim | Official displayed table(s) checked | Observation confirmed by the author-shared screenshots | Status / limit |
|---|---|---|---|
| 004 | Table A-1, both Oct 2 and Nov 6 editions | Seasonally adjusted TOTAL unemployment rate is shown for May-Sep in the former and June-Oct in the latter; the two A-1 tables do not include March-April. A single October value cannot establish the full range since March. | **Substantive failure reason confirmed**. Exact original predicted cell `cps_empsit_a01:R21:C10` with complete parent heading was not separately displayed and its full semantic location is not certified by the author screenshot. Out-of-corpus decision remains conditional on the declared table-only scope and broader catalog audit. |
| 005 | Summary table A, Nov 6 | Adult men (20 years and over) unemployment is 3.9% in September and 3.9% in October; a September cell cannot prove the October claim. | Predicted/gold values and period mismatch visually confirmed. |
| 012 | Table A-12, Nov 6 (also Summary table A) | SA, August Less than 5 weeks = 2,000 thousand; SA, October 27 weeks and over = 1,963 thousand. | Predicted/gold numerical rows visually confirmed; correct public table is **A-12**, despite internal ID `cps_empsit_a09`. |
| 027 | Table B-1 and Summary table B, Nov 6 | Health care Sept-to-Oct = +41.6 thousand (rounds to +42 thousand); Leisure and hospitality Aug = +42 thousand. | Both compared values visually confirmed. |
| 039 | Table B-1 and Summary table B, Nov 6 | Computer/electronic manufacturing Sept-to-Oct = +6.7 thousand (rounds to +7 thousand); Financial activities October = +7 thousand. | Both compared values visually confirmed. |
| 043 | Tables B-3 and B-2, Nov 6 | Total private average hourly earnings $36.85 in Oct 2025 and $38.00 in Oct 2026 (growth approx. 3.12%, rounds to 3.1%); Manufacturing August average overtime = 3.1 **hours**. | Both correct proof inputs and erroneous unit/value visually confirmed. |
| 044 | Table B-8, Nov 6 | Total private production/nonsupervisory average hourly earnings $32.63 in September and $32.75 in October; difference $0.12, approx. 0.368%, rounded to 0.4%. | Complete two-cell proof and one-cell partial-baseline link visually confirmed. |
| 051 | Summary table B (Oct 2 and Nov 6), plus Table B-1 (Nov 6) | Payroll monthly changes: Aug 133 -> 186 thousand, Sept 29 -> 60 thousand; 53+31=84 thousand. Table B-1 separately shows an unrelated communications equipment employment level of 84.0 thousand for October. | Correct 4-cell mixed-edition calculation and unrelated numerical collision visually confirmed. Historical-vintage equivalence is not broadly certified. |
| 008 (extra) | Summary table A, Nov 6 | White-group unemployment rate Aug 3.7% and Oct 3.7%; baseline picks August for October claim. | Same-number wrong-period failure visually confirmed. |

### Qualification of the review record

1. This addendum **does not** change the 44-claim proposed gold set or the 88 frozen matcher predictions. It supports an author-guided review of concrete failure explanations.
2. The author's screenshots substantiate the displayed table locations and salient arithmetic; they do not independently check all 12,852 raw source cells or all cell metadata.
3. Alternative valid proof sets were **not exhaustively enumerated**. No positive claim of their absence is made.
4. The original source-HTML numerical-cell audit and unit/metadata sensitivity run are separately reported; this author review should not be conflated with them.
5. Particular care is required not to infer BLS's *official* table number from internal parser suffixes: `cps_empsit_a09` points to official A-12; `ces_table10` points to official Summary table B.

### Report update

The new working report revision `Apart_Epistemics_Track2_Submission_v0.2_REVIEW` describes this check as *targeted author visual review*, states the evaluation and corpus constraints, and retains provisional cross-vintage working labels. It is a **review draft**, not yet submitted.
