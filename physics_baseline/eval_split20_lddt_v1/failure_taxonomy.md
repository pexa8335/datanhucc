# Physics Baseline Failure Taxonomy

## Status Counts

- `ok`: 235
- `unsupported`: 18
- `wrong`: 11
- `validator_failed`: 6

## Failure Buckets

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 11

- `TD398` family=`capacitor` gold=`1.66 nJ` pred=`1.660125 μJ`
- `TD395` family=`capacitor` gold=`20.33 mN` pred=`20329.8 N`
- `TD402` family=`capacitor` gold=`100 μ` pred=`100 μF`
- `LD391` family=`electrostatics_field` gold=`2.89*10^6 V/m` pred=`2.88766e+07 V/m`
- `LD082` family=`electrostatics_field` gold=`389 kV/m` pred=`389711 V/m`
- `LD238` family=`electrostatics_field` gold=`11.0851 N` pred=`2.77128e+06 V/m`
- `LD279` family=`electrostatics_field` gold=`2.7713 N` pred=`1.38564e+06 V/m`
- `DT084` family=`electrostatics_field` gold=`245.91 N/C` pred=`50.911688 V/m`

### RLC formula not covered

Rows: 8

- `CH238` family=`ac_rlc` gold=`69.28 V` pred=` -`
- `CH228` family=`ac_rlc` gold=`50.0 Ω` pred=` -`
- `CH216` family=`ac_rlc` gold=`205.71 W` pred=` -`
- `CH246` family=`ac_rlc` gold=`1 -` pred=` -`
- `CH263` family=`ac_rlc` gold=`80 V` pred=` -`
- `CH171` family=`ac_rlc` gold=`202.5 W` pred=` -`
- `CH141` family=`ac_rlc` gold=`84.85 V` pred=` -`
- `CH102` family=`unknown` gold=`23.09 Ω` pred=` -`

### could not build field geometry coordinates

Rows: 6

- `LD094` family=`electrostatics_field` gold=`5.625 × 10^7 V/m` pred=` -`
- `LD342` family=`electrostatics_field` gold=`2.1*10^6 V/m` pred=` -`
- `LD090` family=`electrostatics_field` gold=`9 × 10^3 V/m` pred=` -`
- `LD347` family=`electrostatics_field` gold=`4.725*10^7 V/m` pred=` -`
- `LD346` family=`electrostatics_field` gold=`8.11*10^6 V/m` pred=` -`
- `LD073` family=`electrostatics_field` gold=`937.5 V/m` pred=` -`

### capacitor formula not covered

Rows: 3

- `TD391` family=`capacitor` gold=`-1.77 μJ` pred=` -`
- `TD375` family=`capacitor` gold=`22.36 V` pred=` -`
- `CHLT015` family=`capacitor` gold=`No -` pred=` -`

### target charge not identified

Rows: 3

- `LD254` family=`electrostatics_force` gold=`1.144*10^-3 N` pred=` -`
- `LD014` family=`electrostatics_force` gold=`3.46 μC` pred=` -`
- `LD021` family=`electrostatics_force` gold=`2.98 N` pred=` -`

### field source charges not identified

Rows: 2

- `LD353` family=`electrostatics_field` gold=`6.02 × 10^7 V/m` pred=` -`
- `DT042` family=`electrostatics_field` gold=`-0.4 . 10^{-4} C` pred=` -`

### target field point not identified

Rows: 2

- `LD398` family=`electrostatics_field` gold=`11.41 × 10^6 V/m` pred=` -`
- `DT043` family=`electrostatics_field` gold=`2.56 mm` pred=` -`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
