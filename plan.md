# EXACT2026 Physics Solver Plan

This file is the running source of truth for what we have learned, what has been implemented, and what should happen next.

## 1. Core Diagnosis

The old approach failed because it treated most problems as:

```text
givens + one formula -> one SymPy solve
```

That is too narrow for `datanhucc/physic.CSV`. The dataset includes scalar formulas, vector geometry, circuit reasoning, measurement/error propagation, symbolic outputs, qualitative text answers, and yes/no answers.

The Program-of-Thought experiment showed a sharper bottleneck:

```text
Qwen can extract many quantities correctly,
but it can choose the wrong physical model.
```

Examples:

- It may compute `AC = sqrt(AB^2 + BC^2)` when the problem says the triangle is right-angled at `A`; the correct relation is `AC = sqrt(BC^2 - AB^2)`.
- It may write `F_AB = k*q_A*q_B/AB^2`, mixing sign into force magnitude. The invariant should be:

```text
magnitude = k * abs(q1*q2) / r^2
signs decide direction only
```

So free-form Qwen code is not trusted as the final solver.

## 2. Architecture Direction

The target architecture is neuro-symbolic:

```text
question
-> deterministic extraction
-> relation/geometry grounding
-> semantic family router
-> controlled executable IR planner
-> plan validator
-> deterministic executor
-> result validator
-> optional repair loop
-> grounded explanation
```

Qwen should eventually help produce controlled IR, but not arbitrary formulas or arbitrary Python.

The controlled planner should mainly:

- map targets
- select primitives
- sequence equation steps
- bind grounded observations/relations
- expose dependencies explicitly

The deterministic layer owns dangerous invariants:

- Coulomb magnitude uses `abs(q1*q2)`
- charge signs decide vector direction
- vector composition is component/law-of-cosines based
- RLC resonance/impedance rules
- measurement-error propagation
- unit conversion and answer formatting

## 3. Dataset Survey Findings

Dataset: `datanhucc/physic.CSV`

Schema:

```text
id, question, cot, answer, unit
```

Row distribution:

```text
LD    396  electrostatics force/field, vector geometry
CH    290  AC/RLC circuits, impedance, resonance, power
NL    190  energy/power, capacitor/inductor, qualitative rows
TD    178  capacitor formulas and unit conversion
DDT   130  magnetic/induction/mixed circuit rows
THCB   80  measurement, uncertainty, simple circuit rows
DT     68  electric field/force geometry
CHLT   20  RLC yes/no resonance
```

Public answer contracts:

- `yes_no`: answer is `Yes` or `No`, unit is `-`
- `numeric`: scalar or numeric multi-output, unit is explicit
- `text`: e.g. `Towards q2`, unit is `-`
- `math_expression`: e.g. `E = 3/2E1`, unit is `-`

Important implication: evaluation cannot be one scalar-only numeric check.

## 4. Baseline V1 Implemented

Main script:

```text
physics_baseline_solver.py
```

Generated artifacts:

```text
results/physics_baseline/dataset_profile.csv
results/physics_baseline/family_summary.csv
results/physics_baseline/baseline_results.csv
results/physics_baseline/failure_taxonomy.md
```

Baseline V1 does:

- CSV-aware UTF-8 reading
- answer-type classification
- numeric/unit extraction
- SI normalization
- relation extraction for distance, right angle, triangle shape, midpoint, included angle
- deterministic solvers for selected families:
  - capacitor/energy/charge/dielectric basics
  - RLC resonance yes/no and simple formulas
  - measurement mean/error basics
  - electrostatics vector cases when target and geometry are grounded
- canonical per-row output:

```text
id, prefix, family, answer_type, pred_answer, pred_unit,
gold_answer, gold_unit, status, failure_reason, trace
```

Latest V1 run before V2 work:

```text
rows: 1352
ok: 276
wrong: 31
unsupported: 1031
validator_failed: 14
```

The important win is not the raw `ok` count yet. The important win is that the pipeline now separates:

- extraction/grounding
- deterministic execution
- validation
- evaluation taxonomy

## 5. V2 Taxonomy Findings

Priority is taxonomy-driven expansion, not fine-tuning.

Current failure clusters:

```text
wrong by family:
capacitor            12
ac_rlc                9
measurement           5
magnetic_induction    3
electrostatics_field  2

validator_failed:
electrostatics_field / could not build field geometry coordinates: 14

unsupported by major reason:
RLC formula not covered                         343
capacitor formula not covered                   200
target charge not identified                    187
field source charges not identified             122
target field point not identified                89
no source charge distances to target             57
measurement formula not covered                  33
```

Interpretation:

- `wrong` must be reduced first because these are confident-but-wrong predictions.
- `validator_failed` should remain rejected until geometry is actually grounded.
- `unsupported` should be clustered by reasoning shape before adding primitives.

## 6. V2 Work In Progress

Planned V2 artifacts:

```text
results/physics_baseline/wrong_review.csv
results/physics_baseline/validator_failed_review.csv
results/physics_baseline/unsupported_clusters.csv
results/physics_baseline/next_abstractions.md
```

V2 implementation priorities:

1. Reduce `wrong`
   - capacitor target detection:
     - percentage reduction
     - qualitative voltage/capacitance change
     - shared charge after reconnecting capacitors
     - voltage/capacitance target ambiguity
   - RLC target detection:
     - power vs current vs impedance vs power factor
     - do not return the first computable quantity
   - measurement:
     - distinguish range/reading/least count
     - distinguish single-output vs multi-output error questions

2. Improve electrostatics grounding
   - map `q1 = q2 = q3` to triangle vertices
   - map unnamed `test charge q`
   - map `charge at C`, `point M`, midpoint/perpendicular-bisector targets
   - recover `AB` from "points A and B, 8 cm apart"
   - infer equilateral side distances
   - convert "M is 3 cm away from AB" into perpendicular distance

3. Expand deterministic primitives
   - AC/RLC:
     - `XL = 2*pi*f*L`
     - `XC = 1/(2*pi*f*C)`
     - `Z = sqrt(R^2 + (XL - XC)^2)`
     - `I = U/Z`
     - `P = I^2 R`
     - `P = U^2/R` at resonance
     - `power_factor = R/Z`
   - measurement:
     - error propagation for `R=U/I`
     - error propagation for `P=UI`
     - series resistance error
     - relative error from least count

4. Prepare controlled IR after deterministic grounding improves
   - every solved row should have an oracle-style trace:

```text
question
-> observations
-> relations
-> verified plan
-> execution trace
-> final answer
```

These traces can later become supervised data for planner distillation/fine-tuning.

## 7. V2 Golden Tests

Keep existing tests:

- `TD401`: capacitor energy
- `TD402`: capacitance
- `LD004`: vector Coulomb
- `LD002`: right-angle geometry and Coulomb force
- `CHLT006`: RLC yes/no resonance
- `THCB088`: mean + mean absolute error

Add taxonomy-driven tests:

- `LD001`: recover `AB` from "8 cm apart" and solve collinear force
- `LD005`: map `q3` to vertex target in equilateral triangle
- `LD060`: midpoint electric field target
- `TD373`: percentage energy reduction
- `TD377`: qualitative voltage halving
- `CH041`: resonance power target
- `CH167`: resonance max power target
- `DDT321`: total impedance
- `THCB001`: least count absolute error
- `THCB003`: propagated absolute error for `R = U/I`

Acceptance gates:

- `wrong` count must decrease before celebrating new `ok` count.
- Every newly solved row must include a trace with target, primitive, observations, and relations.
- No new primitive may branch on row ID.
- Unsupported rows must stay explicit with improved failure reasons.

## 8. Strategic Direction

The long-term path is:

```text
single-formula PoT
-> grounded extraction + deterministic primitives
-> controlled executable IR planning
-> validator/repair loop
-> planner distillation from verified traces
```

Do not jump directly into end-to-end Qwen reasoning. The deterministic family solvers are becoming teacher/oracle systems, not a pile of row-specific hacks.

## 9. V2 Implementation Status - 2026-05-22

Main implementation file:

```text
D:\Project\EXACT2026\datanhucc\physics_baseline\physics_baseline_solver.py
```

Generated artifacts:

```text
D:\Project\EXACT2026\results\physics_baseline\baseline_results.csv
D:\Project\EXACT2026\results\physics_baseline\dataset_profile.csv
D:\Project\EXACT2026\results\physics_baseline\family_summary.csv
D:\Project\EXACT2026\results\physics_baseline\failure_taxonomy.md
D:\Project\EXACT2026\results\physics_baseline\wrong_review.csv
D:\Project\EXACT2026\results\physics_baseline\validator_failed_review.csv
D:\Project\EXACT2026\results\physics_baseline\unsupported_clusters.csv
D:\Project\EXACT2026\results\physics_baseline\next_abstractions.md
```

Latest full run:

```text
python datanhucc\physics_baseline\physics_baseline_solver.py datanhucc/physic.CSV --output-dir results/physics_baseline

rows: 1352
ok: 386
unsupported: 886
wrong: 25
validator_failed: 55
```

Gate result:

- `wrong` decreased from 31 to 25, so V2 passed the first acceptance gate.
- `ok` increased from 276 to 386.
- `unsupported` decreased from 1031 to 886.
- `validator_failed` increased from 14 to 55 because the solver now exposes more geometry grounding failures explicitly instead of leaving them in broad unsupported buckets.

Implemented V2 review pass:

- `wrong_review.csv`: confident-but-wrong rows clustered by review bucket.
- `validator_failed_review.csv`: geometry grounding failures with sample question snippets and trace summaries.
- `unsupported_clusters.csv`: unsupported rows grouped by reasoning shape.
- `next_abstractions.md`: generated next-step summary from the current run.

Implemented V2 solver improvements:

- stricter target detection for capacitor questions so givens like `voltage U = ...` are not mistaken as a voltage target;
- capacitor dielectric energy state;
- distance-doubled capacitance target;
- percentage of remaining capacitor energy;
- LC magnetic energy from total energy minus capacitor electric energy;
- time-dependent inductor energy from `I(t) = I0 cos(omega t)`;
- RLC target guards for impedance/current/power/power factor;
- measurement least-count and uncertainty propagation;
- evaluator support for multi-value numeric answers with units embedded in the answer text.

Remaining `wrong` taxonomy after V2:

- 24 rows: `electrostatics_target_geometry_or_vector`
- 1 row: `capacitor_voltage_capacitance_target_ambiguity`

Important note on the remaining capacitor wrong:

- `TD364` asks "Calculate the capacitance" from `Q = 20 μC`, `U = 5 V`.
- Solver predicts `4 μF`, matching `C = Q/U` and the row COT.
- Dataset answer is `0.100 nC`, which is dimensionally not capacitance.
- Treat this as a suspicious label candidate, not a formula patch target.

Top unsupported clusters after V2:

- `magnetic_induction_primitives`: 108 rows
- `electrostatics_relation_or_vector_gap`: 97 force rows
- `capacitor_energy_state`: 72 rows
- `rlc_resonance`: 59 rows
- `unknown_unsupported`: 53 rows
- `rlc_formula_family`: 45 rows
- `capacitor_network`: 43 rows
- `energy_power_primitives`: 41 rows

Next implementation priority:

1. Keep attacking `wrong` first, especially the 24 electrostatics geometry/vector rows.
2. Add deterministic geometry/vector abstractions for:
   - consecutive collinear three-charge layouts;
   - isosceles triangle force/field composition;
   - perpendicular-bisector field components;
   - point-finding targets where output is a distance/location, not field magnitude.
3. Then unlock high-frequency unsupported clusters by primitive family:
   - magnetic induction;
   - capacitor networks and energy state variants;
   - broader RLC resonance/formula routing.
