# RU authority labels and verification

Every jurisdiction-specific proposition must retain one of these labels in working
notes and review findings. The label need not appear in the clean application.

- `LAW` — supported by a cited provision of an official normative source.
- `RUPTO-PRACTICE` — supported by an official Rospatent/FIPS examination guide or
  published practice material, but not stated as a normative requirement.
- `TRANSLATION` — a translation-review convention from the supplied local guides.
- `DRAFTING` — a professional drafting recommendation derived from the sources.
- `HOUSE-STYLE` — a repository convention for consistency or auditability.
- `VERIFY` — plausible or useful, but not verified against a current primary source.

Use the most specific source locator available, for example
`[LAW RU-INV-107 §62(8)]`. Do not relabel a local summary as `LAW` merely because it
names an order. When sources conflict, prefer the current official normative text,
record the conflict, and do not silently harmonize it.

## Filing-facing verification gate

Before describing a draft as ready for filing review:

1. confirm that the official versions and amendment dates in
   `source-manifest.md` are still current;
2. re-check every `VERIFY` item and any rule affected by a source conflict;
3. confirm that the chosen profile matches the intended Russian protection type;
4. confirm the claims, description, abstract, drawings, terminology, and reference
   numerals against each other;
5. retain unresolved legal or technical issues in the handoff rather than resolving
   them by assumption.

This gate is a drafting quality control. It is not authorization to file and does
not turn the output into legal advice.
