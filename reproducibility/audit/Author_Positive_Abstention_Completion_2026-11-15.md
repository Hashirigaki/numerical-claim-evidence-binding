# Author visual audit — completion record (2026-11-15 JST)

**Provenance:** Retrospective record of the author's reported browser-based inspection of the archived BLS HTML, supplied in the final-submission handoff. This record is not independent expert re-adjudication and does not claim that the present package builder directly witnessed those author checks. The pre-selection forms (`Apart_Track2_Positive_and_Abstention_Author_Check_v0.3.md` and `.csv`) are retained unchanged as dated **pre-check** evidence; their "PENDING" status describes the moment at which they were created, not the final state. This completion record supersedes that pre-check status.

## Selection and scope

- Fixed selection seed: Python `random.Random(20261115)`, selected before author viewing.
- Success cases: six from the 28 correct links not included in the earlier flagged-case inspection; the original correct-link pool contained 35 cases.
- Correct-abstention cases: two from the three not yet checked in the earlier targeted inspection; the original correct-abstention pool contained four cases.
- The previously checked baseline-failure examples were eight preselected cases (004, 005, 012, 027, 039, 043, 044, 051) plus 008.
- The additional eight checks were conducted by the author against archived BLS HTML tables, examining official table identity, statistical row, reference period, numeric cell values, and rounding or arithmetic where needed. The two abstention checks inspected the relevant Table B-1 editions for the required historical reference months.

## Completed author-reported observations

| Claim | Scored outcome | Author-reported observation |
|---|---|---|
| CLAIM-006 | CORRECT_LINK | Adult women October 2026 unemployment rate: 3.6%. |
| CLAIM-018 | CORRECT_LINK | Marginally attached: 1,639 thousand, approximately 1.6 million. |
| CLAIM-026 | CORRECT_LINK | Professional/business services: 22,604 − 22,335 = 269 thousand. |
| CLAIM-037 | CORRECT_LINK | Manufacturing October monthly employment change: +19 thousand. |
| CLAIM-040 | CORRECT_LINK | Machinery manufacturing October change: +3.9 thousand, reported approximately +4,000. |
| CLAIM-045 | CORRECT_LINK | Total private average weekly hours: 34.4 in September and October 2026. |
| CLAIM-035 | CORRECT_ABSTAIN | February 2026 Transportation and warehousing reference level absent from the checked tables. |
| CLAIM-038 | CORRECT_ABSTAIN | December 2025 Manufacturing reference level absent from the checked tables. |

**Observed result:** The author reported no discrepancies in the six correct-link and two correct-abstention checks (**0/8 observed discrepancies**).

**Interpretation:** This small, non-blind author visual check does not independently validate all 35 correct links, establish an error-rate bound, or exhaustively rule out alternative proof sets. The two correct-abstention checks found the requested historical base months absent from the specified permitted editions' Table B-1, not from every possible source elsewhere. The qualitative expression "recent low" for CLAIM-026 was not separately scored.

**Frozen evaluation:** The 51 claim inputs (seven pilots and 44 MAIN), original and audited proposed gold labels, 88 matcher predictions, and recorded 10-versus-35 correct-link counts are unaltered by this author completion record.

See the adjacent `.csv` for a compact case-level machine-readable record. Each observation is attributed to the author, not to an independently blinded evaluator.
