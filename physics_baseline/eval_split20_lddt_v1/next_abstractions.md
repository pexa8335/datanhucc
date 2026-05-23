# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `ok`: 235
- `unsupported`: 18
- `wrong`: 11
- `validator_failed`: 6

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 8 rows; samples: LD391, LD082, LD238, LD279, DT084, DT040
- `capacitor_target_or_formula`: 2 rows; samples: TD395, TD402
- `capacitor_state_change`: 1 rows; samples: TD398

## Validator Failures

- `geometry_relation_missing`: 4 rows; samples: LD094, LD347, LD346, LD073
- `geometry_right_triangle_or_perpendicular`: 1 rows; samples: LD342
- `geometry_equilateral_grounding`: 1 rows; samples: LD090

## Unsupported Clusters To Unlock

- `U001` `rlc_formula_family`: 2 rows (ac_rlc); samples: CH238; CH263
- `U002` `rlc_power`: 2 rows (ac_rlc); samples: CH228; CH216
- `U003` `electrostatics_perpendicular_distance`: 2 rows (electrostatics_field); samples: LD353; DT042
- `U004` `electrostatics_relation_or_vector_gap`: 2 rows (electrostatics_force); samples: LD254; LD014
- `U005` `rlc_current`: 1 rows (ac_rlc); samples: CH171
- `U006` `rlc_power_factor`: 1 rows (ac_rlc); samples: CH246
- `U007` `rlc_resonance`: 1 rows (ac_rlc); samples: CH141
- `U008` `capacitor_energy_state`: 1 rows (capacitor); samples: TD375
- `U009` `capacitor_network`: 1 rows (capacitor); samples: TD391
- `U010` `capacitor_target_or_relation`: 1 rows (capacitor); samples: CHLT015
- `U011` `electrostatics_midpoint_target`: 1 rows (electrostatics_field); samples: LD398
- `U012` `electrostatics_relation_or_vector_gap`: 1 rows (electrostatics_field); samples: DT043
- `U013` `electrostatics_charge_target_mapping`: 1 rows (electrostatics_force); samples: LD021
- `U014` `unknown_unsupported`: 1 rows (unknown); samples: CH102

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
