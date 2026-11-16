# Apart AI × Epistemics Sprint — Track 2 reproducibility package (v0.4)

**Research:** *When Can Numerical Claims Be Linked to Primary Statistical Evidence?*  
**Author:** Hashirigaki — Independent Researcher  
**Archive prepared:** 2026-11-16 JST  
**Status:** Final locally prepared reproducibility archive, **not a claim that the report has already been submitted or that this ZIP has been uploaded publicly**. The author audit was completed 2026-11-15 JST. No independent expert adjudication or unseen-data benchmark was performed.

## What this archive supports

This package supports inspection of the original claims, normalized evidence records, hand-proposed and revised proof labels, deterministic matcher implementations, scored predictions, BLS source HTML snapshots, and audit trail. It allows reproduction of the frozen 88 matcher predictions and the audited in-sample 10-versus-35 comparison. It **does not** demonstrate out-of-sample accuracy, exhaustive source coverage, or complete independent proof validation.

## Contents

- `experiment/` — original immutable 51-unit claim input (7 PILOT, 44 MAIN), initial gold annotations, 12,852-row normalized catalog, 88 frozen predictions, and deterministic Python code.
- `evaluation/` — secondary-audit labels, failure classifications and 44-claim/88-outcome score tables, audit change log, and the audit/rescore Python script.
- `source_html/` — author-saved copies of the October 2 and November 6, 2026 BLS releases, saved 2026-11-15 JST according to the work log; original exact save time was not recorded.
- `audit/` — 29-outcome failure audit, HTML cell checks, eight omitted eligible cells, 192 known unit-normalization defects, earlier author failure-case review, and the fixed-seed success/abstention selection and **completed author visual check**.
- `report/` — `Apart_Epistemics_Track2_Hashirigaki_Final.pdf`, the v0.4 report reflecting the completed additional author checks and the final Code and Data repository reference.
- `MANIFEST_SHA256.txt` — SHA-256 checksums for all archived files other than the manifest itself. Verify file content, not just archive filenames.

## Historical filenames and pre-check records (important)

1. `experiment/lesson4_evidence_normalized_draft.csv` retains its **historical filename**, which contains `draft`, but **is the frozen, evaluated evidence catalog**. Its original content and SHA-256 were preserved; it was not renamed, corrected, or silently replaced. Known defects are documented in `audit/` and in the paper. The word `draft` does not mean this ZIP contains a new provisional dataset.
2. The `audit/Apart_Track2_Positive_and_Abstention_Author_Check_v0.3.*` files are retained verbatim as **pre-inspection selection sheets** and therefore still say checks are "PENDING". This is a historical state, **not** the final audit outcome. The completed author-reported findings are in `audit/Author_Positive_Abstention_Completion_2026-11-15.md` and `.csv` and in the v0.4 PDF.
3. Parser IDs are internal identifiers, not official BLS numbering: `cps_empsit_a08` = official Table A-11, `cps_empsit_a09` = official Table A-12; `ces_table10` = official Summary table B (not Table B-10).
4. Source HTML file SHA-256s establish byte identity with logged local saved snapshots, not publisher-issued cryptographic signatures.

## Reproduce predictions without overwriting archived inputs

Requires Python 3, standard library only. **First extract the ZIP, then work in a separate copy of `experiment/`.** Run `python compare_matchers.py` from the copied `experiment/` directory. It recreates 44 × 2 = 88 predictions. Compare the resulting `matcher_predictions.csv` byte hash to the manifest:

```
49D99550F084602072F271AA06C90E02B981C77FB68FBE94BCD890A2321CDEDB
```

For the audited rescore, create a separate scratch directory containing an unchanged copy of `evaluation/audit_and_rescore.py` and copies of these four files from `experiment/`: `lesson4_matcher_input_frozen.csv`, `lesson4_evidence_normalized_draft.csv`, `gold_main_proposed.csv`, `matcher_predictions.csv`. Run `python audit_and_rescore.py` from that scratch directory. Its `gold_main_audit_v1.csv`, `audit_44_main_v1.csv`, and `comparison_scored_audit_v1.csv` should be byte-identical, respectively, to the archived `evaluation/Apart_Epistemics_Gold_Audit_v1.csv`, `evaluation/Apart_Epistemics_Audit_44_v1.csv`, and `evaluation/Apart_Epistemics_Comparison_Scored_Audit_v1.csv`. This audited rerun is a **recalculation under the stated annotation convention**, not fresh independent judgment.

`experiment/run_all.py` recreates the **initial** proposed gold and provisional scores, not the secondary-audited working labels; its provisional score counts may therefore differ from the report's audited score breakdown. Do not overwrite archived input files when running it.

## Known limitations

- Both matchers search only seasonally adjusted numeric cells from the November 6 edition; audited proposed proofs may combine both editions.
- The attribute-aware implementation uses explicit phrase guards; it was developed with the evaluation corpus visible, as was the proposed reference annotation. Correlated errors may persist.
- Eight eligible cells were omitted from the extracted catalog; 192 known unit/canonical-scale records were misnormalized. A separate corrected-copy sensitivity analysis changed 1 of 88 predictions but **neither 10 nor 35 correct-link counts**.
- The earlier author checked nine failure-related examples. A separately selected six correct links and two correct abstentions were subsequently checked, with **0/8 observed discrepancies**; these are non-blind author checks, not complete independent verification or a generalizable error-rate estimate. Correct-abstention inspection did not exclude all possible alternative evidence.
- All original frozen input, evidence, prediction and initial annotation files remain unmodified. The updated README, author-completion record, report and hash manifest are **release-documentation changes only**.

## Publication state

The companion repository has been created at https://github.com/Hashirigaki/numerical-claim-evidence-binding. This address identifies the project, but the archive contents must be uploaded and verified on GitHub before they can be described as publicly available there. The report PDF can be submitted separately to the Sprint organizer.
