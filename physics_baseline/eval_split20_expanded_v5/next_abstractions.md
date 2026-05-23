# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `ok`: 211
- `unsupported`: 43
- `wrong`: 10
- `validator_failed`: 7

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 8 rows; samples: LD391, LD055, LD050, LD384, LD049, LD400
- `capacitor_state_change`: 1 rows; samples: TD398
- `capacitor_target_or_formula`: 1 rows; samples: TD395

## Validator Failures

- `geometry_relation_missing`: 5 rows; samples: LD082, LD094, LD347, LD346, LD073
- `geometry_right_triangle_or_perpendicular`: 1 rows; samples: LD342
- `geometry_equilateral_grounding`: 1 rows; samples: LD090

## Unsupported Clusters To Unlock

- `U001` `electrostatics_equilateral_vertices`: 7 rows (electrostatics_field); samples: LD306; LD318; LD394; LD322; LD296; LD311; LD377
- `U002` `electrostatics_relation_or_vector_gap`: 7 rows (electrostatics_force); samples: LD254; LD244; LD014; LD246; LD260; LD133; LD217
- `U003` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD053; DT084; DT092; DT090; DT093; DT083
- `U004` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD309; DT059; DT055; DT043; DT036; DT030
- `U005` `electrostatics_perpendicular_distance`: 3 rows (electrostatics_field); samples: LD353; DT042; DT058
- `U006` `rlc_formula_family`: 2 rows (ac_rlc); samples: CH238; CH263
- `U007` `rlc_power`: 2 rows (ac_rlc); samples: CH228; CH216
- `U008` `rlc_current`: 1 rows (ac_rlc); samples: CH171
- `U009` `rlc_power_factor`: 1 rows (ac_rlc); samples: CH246
- `U010` `rlc_resonance`: 1 rows (ac_rlc); samples: CH141
- `U011` `capacitor_network`: 1 rows (capacitor); samples: TD391
- `U012` `capacitor_target_or_relation`: 1 rows (capacitor); samples: CHLT015
- `U013` `electrostatics_charge_target_mapping`: 1 rows (electrostatics_field); samples: DT025
- `U014` `electrostatics_equilateral_vertices`: 1 rows (electrostatics_field); samples: DT040
- `U015` `electrostatics_midpoint_target`: 1 rows (electrostatics_field); samples: LD398
- `U016` `electrostatics_charge_target_mapping`: 1 rows (electrostatics_force); samples: LD021
- `U017` `unknown_unsupported`: 1 rows (unknown); samples: CH102

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
