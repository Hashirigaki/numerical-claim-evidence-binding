# Apart Track 2 — Saved BLS HTML Full Source Verification (v1)

Verification date: **2026-11-15 (JST)**. This is a verification of the **user-provided original browser-saved HTML files** against the frozen evidence catalog, not a new public-website fetch. No source HTML, original CSV, predictions, or reference labels were modified.

## 1. SHA-256 source identity — PASS

| Source | Size (bytes) | SHA-256 | Matches 2026-11-15 work log |
|---|---:|---|---|
| `empsit_10022026.html` | 1,028,311 | `c874654d8892d063a63c6af10b18ed4b1272fd6f6c06bfd8dce729d7549f5fb2` | **YES** |
| `empsit_11062026.html` | 1,026,512 | `9ea0244b6ee264fabd21f4f4ed80fcf593628f4123da736d871128e7a26908a2` | **YES** |

## 2. Full cell transcription check — PASS for all included cells

- Source tables: **54** (27 table elements with BLS IDs per release).
- Frozen evidence CSV records: **12,852** (Nov 6: **6,426**; Oct 2: **6,426**).
- `raw_value` comparison against HTML element at the *same source table ID, source HTML `tr` index, and direct child cell index*: **12,852 exact matches; 0 raw mismatches, 0 unresolvable cell references.**
- Row-label check: **12,356** exact; **496** differ only in spacing around numbered footnote markers (example `item(1)` vs `item ( 1 )`); **0 substantive differences after that narrow normalization**.

## 3. Reverse extraction coverage check — 8 cells omitted

Enumerating all direct `td` cells with no `colspan` in data rows beginning with a row-heading `th` yields **12,860** eligible cells in 54 source tables. The normalized evidence CSV contains **12,852** of those (coverage **99.938%**); **8 are missing**. All eight are the four numeric cells on **Table B-6, `Total private`, row 2** in each release. These were skipped by the original normalizer and are listed individually in `BLS_Saved_HTML_8_Omitted_Cells_v1.csv`.

**Scope:** This is completeness under the *explicit direct-child table-cell enumeration rule*; the rule excludes spanning cells, section headers and other structures. It does not imply semantic completeness of all claims or tables.

## 4. Known metadata issues — present in authentic source snapshots

- **192** numeric cells in the prior anomaly list are present and their raw values match their corresponding saved HTML cells.
- **160** in Table A-11: percentages in `PERCENT DISTRIBUTION` or `UNEMPLOYED AS A PERCENT OF THE CIVILIAN LABOR FORCE`, but the CSV records `THOUSAND_PEOPLE`.
- **32** in Table A-12: average/median duration **in weeks**, but the CSV records `THOUSAND_PEOPLE`.
- All 192 are inflated by a factor of **1,000** in `canonical_value` relative to their numeric raw values under the erroneous people-unit conversion.
- This is a **scoped set of known metadata defects**, not a full semantic audit of all 12,852 metadata records. Original HTML confirms the relevant table sections and labels.
- Prior 77 selected-cell cross-check: **76** passed row/period/seasonal-adjustment/unit checks; **one** (A-11 `Job leavers` percentage) required review for its unit. All 77 source `raw_value` cells now also pass direct saved-HTML comparison.

## 5. Interpretation and remaining boundary

**Verified:** The two original snapshots are byte-identical to previously logged local originals; each of the 12,852 included raw table-cell values maps exactly to the specified original HTML location; the row-label content is correct aside from footnote spacing; an independently reverse-counted eight cells are absent; the 192 previously detected known unit/canonical errors are genuine in the same saved snapshot.

**Not established:** Correctness of every period label, seasonal-adjustment flag, unit code, canonical conversion, historical-series comparability, alternative acceptable proof set, or held-out matcher performance. Hash equality confirms identity to the *logged local snapshots*, not that the snapshots are cryptographically authenticated by the BLS publisher.

**Prediction impact:** The earlier separate unit-metadata sensitivity test changed one Simple Matching prediction (CLAIM-030, wrong link to abstain) and did not change Attribute-Aware predictions. That is an existing **copy-only sensitivity analysis**, not a new prediction run on the frozen data during this source verification.

## Reproducibility

Run `python verify_bls_saved_html_v1.py` alongside the two exact HTML files and the prior frozen CSV/selected-check/anomaly files at the paths configured in the script. Read-only originals are hashed and asserted; the verifier writes only new audit outputs.
