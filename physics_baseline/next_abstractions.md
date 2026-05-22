# V2 Next Abstractions

This file is generated from `baseline_results.csv`; it is a taxonomy review, not a row-ID solver plan.

## Current Status

- `unsupported`: 886
- `ok`: 386
- `validator_failed`: 55
- `wrong`: 25

## Wrong Rows First

- `electrostatics_target_geometry_or_vector`: 24 rows; samples: LD017, LD028, LD033, LD046, LD049, LD050
- `capacitor_voltage_capacitance_target_ambiguity`: 1 rows; samples: TD364

## Validator Failures

- `geometry_relation_missing`: 19 rows; samples: LD052, LD071, LD073, LD082, LD086, LD094
- `geometry_perpendicular_bisector_or_equidistant`: 19 rows; samples: LD066, LD074, LD091, LD098, LD099, LD100
- `geometry_midpoint_grounding`: 11 rows; samples: LD088, LD298, LD300, LD312, LD321, LD326
- `geometry_right_triangle_or_perpendicular`: 4 rows; samples: DT048, LD342, LD355, LD358
- `geometry_equilateral_grounding`: 2 rows; samples: LD069, LD090

## Unsupported Clusters To Unlock

- `U001` `magnetic_induction_primitives`: 108 rows (magnetic_induction); samples: NL007; NL008; NL010; NL015; NL016; NL019; NL023; NL028
- `U002` `electrostatics_relation_or_vector_gap`: 97 rows (electrostatics_force); samples: LD008; LD009; LD011; LD013; LD014; LD015; LD016; LD019
- `U003` `capacitor_energy_state`: 72 rows (capacitor); samples: TD361; TD362; TD367; TD370; TD371; TD372; TD375; TD378
- `U004` `rlc_resonance`: 59 rows (ac_rlc); samples: DDT333; CHLT007; CHLT012; CH023; CH024; CH033; CH063; CH065
- `U005` `unknown_unsupported`: 53 rows (unknown); samples: THCB004; THCB007; THCB066; THCB067; THCB068; THCB069; THCB070; THCB071
- `U006` `rlc_formula_family`: 45 rows (ac_rlc); samples: DT047; DDT330; DDT347; CHLT014; CH021; CH026; CH028; CH061
- `U007` `capacitor_network`: 43 rows (capacitor); samples: TD007; TD008; TD009; TD010; TD011; TD015; TD017; TD021
- `U008` `energy_power_primitives`: 41 rows (energy_power); samples: THCB075; THCB077; THCB082; THCB084; NL025; NL026; NL095; NL100
- `U009` `electrostatics_relation_or_vector_gap`: 39 rows (electrostatics_field); samples: LD068; LD075; LD083; DT020; DT027; DT029; DT030; DT036
- `U010` `capacitor_target_or_relation`: 33 rows (capacitor); samples: TD014; TD095; TD096; TD099; TD358; TD363; TD393; DDT351
- `U011` `electrostatics_relation_or_vector_gap`: 32 rows (electrostatics_field); samples: LD053; LD059; LD085; LD092; DT019; DT028; DT049; DT050
- `U012` `electrostatics_perpendicular_distance`: 30 rows (electrostatics_force); samples: LD006; LD007; LD025; LD037; LD045; LD124; LD137; LD142
- `U013` `rlc_power`: 25 rows (ac_rlc); samples: CH045; CH046; CH047; CH048; CH049; CH051; CH053; CH056
- `U014` `rlc_current`: 21 rows (ac_rlc); samples: DDT323; DDT326; DDT338; CH101; CH108; CH151; CH171; CH173
- `U015` `electrostatics_equilateral_vertices`: 21 rows (electrostatics_field); samples: LD084; LD096; LD296; LD301; LD305; LD306; LD310; LD311
- `U016` `measurement_error_propagation`: 20 rows (measurement); samples: THCB005; THCB008; THCB086; THCB089; THCB091; THCB095; THCB096; THCB099
- `U017` `electrostatics_midpoint_target`: 18 rows (electrostatics_field); samples: LD064; LD067; LD070; LD079; LD095; DT054; DT057; DT096
- `U018` `electrostatics_perpendicular_distance`: 16 rows (electrostatics_field); samples: LD081; DT007; DT008; DT041; DT042; DT044; DT058; DT081
- `U019` `electrostatics_charge_target_mapping`: 14 rows (electrostatics_force); samples: LD032; LD034; LD039; LD044; LD101; LD103; LD104; LD105
- `U020` `capacitor_dielectric_state`: 13 rows (capacitor); samples: TD001; TD002; TD012; TD091; TD092; TD097; TD100; TD384

## Implementation Guardrails

- Keep Qwen outside trusted execution until the controlled IR schema is stable.
- Add primitives by reasoning shape, not by row ID.
- Every newly solved row should expose target, primitive, grounded observations, relations, and formula in `trace`.
- Wrong rows are higher priority than raising raw coverage.
