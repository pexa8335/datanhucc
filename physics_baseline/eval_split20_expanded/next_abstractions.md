# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `ok`: 138
- `unsupported`: 97
- `executor_failed`: 19
- `wrong`: 17

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 4 rows; samples: LD055, LD050, LD049, NL340
- `capacitor_state_change`: 3 rows; samples: TD398, TD391, TD012
- `capacitor_target_or_formula`: 2 rows; samples: TD395, TD101
- `magnetic_induction_wrong`: 2 rows; samples: NL104, NL015
- `rlc_current_target`: 2 rows; samples: CH274, CH268
- `energy_power_wrong`: 1 rows; samples: NL095
- `capacitor_voltage_capacitance_target_ambiguity`: 1 rows; samples: NL397
- `rlc_power_target`: 1 rows; samples: CH275
- `rlc_target_selection`: 1 rows; samples: CHLT014

## Validator Failures

- No validator failures in this run.

## Unsupported Clusters To Unlock

- `U001` `electrostatics_perpendicular_distance`: 9 rows (electrostatics_force); samples: LD215; LD272; LD220; LD262; LD266; LD137; LD255; LD152
- `U002` `electrostatics_relation_or_vector_gap`: 8 rows (electrostatics_force); samples: LD254; LD193; LD244; LD014; LD246; LD260; LD133; LD217
- `U003` `magnetic_induction_primitives`: 8 rows (magnetic_induction); samples: DDT380; DDT160; DDT152; DDT154; DDT389; DDT377; DDT145; DDT373
- `U004` `rlc_resonance`: 7 rows (ac_rlc); samples: CH212; CH145; CH368; CH200; CH198; CH202; CH141
- `U005` `electrostatics_equilateral_vertices`: 7 rows (electrostatics_field); samples: LD306; LD318; LD394; LD322; LD296; LD311; LD377
- `U006` `rlc_formula_family`: 6 rows (ac_rlc); samples: CH238; CH201; CH252; CH254; CH263; CH199
- `U007` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD053; DT084; DT092; DT090; DT093; DT083
- `U008` `electrostatics_relation_or_vector_gap`: 6 rows (electrostatics_field); samples: LD309; DT059; DT055; DT043; DT036; DT030
- `U009` `unknown_unsupported`: 6 rows (unknown); samples: CH353; CH344; CH347; CH068; CH225; CH102
- `U010` `capacitor_energy_state`: 5 rows (capacitor); samples: NL099; NL022; NL399; NL327; NL128
- `U011` `energy_power_primitives`: 5 rows (energy_power); samples: NL394; NL400; NL317; DDT353; CH052
- `U012` `capacitor_target_or_relation`: 4 rows (capacitor); samples: DDT357; CHLT015; CH086; CH083
- `U013` `electrostatics_perpendicular_distance`: 3 rows (electrostatics_field); samples: LD353; DT042; DT058
- `U014` `electrostatics_charge_target_mapping`: 3 rows (electrostatics_force); samples: LD044; LD109; LD105
- `U015` `rlc_power`: 2 rows (ac_rlc); samples: CH228; CH216
- `U016` `electrostatics_midpoint_target`: 2 rows (electrostatics_force); samples: LD035; LD022
- `U017` `rlc_current`: 1 rows (ac_rlc); samples: CH171
- `U018` `rlc_impedance`: 1 rows (ac_rlc); samples: CH015
- `U019` `rlc_power_factor`: 1 rows (ac_rlc); samples: CH246
- `U020` `capacitor_dielectric_state`: 1 rows (capacitor); samples: TD097

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
