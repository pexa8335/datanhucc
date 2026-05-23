# Physics Baseline Failure Taxonomy

## Status Counts

- `unsupported`: 886
- `ok`: 386
- `validator_failed`: 55
- `wrong`: 25

## Failure Buckets

### RLC formula not covered

Rows: 337

- `DT047` family=`ac_rlc` gold=`1/2 . (1/ \sqrt{E_A} + 1/ \sqrt{E_B}) -` pred=` -`
- `THCB004` family=`unknown` gold=`0.26 A` pred=` -`
- `THCB007` family=`unknown` gold=`0.13 A` pred=` -`
- `THCB066` family=`unknown` gold=`I_D₁ = 1.0; I_D₂ = 1.0; I_total = 2.0 A; A; A` pred=` -`
- `THCB067` family=`unknown` gold=`I_D₂ = 0.6 A` pred=` -`
- `THCB068` family=`unknown` gold=`I_total = 1.5 A` pred=` -`
- `THCB069` family=`unknown` gold=`I_D = 1.0 A` pred=` -`
- `THCB070` family=`unknown` gold=`I_total_new = 0.5 A` pred=` -`

### capacitor formula not covered

Rows: 202

- `TD001` family=`capacitor` gold=`150 V` pred=` -`
- `TD002` family=`capacitor` gold=`300 V` pred=` -`
- `TD007` family=`capacitor` gold=`1200 V` pred=` -`
- `TD008` family=`capacitor` gold=`600 V` pred=` -`
- `TD009` family=`capacitor` gold=`3 nC` pred=` -`
- `TD010` family=`capacitor` gold=`100 V` pred=` -`
- `TD011` family=`capacitor` gold=`5 nF` pred=` -`
- `TD012` family=`capacitor` gold=`3 μC` pred=` -`

### target charge not identified

Rows: 143

- `LD006` family=`electrostatics_force` gold=`1.23 × 10^-3 N` pred=` -`
- `LD007` family=`electrostatics_force` gold=`17.28 N` pred=` -`
- `LD008` family=`electrostatics_force` gold=`7 N` pred=` -`
- `LD009` family=`electrostatics_force` gold=`8.66 N` pred=` -`
- `LD011` family=`electrostatics_force` gold=`5 N` pred=` -`
- `LD013` family=`electrostatics_force` gold=`10 N` pred=` -`
- `LD014` family=`electrostatics_force` gold=`3.46 μC` pred=` -`
- `LD015` family=`electrostatics_force` gold=`15.13 N` pred=` -`

### target field point not identified

Rows: 83

- `LD064` family=`electrostatics_field` gold=`10000 V/m` pred=` -`
- `LD067` family=`electrostatics_field` gold=`9.8 × 10^5 N/C` pred=` -`
- `LD068` family=`electrostatics_field` gold=`538 N/C` pred=` -`
- `LD070` family=`electrostatics_field` gold=`4.5 × 10^5 V/m` pred=` -`
- `LD075` family=`electrostatics_field` gold=`18 cm` pred=` -`
- `LD079` family=`electrostatics_field` gold=`0 V/m` pred=` -`
- `LD083` family=`electrostatics_field` gold=`9.6 × 10^2 V/m` pred=` -`
- `LD084` family=`electrostatics_field` gold=`0 V/m` pred=` -`

### field source charges not identified

Rows: 62

- `LD053` family=`electrostatics_field` gold=`3.125 × 10^6 V/m` pred=` -`
- `LD059` family=`electrostatics_field` gold=`0 V/m` pred=` -`
- `LD061` family=`electrostatics_field` gold=`1.2178 × 10^-3 V/m` pred=` -`
- `LD063` family=`electrostatics_field` gold=`0.7031 × 10^-3 V/m` pred=` -`
- `LD076` family=`electrostatics_field` gold=`-4 × 10^-7 C` pred=` -`
- `LD077` family=`electrostatics_field` gold=`E1 = (3/4)E2 -` pred=` -`
- `LD078` family=`electrostatics_field` gold=`16 V/m` pred=` -`
- `LD080` family=`electrostatics_field` gold=`1.218 x 10^-3 V/m` pred=` -`

### could not build field geometry coordinates

Rows: 55

- `LD052` family=`electrostatics_field` gold=`3.51 × 10^5 V/m` pred=` -`
- `LD066` family=`electrostatics_field` gold=`2000 V/m` pred=` -`
- `LD069` family=`electrostatics_field` gold=`9000 N/C` pred=` -`
- `LD071` family=`electrostatics_field` gold=`2 × 10^5 V/m` pred=` -`
- `LD073` family=`electrostatics_field` gold=`937.5 V/m` pred=` -`
- `LD074` family=`electrostatics_field` gold=`2160 V/m` pred=` -`
- `LD082` family=`electrostatics_field` gold=`389 kV/m` pred=` -`
- `LD086` family=`electrostatics_field` gold=`27 cm` pred=` -`

### measurement formula not covered

Rows: 31

- `THCB005` family=`measurement` gold=`4.21 %` pred=` -`
- `THCB008` family=`measurement` gold=`0.19 W` pred=` -`
- `THCB086` family=`measurement` gold=`0.8 %` pred=` -`
- `THCB089` family=`measurement` gold=`0.83 %` pred=` -`
- `THCB091` family=`measurement` gold=`0.63 %` pred=` -`
- `THCB095` family=`measurement` gold=`3.33 %` pred=` -`
- `THCB096` family=`measurement` gold=`1.11 %` pred=` -`
- `THCB099` family=`measurement` gold=`0.55 %` pred=` -`

### no source charge distances to target

Rows: 28

- `LD022` family=`electrostatics_force` gold=`14.4 N` pred=` -`
- `LD024` family=`electrostatics_force` gold=`6.04 N` pred=` -`
- `LD030` family=`electrostatics_force` gold=`7.2 × 10^-4 N` pred=` -`
- `LD031` family=`electrostatics_force` gold=`1.125 × 10^-1 N` pred=` -`
- `LD032` family=`electrostatics_force` gold=`0.05 N` pred=` -`
- `LD034` family=`electrostatics_force` gold=`4 × 10^-7 N` pred=` -`
- `LD039` family=`electrostatics_force` gold=`0 N` pred=` -`
- `LD042` family=`electrostatics_force` gold=`0 N` pred=` -`

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 25

- `LD017` family=`electrostatics_force` gold=`3.6 N` pred=`5.4 N`
- `LD028` family=`electrostatics_force` gold=`27.65 × 10^-3 N` pred=`0.02304 N`
- `LD033` family=`electrostatics_force` gold=`8.4 × 10^-4 N` pred=`0.000144222 N`
- `LD046` family=`electrostatics_force` gold=`26.2 N` pred=`10.8 N`
- `LD049` family=`electrostatics_force` gold=`14.34 N` pred=`4.5 N`
- `LD050` family=`electrostatics_force` gold=`14.4 N` pred=`1.8 N`
- `LD055` family=`electrostatics_force` gold=`0.7 N` pred=`0.45 N`
- `LD062` family=`electrostatics_field` gold=`16000 V/m` pred=`4500 V/m`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
