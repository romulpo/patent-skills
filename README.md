# patent-skills

Agent skills for drafting, reviewing, examining, and reviewing patent
applications [USPTO, ROSPATENT].

## Skills

| Skill | Purpose | Jurisdiction |
|---|---|---|
| `patent-draft` | Evidence-grounded drafting, revision, claim planning, and translation/adaptation | US and Russia |
| `patent-audit` | Primary-source pre-filing audit | US utility |
| `patent-examine` | Recurrent simulated examination | US utility |
| `patent-workaround` | Adversarial design-around testing | US utility |

`patent-draft` requires one explicit profile:

- `us-utility` — source-mapped U.S. utility drafting, including specification,
  claims, § 112 support, abstract/drawings coordination, and software/AI guidance;
- `ru-invention` — source-mapped Rospatent invention drafting;
- `ru-utility-model` — source-mapped Rospatent utility-model drafting.

The jurisdiction profiles separate law, office practice, drafting guidance, house
style, and rules that still need verification. Each drafting-ready profile includes
dedicated description, claims, abstract, and rule-check templates; the Russian
profiles also include EN-to-RU review. User-supplied evidence is hashed in place,
and external authority text is cited rather than copied into the repository.

## Start a drafting case

```bash
python patent-draft/scripts/init_case.py \
  --profile ru-invention \
  --mode new_draft \
  --language ru \
  --filing-context pre_filing \
  --source invention-disclosure.md \
  --output case-dir
```

Modes: `new_draft`, `revise`, and `translate_adapt` where supported. U.S. and
Russian outputs include a filing-facing source-verification gate because laws and
office practice change.

## Install

Copy the required skill directories into your agent's skills directory, then invoke
the relevant skill by name. Python 3 is required for deterministic scripts.

Example:

```text
Use $patent-draft with the ru-utility-model profile to draft from these materials.
```

## Safety

This repository is not a law firm and does not provide legal advice. The skills do
not file applications, sign documents, contact patent offices, or guarantee
allowance, validity, enforceability, or commercial scope. Verify current official
sources and use qualified counsel when the consequences require it.

## Validation

The RU drafting evaluation corpus contains six synthetic cases covering claim
architecture, profile mismatch, translation integrity, missing disclosure, and new
matter after filing.

```bash
python -m unittest discover -s patent-draft/tests -v
python patent-draft/scripts/validate_evals.py
python patent-workaround/scripts/test_coverage_state.py
```

Licensed under GPL-3.0.
