# U.S. utility claim drafting

## Claim architecture

Build the claim plan from supported commercial and technical boundaries. For each
independent claim, select one statutory category and a technically coherent
combination of limitations. Common supported families include a method, a machine
or system, an article or manufacture, and a non-transitory computer-readable
medium. Do not add parallel families mechanically. `[LAW US-35-112(b)]
[USPTO-PRACTICE US-MPEP-2106] [DRAFTING]`

For software media claims, use `non-transitory` only when the supplied disclosure
supports storage media. A claim whose broadest reasonable interpretation includes
a carrier wave or signal can encompass nonstatutory transitory subject matter.
`[USPTO-PRACTICE US-MPEP-2106.03]`

## Independent claims

- Recite all features needed for the selected technical combination, but do not
  import optional embodiment details without an explicit scope reason.
- Put relationships, data flow, ordering, and conditions into the claim when they
  are necessary to distinguish the technical operation.
- Keep the actor and system boundary clear. Do not mix a system with user actions
  in a way that makes it unclear what product or conduct satisfies the claim.
- Use functional language only when its scope is understandable from the claim and
  supported description. A result alone is not a disclosed implementation.
- Record every deliberate omission, breadth choice, and unresolved term in the
  claim plan.

`[LAW US-35-112(a)–(b)] [USPTO-PRACTICE US-MPEP-2163, US-MPEP-2164,
US-MPEP-2173] [DRAFTING]`

## Dependent claims

A dependent claim must refer to a previous claim and further limit it; it must not
replace or contradict a parent limitation. Use supported fallback positions tied
to architecture, operation, ranges, materials, data processing, error handling, or
other disclosed distinctions. `[LAW US-35-112(d)] [RULE US-37-P1 §1.75(c)]`

If a multiple dependent claim is used, it must refer to prior claims in the
alternative only, and another multiple dependent claim may not depend from it.
Prefer single dependencies unless the user has a reason for the additional form
and fee complexity. `[LAW US-35-112(e)] [RULE US-37-P1 §1.75(c)] [DRAFTING]`

## Clarity and support checks

- Every claim term must have clear support or antecedent basis in the description.
- Introduce elements before referring to `the` or `said` element; choose one
  convention and use it consistently.
- Define relative or degree terms through disclosed context, boundaries, examples,
  or measurement methods when their scope would otherwise be uncertain.
- Check numerical ranges for units, inclusivity, overlap, precision, and support
  for endpoints and subranges.
- Check alternatives independently. Each branch must combine grammatically and
  technically with the rest of the claim.
- Read each claim as a whole and against the drawings, terminology map, and support
  map. Do not rely on an unstated intended interpretation.

`[RULE US-37-P1 §1.75(d)(1)] [USPTO-PRACTICE US-MPEP-608.01(o),
US-MPEP-2173] [DRAFTING]`

## Section 112(f)

Decide deliberately whether a functional limitation is intended to invoke
35 U.S.C. § 112(f). The absence of the word `means` does not guarantee that
§ 112(f) is avoided; a generic placeholder coupled to function may still be
treated as means-plus-function language. If § 112(f) may apply, map the complete
claimed function to corresponding structure, material, or acts in the description.
`[LAW US-35-112(f)] [USPTO-PRACTICE US-MPEP-2181]`

For a computer-implemented § 112(f) limitation, disclose the computer or processor
and an algorithm that performs the entire claimed function. Repeating the desired
result or naming a black-box `module`, `engine`, or `manager` is not an algorithm.
`[USPTO-PRACTICE US-MPEP-2181 II.B]`
