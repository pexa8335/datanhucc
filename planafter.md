
Đúng: nếu test toàn dạng mới hoàn toàn mà deterministic solver chưa có primitive/logic tương ứng, thì solver rule-based sẽ không tự nghĩ ra được. Nhưng trong hệ hybrid của mình, nó không nên bỏ trắng: nó phải chuyển sang qwen_fallback.

Vấn đề hiện tại là fallback Qwen đang yếu, nên cần làm 3 tầng:

Deterministic solver cho dạng chắc chắn

Dùng cho TD/NL/DDT/THCB/CH đơn giản, vì hiện đang đúng rất cao.
Ưu điểm: chính xác, có trace, ít hallucination.
Nhược: gặp dạng lạ thì unsupported.
Qwen Planner + Generic Executor cho dạng mới

Thay vì hard-code thêm từng dạng, cho Qwen sinh plan:
{
  "answer_type": "numeric",
  "givens": [...],
  "steps": [
    {"type": "equation", "equation": "F = k*q1*q2/r^2", "solves_for": "F"}
  ]
}
Python chỉ kiểm tra biến, đơn vị, solve equation.
Nếu Qwen lập thiếu bước thì repair loop sửa.
Đây là cách giúp xử lý dạng mới tốt hơn deterministic thuần.
Qwen direct fallback cho text/symbolic/quá khó

Nếu bài không hợp executor, Qwen trả lời trực tiếp.
Nhưng phải fine-tune/prompt lại mạnh hơn, vì hiện fallback chỉ đúng 3/50.
Mình đề xuất hướng thực tế nhất:

Giữ deterministic solver làm “máy ăn điểm chắc”.
Dùng kết quả deterministic đúng để tạo planner_sft: dạy Qwen sinh plan chuẩn.
Bổ sung synthetic data rộng miền: điện trường, tụ điện, RLC, từ trường, sai số, vector, quan hệ tỉ lệ.
Với unsupported rows, không để model trả lời tự do quá; ép nó theo format:
givens → formula → substitution → final answer.
Thêm RAG/formula sheet nhỏ cho Physics: Qwen được xem công thức liên quan trước khi lập plan.
Nói ngắn gọn: deterministic solver không thể generalize vô hạn. Muốn gặp dạng mới vẫn trả lời được, phải để Qwen làm planner/reasoner, còn Python làm executor/verifier. Đây mới là kiến trúc bền hơn cho private test.

deterministic_solver
→ nếu fail: Qwen Planner sinh JSON plan
→ Python generic executor chạy equation/compare
→ nếu lỗi: repair loop tối đa 2 lần
→ nếu vẫn fail: direct_fallback bằng Qwen
Mình cũng thêm:

Formula hints/RAG mini trong Cell 13.
JSON parser cho plan.
PlanValidator nhẹ: thiếu biến, target không có trong equation, equation không parse được.
SymPy executor cho equation.
Compare executor cho boolean.
Circuit breaker nếu repair lặp cùng lỗi.
Direct fallback nhận structured error để tránh lặp lỗi.
Output CSV có thêm các cột như prediction_source, planner_attempts, planner_error, planner_plan.
Mình cũng sửa phần planner-SFT:

make_planner_sft_data.py

Giờ file này không sinh deterministic_primitive nữa, mà sinh đúng schema executor mới:

{"type": "equation", "equation": "Q=C*U", "solves_for": "Q"}
Đã regenerate planner data:

train_planner_records: 603
test_planner_records: 208
File zip để bạn upload thêm lên Kaggle nếu muốn train planner-SFT:

planner_sft.zip

Khi chạy Kaggle:

Upload notebook mới: finetuneqwen2-57bcoder.ipynb.
Attach dataset có 80.csv và 20.csv.
Optional nhưng nên làm: upload planner_train.jsonl từ thư mục planner_sft lên Kaggle dataset, sao cho path dạng:
/kaggle/input/planner-sft/planner_train.jsonl
Chạy từ trên xuống. Cell 8 sẽ tự báo nếu tìm thấy planner-SFT:
Added planner-SFT examples: ...
Cell 13 sẽ xuất:
Source counts: {
  deterministic_solver: ...,
  planner_executor: ...,
  planner_direct: ...,
  direct_fallback: ...
}
Lưu ý: Cell 13 sẽ chậm hơn vì 50 câu fallback giờ có thể gọi planner + repair trước khi direct fallback. Nhưng đổi lại, nếu private test có dạng mới, nó có cơ hội giải bằng plan tổng quát thay vì chỉ đoán trực tiếp.


Có, và phân tích chính khá rõ:

File sai hiện tại có 57 dòng sai. Trong đó:

deterministic_solver sai: 10 dòng
qwen_fallback sai: 47 dòng
Điều này nói lên một chuyện rất quan trọng: solver rule-based không phải vấn đề chính nữa. Vấn đề lớn nhất là những câu rơi vào fallback Qwen.

1. Nhóm Sai Lớn Nhất: LD/DT

Sai nhiều nhất nằm ở:

LD: 33 dòng sai
DT: 13 dòng sai
Đây đều là nhóm điện trường/lực điện có hình học:

điểm nằm trên đường thẳng AB,
điểm ngoài đoạn AB,
trung điểm,
đường trung trực,
tam giác đều,
tam giác vuông cân,
tổng hợp vector điện trường/lực điện,
tìm vị trí điện trường bằng 0.
Nói ngắn gọn: Qwen đang yếu ở hình học + vector electrostatics.

2. Deterministic Solver Sai Ít Nhưng Có Pattern

10 dòng deterministic sai gồm:

LD049, LD050, LD055, LD105
LD384, LD391, LD400
NL340
TD395, TD398
Trong đó:

LD049, LD050, LD055, LD105: lỗi tổng hợp lực Coulomb theo hình học tam giác/đường thẳng.
LD384, LD391, LD400: lỗi điện trường trên đường trung trực, có khả năng solver hiểu sai khoảng cách hoặc cách cộng vector.
NL340: lỗi chọn sai target. Đề hỏi năng lượng điện trường còn lại, solver lại tính dòng điện.
TD395, TD398: rất đáng nghi là label/unit noise hoặc cách dataset kỳ lạ. Ví dụ TD398 solver ra 1.660125 μJ, gold là 1.66 nJ, lệch đúng hệ số 1000.
3. Qwen Fallback Sai Chủ Yếu Vì Không Bị Ép Format/Plan Đủ Chặt

Một số dòng fallback trả ra kiểu:

Step 7: Solve for ...
Step 9: Calculate ...
Ex1 = ...
Ví dụ:

CH102
DT059
LD347
LD353
Tức là model không trả final answer sạch, dù prompt yêu cầu. Đây là lý do mình vừa thêm lớp planner_executor + repair loop trước direct fallback. Bản CSV này là kết quả cũ kiểu deterministic -> qwen_fallback; sau khi chạy notebook mới, ta cần xem lại các dòng này có chuyển sang planner_executor được không.

4. Có 2 Dòng Có Vẻ Metric Bị Khắt Khe

DT058: gold = 8E V/m, pred = 8E V/m
LD306: gold = 1.99×10^6 V/m, pred = 2.03×10^6 V/m
Hai dòng này answer_ok=True, unit_ok=True nhưng pair_ok=False. Nên đây không hẳn là lỗi mô hình, mà là lỗi/độ khắt khe của hàm compare. Có thể sửa metric để điểm tăng nhẹ.

5. Ưu Tiên Cải Thiện

Theo impact, mình sẽ ưu tiên như sau:

Ưu tiên 1: LD/DT geometry electrostatics
Ưu tiên 2: ép fallback qua planner_executor trước direct answer
Ưu tiên 3: sửa metric mismatch DT058/LD306
Ưu tiên 4: xử lý riêng vài case CH/RLC phức tạp
Ưu tiên 5: đánh dấu TD395/TD398 là possible label noise
Kết luận: file sai cho thấy hệ thống hiện tại đã “ăn chắc” tốt bằng deterministic solver, nhưng để tăng tiếp thì không nên fine-tune mù nữa. Cần tập trung vào LD/DT vector geometry và kiểm tra lại kết quả sau khi chạy notebook mới có planner_executor.


Được, mình sẽ tập trung đúng Ưu tiên 1: LD/DT geometry electrostatics. Mình sẽ không động lung tung sang fine-tune/RLC; mục tiêu là giảm các dòng sai/unsupported thuộc điện trường, lực điện, hình học vector trước.


Ran 3 commands
Mình thấy ngay trong baseline hiện tại: nhiều case LD/DT chưa vào solver vì không map được “target charge/field point”; một số case vào rồi nhưng cộng vector sai do geometry đặc biệt. Mình sẽ thêm các primitive electrostatics theo reasoning-shape, không theo row ID: collinear zero-field, equilateral/right-isosceles triangle, perpendicular bisector, field/force at third vertex.


Ran 6 commands
Mình sẽ sửa theo hai lớp: trước hết sửa extractor để hiểu đúng các quan hệ như AC = BC = 8 cm, from C to B is 4 cm, “a point 6 cm from A and 8 cm from B”; sau đó thêm các solver hình học LD/DT phổ biến như tam giác đều, tam giác vuông cân, zero-field trên trục, đĩa tích điện, dây dài, bụi cân bằng.


Edited 1 file, ran 1 command
Extractor và primitive mới đã compile OK. Mình chạy lại đánh giá 20% để xem riêng LD/DT tăng hay có dòng nào bị regression.


Edited 1 file, ran 7 commands
Context automatically compacted
Mình sẽ làm tiếp “Ưu tiên 1” theo đúng hướng: mở rộng deterministic solver cho các dạng LD/DT điện trường/lực điện còn rơi vào unsupported hoặc sai, rồi chạy lại eval 20% để đo thật chứ không đo cảm giác. Trước tiên mình đọc nhanh trạng thái file solver hiện tại và các hàng sai còn lại.


Ran 3 commands
Mình thấy các hàm mới đã được thêm vào solver, nhưng theo dấu hiệu trong file thì khả năng một số hàm chưa được móc vào danh sách chạy chính. Giờ mình mở đúng đoạn điều phối và vài hàm hay gây sai để vá gọn.


Ran 6 commands
Đúng là danh sách sai còn lại chủ yếu là LD/DT đặc thù hình học: một phần đã có hàm riêng nhưng chưa được gọi, một phần do parse đơn vị/điểm hỏi. Mình sẽ vá phần điều phối trước, rồi thêm vài parse rất hẹp nhưng vẫn theo dạng vật lý tổng quát của LD/DT.