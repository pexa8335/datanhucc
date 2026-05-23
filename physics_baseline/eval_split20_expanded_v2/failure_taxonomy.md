# Physics Baseline Failure Taxonomy

## Status Counts

- `ok`: 160
- `unsupported`: 86
- `wrong`: 13
- `validator_failed`: 12

## Failure Buckets

### RLC formula not covered

Rows: 23

- `CH238` family=`ac_rlc` gold=`69.28 V` pred=` -`
- `CH353` family=`unknown` gold=`105.54 µF` pred=` -`
- `CH212` family=`ac_rlc` gold=`0.707 -` pred=` -`
- `CH228` family=`ac_rlc` gold=`50.0 Ω` pred=` -`
- `CH201` family=`ac_rlc` gold=`3.0 -` pred=` -`
- `CH216` family=`ac_rlc` gold=`205.71 W` pred=` -`
- `CH252` family=`ac_rlc` gold=`150 V` pred=` -`
- `CH344` family=`unknown` gold=`56.27 Hz` pred=` -`

### no source charge distances to target

Rows: 15

- `LD215` family=`electrostatics_force` gold=`0.566 N` pred=` -`
- `LD272` family=`electrostatics_force` gold=`2.273 N` pred=` -`
- `LD044` family=`electrostatics_force` gold=`9.45 N` pred=` -`
- `LD220` family=`electrostatics_force` gold=`0.509*10^-3 N` pred=` -`
- `LD262` family=`electrostatics_force` gold=`2.55 × 10^-4 N` pred=` -`
- `LD035` family=`electrostatics_force` gold=`0.36 N` pred=` -`
- `LD266` family=`electrostatics_force` gold=`32.16*10^-3 N` pred=` -`
- `LD137` family=`electrostatics_force` gold=`0.115 N` pred=` -`

### target field point not identified

Rows: 15

- `LD306` family=`electrostatics_field` gold=`1.99 × 10^6 V/m` pred=` -`
- `LD318` family=`electrostatics_field` gold=`5.8 × 10^6 V/m` pred=` -`
- `LD394` family=`electrostatics_field` gold=`14.03 × 10⁶ V/m` pred=` -`
- `LD309` family=`electrostatics_field` gold=`3.12 × 10^6 V/m` pred=` -`
- `LD322` family=`electrostatics_field` gold=`6.92 × 10^6 V/m` pred=` -`
- `LD398` family=`electrostatics_field` gold=`11.41 × 10^6 V/m` pred=` -`
- `LD296` family=`electrostatics_field` gold=`7.05 × 10^6 V/m` pred=` -`
- `LD311` family=`electrostatics_field` gold=`1.76 × 10^6 V/m` pred=` -`

### prediction did not match ground truth (numeric_unit_tolerant)

Rows: 13

- `TD398` family=`capacitor` gold=`1.66 nJ` pred=`1.660125 μJ`
- `TD395` family=`capacitor` gold=`20.33 mN` pred=`20329.8 N`
- `LD391` family=`electrostatics_field` gold=`2.89*10^6 V/m` pred=`1.21365e+07 V/m`
- `LD055` family=`electrostatics_force` gold=`0.7 N` pred=`0.45 N`
- `LD050` family=`electrostatics_force` gold=`14.4 N` pred=`1.8 N`
- `LD384` family=`electrostatics_field` gold=`5.27*10^6 V/m` pred=`4.03397e+06 V/m`
- `LD049` family=`electrostatics_force` gold=`14.34 N` pred=`4.5 N`
- `LD400` family=`electrostatics_field` gold=`2.01*10^7 V/m` pred=`1.5932e+06 V/m`

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

### capacitor formula not covered

Rows: 10

- `TD391` family=`capacitor` gold=`-1.77 μJ` pred=` -`
- `NL327` family=`capacitor` gold=`Conservation of energy -` pred=` -`
- `NL128` family=`capacitor` gold=`67 %` pred=` -`
- `NL317` family=`energy_power` gold=`Reduced to 1/4 -` pred=` -`
- `DDT357` family=`capacitor` gold=`0 V` pred=` -`
- `DDT353` family=`energy_power` gold=`U = 0.5*L*I_max² J` pred=` -`
- `CHLT015` family=`capacitor` gold=`No -` pred=` -`
- `CH086` family=`capacitor` gold=`316.63 mH` pred=` -`

### field source charges not identified

Rows: 10

- `LD053` family=`electrostatics_field` gold=`3.125 × 10^6 V/m` pred=` -`
- `LD353` family=`electrostatics_field` gold=`6.02 × 10^7 V/m` pred=` -`
- `DT084` family=`electrostatics_field` gold=`245.91 N/C` pred=` -`
- `DT092` family=`electrostatics_field` gold=`1.23 . 10^6 V/m` pred=` -`
- `DT042` family=`electrostatics_field` gold=`-0.4 . 10^{-4} C` pred=` -`
- `DT090` family=`electrostatics_field` gold=`540 V/m` pred=` -`
- `DT058` family=`electrostatics_field` gold=`8E V/m` pred=` -`
- `DT040` family=`electrostatics_field` gold=`4 . 10^{-9} C` pred=` -`

### target charge not identified

Rows: 9

- `LD254` family=`electrostatics_force` gold=`1.144*10^-3 N` pred=` -`
- `LD193` family=`electrostatics_force` gold=`8.0 N` pred=` -`
- `LD244` family=`electrostatics_force` gold=`56.57*10^-6 N` pred=` -`
- `LD014` family=`electrostatics_force` gold=`3.46 μC` pred=` -`
- `LD246` family=`electrostatics_force` gold=`20.360 N` pred=` -`
- `LD260` family=`electrostatics_force` gold=`0.226*10^-3 N` pred=` -`
- `LD133` family=`electrostatics_force` gold=`0.434 N` pred=` -`
- `LD217` family=`electrostatics_force` gold=`0.815 N` pred=` -`

### magnetic induction formula not covered

Rows: 4

- `DDT152` family=`magnetic_induction` gold=`Current through the solenoid —` pred=` -`
- `DDT377` family=`magnetic_induction` gold=`1.26×10⁻³ J` pred=` -`
- `DDT145` family=`magnetic_induction` gold=`Current intensity —` pred=` -`
- `DDT373` family=`magnetic_induction` gold=`3.77×10⁻³ T` pred=` -`

## Known Architectural Bottlenecks

- Free-form PoT can produce executable but physically wrong formulas; keep it behind IR validation.
- Geometry facts such as right angle, between, and included angle must come from deterministic relations when possible.
- Unsupported rows are explicit baseline gaps, not silent model guesses.
