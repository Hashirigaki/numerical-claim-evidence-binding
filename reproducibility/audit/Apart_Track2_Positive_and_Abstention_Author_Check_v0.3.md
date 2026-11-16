# Author visual audit — additional success / correct-abstention sample (v0.3)

Selection fixed before author viewing these cases. The eight prior targeted cases and separately checked CLAIM-008 were excluded from the positive-link sampling frame. `CORRECT_LINK` candidate pool: 28 previously unreviewed out of 35. `CORRECT_ABSTAIN` pool: three previously unreviewed out of four. The sampling used Python `random.Random(20261115)`, selecting six from the first sorted pool and two from the second. No matcher input, gold reference, prediction, or outcome was modified.

**Status:** ALL EIGHT NEW AUTHOR CHECKS PENDING. The values below come from the stored normalized catalog; they are instructions for author comparison, not independent confirmation.

## Cases and source locations

### CLAIM-006 — CORRECT_LINK

In October, unemployment rate by group: adult women (3.6 percent).

**Where to look:** 2026-11-06:cps_empsit_sum:R15:C5 | Official Summary table A | Adult women (20 years and over) | Oct. 2026 | 3.6 (PERCENT) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-018 — CORRECT_LINK

Among those not in the labor force who wanted a job, the number of people marginally attached to the labor force changed little at 1.6 million in October.

**Where to look:** 2026-11-06:cps_empsit_sum:R47:C5 | Official Summary table A | Marginally attached to the labor force | Oct. 2026 | 1,639 (THOUSAND_PEOPLE) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-026 — CORRECT_LINK

Professional and business services has added 269,000 jobs since a recent low in October 2025.

**Where to look:** 2026-11-06:ces_table1:R122:C6 | Official Table B-1 | Professional and business services | Oct. 2025 | 22,335 (THOUSAND_JOBS) | SA || 2026-11-06:ces_table1:R122:C9 | Official Table B-1 | Professional and business services | Oct. 2026(p) | 22,604 (THOUSAND_JOBS) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-037 — CORRECT_LINK

Manufacturing employment continued to trend up in October (+19,000).

**Where to look:** 2026-11-06:ces_table10:R8:C5 | Official Summary table B | Manufacturing | Oct. 2026(p) | 19 (THOUSAND_JOBS) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-040 — CORRECT_LINK

In October, job gains occurred in machinery manufacturing (+4,000).

**Where to look:** 2026-11-06:ces_table1:R33:C10 | Official Table B-1 | Machinery manufacturing | Change from: Sept.2026 - Oct.2026(p) | 3.9 (THOUSAND_JOBS) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-045 — CORRECT_LINK

The average workweek for all employees on private nonfarm payrolls remained at 34.4 hours in October.

**Where to look:** 2026-11-06:ces_table2:R3:C4 | Official Table B-2 | Total private | Sept. 2026(p) | 34.4 (HOURS) | SA || 2026-11-06:ces_table2:R3:C5 | Official Table B-2 | Total private | Oct. 2026(p) | 34.4 (HOURS) | SA

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-035 — CORRECT_ABSTAIN

Transportation and warehousing added 104,000 jobs since a recent employment low in February.

**Where to look:** Official Table B-1, Oct 2 and Nov 6 editions. Confirm neither edition provides a February 2026 source observation within its table columns.

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

### CLAIM-038 — CORRECT_ABSTAIN

Manufacturing employment has increased by 101,000 since a recent low in December 2025.

**Where to look:** Official Table B-1, Oct 2 and Nov 6 editions. Confirm neither edition provides a December 2025 source observation within its table columns.

**Author decision:** ☐ agreed  ☐ discrepancy  ☐ cannot decide

## Audit interpretation

For CORRECT_LINK: check the official source edition, actual table caption, row name, period, units and source values. For DERIVED two-cell proofs, recompute the operation and declared rounding. For CORRECT_ABSTAIN: inspect the official table structure and whether the missing historical reference period appears in either allowed release; do not infer factual falsity.

Record `author_html_visual_checked=YES` only after the author has inspected the original HTML; log any discrepancy explicitly before changing any report figures. Six successful predictions and two correct abstentions are a small purposive follow-up, not an independently adjudicated or blind holdout set.
