# RU source manifest

Verified on 2026-10-19 for this skill revision. Local source files remain outside
the repository; hashes identify the exact material reviewed.

## Primary and official practice sources

| ID | Source | Version observed | Role | SHA-256 |
|---|---|---|---|---|
| `RU-INV-107` | Official FIPS PDF, Order of the Ministry of Economic Development No. 107 of 2023 | consolidated through 2024-03-15 in the retrieved PDF | normative source for invention application documents | `aa984f9788227a42877acd19745c1b9c2caaf1b2bbd2ed386ee7f76262a4ff68` |
| `RU-PM-701` | Official FIPS PDF, Order No. 701 of 2015 | consolidated through 2024-03-15 | normative source for utility-model application documents | `e00e810b621c9925e19bf0319ed3ebd98856810bd27829e4f9c6100227652174` |
| `RU-PM-GUIDE` | Official FIPS utility-model examination guide, Order of Rospatent No. 233 of 2018 | retrieved 2026-10-19 | official practice source; subordinate to current normative text | `dba66d9fea4f60b20684371eb0789b70cf3e6cdb140b6a6b3478555d4694655a` |

Official locations:

- `RU-INV-107`: <https://new.fips.ru/documents/npa-rf/prikazy-minekonomrazvitiya-rf/prikaz-minekonomrazvitiya-107-21022023.pdf>
- `RU-PM-701`: <https://new.fips.ru/documents/npa-rf/prikazy-minekonomrazvitiya-rf/prikaz-minekonomrazvitiya-701-30092015-2.pdf>
- `RU-PM-GUIDE`: <https://new.fips.ru/to-applicants/inventions/ruc_pm.pdf>

## Supplied working sources

| ID | Local source | Role | SHA-256 |
|---|---|---|---|
| `LOCAL-INV-SUMMARY` | `knowledge/rospatent-prikaz-107-2023.md` | searchable summary; never primary authority | `0d9e0fe815f7f49a2d096b970d712a78169afefb7d1b3e2cf3841c3ff8f89248` |
| `LOCAL-PM-SUMMARY` | `knowledge/rospatent-prikaz-701-2015-pm.md` | searchable summary; never primary authority | `2ed446e9d7e118cbc42a2eef044f02e95a7960eded64207a7560da8477685d80` |
| `LOCAL-INV-TRANSLATION` | `guideline-translation-review-invention.md` | EN-to-RU review and terminology conventions | `d64c8662c956db5e5f041caa250109e4bbc58cd6c83d0d09950906d45089b8a7` |
| `LOCAL-PM-TRANSLATION` | `guideline-translation-review-utility-model.md` | EN-to-RU utility-model review conventions | `7deb986ed9e2c2bb9a4c43dc4fb7ae7e0c8e111415c950658736bf8ff62af722` |

## Known conflicts and limits

- The local utility-model summary contains a later statement suggesting that
  multiple independent claims for variants may be possible. The official
  `RU-PM-701` text, §§2 and 40(1), requires one independent claim. Use the official
  rule: exactly one independent claim.
- The local invention translation guide names an amendment dated 2024-09-27, while
  the official FIPS PDF retrieved for this review identifies consolidation through
  2024-03-15. Treat post-2024-03-15 amendment assertions as `VERIFY` until checked
  against a current official publication.
- The supplied materials focus on IT, AI, devices, systems, methods, and
  machine-readable media. Chemistry, biotechnology, pharmaceuticals, sequences,
  and other specialized subjects require additional authoritative references.
- This repository stores distilled drafting instructions, not copies of the
  external source corpus. Recompute hashes when a source file changes.
