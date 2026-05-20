# Tóm tắt toàn bộ thảo luận về kiến trúc solver Physics QA

## 1. Bối cảnh bài toán

Ta đang xây một hệ thống giải bài tập Vật lý cho challenge. Dataset không chỉ gồm các bài số học đơn giản mà trải rộng trên nhiều nhóm:

* **TD**: tụ điện
* **LD**: lực điện, điện trường, vector, hình học
* **DT**: điện trường / lực từ điện trường
* **NL**: năng lượng
* **CH**: mạch AC, cộng hưởng, trở kháng, công suất
* **TH**: đo lường, sai số
* **DD**: từ trường / cảm ứng
* **QA**: có 401 dòng answer trống

Codex đã rà dataset và nhận thấy nhiều tín hiệu cho bài toán **nhiều bước**:

```text
net: 341
resultant: 137
series: 171
parallel: 153
angle: 213
triangle: 125
resonance: 127
power: 104
energy: 288
```

Điều này cho thấy private test hoàn toàn có thể chứa các tổ hợp suy luận chưa xuất hiện nguyên xi trong train, nhất là vì challenge cho phép dùng **universal external data**. 

---

# 2. Notebook hiện tại thực sự đang làm gì?

Notebook/root.py hiện tại có pipeline:

```text
Question
→ Qwen trích xuất:
   - givens
   - target
   - one formula string
→ Pint đổi đơn vị
→ SymPy giải đúng 1 phương trình
→ Qwen viết explanation dựa trên solver trace
```

Điểm quan trọng:

> Notebook **không** phải solver chuyên biệt cho Coulomb hay một dạng bài duy nhất.
> Nó là **generic single-equation solver**.

Nó đọc công thức từ Qwen rồi dùng SymPy để giải, chứ không hard-code riêng:

* solver Coulomb,
* map A→1, B→2,
* regex cho CA/CB,
* hay branch riêng cho từng công thức. 

---

# 3. Vấn đề thật của kiến trúc cũ

Lỗi không phải:

> “Code bị overfit vào bài Coulomb.”

Mà là:

> **Toàn bộ kiến trúc giả định mọi bài toán đều có dạng:**
>
> ```text
> givens + one formula string → one SymPy solve
> ```

Đây là giới hạn quá hẹp. 

---

# 4. Vì sao bài điện tích q1, q2, q3 làm pipeline fail?

Bài:

```text
q1 = 6×10^-8 C
q2 = -6×10^-8 C
q3 = 6×10^-8 C
CA = 5 cm
CB = 3 cm
AB = 8 cm
Tìm lực tác dụng lên q3
```

Qwen hiện tại sinh:

```json
"formula": "F3 = k * (q1 * q3 / r13^2 + q2 * q3 / r23^2)"
```

Đây là sai về vật lý vì nó cố ép cả một chuỗi suy luận vào **một công thức scalar duy nhất**:

1. Tính lực do q1 tác dụng lên q3
2. Tính lực do q2 tác dụng lên q3
3. Xét vị trí C nằm giữa A và B
4. Xét chiều lực
5. Cộng lực cùng chiều

Đúng ra cần dạng multi-step:

```text
F13 = k * |q1 q3| / r13²
F23 = k * |q2 q3| / r23²
F3 = F13 + F23
```

Nhưng schema cũ chỉ có `"formula"`, nên Qwen bị ép collapse reasoning thành một biểu thức duy nhất và sai. 

---

# 5. Claude có đúng khi nói code specialized không?

## Claude đúng ở điểm:

Kiến trúc hiện tại **không đủ tổng quát** cho dataset rộng và bài multi-step.

## Claude sai nếu nói:

> Stage 2 đã là tập hợp các special-case solver Coulomb/vector/regex.

Trong notebook hiện tại, điều đó **không tồn tại**. Stage 2 vẫn là generic single-equation SymPy solver. 

### Kết luận chính xác:

> Code không specialized theo **topic**,
> nhưng specialized theo **reasoning shape**:
> **một bài = một công thức**.

---

# 6. Ban đầu Codex đề xuất kiến trúc gì?

Codex đề xuất chuyển từ:

```text
one formula
```

sang:

```text
ordered calculation plan
```

và dùng một executor tổng quát hơn.

Nó đề xuất các step type:

```text
equation
assign
convert_unit
compare
resultant
```

Kiến trúc Codex đề xuất:

```text
Question
→ LLM tạo plan
→ generic executor chạy từng bước
→ verifier kiểm tra target, unit, unresolved variables
→ LLM viết explanation
```



---

# 7. Sau khi thảo luận kỹ, ta chỉnh lại đề xuất của Codex

Ta nhận ra:

## `equation`

Nên giữ. Đây là lõi tổng quát nhất.

Ví dụ:

```json
{
  "equation": "P = U * I",
  "solves_for": "P"
}
```

---

## `assign`

Không cần riêng.

Ví dụ:

```text
Q1 = Q0
```

có thể viết luôn dưới dạng equation.

---

## `convert_unit`

Không nên bắt Qwen sinh step đổi đơn vị.

Nên để **executor tự convert ngầm khi đọc givens**, vì:

* nhẹ gánh cho Qwen,
* ít step hơn,
* ít lỗi hơn.

Ví dụ:

```text
5 cm → executor tự đổi thành 0.05 m nếu cần tính
```

Đáp án cuối có thể hiển thị ở unit phù hợp, miễn tương đương, ví dụ:

* `0.045 J`
* `45 mJ`

đều đúng về vật lý nếu format đánh giá cho phép.

---

## `resultant`

Ta quyết định **không thêm sớm**.

Lý do:

* nó đã là một op mang tính domain hơn,
* bắt đầu đóng gói riêng “hợp lực/vector” vào executor,
* nếu test rộng và bất ngờ, việc thêm từng op kiểu này dễ biến thành whack-a-mole.

Thay vì:

```json
{"type": "resultant"}
```

hãy để Qwen viết bằng các equation thường:

```text
Fx = F1 + F2*cos(theta)
Fy = F2*sin(theta)
F = sqrt(Fx^2 + Fy^2)
```

Executor chỉ giải phương trình. Như vậy generic hơn. 

---

## `compare`

Ta quyết định **giữ lại**.

Lý do:

* Nó không specialized vào một hiện tượng vật lý cụ thể.
* Nó hỗ trợ task kiểu boolean / logic:

  * có cộng hưởng hay không,
  * A có lớn hơn B không,
  * hai đại lượng có xấp xỉ bằng nhau không.

Ví dụ:

```json
{
  "type": "compare",
  "left": "XL",
  "operator": "approximately_equal",
  "right": "XC",
  "output": "resonance"
}
```

---

# 8. DSL là gì, và vì sao phải cẩn thận?

**DSL = Domain-Specific Language**
Tức là một “ngôn ngữ mini” dành riêng cho một miền bài toán.

Trong hệ thống này, nếu ta tạo những step như:

```text
coulomb_force
resultant
resonance_check
series_resistance
parallel_capacitance
```

thì ta đang dần xây một **DSL vật lý**.

DSL không phải lúc nào cũng xấu, nhưng trong bài này rất nguy hiểm vì:

* challenge quá universal,
* private test không thể lường hết,
* mỗi op mới chỉ giải quyết một pattern nhìn thấy trước,
* dễ dẫn đến kiến trúc specialized dần theo train set. 

---

# 9. Hướng kiến trúc cuối cùng đã thống nhất

## Với bài numeric / boolean

Pipeline nên là:

```text
Question
→ Qwen Planner
→ PlanValidator
→ Executor
→ ResultValidator
→ Qwen Explainer
```

Chi tiết:

### 1. Qwen Planner

Đọc đề và xuất:

* `answer_type`
* `givens`
* `target`
* `steps`

Ví dụ:

```json
{
  "answer_type": "numeric",
  "target": {
    "symbol": "P",
    "unit": "W"
  },
  "givens": [
    {"symbol": "I", "value": 2, "unit": "A"},
    {"symbol": "R", "value": 3, "unit": "ohm"}
  ],
  "steps": [
    {
      "id": "s1",
      "type": "equation",
      "equation": "U = I * R",
      "solves_for": "U"
    },
    {
      "id": "s2",
      "type": "equation",
      "equation": "P = U * I",
      "solves_for": "P"
    }
  ]
}
```

---

### 2. PlanValidator

Đây là **Python rule-based**, không phải model.

Nó kiểm tra trước khi chạy:

* JSON schema có hợp lệ không,
* `equation` parse được không,
* `solves_for` có nằm trong equation không,
* step hiện tại có dùng biến chưa được cho hoặc chưa được tính ở step trước không.

Ví dụ:

```text
P = U * I
```

mà `U` chưa có trong givens và chưa được sinh ra trước đó, validator báo lỗi thiếu biến. 

---

### 3. Executor

Đây là **Python tính toán**, chủ yếu dùng:

* Pint cho unit,
* SymPy cho solve,
* state để lưu biến trung gian.

Ví dụ:

```text
U = I*R → U = 6
P = U*I → P = 12
```

Executor không hiểu vật lý sâu. Nó chỉ thực hiện plan. 

---

### 4. ResultValidator

Cũng là **Python rule-based**, kiểm tra sau khi executor chạy:

* target có được tạo ra chưa,
* output có đúng kiểu không,
* nếu numeric thì có thực sự là số không,
* có còn unresolved symbol không,
* unit có hợp lệ không,
* có NaN/infinity không.

Nó **không verify được plan đúng vật lý hay sai vật lý**.
Ví dụ Qwen viết sai:

```text
P = U / I
```

thay vì:

```text
P = U * I
```

thì nếu đủ biến, executor vẫn chạy được. Validator không biết đó là sai công thức vật lý. 

---

### 5. Qwen Explainer

Chỉ viết lời giải dựa trên solver trace đã chạy xong.
Không tự đổi đáp án.

---

# 10. Verifier thực chất là gì?

Tên “verifier” dễ gây hiểu nhầm.

Nên tách rõ:

```text
PlanValidator
ResultValidator
```

Cả hai đều là:

* Python code,
* if/else,
* schema checks,
* SymPy free-symbol checks,
* type checks,
* unit checks.

Nó có thể trả JSON error đơn giản vì Python tạo `dict` rồi dump ra JSON. Ví dụ:

```json
{
  "status": "failed",
  "stage": "plan_validation",
  "step_id": "s2",
  "error_type": "missing_symbol",
  "message": "Cannot solve P = U * I because U is not given or computed by previous steps.",
  "missing_symbols": ["U"]
}
```



---

# 11. Nếu planner thiếu bước thì sao?

Ví dụ planner viết:

```text
P = U*I
```

nhưng `U` chưa biết.

Có hai khả năng:

## Cách đơn giản

Báo lỗi rồi dừng.

## Cách tốt hơn

Dùng **repair loop**:

```text
Planner tạo plan
→ Validator phát hiện thiếu U
→ gửi lỗi lại cho Qwen:
   "U is missing. Revise the plan."
→ Qwen sửa plan
→ chạy lại
```

Điểm quan trọng:

* Planner **vốn dĩ phải tự lập plan đủ bước ngay từ đầu**.
* Repair loop chỉ là phao cứu sinh khi planner thiếu bước.

---

# 12. Không phải bài nào cũng nên đi qua executor

Ta xác định có ít nhất 4 loại answer:

```text
numeric
boolean
symbolic_expression
text
```

---

## A. `numeric`

Ví dụ:

```text
45 mJ
```

→ đi qua planner → validator → executor → result validator → explainer.

---

## B. `boolean`

Ví dụ:

```text
Có cộng hưởng hay không?
```

→ có thể dùng compare.

---

## C. `symbolic_expression`

Ví dụ LD077:

```text
E1 = (3/4)E2
```

Đây là quan hệ đại số, không nhất thiết có unit, unit là `"-"`.

Ta đã chốt:

> **Baseline nên để Qwen tự reasoning và đưa ra symbolic expression.**

Python executor có thể làm symbolic math bằng SymPy, nhưng để làm tổng quát là một bài toán riêng phức tạp:

* suy ra quan hệ giữa hai biến,
* biến đổi symbolic đúng dạng,
* trình bày expression giống đáp án mong muốn.

Vì vậy baseline chưa cần ôm.
Verifier ở case này chỉ kiểm tra format/output nhẹ, **không biết logic sâu đúng hay sai**.

---

## D. `text`

Ví dụ LD047:

```text
Hướng về phía q₂
```

Đây là bài qualitative reasoning.

Ta chốt:

* Qwen phân loại `answer_type = text`
* Qwen tự reasoning và sinh answer
* Không ép executor đi qua.

Ý tưởng tách:

* `calculation_plan`
* `qualitative_reasoning`

là hợp lý cho tương lai, nhưng baseline nên giữ đơn giản trước.

---

# 13. Điểm rất quan trọng: nếu Qwen không biết vật lý thì executor không cứu được

Ta đã thảo luận kỹ điều này.

Ví dụ bài q1, q2, q3:

* nếu Qwen không biết `F3 = F13 + F23`,
* hoặc hiểu sai chiều lực,
* thì executor không thể tự nghĩ hộ.

Executor chỉ:

* tính đúng,
* đổi unit đúng,
* phát hiện plan không chạy được.

Nó không tự phát minh physics reasoning.

Vì vậy trọng tâm thật sự là:

> **Nâng năng lực physics reasoning của Qwen trên phạm vi rộng.** 

---

# 14. Vì sao không nên nhét rule chuyên biệt vào prompt?

Ta từng nghĩ tới:

* force cùng chiều thì cộng,
* ngược chiều thì trừ,
* có góc thì resultant.

Sau đó nhận ra cách này nguy hiểm vì:

* đó là specialized prompt rule,
* bản chất không khác “hard-code solver” là bao,
* universal external data nghĩa là test có thể rộng hơn rất nhiều so với các motif train.

Vì vậy ta chuyển hướng:

```text
Không hard-code physics reasoning theo task
Mà làm Qwen trở thành physics reasoner tốt hơn
```

Thông qua:

* external data rộng,
* fine-tuning,
* retrieval,
* synthetic reasoning examples rộng miền,
* huấn luyện planner behavior: chia bài thành equation steps. 

---

# 15. Few-shot có dùng không?

Có, nhưng chỉ nên dùng để dạy:

* format JSON,
* thói quen chia multi-step plan,
* không collapse nhiều bước vào một formula.

Không nên dùng few-shot để “dạy mẹo riêng” cho:

* Coulomb,
* resonance,
* error propagation,
* vector patterns cụ thể.

Những tri thức đó nên đến từ:

* pretrained knowledge,
* retrieval,
* fine-tuning external data rộng. 

---

# 16. Chiến lược tổng quát cuối cùng

## Kiến trúc nên hướng tới

```text
Broad physics knowledge
→ Qwen Planner tạo mathematical plan tổng quát
→ Python PlanValidator kiểm tra plan có chạy được
→ Python Executor chạy equation plan
→ Python ResultValidator kiểm tra output
→ Qwen Explainer viết lời giải từ trace
```

## Schema step tối giản

```json
{
  "answer_type": "numeric | boolean | symbolic_expression | text",
  "target": {
    "name": "string",
    "symbol": "string",
    "unit": "string"
  },
  "givens": [
    {
      "name": "string",
      "symbol": "string",
      "value": "number|string",
      "unit": "string"
    }
  ],
  "steps": [
    {
      "id": "s1",
      "type": "equation | compare",
      "equation": "string",
      "solves_for": "string"
    }
  ]
}
```

Trong đó:

* `equation` là core.
* `compare` giữ lại.
* `assign` bỏ.
* `convert_unit` executor làm ngầm.
* `resultant` chưa thêm.

---

# 17. Những bài không đơn vị

Ta chốt:

* Nếu `answer_type = symbolic_expression` hoặc `text`, thì `unit = "-"`.
* Không ép unit vào những answer dạng:

  * quan hệ biểu thức,
  * mô tả bằng lời.

Ví dụ:

```text
E1 = (3/4)E2, unit = "-"
```

hoặc:

```text
Hướng về phía q₂, unit = "-"
```

---

# 18. Dataset có noise

Codex chỉ ra một ví dụ:

* `100 μF`, `30 V`
* vật lý đúng:

  ```text
  E = 0.045 J = 45 mJ
  ```
* nhưng dataset row lại ghi:

  ```text
  45 J
  ```

Điều đó nghĩa là có **label/unit noise**, cần cẩn thận khi:

* đánh giá,
* tạo synthetic,
* fine-tune,
* so sánh answer exact match. 

---

# 19. Kết luận cuối cùng

## Điều không nên làm

* Không thêm solver riêng cho từng topic.
* Không thêm `resultant` sớm chỉ vì train có resultant.
* Không biến executor thành physics DSL quá sớm.
* Không nhét prompt rule đặc thù từng họ bài rồi tưởng là generalization.

## Điều nên làm

1. Chuyển pipeline từ:

   ```text
   one formula
   ```

   sang:

   ```text
   ordered plan of equations
   ```

2. Giữ executor generic:

   * giải equation,
   * unit conversion ngầm,
   * state variables,
   * target check.

3. Giữ `compare` cho boolean logic.

4. Thêm:

   * `PlanValidator`
   * `ResultValidator`

5. Dùng repair loop nếu plan thiếu biến / không chạy được.

6. Với `symbolic_expression` và `text`:

   * baseline để Qwen reasoning trực tiếp,
   * verifier chỉ kiểm tra format nhẹ.

7. Muốn general thật sự:

   * tăng tri thức Qwen bằng **external data, fine-tuning, retrieval**,
   * chứ không tăng special-case rules. 

---

# Một đoạn ngữ cảnh ngắn có thể paste sang chat mới

```text
We are designing a Physics QA solver for a broad competition dataset. The current root.py/root.ipynb pipeline is not overfit to Coulomb force; it is a generic single-equation solver:
Question → Qwen extracts givens/target/formula → Pint converts units → SymPy solves one equation → Qwen explains from solver trace.

The true flaw is architectural: it assumes every problem can be represented as “givens + one formula string → one SymPy solve.” This breaks on multi-step problems. A Coulomb three-charge case failed because Qwen collapsed several reasoning stages into one wrong scalar formula instead of computing F13, F23, then combining them.

We decided not to build topic-specific solvers or a large physics DSL, because the dataset and private tests may be very broad and universal external data is allowed. Codex proposed step types equation/assign/convert_unit/compare/resultant, but we refined this:
- Keep equation as the core operation.
- Keep compare for boolean/logical tasks.
- Drop assign because equation can express it.
- Let executor handle unit conversion implicitly when reading givens.
- Do not add resultant yet because it becomes domain-specific; Qwen should express vector/resultant reasoning through ordinary equations.

Target architecture:
Question → Qwen Planner → PlanValidator → Executor → ResultValidator → Qwen Explainer.

Qwen Planner outputs:
- answer_type: numeric | boolean | symbolic_expression | text
- givens
- target
- ordered steps of equations, optionally compare steps.

PlanValidator and ResultValidator are Python rule-based checks, not AI. They validate schema, missing symbols, unresolved variables, target reached, output type, unit logic, etc. Executor is Python using Pint + SymPy to execute the plan and store intermediate variables. If the plan references missing variables, validator/executor should return structured JSON errors; a repair loop can ask Qwen to revise the plan.

For numeric/boolean tasks, use planner → validator → executor → validator → explainer.
For symbolic_expression tasks, such as E1 = (3/4)E2, baseline should let Qwen reason and answer directly; Python symbolic solving is possible but not baseline.
For text tasks, such as “direction toward q2,” Qwen should classify as text and reason directly; no executor is required.

The main research direction is not to hard-code physics rules in prompts or special solvers, but to improve Qwen’s broad physics reasoning through external data, retrieval, and/or fine-tuning, while Python provides deterministic computation and technical validation.
```
