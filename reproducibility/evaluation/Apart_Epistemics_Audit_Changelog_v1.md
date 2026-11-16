# Apart AI x Epistemics Sprint — secondary audit and report change log

Audit date: 2026-11-15 (JST)

## Scope and source integrity

- The attached original ZIP and its four important inputs have not been changed.
- `lesson4_matcher_input_frozen.csv` SHA-256: `92EAAB457A11E634A64446975E94083A8676AF26B85B7A74D806F5938C587C15`.
- `lesson4_evidence_normalized_draft.csv` SHA-256: `778ED34144247A04E03AF7F30C308D2E573C2630517663CD65985D74FABD25F6`.
- `gold_main_proposed.csv` SHA-256: `6F8949C065E745014008EEEA96502831EA13358A51D04EB36F3F71CB01BB7D31`.
- `matcher_predictions.csv` SHA-256: `49D99550F084602072F271AA06C90E02B981C77FB68FBE94BCD890A2321CDEDB`.

## Summary

- The source ZIP contains 44 MAIN claims, 28 originally DIRECT, 9 DERIVED, 7 OUT_OF_CORPUS.
- Each original accepted evidence ID exists in the 12,852-record normalized evidence CSV and references a numeric cell, with matching stated row identity, season and date where applicable in the secondary inspection.
- 3 historical monthly-average claims were originally labeled OUT_OF_CORPUS on the assumption that all 12 monthly changes had to be present. They can instead be reconstructed by telescoping the 12-month sum of changes using two endpoint levels, drawing on the two eligible publication editions.
- This correction is conditional on comparing seasonally adjusted levels across publication vintages; no independent archived HTML checksum audit or expert adjudication was performed.
- Revised working label counts: 28 DIRECT, 12 DERIVED, 4 OUT_OF_CORPUS. Neither frozen claim text nor matcher predictions were modified.

## Item-level changes

| Claim | Original -> audit label | Full numerical reconstruction | Accepted proof IDs |
|---|---|---|---|
| 020 | OUT_OF_CORPUS -> DERIVED | (159,128,000 - 158,548,000)/12 = 48,333.3 -> 48,000 | `2026-10-02:ces_table1:R3:C6`, `2026-11-06:ces_table1:R3:C8` |
| 022 | OUT_OF_CORPUS -> DERIVED | (22,534,000 - 22,359,000)/12 = 14,583.3 -> 15,000 | `2026-10-02:ces_table1:R122:C6`, `2026-11-06:ces_table1:R122:C8` |
| 028 | OUT_OF_CORPUS -> DERIVED | (18,550,400 - 18,181,800)/12 = 30,716.7 -> 31,000 | `2026-10-02:ces_table1:R150:C6`, `2026-11-06:ces_table1:R150:C8` |

These claims refer to the 12 months *preceding October 2026* (Sep 2025 -> Sep 2026). Using Oct 2025 -> Oct 2026 would include October 2026 and is not the intended window.

## Revised outcome counts (same fixed predictions)

| Outcome | Simple Matching | Attribute-Aware Matching |
|---|---:|---:|
| Correct links | 10 | 35 |
| Wrong links | 23 | 0 |
| Unjustified links | 1 | 0 |
| Over-abstentions | 7 | 5 |
| Correct abstentions | 3 | 4 |
| Correct links among all 44 | 22.7% | 79.5% |
| Correct links among 40 linkable | 25.0% | 87.5% |

- Simple originally had 22 WRONG_LINK and 2 UNJUSTIFIED_LINK. CLAIM-022 shifts from UNJUSTIFIED_LINK to WRONG_LINK. CLAIM-020 and CLAIM-028 shift from CORRECT_ABSTAIN to OVER_ABSTAIN.
- Attribute-Aware originally had 2 OVER_ABSTAIN and 7 CORRECT_ABSTAIN. CLAIM-020, -022 and -028 shift from CORRECT_ABSTAIN to OVER_ABSTAIN.
- The absolute 35 vs 10 correct-link counts and the combined 24 wrong/unjustified baseline links are unchanged.

## Report changes from bundled report_draft.md

- Replaced 37 linkable / 7 out-of-corpus with provisional 40 / 4 and explained the cross-edition rule.
- Updated linkable-denominator rates, abstention counts and all case analyses affected by the reclassification.
- Added a clear distinction between normalized-CSV secondary audit and independent source-HTML audit.
- Added FEVER and W3C PROV-related-work context, explicit conclusion and an LLM usage disclosure.
- Reformatted using the authentic Apart Research Google Docs submission template obtained from the organizer link and exported to DOCX; the report is a review candidate and has **not** been submitted.
- Preserved the organizer-mandated 150-250-word abstract and “Limitations and Dual-Use / Ethical Considerations” appendix.

## Open review boundary before publication

1. Confirm permission to accept the cross-edition September 2025 / September 2026 comparison as a complete proof for the three average-gain claims.
2. Independently verify archived source HTML extraction and hashes if claiming fully validated provenance.
3. Review the unenumerated alternative evidence proofs and the deliberate numerical-only scoring scope.

No new matching implementation, holdout experiment, or independent source-archive validation was performed in this audit.
