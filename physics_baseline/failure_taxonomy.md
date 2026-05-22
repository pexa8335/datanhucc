# Physics Baseline Failure Taxonomy

## Status Counts

- `unsupported`: 1031
- `ok`: 276
- `wrong`: 31
- `validator_failed`: 14

## Failure Buckets

### RLC formula not covered

Rows: 343

- `DT047` family=`ac_rlc` gold=`1/2 . (1/ \sqrt{E_A} + 1/ \sqrt{E_B}) -` pred=` -`
- `THCB004` family=`unknown` gold=`0.26 A` pred=` -`
- `THCB007` family=`unknown` gold=`0.13 A` pred=` -`
- `THCB066` family=`unknown` gold=`I_D₁ = 1.0; I_D₂ = 1.0; I_total = 2.0 A; A; A` pred=` -`
- `THCB067` family=`unknown` gold=`I_D₂ = 0.6 A` pred=` -`
- `THCB068` family=`unknown` gold=`I_total = 1.5 A` pred=` -`
- `THCB069` family=`unknown` gold=`I_D = 1.0 A` pred=` -`
- `THCB070` family=`unknown` gold=`I_total_new = 0.5 A` pred=` -`

### capacitor formula not covered

Rows: 200

- `TD001` family=`capacitor` gold=`150 V` pred=` -`
- `TD002` family=`capacitor` gold=`300 V` pred=` -`
- `TD006` family=`capacitor` gold=`1 pF` pred=` -`
- `TD007` family=`capacitor` gold=`1200 V` pred=` -`
- `TD008` family=`capacitor` gold=`600 V` pred=` -`
- `TD009` family=`capacitor` gold=`3 nC` pred=` -`
- `TD010` family=`capacitor` gold=`100 V` pred=` -`
- `TD011` family=`capacitor` gold=`5 nF` pred=` -`

### target charge not identified

Rows: 187

- `LD005` family=`electrostatics_force` gold=`9√3 × 10^-27 N` pred=` -`
- `LD006` family=`electrostatics_force` gold=`1.23 × 10^-3 N` pred=` -`
- `LD007` family=`electrostatics_force` gold=`17.28 N` pred=` -`
- `LD008` family=`electrostatics_force` gold=`7 N` pred=` -`
- `LD009` family=`electrostatics_force` gold=`8.66 N` pred=` -`
- `LD010` family=`electrostatics_force` gold=` 6.24 N` pred=` -`
- `LD011` family=`electrostatics_force` gold=`5 N` pred=` -`
- `LD012` family=`electrostatics_force` gold=`0.39 N` pred=` -`

### field source charges not identified

Rows: 122

- `LD051` family=`electrostatics_field` gold=`6.4 × 10^5 V/m` pred=` -`
- `LD052` family=`electrostatics_field` gold=`3.51 × 10^5 V/m` pred=` -`
- `LD053` family=`electrostatics_field` gold=`3.125 × 10^6 V/m` pred=` -`
- `LD056` family=`electrostatics_field` gold=`33.6 × 10^5 V/m` pred=` -`
- `LD058` family=`electrostatics_field` gold=`64 × 10^5 V/m` pred=` -`
- `LD059` family=`electrostatics_field` gold=`0 V/m` pred=` -`
- `LD062` family=`electrostatics_field` gold=`16000 V/m` pred=` -`
- `LD065` family=`electrostatics_field` gold=`2160 V/m` pred=` -`

### target field point not identified

Rows: 89

- `LD060` family=`electrostatics_field` gold=`36000 V/m` pred=` -`
- `LD061` family=`electrostatics_field` gold=`1.2178 × 10^-3 V/m` pred=` -`
- `LD063` family=`electrostatics_field` gold=`0.7031 × 10^-3 V/m` pred=` -`
- `LD064` family=`electrostatics_field` gold=`10000 V/m` pred=` -`
- `LD067` family=`electrostatics_field` gold=`9.8 × 10^5 N/C` pred=` -`
- `LD068` family=`electrostatics_field` gold=`538 N/C` pred=` -`
- `LD070` family=`electrostatics_field` gold=`4.5 × 10^5 V/m` pred=` -`
- `LD075` family=`electrostatics_field` gold=`18 cm` pred=` -`

### no source charge distances to target

Rows: 57

- `LD001` family=`electrostatics_force` gold=`0.05 N` pred=` -`
- `LD022` family=`electrostatics_force` gold=`14.4 N` pred=` -`
- `LD044` family=`electrostatics_force` gold=`9.45 N` pred=` -`
- `LD046` family=`electrostatics_force` gold=`26.2 N` pred=` -`
- `LD050` family=`electrostatics_force` gold=`14.4 N` pred=` -`
- `LD101` family=`electrostatics_force` gold=`2.707*10^-3 N` pred=` -`
- `LD102` family=`electrostatics_force` gold=`0.238 N` pred=` -`
- `LD103` family=`electrostatics_force` gold=`1.480 N` pred=` -`

### measurement formula not covered

Rows: 33

- `THCB003` family=`measurement` gold=`1.0 Ω` pred=` -`
- `THCB005` family=`measurement` gold=`4.21 %` pred=` -`
- `THCB008` family=`measurement` gold=`0.19 W` pred=` -`
- `THCB009` family=`measurement` gold=`1.5 Ω` pred=` -`
- `THCB086` family=`measurement` gold=`0.8 %` pred=` -`
- `THCB089` family=`measurement` gold=`0.83 %` pred=` -`
- `THCB091` family=`measurement` gold=`0.63 %` pred=` -`
- `THCB095` family=`measurement` gold=`3.33 %` pred=` -`

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 28

- `DT033` family=`electrostatics_field` gold=`6300000 V/m` pred=`9.39628e+06 V/m`
- `DT035` family=`electrostatics_field` gold=`45.10^{5} V/m` pred=`3.7108e+06 V/m`
- `TD364` family=`capacitor` gold=`0.100 nC` pred=`4 μF`
- `TD373` family=`capacitor` gold=`50 %` pred=`400 μJ`
- `TD381` family=`capacitor` gold=`125 μJ` pred=`250 μJ`
- `TD385` family=`capacitor` gold=`4.000 μJ` pred=`2 μJ`
- `TD387` family=`capacitor` gold=`2.140 μF` pred=`6 V`
- `TD388` family=`capacitor` gold=`72 μJ` pred=`144 μJ`

### could not build field geometry coordinates

Rows: 14

- `LD066` family=`electrostatics_field` gold=`2000 V/m` pred=` -`
- `LD071` family=`electrostatics_field` gold=`2 × 10^5 V/m` pred=` -`
- `LD074` family=`electrostatics_field` gold=`2160 V/m` pred=` -`
- `LD088` family=`electrostatics_field` gold=`73718 V/m` pred=` -`
- `LD094` family=`electrostatics_field` gold=`5.625 × 10^7 V/m` pred=` -`
- `LD097` family=`electrostatics_field` gold=`3.75 × 10^7 V/m` pred=` -`
- `LD098` family=`electrostatics_field` gold=`1.152 × 10^7 V/m` pred=` -`
- `DT034` family=`electrostatics_field` gold=`27.6 cm` pred=` -`

### prediction did not match ground truth (unparsed_or_shape_mismatch)

Rows: 2

- `THCB006` family=`measurement` gold=`0.4 Ω` pred=`0.4; 3.921569 Ω; %`
- `THCB072` family=`measurement` gold=`I_total = 3.0 A` pred=`I1 = 1; I2 = 2 A; A`

### prediction did not match ground truth (text_exact)

Rows: 1

- `TD377` family=`capacitor` gold=`the voltage is halfed -` pred=`10 V`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
