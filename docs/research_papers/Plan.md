# RESEARCH PROPOSAL: PROJECT TRIAD

## **Trembling Hands and Reluctant Heroes: A Unified Game-Theoretic Framework for Robustness, Welfare, and Alignment in Multi-Agent LLMs**

*(Bàn tay run rẩy và Những người hùng bất đắc dĩ: Khung lý thuyết thống nhất về độ bền vững và phúc lợi trong LLM đa tác tử)*

---

### 1. Abstract (Viết lại chuẩn giọng UAI/NeurIPS)

> **Abstract:**
> Khi các hệ thống AI chuyển dịch từ tương tác song phương (dyadic, N=2) sang đa phương (triadic, N=3), sự phức tạp chiến lược tăng vọt với sự xuất hiện của các liên minh động và trách nhiệm tập thể. Các benchmark hiện tại (như FAIRGAME) thường bỏ qua "độ nhiễu" (noise) của môi trường thực tế, dẫn đến các đánh giá quá lạc quan về khả năng hợp tác của LLM.
> Nghiên cứu này giới thiệu **PROJECT TRIAD**, một khung đánh giá toàn diện sử dụng bộ ba trò chơi chiến lược (**The Strategic Triad**): **(1) 3-Player Prisoner's Dilemma** để kiểm tra độ bền vững của liên minh dưới áp lực phản bội; **(2) Public Goods Game** để đo lường sự tuân thủ quy chuẩn nhóm; và **(3) Volunteer's Dilemma** để đánh giá tính anh hùng và hiệu ứng người ngoài cuộc (bystander effect).
> Chúng tôi đề xuất khái niệm **"Trembling Hand Perfection"** như một thước đo mới cho trí tuệ xã hội AI: khả năng phân biệt giữa lỗi thực thi ngẫu nhiên (nhiễu từ 1-10%) và ý định ác ý. Thông qua các nghiên cứu loại bỏ (ablation studies) trên các quy mô mô hình (7B vs 70B), chúng tôi phát hiện ra một **"Nghịch lý Hiệu quả" (Efficiency Paradox)**: các mô hình lớn hơn thể hiện sự bao dung cao hơn nhưng lại dễ bị tổn thương trước các chiến lược "ăn theo tinh vi" (sophisticated free-riding). Việc áp dụng **Shapley Values** cho phép chúng tôi định lượng chính xác "Alignment Gap" – khoảng cách giữa tối ưu cá nhân và phúc lợi xã hội.

---

### 2. The Strategic Triad (Bộ 3 Game "Thần thánh")

Thay vì 4 game, chúng ta định nghĩa 3 game này là 3 trụ cột của trí tuệ xã hội:

#### **Pillar 1: The Robustness Test (3-IPD)**

* **Bản chất:** Xung đột lợi ích (Conflict).
* **Cơ chế:** Tensor payoff .
* **Điểm nhấn:** Tập trung vào **Coalition Entropy**. Khi A và B liên minh phản bội C, nếu ta bơm nhiễu vào (A lỡ tay phản B), liên minh này vỡ nhanh hay chậm?
* *Giả thuyết:* Model thông minh sẽ duy trì liên minh bất chấp nhiễu nhỏ.



#### **Pillar 2: The Collectivism Test (Public Goods Game)**

* **Bản chất:** Lợi ích tập thể (Welfare).
* **Cơ chế:** Đóng góp quỹ chung + Trừng phạt (Punishment).
* **Điểm nhấn:** Tập trung vào **Inequality Aversion**. LLM có chấp nhận bỏ tiền túi ra trừng phạt kẻ Free-rider để giữ công bằng không?
* *Giả thuyết:* Model "Nicer than Humans" sẽ ngại trừng phạt, dẫn đến sự sụp đổ của quỹ chung (Toxic Kindness).



#### **Pillar 3: The Safety Test (Volunteer's Dilemma)**

* **Bản chất:** Đạo đức & An toàn (Safety/Alignment).
* **Cơ chế:** Một người hy sinh để cứu cả tàu.
* **Điểm nhấn:** Tập trung vào **Diffusion of Responsibility**.
* *Giả thuyết:* GPT-4 sẽ tính toán quá kỹ và đợi người khác làm ("strategic waiting"), trong khi model nhỏ hơn có thể hành động ngẫu nhiên nhưng lại cứu được tàu. -> Đây là điểm rất hay để bàn về **AI Safety**.



---

### 3. Phương pháp luận: "The Trembling Hand" (Giữ nguyên concept này vì quá hay)

Chúng ta sẽ bơm nhiễu theo quy trình 2 bước:

1. **Execution Noise:** Agent chọn A, nhưng hệ thống thực thi B (xác suất ). -> Test xem đối thủ có "tha thứ" không.
2. **Perception Noise:** Agent chọn A, hệ thống thực thi A, nhưng báo cho đối thủ là B. -> Test xem giao tiếp có bị hiểu sai không.

Metric chính:

* **Trembling Robustness Score ():** Độ dốc của đường cong phúc lợi khi  tăng.

---
