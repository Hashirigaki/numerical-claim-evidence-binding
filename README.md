# Numerical Claim Evidence Binding

**When Can Numerical Claims Be Linked to Primary Statistical Evidence?**  
Hashirigaki · Independent Researcher  
Apart AI × Epistemics Research Sprint 2026 · Track 2 — Trust Infrastructure

> **Repository status (2026-11-16 JST):** The Sprint project was submitted on 2026-11-16 JST. The final research PDF, frozen code and data, audit records, saved BLS source HTML, and per-file checksums are available in [reproducibility/](reproducibility/).

## Research question

When a numerical claim cites an authoritative source, does the cited evidence *actually establish the claimed number*? Matching a value is insufficient if the cell belongs to a different statistical indicator, population, reporting period, unit, or publication edition. Changes and revisions may require a **complete set of cells and an explicit calculation**, rather than a single matching value.

This bounded study compares two **deterministic Python matchers** on claims from the U.S. Bureau of Labor Statistics (BLS) *Employment Situation — October 2026* release. It does not evaluate an autonomous agent or perform LLM inference at prediction time.

## Study at a glance

| Item | Scope / result |
| --- | --- |
| Claim units | 51 total: 7 PILOT, 44 frozen MAIN |
| Primary sources | BLS release editions dated 2026-10-02 and 2026-11-06 |
| Normalized evidence catalog | 54 table instances; 12,852 records |
| Proposed auditable proof labels | 28 DIRECT, 12 DERIVED, 4 OUT_OF_CORPUS after audit |
| Numerically linkable MAIN claims | 40 / 44 under the stated mixed-edition proof convention |
| Correct complete links — Simple Matching | **10 / 44** (22.7%) |
| Correct complete links — Attribute-Aware Matching | **35 / 44** (79.5%) |
| Wrong or unjustified links | Simple **24**, Attribute-Aware **0** |
| Over-abstentions | Simple **7**, Attribute-Aware **5** |

A *correct complete link* agrees with a **manually proposed accepted numerical proof set**, not with an independently adjudicated universal ground truth. These are **in-sample descriptive counts**, not estimates of accuracy on unseen data.

### Why links failed

The 24 Simple Matching wrong/unjustified links were classified by primary cause as: wrong statistic/group/row/unit (14), wrong reporting period (7), incomplete proof set (2), and a claim not fully provable from the permitted tables (1).

The Attribute-Aware matcher had five over-abstentions: four cross-edition calculations excluded by implementation scope or explicit guards, and one missing correspondence between a paraphrased indicator and its official table label.

Both matchers searched **seasonally adjusted numeric cells from only the 2026-11-06 release**, while the audited proof convention also permitted combinations across the two editions. The attribute-aware matcher additionally used explicit phrase guards. Its zero false links must not be interpreted as general autonomous verification ability.

## Source and author audits

- Programmatic checks found all **12,852 included raw cell values** matched the two author-saved HTML snapshots.
- The audit detected **8 omitted eligible cells** and **192 known unit/canonical-scale defects** in the normalized catalog.
- A corrected-*copy* sensitivity test changed **1 of 88 predictions**, but did not change the **10 vs 35** correct-link counts.
- The author visually inspected nine failure-related examples, then a fixed-seed selection of **six correct links and two correct abstentions**; no discrepancies were observed in the eight additional checks.
- The sampled, non-blind author checks are **not** independent expert validation of all proposed proof sets. The correct-abstention checks did not exhaustively rule out every alternative evidence source.

The original evaluated inputs, predictions, and initial annotations were preserved. Changes to working proof labels and sensitivity-test outputs are documented separately.

## Reproducibility materials

The final reproducibility package, distributed as **`Apart_Epistemics_Track2_Reproducibility_Final.zip`**, is published at [reproducibility/](reproducibility/). Its internal folder structure is preserved:

| Path | Contents |
| --- | --- |
| [`report/`](reproducibility/report/) | Final research PDF |
| [`experiment/`](reproducibility/experiment/) | Frozen claims, normalized evidence, initial proof proposals, two matchers, scorer, 88 predictions |
| [`evaluation/`](reproducibility/evaluation/) | Audited working annotations, outcomes, failure analysis, rescoring script |
| [`source_html/`](reproducibility/source_html/) | Two locally saved BLS release HTML files |
| [`audit/`](reproducibility/audit/) | Source checks, known metadata defects, author visual-audit records |
| [`MANIFEST_SHA256.txt`](reproducibility/MANIFEST_SHA256.txt) | Per-file SHA-256 fingerprints |
| [`README.md` (archive)](reproducibility/README.md) | Detailed rerun instructions and historical-file notes |

**Re-running:** Extract the archive, copy `experiment/` to a scratch directory, and run `python compare_matchers.py` from within that copied directory. For audited rescoring, run `evaluation/audit_and_rescore.py` in a *separate* scratch directory with copies of `lesson4_matcher_input_frozen.csv`, `lesson4_evidence_normalized_draft.csv`, `gold_main_proposed.csv`, and `matcher_predictions.csv`. Python 3 standard library is sufficient for those scripts. Check generated files against the archive's manifest; do not overwrite the frozen inputs.

The historical filename `lesson4_evidence_normalized_draft.csv` is retained for traceability: despite the word `draft`, **it is the frozen evaluated evidence catalog**. Known extraction and normalization defects are documented; they have not been silently corrected in the evaluated input.

## Limitations and transparency

The simple baseline was intentionally weak. Proposed gold annotations and matcher rules were developed with visibility into this evaluation corpus, using a shared AI-assisted workflow; correlated misunderstandings are possible. No held-out evaluation or independent expert adjudication was performed. Several accepted mixed-edition reconstructions remain conditional on the comparability of revised seasonally adjusted series.

An LLM assisted with claim splitting, proposed proof annotations, Python implementation, audit scripts, and writing. **Prediction-time matching was performed by local deterministic Python code, without LLM inference.** The author retains responsibility for the research.

## Primary sources

- [BLS Employment Situation — October 2026 (released November 6, 2026)](https://www.bls.gov/news.release/archives/empsit_11062026.htm)
- [BLS Employment Situation — September 2026 (released October 2, 2026)](https://www.bls.gov/news.release/archives/empsit_10022026.htm)

See the [final research PDF](reproducibility/report/Apart_Epistemics_Track2_Hashirigaki_Final.pdf) for the full references, scoring definitions, audit limitations, and examples of structured evidence links.
