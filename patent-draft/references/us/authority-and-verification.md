# U.S. authority labels and verification

Retain an authority label and source locator for every jurisdiction-specific rule
in working notes and in `us-rule-check.md`. Do not put the labels in the clean
application.

- `LAW` — enacted U.S. Code.
- `RULE` — current 37 CFR requirement.
- `USPTO-PRACTICE` — MPEP or other official USPTO examination guidance; it does
  not itself have the force of substantive law.
- `DRAFTING` — a professional drafting recommendation derived from the sources.
- `HOUSE-STYLE` — a repository convention for support mapping and consistency.
- `VERIFY` — useful but not confirmed against a current controlling source, or a
  conclusion requiring case-specific legal judgment.

Use locators such as `[LAW US-35-112(a)]`, `[RULE US-37-P1 §1.75(d)(1)]`, and
`[USPTO-PRACTICE US-MPEP-2163.02]`. A citation to the MPEP must not be relabeled
as `LAW` merely because the section quotes a statute or rule.

## Filing-facing verification gate

Before describing a packet as ready for attorney filing review:

1. check the current U.S. Code, eCFR, MPEP landing page, and any later controlling
   USPTO guidance against `source-manifest.md`;
2. resolve every `VERIFY` item or carry it into the handoff as a blocker;
3. confirm that the selected matter is a U.S. utility application and that any
   provisional, continuation, national-stage, or reissue context has been routed
   for specialist review;
4. cross-check claims, description, abstract, drawings brief, terminology,
   numerical ranges, and reference numerals;
5. confirm exact as-filed support for every change to a filed or pending case; and
6. keep unresolved technical and legal questions visible rather than answering
   them by assumption.

This is a drafting-quality gate. It is not authorization to file and does not turn
the packet into legal advice.
