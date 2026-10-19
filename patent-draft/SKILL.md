---
name: patent-draft
description: Plan and draft a patent application from supplied invention evidence under an explicit U.S. utility, Russian invention, or Russian utility-model profile. Use for new drafting, supported revision, claim architecture, or EN-to-RU adaptation; not for filing, prosecution, infringement opinions, freedom-to-operate opinions, or unsupported invention of technical matter.
---

# Patent application drafting

Turn authentic invention evidence into a support-mapped draft. Preserve the user's
source material and keep drafting decisions auditable.

## Select the profile before drafting

Use exactly one profile:

- `us-utility`
- `ru-invention`
- `ru-utility-model`

Do not infer the profile from the document language or from the fact that the
invention is a device. If the intended profile is not established, obtain it before
making jurisdiction-specific drafting choices.

Read [references/common/drafting-workflow.md](references/common/drafting-workflow.md),
[references/common/evidence-and-no-fabrication.md](references/common/evidence-and-no-fabrication.md),
[references/common/claim-first-method.md](references/common/claim-first-method.md),
and [references/common/deliverable-contract.md](references/common/deliverable-contract.md).
Then read only the selected profile:

- [references/profiles/us-utility.md](references/profiles/us-utility.md)
- [references/profiles/ru-invention.md](references/profiles/ru-invention.md)
- [references/profiles/ru-utility-model.md](references/profiles/ru-utility-model.md)

For either Russian profile, use only the RU references routed by that profile.
Treat their authority labels as part of the rule: a local drafting or translation
convention is not a statement of law. Before any filing-facing handoff, confirm the
current official text as required by the RU source manifest; this skill does not file.

## Initialize the case

Run:

```bash
python scripts/init_case.py --profile PROFILE --mode MODE \
  --language LANGUAGE --filing-context CONTEXT --output CASE_DIR \
  [--source FILE ...]
```

Allowed modes are `new_draft`, `revise`, and `translate_adapt`. Allowed filing
contexts are `pre_filing` and `filed_pending`. The initializer records hashes and
creates profile- and mode-specific working artifacts; it does not modify or copy the
source files.

## Non-negotiable drafting invariants

- Do not invent embodiments, alternatives, measurements, performance, technical
  effects, prior-art facts, dates, or inventor facts.
- Distinguish supplied fact, supported inference, requested confirmation, and
  unsupported matter.
- Create the invention thesis and claim plan before drafting a full description.
- Map every planned claim limitation to supplied support. Unsupported limitations
  do not enter the draft.
- Treat filed or pending material as frozen for new-matter purposes: propose no
  substantive addition without exact as-filed support.
- Keep unresolved inventor choices visible. Silence is not confirmation.
- Do not file, submit, sign, contact an office, or characterize the output as legal
  advice or a patentability, validity, infringement, or freedom-to-operate opinion.

## Completion

A drafting run is complete only when it returns the artifacts required by the
deliverable contract, including the support map and unresolved decisions. A clean
application without those audit artifacts is incomplete.
