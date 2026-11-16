# Apart Research Track 2 — Primary-source cross-check (v1)

**Audit date:** 2026-11-15 JST  
**Scope:** BLS October 2026 Employment Situation release (published 2026-11-06) and September 2026 Employment Situation release (published 2026-10-02).  
**Status:** Cross-check of *publicly displayed official BLS archive HTML* against the **unchanged** normalized evidence CSV. This is **not** verification of the bytes of the two locally saved HTML snapshots.

## Executive finding

- The audit selected **77 distinct evidence cell IDs**: all **58 distinct evidence IDs used in the audited proposed gold proof sets**, and all **21 distinct evidence IDs incorrectly chosen by Simple Matching**, with two overlapping IDs. This is a *purposive evaluation-critical selection*, **not** a random 50-cell sample.
- **77/77 values and row identities** matched the BLS archived public tables when manually transcribed from the official site's table display.
- **76/77** of the selected cells also matched the period, seasonality, and unit implied by the source table; **1/77** had an incorrect unit label in the normalized CSV (shown below). The selected 58 gold reference cells have **no detected mismatch** in those checked dimensions.
- A targeted follow-up **metadata scan** identified **192 numeric cells** with clear unit-label errors and corresponding canonical-value scaling errors in table A-11 and A-12 across the two release editions. These are structural unit-annotation errors, **not 192 independently confirmed numerical transcription errors**.
- The frozen matcher input, predictions, gold labels, normalized evidence CSV, and original report have **not** been modified or rescored. A separate, labeled sensitivity run on a corrected **copy** is documented below.

## Sources and audit method

1. Official BLS release, November 6: <https://www.bls.gov/news.release/archives/empsit_11062026.htm> (Table A summary around lines 287–341; Summary B 343–398; A-1 739–762; A-11 1325–1360; A-12 1363–1391; B-1 1514–1709; B-2 1711–1744; B-3 1746–1781; B-7 1895–1929; B-8 1931–1966).
2. Official BLS release, October 2: <https://www.bls.gov/news.release/archives/empsit_10022026.htm> (Summary B 340–376; A-11 1322–1358; A-12 1360–1388; B-1 1511–1706).
3. Compared specific official rows and numeric columns with `lesson4_evidence_normalized_draft.csv`, including source edition, row label, displayed raw value, header period, seasonal-adjustment column, and declared units. The mapping of official values/line positions was transcribed from the web-readable tables, and the comparison was checked programmatically. Evidence-cell IDs, compared values, official URL and line locator appear in `BLS_Official_Site_Evidence_Crosscheck_v1.csv`.
4. Numeric cell IDs were selected directly from `Apart_Epistemics_Gold_Audit_v1.csv` and the 24 Simple Matching wrong/unjustified prediction records in `Apart_Epistemics_Comparison_Scored_Audit_v1.csv`. The original source files and scorer are unchanged.

**Methodological boundary:** Because the original local HTML files were not included in the research ZIP or review ZIP, the checks do **not** verify local HTML SHA-256, full HTML parsing fidelity, or all 12,852 normalized cells. The web text is a representation of the official online archive, not a byte-identical copy of the experiment's saved files. Manual transcription can itself introduce errors, although each comparison row includes its source locator for independent review.

## Selected 77-cell cross-check

| Verification dimension | Matches | Needs review |
|---|---:|---:|
| Displayed numeric value | 77 | 0 |
| Statistical row identity | 77 | 0 |
| Reporting period / publication edition | 77 | 0 |
| Seasonal adjustment label | 77 | 0 |
| Statistical unit | 76 | 1 |

The **one selected unit discrepancy** is `2026-11-06:cps_empsit_a08:R17:C6`: official **Table A-11, PERCENT DISTRIBUTION, Job leavers, June 2026 = 11.0%**. The CSV's `raw_value = 11.0` is correct but `unit_code = THOUSAND_PEOPLE` incorrectly implies 11,000 people. It was selected by the **Simple Matching wrong-link** outputs, **not** by the gold reference set.

## Secondary systematic metadata anomaly detection

The source Table A-11 has separate sections for (a) counts, (b) *PERCENT DISTRIBUTION*, and (c) *UNEMPLOYED AS A PERCENT OF THE CIVILIAN LABOR FORCE*. In the normalized CSV, **all three sections** were labeled `THOUSAND_PEOPLE`, so percentage rows were mislabeled. Source Table A-12 records *average* and *median duration in weeks*, but the extracted unit was again `THOUSAND_PEOPLE`.

| Release date | Source table | Incorrect numeric-cell unit labels | Correct unit |
|---|---|---:|---|
| Nov 6, 2026 | A-11: percent distribution + unemployment as % of labor force | 70 | `PERCENT` |
| Oct 2, 2026 | A-11: same two sections | 90 | `PERCENT` |
| Nov 6, 2026 | A-12: average and median unemployment duration | 14 | `WEEKS` |
| Oct 2, 2026 | A-12: same duration measures | 18 | `WEEKS` |
| **Total** | | **192** | |

For all **192 affected cells**, the faulty `THOUSAND_PEOPLE` unit also incorrectly multiplies the stored `canonical_value` by 1,000 (for example, the source **11.0%** becomes `canonical_value=11000.0`; **25.5 weeks** becomes `canonical_value=25500.0`). These are *clear, rule-identifiable unit and normalized-value discrepancies in this limited set of sections*. The list may not exhaust other unit-annotation issues in the 54 normalized source tables. The table-level section semantics were verified on both official source pages; **the 192 individual raw values were not each manually confirmed**. All 192 evidence IDs appear in `BLS_Unit_Metadata_Anomalies_v1.csv`.

**Effect on current evaluation:** None of the **58 selected gold evidence IDs** belongs to the detected 192 mislabelled cells; one of the **21 wrong-prediction IDs** does. The matcher uses the normalized metadata when searching the wider candidate corpus. This was tested in a **separate sensitivity run on a copy** as described below. Retain original frozen predictions as the reported baseline experiment and disclose the sensitivity run distinctly.

## Supplemental sensitivity run — on a copy only

For each of the **192** identified misunit cells, a *separate copy* of the frozen normalized catalog was changed to `unit_code=PERCENT` or `unit_code=WEEKS` as appropriate and `canonical_value=numeric_value` (instead of multiplying the raw reading by 1,000). No other values or source files were changed. The original deterministic matchers were rerun using that corrected copy; 44 claims × two methods = 88 outputs.

- **Only 1 of 88 predictions changed**: in Simple Matching, `CLAIM-030` changed from `LINK` to `ABSTAIN`. Originally the baseline chose `2026-11-06:cps_empsit_a08:R17:C6`, which is **11.0 percent** in the public table but was wrongly encoded as **11,000 people**. Once fixed, the spurious numeric match disappeared. This is direct sensitivity evidence that a unit-normalization bug caused an error in the frozen baseline.
- Attribute-Aware output: **44/44 unchanged**.
- Headline correct links remain **Simple 10/44, Attribute-Aware 35/44**. The original Simple error breakdown (23 wrong + 1 unjustified + 7 over-abstain + 3 correct abstain) becomes **22 wrong + 1 unjustified + 8 over-abstain + 3 correct abstain** in this *supplemental corrected-copy run*. Attribute-Aware stays at 35 correct, 0 wrong, 0 unjustified, 5 over-abstain, 4 correct abstain.
- This sensitivity run **does not** validate all 12,852 cell annotations or demonstrate performance on new releases. It isolates the effect of the 192 identified corrections on these 88 deterministic in-sample predictions.

The item-level and summary counts are saved in `BLS_Unit_Metadata_Sensitivity_v1.csv`. The corrected full 12,852-row catalog is **not** included in the compact audit ZIP; it can be reconstructed from the original research bundle plus the anomaly list.

## Cross-edition derivations: source values match

The six endpoint cells used for the three revised gold labels were found in the indicated November/October release tables. Their arithmetic is:

| Claim | Official table endpoints (in thousands) | Recomputed average monthly change (in thousands) |
|---|---|---|
| 020: total nonfarm | 159,128 − 158,548 | 48.333 → 48 |
| 022: professional/business | 22,534 − 22,359 | 14.583 → 15 |
| 028: health care | 18,550.4 − 18,181.8 | 30.717 → 31 |

The revision combined in CLAIM-051 likewise uses official Summary B values: August 186 vs 133 (thousand), September 60 vs 29 (thousand): **53 + 31 = 84 thousand**.

**Important remaining assumption:** Cross-edition seasonal adjustment revisions can affect whether older and newer seasonally adjusted levels are strictly comparable. Agreement with the report's displayed rounded number is not independent certification of the edition-mixing policy.

## File integrity and remaining gap

- The unchanged evidence CSV SHA-256 is `778ED34144247A04E03AF7F30C308D2E573C2630517663CD65985D74FABD25F6`, matching the pre-existing audit changelog.
- The prior work log records source HTML hashes (Nov 6: `9EA0244B6EE264FABD21F4F4ED80FCF593628F4123DA736D871128E7A26908A2`; Oct 2: `C874654D8892D063A63C6AF10B18ED4B1272FD6F6C06BFD8DCE729D7549F5FB2`), but these hashes **could not be independently recomputed here** because the saved HTML files are unavailable in the supplied packages.
- To complete *archived-local-original* validation, inspect `data/raw/bls/empsit_11062026.html` and `empsit_10022026.html` from the local Windows project, recalculate their SHA-256 and check the HTML cells and extraction selectors directly. Do not label this step complete based on this web-only cross-check.

## Disposition for the research submission

1. Record **77/77 selected raw cell values/row identities matched** publicly archived BLS data and **1 selected unit metadata exception**.
2. Disclose the **192 clear unit metadata and canonical-value scaling errors** identified by a section-based targeted scan and the separate corrected-copy sensitivity run (1/88 predictions changed). This does **not** mean the entire normalized evidence catalog was exhaustively checked.
3. Keep the original evaluation frozen, treat the source metadata anomaly separately, and do not silently replace the original evidence CSV.
4. After local HTML-source verification, decide whether to add the sensitivity result to the report and how to describe the limits of the original 35-vs-10 comparison.

**Companion files:** `BLS_Official_Site_Evidence_Crosscheck_v1.csv`, `BLS_Unit_Metadata_Anomalies_v1.csv`, `BLS_Unit_Metadata_Sensitivity_v1.csv`, and the two audit scripts.
