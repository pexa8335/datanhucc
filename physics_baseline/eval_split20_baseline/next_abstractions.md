# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `unsupported`: 178
- `ok`: 75
- `validator_failed`: 12
- `wrong`: 6

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 6 rows; samples: LD391, LD055, LD050, LD384, LD049, LD400

## Validator Failures

- `geometry_relation_missing`: 5 rows; samples: LD082, LD094, LD347, LD346, LD073
- `geometry_midpoint_grounding`: 3 rows; samples: LD298, LD312, LD333
- `geometry_perpendicular_bisector_or_equidistant`: 2 rows; samples: LD331, LD316
- `geometry_right_triangle_or_perpendicular`: 1 rows; samples: LD342
- `geometry_equilateral_grounding`: 1 rows; samples: LD090

## Unsupported Clusters To Unlock

- `U001` `magnetic_induction_primitives`: 22 rows (magnetic_induction); samples: NL104; NL318; NL098; NL093; NL360; NL015; NL303; NL313
- `U002` `electrostatics_relation_or_vector_gap`: 17 rows (electrostatics_force); samples: LD254; LD164; LD193; LD244; LD014; LD169; LD246; LD177
- `U003` `capacitor_energy_state`: 13 rows (capacitor); samples: TD371; TD380; TD372; NL397; NL099; NL089; NL022; NL038
- `U004` `unknown_unsupported`: 13 rows (unknown); samples: THCB085; THCB079; THCB070; DDT358; CH342; CH353; CH344; CH035
- `U005` `rlc_resonance`: 11 rows (ac_rlc); samples: CH212; CH024; CH033; CH145; CH368; CH200; CH198; CH202
- `U006` `energy_power_primitives`: 11 rows (energy_power); samples: THCB077; NL369; NL095; NL394; NL310; NL400; NL317; NL390
- `U007` `capacitor_network`: 10 rows (capacitor); samples: TD056; TD395; TD391; TD101; NL385; CH034; CH030; CH031
- `U008` `rlc_formula_family`: 9 rows (ac_rlc); samples: CH028; CH238; CH201; CH061; CH252; CHLT014; CH254; CH263
- `U009` `electrostatics_perpendicular_distance`: 9 rows (electrostatics_force); samples: LD215; LD272; LD220; LD262; LD266; LD137; LD255; LD152
- `U010` `electrostatics_relation_or_vector_gap`: 8 rows (electrostatics_field); samples: LD365; LD053; LD364; DT084; DT092; DT090; DT093; DT083
- `U011` `electrostatics_equilateral_vertices`: 7 rows (electrostatics_field); samples: LD306; LD318; LD394; LD322; LD296; LD311; LD377
- `U012` `electrostatics_relation_or_vector_gap`: 7 rows (electrostatics_field); samples: LD309; DT059; DT055; DT043; DT036; DT030; NL340
- `U013` `capacitor_target_or_relation`: 6 rows (capacitor); samples: DDT357; CHLT015; CH075; CH086; CH072; CH083
- `U014` `capacitor_dielectric_state`: 5 rows (capacitor); samples: TD386; TD398; TD097; TD012; TD100
- `U015` `rlc_current`: 4 rows (ac_rlc); samples: DDT323; CH274; CH171; CH268
- `U016` `electrostatics_perpendicular_distance`: 4 rows (electrostatics_field); samples: LD366; LD353; DT042; DT058
- `U017` `rlc_power`: 3 rows (ac_rlc); samples: CH228; CH216; CH275
- `U018` `electrostatics_charge_target_mapping`: 3 rows (electrostatics_force); samples: LD044; LD109; LD105
- `U019` `measurement_error_propagation`: 3 rows (measurement); samples: THCB115; THCB130; THCB116
- `U020` `rlc_power_factor`: 2 rows (ac_rlc); samples: CH177; CH246

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
