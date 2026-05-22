# V2 Taxonomy-Driven Neuro-Symbolic Expansion

## Summary

Next iteration should improve the current baseline by attacking the real taxonomy, not by adding free-form Qwen formulas. Current run is:

```text
ok: 276
wrong: 31
unsupported: 1031
validator_failed: 14
```

V2 goal: reduce `wrong` first, then unlock high-frequency unsupported clusters by adding missing grounding abstractions and deterministic primitives. Qwen remains outside the trusted execution path until controlled IR is stable.

## Key Changes

- Add a taxonomy review pass that reads `results/physics_baseline/baseline_results.csv` and emits:
  - `wrong_review.csv`
  - `validator_failed_review.csv`
  - `unsupported_clusters.csv`
  - `next_abstractions.md`
- Treat `wrong` as highest priority because these are cases where the system was confident but incorrect.
  - Capacitor wrongs: improve target detection for percentage reduction, qualitative change, shared charge after reconnection, and voltage/capacitance target ambiguity.
  - RLC wrongs: distinguish asking for `power`, `current`, `impedance`, or `power factor`; do not return the first computable RLC quantity.
  - Measurement wrongs: distinguish least count from range/reading and single-output vs multi-output error questions.
- Treat all `validator_failed` as geometry grounding failures.
  - Add field geometry support for midpoint, perpendicular bisector, equidistant point, on-line point, and symbolic side `a`.
  - Validator should continue rejecting impossible/incomplete coordinates rather than guessing.
- Cluster `unsupported` by reasoning shape before adding primitives.
  - Electrostatics target grounding: map `q1=q2=q3`, vertices, unnamed “test charge q”, “charge at C”, “point M”, midpoint/perpendicular-bisector targets.
  - Relation extraction: recover `AB` from “points A and B, 8 cm apart”; infer equilateral side distances; convert “M is 3 cm away from AB” into perpendicular distance.
  - AC/RLC formulas: add impedance `Z=sqrt(R^2+(XL-XC)^2)`, `I=U/Z`, `P=I^2R`, `P=U^2/R` at resonance, and power factor `R/Z`.
  - Measurement formulas: propagate error for `R=U/I`, `P=UI`, series resistance, relative error from least count.

## Controlled IR Direction

- Introduce an internal plan object only after the deterministic target/relations are improved:
  - `target`: symbol, answer type, expected unit
  - `bindings`: observation/relation IDs only
  - `steps`: allowed primitive calls or generic equations
  - `final`: output fields and formatter
- Do not let Qwen emit arbitrary formulas in V2.
- Deterministic solvers should be converted into trace-producing teacher/oracle plans:
  - `question -> observations -> relations -> verified plan -> trace -> answer`
- Qwen can later learn to produce this IR, but only after the oracle traces are stable.

## Test Plan

- Keep current golden tests and add failing-taxonomy goldens:
  - `LD001`: recover `AB` from “8 cm apart” and solve collinear force.
  - `LD005`: map `q3` to vertex target in equilateral triangle.
  - `LD060`: midpoint electric field target.
  - `TD373`: percentage energy reduction.
  - `TD377`: qualitative voltage halving.
  - `CH041`, `CH167`: resonance power target.
  - `DDT321`: total impedance.
  - `THCB001`: least count absolute error.
  - `THCB003`: propagated absolute error for `R=U/I`.
- Acceptance gates for V2:
  - `wrong` count must decrease before celebrating any `ok` increase.
  - Every newly solved row must include a trace showing target, primitive, observations, and relations.
  - No new primitive may branch on row ID.
  - Unsupported rows must remain explicit with improved failure reasons.

## Assumptions

- Priority remains taxonomy-driven expansion, not fine-tuning.
- Qwen role remains controlled planner/distillation target, not trusted formula writer.
- Deterministic primitives own dangerous invariants: signed charge direction, `abs(q1*q2)` Coulomb magnitude, vector composition, resonance conditions, unit conversion, and measurement-error propagation.
- The next implementation should keep outputs under `results/physics_baseline/` and preserve the existing canonical row schema.
