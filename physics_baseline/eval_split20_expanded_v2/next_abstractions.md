# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `ok`: 160
- `unsupported`: 86
- `wrong`: 13
- `validator_failed`: 12

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 7 rows; samples: LD391, LD055, LD050, LD384, LD049, LD400
- `rlc_current_target`: 2 rows; samples: CH274, CH268
- `capacitor_state_change`: 1 rows; samples: TD398
- `capacitor_target_or_formula`: 1 rows; samples: TD395
- `rlc_power_target`: 1 rows; samples: CH275
- `rlc_impedance_target`: 1 rows; samples: CH379

## Validator Failures

- `geometry_relation_missing`: 5 rows; samples: LD082, LD094, LD347, LD346, LD073
- `geometry_midpoint_grounding`: 3 rows; samples: LD298, LD312, LD333
- `geometry_perpendicular_bisector_or_equidistant`: 2 rows; samples: LD331, LD316
- `geometry_right_triangle_or_perpendicular`: 1 rows; samples: LD342
- `geometry_equilateral_grounding`: 1 rows; samples: LD090

## Unsupported Clusters To Unlock

- `U001` `electrostatics_perpendicular_distance`: 9 rows (electrostatics_force); samples: LD215; LD272; LD220; LD262; LD266; LD137; LD255; LD152
- `U002` `electrostatics_relation_or_vector_gap`: 8 rows (electrostatics_force); samples: LD254; LD193; LD244; LD014; LD246; LD260; LD133; LD217
- `U003` `rlc_resonance`: 7 rows (ac_rlc); samples: CH212; CH145; CH368; CH200; CH198; CH202; CH141
- `U004` `electrostatics_equilateral_vertices`: 7 rows (electrostatics_field); samples: LD306; LD318; LD394; LD322; LD296; LD311; LD377
- `U005` `rlc_formula_family`: 6 rows (ac_rlc); samples: CH238; CH201; CH252; CH254; CH263; CH199
- `U006` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD053; DT084; DT092; DT090; DT093; DT083
- `U007` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD309; DT059; DT055; DT043; DT036; DT030
- `U008` `unknown_unsupported`: 6 rows (unknown); samples: CH353; CH344; CH347; CH068; CH225; CH102
- `U009` `capacitor_target_or_relation`: 4 rows (capacitor); samples: DDT357; CHLT015; CH086; CH083
- `U010` `magnetic_induction_primitives`: 4 rows (magnetic_induction); samples: DDT152; DDT377; DDT145; DDT373
- `U011` `electrostatics_perpendicular_distance`: 3 rows (electrostatics_field); samples: LD353; DT042; DT058
- `U012` `electrostatics_charge_target_mapping`: 3 rows (electrostatics_force); samples: LD044; LD109; LD105
- `U013` `energy_power_primitives`: 3 rows (energy_power); samples: NL317; DDT353; CH052
- `U014` `rlc_power`: 2 rows (ac_rlc); samples: CH228; CH216
- `U015` `capacitor_energy_state`: 2 rows (capacitor); samples: NL327; NL128
- `U016` `electrostatics_midpoint_target`: 2 rows (electrostatics_force); samples: LD035; LD022
- `U017` `rlc_current`: 1 rows (ac_rlc); samples: CH171
- `U018` `rlc_power_factor`: 1 rows (ac_rlc); samples: CH246
- `U019` `capacitor_network`: 1 rows (capacitor); samples: TD391
- `U020` `electrostatics_charge_target_mapping`: 1 rows (electrostatics_field); samples: DT025

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
