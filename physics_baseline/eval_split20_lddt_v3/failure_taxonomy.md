# Physics Baseline Failure Taxonomy

## Status Counts

- `ok`: 255
- `unsupported`: 11
- `wrong`: 4

## Failure Buckets

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

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 4

- `TD398` family=`capacitor` gold=`1.66 nJ` pred=`1.660125 μJ`
- `TD395` family=`capacitor` gold=`20.33 mN` pred=`20329.8 N`
- `LD391` family=`electrostatics_field` gold=`2.89*10^6 V/m` pred=`2.88766e+07 V/m`
- `NL340` family=`electrostatics_field` gold=`0.2 J` pred=`3.162278 A`

### capacitor formula not covered

Rows: 3

- `TD391` family=`capacitor` gold=`-1.77 μJ` pred=` -`
- `TD375` family=`capacitor` gold=`22.36 V` pred=` -`
- `CHLT015` family=`capacitor` gold=`No -` pred=` -`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
