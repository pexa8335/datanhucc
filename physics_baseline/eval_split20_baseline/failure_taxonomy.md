# Physics Baseline Failure Taxonomy

## Status Counts

- `unsupported`: 178
- `ok`: 75
- `validator_failed`: 12
- `wrong`: 6

## Failure Buckets

### RLC formula not covered

Rows: 66

- `THCB085` family=`unknown` gold=`I₃ = 0.6 A` pred=` -`
- `THCB079` family=`unknown` gold=`I_total = 2.0 A` pred=` -`
- `THCB070` family=`unknown` gold=`I_total_new = 0.5 A` pred=` -`
- `NL104` family=`magnetic_induction` gold=`0.04 A` pred=` -`
- `NL318` family=`magnetic_induction` gold=`Half of the total energy J` pred=` -`
- `NL098` family=`magnetic_induction` gold=`0.0006 H` pred=` -`
- `NL093` family=`magnetic_induction` gold=`0.07 A` pred=` -`
- `NL360` family=`magnetic_induction` gold=`2.83 A` pred=` -`

### capacitor formula not covered

Rows: 45

- `TD371` family=`capacitor` gold=`9 times` pred=` -`
- `TD386` family=`capacitor` gold=`decreases by half -` pred=` -`
- `TD398` family=`capacitor` gold=`1.66 nJ` pred=` -`
- `TD056` family=`capacitor` gold=`31.75 pF` pred=` -`
- `TD395` family=`capacitor` gold=`20.33 mN` pred=` -`
- `TD380` family=`capacitor` gold=`decreases by 4 times -` pred=` -`
- `TD391` family=`capacitor` gold=`-1.77 μJ` pred=` -`
- `TD372` family=`capacitor` gold=`14.14 V` pred=` -`

### target charge not identified

Rows: 28

- `LD215` family=`electrostatics_force` gold=`0.566 N` pred=` -`
- `LD254` family=`electrostatics_force` gold=`1.144*10^-3 N` pred=` -`
- `LD272` family=`electrostatics_force` gold=`2.273 N` pred=` -`
- `LD164` family=`electrostatics_force` gold=`11.4018 N` pred=` -`
- `LD220` family=`electrostatics_force` gold=`0.509*10^-3 N` pred=` -`
- `LD193` family=`electrostatics_force` gold=`8.0 N` pred=` -`
- `LD262` family=`electrostatics_force` gold=`2.55 × 10^-4 N` pred=` -`
- `LD035` family=`electrostatics_force` gold=`0.36 N` pred=` -`

### target field point not identified

Rows: 16

- `LD306` family=`electrostatics_field` gold=`1.99 × 10^6 V/m` pred=` -`
- `LD318` family=`electrostatics_field` gold=`5.8 × 10^6 V/m` pred=` -`
- `LD394` family=`electrostatics_field` gold=`14.03 × 10⁶ V/m` pred=` -`
- `LD309` family=`electrostatics_field` gold=`3.12 × 10^6 V/m` pred=` -`
- `LD322` family=`electrostatics_field` gold=`6.92 × 10^6 V/m` pred=` -`
- `LD398` family=`electrostatics_field` gold=`11.41 × 10^6 V/m` pred=` -`
- `LD296` family=`electrostatics_field` gold=`7.05 × 10^6 V/m` pred=` -`
- `LD311` family=`electrostatics_field` gold=`1.76 × 10^6 V/m` pred=` -`

### field source charges not identified

Rows: 13

- `LD365` family=`electrostatics_field` gold=`57.41 × 10^6 V/m` pred=` -`
- `LD366` family=`electrostatics_field` gold=`13.48 × 10^6 V/m` pred=` -`
- `LD053` family=`electrostatics_field` gold=`3.125 × 10^6 V/m` pred=` -`
- `LD364` family=`electrostatics_field` gold=`7.32 × 10^6 V/m` pred=` -`
- `LD353` family=`electrostatics_field` gold=`6.02 × 10^7 V/m` pred=` -`
- `DT084` family=`electrostatics_field` gold=`245.91 N/C` pred=` -`
- `DT092` family=`electrostatics_field` gold=`1.23 . 10^6 V/m` pred=` -`
- `DT042` family=`electrostatics_field` gold=`-0.4 . 10^{-4} C` pred=` -`

### could not build field geometry coordinates

Rows: 12

- `LD298` family=`electrostatics_field` gold=`8.14 × 10^6 V/m` pred=` -`
- `LD312` family=`electrostatics_field` gold=`3.2 × 10^7 V/m` pred=` -`
- `LD082` family=`electrostatics_field` gold=`389 kV/m` pred=` -`
- `LD094` family=`electrostatics_field` gold=`5.625 × 10^7 V/m` pred=` -`
- `LD342` family=`electrostatics_field` gold=`2.1*10^6 V/m` pred=` -`
- `LD090` family=`electrostatics_field` gold=`9 × 10^3 V/m` pred=` -`
- `LD331` family=`electrostatics_field` gold=`9.932*10^6 V/m` pred=` -`
- `LD347` family=`electrostatics_field` gold=`4.725*10^7 V/m` pred=` -`

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 6

- `LD391` family=`electrostatics_field` gold=`2.89*10^6 V/m` pred=`1.21365e+07 V/m`
- `LD055` family=`electrostatics_force` gold=`0.7 N` pred=`0.45 N`
- `LD050` family=`electrostatics_force` gold=`14.4 N` pred=`1.8 N`
- `LD384` family=`electrostatics_field` gold=`5.27*10^6 V/m` pred=`4.03397e+06 V/m`
- `LD049` family=`electrostatics_force` gold=`14.34 N` pred=`4.5 N`
- `LD400` family=`electrostatics_field` gold=`2.01*10^7 V/m` pred=`1.5932e+06 V/m`

### measurement formula not covered

Rows: 5

- `THCB115` family=`measurement` gold=`2.0 %` pred=` -`
- `THCB119` family=`measurement` gold=`1.67 %` pred=` -`
- `THCB130` family=`measurement` gold=`1.0; 0.61 cm; %` pred=` -`
- `THCB116` family=`measurement` gold=`0.5 %` pred=` -`
- `CH001` family=`measurement` gold=`40 Ω` pred=` -`

### no source charge distances to target

Rows: 5

- `LD044` family=`electrostatics_force` gold=`9.45 N` pred=` -`
- `LD022` family=`electrostatics_force` gold=`14.4 N` pred=` -`
- `LD102` family=`electrostatics_force` gold=`0.238 N` pred=` -`
- `LD109` family=`electrostatics_force` gold=`3.5*10^-3 N` pred=` -`
- `LD105` family=`electrostatics_force` gold=`0.058 N` pred=` -`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
