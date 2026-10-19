# EN-to-RU translation and adaptation review

Use only in `translate_adapt` mode. The source application and supplied target draft
are evidence; preserve both and record hashes. Translation may adapt expression to
the selected Russian profile, but it may not add technical matter or silently change
scope.

## Review sequence

1. Align source and target by title, section, paragraph, claim, figure, table, and
   reference numeral.
2. Build the terminology map before revising claims. Assign one preferred Russian
   term to each source concept and record justified exceptions.
3. Review claims first: object category, claim count, dependencies, limitations,
   alternatives, numerical values, units, and one-sentence structure.
4. Review the disclosure, implementation, drawings, and abstract against the revised
   claims and technical result.
5. Record every substantive adaptation in the change log with source location,
   target location, reason, support, and scope effect.

## Finding severity

- `critical`: unsupported matter, lost or changed claim limitation, wrong object
  category, invalid utility-model claim architecture, changed numerical value/unit,
  or a contradiction affecting scope or implementation;
- `material`: inconsistent terminology, lost causal relationship, incorrect
  dependency, figure mismatch, or an omission likely to impair clarity/support;
- `editorial`: style or language that does not change technical meaning or scope.

The severity system is a local review convention, not a statutory classification.
`[TRANSLATION LOCAL-INV-TRANSLATION] [TRANSLATION LOCAL-PM-TRANSLATION]`

## Translation controls

- Do not translate `method/process` mechanically as `метод` or `процесс` when the
  claimed Russian object is a patentable method; evaluate `способ` in context.
- Treat `configured to` as a technical capability. `выполненный с возможностью` is a
  common starting point for a device, but use it only when the disclosed structure
  supports that capability and the phrasing remains clear.
- Translate `computer-readable medium` consistently as `машиночитаемый носитель`
  when that object belongs in the selected invention profile. Do not add a medium
  claim to a utility-model draft.
- Preserve numbers, ranges, signs, formulae, units, identifiers, and reference
  numerals exactly unless a documented supported conversion is required.
- Do not translate a business, informational, or aesthetic effect into a technical
  result by embellishment. Flag the source problem instead.

Return both a clean adapted draft and the completed review/change-log artifact.
