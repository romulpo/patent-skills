# Russian utility-model-specific drafting

## Hard profile constraints

- The claimed object is a device: an article comprising one or more parts in a
  functional and structural unity. A method, substance, application, or
  machine-readable medium is not claimed under this profile.
  `[LAW RU-PM-701 §35]`
- The claims contain exactly one independent claim. A multi-claim set may add only
  dependent claims to that independent claim.
  `[LAW RU-PM-701 §§2,40(1)]`
- Do not place alternative essential features in the independent claim. A continuous
  numerical range is not treated as an alternative merely because it states end
  values. `[LAW RU-PM-701 §40(1)(a)]`
- Characterize the device in a static state. A supported indication that an element
  is movable or capable of performing a function is permitted.
  `[LAW RU-PM-701 §40(9)]`

These constraints override the conflicting sentence in the supplied local summary
about multiple independent claims for variants; see `source-manifest.md`.

## Drafting workflow

1. Confirm the generic device concept and intended purpose.
2. Build one minimum, supported, technically coherent independent feature set.
3. Test every feature for structural or functional connection to the device and the
   technical result; do not disguise method steps as device elements.
4. Move supported particular implementations into dependent claims without deleting
   or contradicting parent limitations.
5. Describe the construction in a static state, then its operation and the causal
   path to the technical result.
6. Check that every claimed element and relationship appears in the description and,
   where used, consistently on the drawings.

If the evidence contains a device, method, and medium claim set from another
jurisdiction, do not silently collapse or discard it. Preserve all source matter in
the evidence inventory, draft only the supported device family under this profile,
list omitted claim categories and scope consequences, and ask whether a parallel
`ru-invention` draft is wanted. `[HOUSE-STYLE]`

## IT devices

An IT implementation does not remove the device-only constraint. Identify supported
hardware or system elements, their relationships, data/control connections, and
functional capabilities. Do not convert a sequence of software actions into a device
claim merely by prefixing each action with `модуль, выполненный с возможностью`.
The disclosure must support the claimed architecture and its ability to perform the
functions. `[LAW RU-PM-701 §§29,38,40] [DRAFTING]`

## Stop conditions

Stop the clean-claim pass and leave an unresolved decision when:

- the only authentic subject is a method or other non-device object;
- more than one independent claim is necessary to preserve the requested scope;
- an essential limitation is expressed only as unsupported alternatives;
- the source lacks a coherent device structure or support for its operation.
