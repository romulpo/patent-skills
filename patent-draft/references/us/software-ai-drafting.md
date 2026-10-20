# U.S. software and AI drafting

Use this reference when software, machine learning, or AI supplies a material part
of the claimed technical contribution. It supplements, rather than replaces, the
general specification and claim rules.

## Establish the technical teaching

Before drafting claims, record from supplied evidence:

- the technical problem and the computer or other technology being improved;
- the system boundary, components, and allocation of functions;
- input data, its source and representation, preprocessing, state, and outputs;
- the ordered algorithm, decision conditions, data structures, and exceptional
  paths needed to perform each material function;
- the disclosed mechanism connecting features to the asserted improvement; and
- the test, metric, or observation supporting any performance statement.

Do not turn a business objective, desired prediction, or model label into a
technical mechanism. Do not invent architecture, hyperparameters, datasets,
benchmarks, accuracy, latency, or resource savings. `[LAW US-35-112(a)]
[USPTO-PRACTICE US-MPEP-2163, US-MPEP-2164] [DRAFTING]`

## Training and inference

Treat training and inference as different processes unless the evidence expressly
combines them. For a supported training invention, capture the source and structure
of training data, labeling or target generation, feature preparation, model update
procedure, objective, stopping or validation logic, and produced model artifact at
the level actually disclosed. For a supported inference invention, capture model
inputs, preprocessing, execution, output interpretation, downstream control, and
technical effect.

Claim neither a training method nor a trained model merely because the other is
disclosed. Generalize across model types only when the evidence teaches the shared
mechanism and the breadth is enabled. `[LAW US-35-112(a)] [USPTO-PRACTICE
US-MPEP-2163.02, US-MPEP-2164.08]`

## Eligibility-aware disclosure

Current USPTO eligibility analysis is claim-specific. A specification asserting a
technological improvement should explain what the improvement is and how the
disclosed features produce it. Generic computer implementation, field-of-use
language, data collection, or post-solution activity alone should not be treated as
a guaranteed practical application. `[USPTO-PRACTICE US-MPEP-2106]`

Drafting for an eligibility record does not establish that a claim is eligible.
Mark uncertain classifications and case-law-dependent conclusions `VERIFY` and
route them for legal review. `[DRAFTING]`

## Functional claiming and disclosure depth

For each claimed software function, the support map should point to more than a
box name. Identify the disclosed steps, rules, mathematical operations, data
transformation, or other algorithmic detail that performs it. The form may be
prose, a flowchart, pseudocode, equations, or another understandable representation
supported by the evidence. `[USPTO-PRACTICE US-MPEP-2161.01, US-MPEP-2181 II.B]`

If the disclosed implementation is too thin for the requested scope, narrow to the
supported mechanism or ask the inventor for missing technical detail. Do not fill
the gap with conventional-sounding code or architecture. `[HOUSE-STYLE]`
