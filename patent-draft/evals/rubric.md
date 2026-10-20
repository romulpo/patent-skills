# RU drafting evaluation rubric

Use these cases for forward-testing `patent-draft`; do not load this rubric during a
normal drafting task.

## Isolation

Give the drafting agent only the case request and the source files listed in
`cases.json`. Do not provide the expected disposition, required observations,
forbidden outcomes, or another run's output. Initialize each run in a new temporary
directory.

## Scoring

For every required observation, assign:

- `pass` — the packet shows the required decision and identifies its support;
- `fail` — the packet contradicts or omits the requirement;
- `cannot_assess` — an expected artifact is missing or unreadable.

For every forbidden outcome, assign `absent` or `present`. Quote the relevant packet
location; do not score by matching preferred wording. A case passes only when every
required observation passes and every forbidden outcome is absent.

## Global failure conditions

Fail a case if the output:

- introduces unsupported technical matter into a clean draft;
- silently switches profiles or object categories;
- hides a blocking choice instead of recording it;
- treats a translation convention or drafting preference as law;
- calls the packet filed, filing-ready, allowed, valid, or legally sufficient;
- modifies a source file.

The corpus validates drafting behavior, not patentability, novelty, inventive step,
or legal advice.
