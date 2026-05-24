# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `ok`: 255
- `unsupported`: 11
- `wrong`: 4

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 2 rows; samples: LD391, NL340
- `capacitor_state_change`: 1 rows; samples: TD398
- `capacitor_target_or_formula`: 1 rows; samples: TD395

## Validator Failures

- No validator failures in this run.

## Unsupported Clusters To Unlock

- `U001` `rlc_formula_family`: 2 rows (ac_rlc); samples: CH238; CH263
- `U002` `rlc_power`: 2 rows (ac_rlc); samples: CH228; CH216
- `U003` `rlc_current`: 1 rows (ac_rlc); samples: CH171
- `U004` `rlc_power_factor`: 1 rows (ac_rlc); samples: CH246
- `U005` `rlc_resonance`: 1 rows (ac_rlc); samples: CH141
- `U006` `capacitor_energy_state`: 1 rows (capacitor); samples: TD375
- `U007` `capacitor_network`: 1 rows (capacitor); samples: TD391
- `U008` `capacitor_target_or_relation`: 1 rows (capacitor); samples: CHLT015
- `U009` `unknown_unsupported`: 1 rows (unknown); samples: CH102

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
