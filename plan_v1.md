This plan is for debugging and reviewing the actual data.
# Kế Hoạch Xây Solver Tổng Quát Cho `physic.CSV`

## Tóm Tắt

Mục tiêu là xây một baseline chạy được trên toàn bộ `datanhucc/physic.CSV`, đo coverage/failure rõ ràng, rồi mở rộng thành kiến trúc neuro-symbolic tổng quát. Qwen không được viết Python tự do làm lời giải cuối; ở v1 Qwen sẽ sinh **controlled IR plan**, còn validator/executor chịu trách nhiệm kiểm tra unit, relation, geometry, vector, output type.

Success criteria v1:

- Chạy được toàn bộ CSV và xuất per-row result CSV.
- Mỗi row có `pred_answer`, `pred_unit`, `answer_type`, `family`, `status`, `failure_reason`, `trace`.
- Không overfit theo row ID; prefix chỉ dùng để audit, không dùng làm logic bắt buộc ở inference.
- Hỗ trợ 4 answer contract công khai:
  - `yes_no`: answer `Yes/No`, unit `-`
  - `numeric`: scalar hoặc numeric list, answer là số, unit là unit tương ứng
  - `text`: ví dụ `Towards q2`, unit `-`
  - `math_expression`: ví dụ `E = 3/2E1`, unit `-`

## Data Survey & Audit

- Viết audit script đọc CSV bằng `csv.DictReader` UTF-8, không line-based parsing.
- Phân loại toàn bộ row theo:
  - prefix/family: `LD`, `DT`, `TD`, `NL`, `CH`, `CHLT`, `DDT`, `THCB`
  - answer type: `yes_no`, `numeric`, `text`, `math_expression`
  - numeric subshape: scalar, scientific notation, symbolic numeric, multi-value
  - required reasoning: unit conversion, geometry relation, vector composition, circuit relation, measurement/error, qualitative/text
- Sinh các artifact audit:
  - `dataset_profile.csv`: one row per dataset row with labels above
  - `family_summary.csv`: counts by family/reasoning/output type
  - `failure_taxonomy.md`: taxonomy with representative examples
- Kiểm tra riêng các relation mà Qwen hay yếu:
  - collinear/between: `AB = 5, CA = 3, CB = 2 => C between A and B`
  - right triangle / 3-4-5 / Pythagorean
  - equilateral / isosceles / perpendicular bisector
  - midpoint and symmetry
  - same/opposite force direction from charge signs

## Architecture & Interfaces

- Build pipeline:

```text
question
-> deterministic extractor
-> semantic router
-> controlled Qwen IR planner
-> plan validator
-> deterministic executor
-> result validator
-> optional repair loop
-> grounded explanation
```

- Canonical row output:

```json
{
  "id": "LD004",
  "family": "electrostatics_vector",
  "answer_type": "numeric",
  "pred_answer": "5.234e-3",
  "pred_unit": "N",
  "status": "ok|validator_failed|executor_failed|unsupported|wrong",
  "failure_reason": "",
  "trace": {}
}
```

- Observation extractor owns:
  - numeric value parsing: `3 × 10^-8`, `10⁻⁸`, fractions, decimals
  - unit parsing and SI normalization
  - symbol hints: `q1`, `q0`, `AB`, `C`, `L`, `R`, `U`
  - no final physics reasoning

- Relation extractor owns high-confidence facts:
  - distances between points
  - triangle side relations
  - midpoint, collinearity, between, perpendicular, equilateral
  - circuit topology cues: series, parallel, resonance
  - measurement cues: mean, absolute error, relative error

- Qwen IR planner emits only schema-valid plans:
  - references observations by ID, not copied values
  - references relations by ID, not free-form geometry claims
  - uses allowed operations only: `equation`, `compare`, `format_text`, `format_expression`
  - does not perform hidden arithmetic in prose

- Validator rejects:
  - copied numbers that do not match observations
  - vector magnitude addition/subtraction without direction proof
  - unresolved symbols
  - missing final target
  - answer type mismatch
  - invalid unit/output contract

## Solver Strategy

- Implement deterministic primitives, not row-specific solvers:
  - unit conversion and output-unit conversion
  - algebra/equation execution with SymPy
  - geometry facts: cosine law, between check, right triangle, midpoint
  - vector algebra: components, resultant magnitude/direction
  - electrostatics: Coulomb force, electric field, dielectric scaling
  - capacitor/energy: `Q=CU`, `E=0.5CU^2`
  - AC/RLC: reactance, impedance, resonance, power, power factor
  - magnetic/induction: solenoid field, flux, Faraday law, inductive energy
  - measurement: mean, absolute error, relative error, mean absolute error
  - output formatter for numeric, yes/no, text, math expression

- Family rollout order:
  1. `TD`, `CHLT`, `THCB measurement`: easiest to validate and good for baseline coverage.
  2. `LD`, `DT`: geometry + vector executor, highest risk and highest value.
  3. `CH`, `DDT`, `NL`: AC/RLC, magnetic, energy, qualitative rows.
  4. Unsupported rows become explicit `unsupported`, never silent guesses.

- Qwen repair loop:
  - only triggered after validator/executor failure
  - receives structured error and allowed schema
  - cannot bypass validator
  - record both original plan and repaired plan in trace

## Test Plan

- Unit tests:
  - parse `μF`, `µF`, `mC`, `nC`, `pF`, `cm`, `mm`, scientific notation, unicode superscripts
  - classify answer types from examples: `Yes`, `0.5 N`, `Towards q2`, `E = 3/2E1`
  - detect `C between A and B` from side lengths
  - compute right-triangle/equilateral angles
  - reject invalid vector scalar subtraction

- Golden row tests:
  - `TD401`: capacitor energy -> `0.045 J`
  - `TD402`: capacitance -> `100 μF`
  - `LD004`: vector Coulomb -> `5.234 × 10^-3 N`
  - `CHLT006`: resonance -> `Yes`, unit `-`
  - `THCB088`: mean + mean absolute error -> `10.2; 0.067`, unit `cm; cm`
  - add 3-5 rows per family after audit selects representative cases

- Dataset evaluation:
  - run all 1,352 rows
  - report exact/normalized match by family and answer type
  - report unsupported rate separately from wrong-answer rate
  - produce failure taxonomy: extraction failure, relation failure, planner failure, validation failure, executor gap, output formatting mismatch

## Assumptions

- Priority is baseline coverage measurement first, not immediate fine-tuning.
- Qwen role is controlled IR planner, not free-form PoT final solver.
- Public answer contract remains four types; multi-value numeric is treated as a `numeric` variant internally.
- Ground truth in `physic.CSV` is useful for evaluation, but audits should still flag suspicious labels instead of blindly training on them.
- The architecture must generalize by primitive/relation abstractions, not by row ID, exact train examples, or growing one-off prompt hacks.
