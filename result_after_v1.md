Implemented the v1 baseline.

Main file:
[physics_baseline_solver.py](D:/Project/EXACT2026/physics_baseline_solver.py)

Generated artifacts:
[baseline_results.csv](D:/Project/EXACT2026/results/physics_baseline/baseline_results.csv)  
[dataset_profile.csv](D:/Project/EXACT2026/results/physics_baseline/dataset_profile.csv)  
[family_summary.csv](D:/Project/EXACT2026/results/physics_baseline/family_summary.csv)  
[failure_taxonomy.md](D:/Project/EXACT2026/results/physics_baseline/failure_taxonomy.md)

What it does now:

- Reads `datanhucc/physic.CSV` with CSV-aware UTF-8 parsing.
- Classifies answer contracts: `yes_no`, `numeric`, `text`, `math_expression`.
- Extracts observations: values, units, SI values, symbol hints.
- Extracts high-confidence relations: distances, right angle, triangle shape, midpoint, between/included-angle from side lengths.
- Runs deterministic solvers for first baseline coverage:
  - capacitor/energy/charge/dielectric cases
  - RLC resonance yes/no and simple RLC formulas
  - measurement mean/error cases
  - electrostatics vector cases where target/geometry are extractable
- Explicitly reports `unsupported`, `validator_failed`, `wrong`, and `ok`.

Important fix for your bottleneck: the electrostatics solver does **not** trust Qwen-style signed force formulas like:

```python
F_AB = k * q_A * q_B / AB**2
```

It uses:

```python
magnitude = k * abs(q_source * q_target) / r**2
```

Then charge signs only decide direction: attraction vs repulsion. It also handles the LD002-style geometry correctly: right angle at `A` means `AC = sqrt(BC^2 - AB^2)`, not `sqrt(AB^2 + BC^2)`.

Validation run:

```text
python physics_baseline_solver.py --self-test
self-test ok

python physics_baseline_solver.py datanhucc/physic.CSV --output-dir results/physics_baseline
rows: 1352
ok: 276
wrong: 31
unsupported: 1031
validator_failed: 14
```

This is intentionally honest coverage, not inflated guessing. The biggest remaining gap is extractor/planner coverage for LD/DT electrostatics target mapping and CH/RLC formulas, which is exactly where the next controlled-IR planner layer should go.