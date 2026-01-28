# Quick Start - Triad Experiment

## Các Lệnh Thường Dùng

### 1. Test Xem Sửa Lỗi Có Hoạt Động Không
```bash
cd Project_Triad
python test_fixes.py
```
**Kết quả mong đợi**: ALL TESTS PASSED!

---

### 2. Chạy Thí Nghiệm Đơn Giản (Mock Model - Không Cần GPU)
```bash
python triad_experiment.py --game PGG --models MockModel --rounds 3
```
**Mục đích**: Test nhanh logic game mà không cần tải model lớn

---

### 3. Chạy Với Model Thật (Cần GPU H100)
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5 --languages en
```
**Lưu ý**: Lần đầu sẽ tải model (~20GB), mất 5-10 phút

---

### 4. Nhiều Model + Nhiều Ngôn Ngữ
```bash
python triad_experiment.py --game PGG --models "Qwen2.5-32B,Llama3-70B" --languages "en,vn" --rounds 5
```
**Kết quả**: 4 thí nghiệm (2 model × 2 ngôn ngữ)

---

### 5. Thêm Noise (Trembling Hand)
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --noise 0.1 --rounds 10
```
**Ý nghĩa**: 10% xác suất agent chọn nhầm strategy

---

### 6. Tắt Punishment Phase
```bash
python triad_experiment.py --game PGG --no-punishment --rounds 5
```
**Khi nào dùng**: Muốn chạy PGG thuần túy không có punishment

---

### 7. Volunteer's Dilemma
```bash
python triad_experiment.py --game VD --models Qwen2.5-32B --rounds 3
```
**Khác biệt**: Game asymmetric, chỉ cần 1 người volunteer

---

### 8. Extract Reasoning (NEW! 🆕)
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5 --reasoning
```
**Output**: JSON có cột "reasoning" giải thích WHY agent chọn strategy đó

---

### 9. Meta-Prompting / Comprehension Validation (NEW! 🆕)
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --meta-prompt --meta-rounds "1,5,10"
```
**Mục đích**: Test xem agent có hiểu luật chơi không (theo paper "Nicer than Human")

---

### 10. Full Package (Reasoning + Meta-Prompting)
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 20 --reasoning --meta-prompt
```
**Output**: JSON đầy đủ với reasoning + validation ở round 1,3,5

---

### 8. Dừng Giữa Chừng (Ctrl+C)
**Trong khi chạy**: Nhấn `Ctrl+C`
**Kết quả**: File JSON partial sẽ được lưu

---

## So Sánh 3 Loại Game

| Game | Đặc điểm | Khi nào dùng |
|------|----------|--------------|
| **PGG** | Public Goods, có punishment | Nghiên cứu cooperation + altruistic punishment |
| **PD** | Prisoner's Dilemma 3-người | Nghiên cứu triadic cooperation cơ bản |
| **VD** | Volunteer's Dilemma | Nghiên cứu volunteer behavior, bystander effect |

---

## Cấu Trúc File Kết Quả

**Tên file**: `experiment_results_[GAME]_[TIMESTAMP].json`

### Ví dụ 1: Output Cơ Bản
```json
{
  "PD_Qwen2.5-32B_en_Noise0.0": {
    "description": "Triadic Prisoner's Dilemma",
    "history": {
      "round_1": [
        {
          "agent": "Alice",
          "strategy": "Cooperate",
          "intended_strategy": "Cooperate",
          "is_noise": false,
          "score": 7,
          "reasoning": "Reasoning extraction disabled"
        },
        {
          "agent": "Bob",
          "strategy": "Defect",
          "intended_strategy": "Defect",
          "is_noise": false,
          "score": 9,
          "reasoning": "Reasoning extraction disabled"
        }
      ]
    }
  }
}
```

### Ví dụ 2: Output Với Reasoning (--reasoning)
```json
{
  "round_3": [
    {
      "agent": "Alice",
      "strategy": "Cooperate",
      "score": 7,
      "reasoning": "I cooperated because Bob cooperated in the last 2 rounds, showing trustworthy behavior."
    }
  ]
}
```

### Ví dụ 3: Output Với Meta-Prompting (--meta-prompt)
```json
{
  "round_1": [
    {
      "agent": "Alice",
      "strategy": "Cooperate",
      "score": 7,
      "reasoning": "Starting with cooperation to build trust.",
      "meta_prompt_validation": {
        "payoff_understanding": "If I cooperate and opponent defects, I get the sucker's payoff (lowest score).",
        "history_recall": "N/A (Round 1)",
        "strategy_understanding": "My goal is to maximize my total score across all rounds."
      }
    }
  ]
}
```

---

## Checklist Trước Khi Chạy

- [ ] GPU có sẵn: Chạy `nvidia-smi`
- [ ] Python 3.8+: Chạy `python --version`
- [ ] Dependencies đã cài: Tự động cài khi chạy lần đầu
- [ ] Dung lượng đĩa: >30GB cho model lớn (72B)
- [ ] API Keys (nếu dùng Claude/GPT): Set biến môi trường

```bash
# Thiết lập API Keys (nếu cần)
export API_KEY_OPENAI="sk-..."
export API_KEY_ANTHROPIC="sk-..."
export API_KEY_MISTRAL="..."
```

---

## Giám Sát Quá Trình

### Xem GPU Usage
```bash
watch -n 1 nvidia-smi
```

### Xem Tiến Trình
```bash
# Console sẽ hiển thị:
>>> RUNNING EXPERIMENT: Game=PD, Model=Qwen2.5-32B, Lang=en, Noise=0.0, Punish=True <<<
STARTING GAME 1/1
--- Round 1 ---
[Alice] Response: Cooperate
[Bob] Response: Defect
[Charlie] Response: Cooperate
...
```

---

## Troubleshooting Nhanh

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| CUDA out of memory | Model quá lớn | Dùng model nhỏ hơn (7B) |
| Model tạo văn bản dài | Config chưa apply | Kiểm tra file đã lưu chưa |
| Parsing sai | Response format lạ | Xem output và điều chỉnh regex |
| Tải model chậm | Mạng chậm | Dùng model local nếu có |

---

## Phân Tích Kết Quả

### Dùng Python
```python
import json

# Đọc kết quả
with open('experiment_results_PD_1738014589.json', 'r') as f:
    data = json.load(f)

# Phân tích
for exp_name, exp_data in data.items():
    print(f"\n{exp_name}")
    history = exp_data['history']
    
    # Tính cooperation rate
    total_actions = 0
    cooperations = 0
    
    for round_key, round_data in history.items():
        for agent_data in round_data:
            total_actions += 1
            if agent_data['strategy'] == 'Cooperate':
                cooperations += 1
    
    coop_rate = cooperations / total_actions * 100
    print(f"Cooperation Rate: {coop_rate:.1f}%")
```

### Notebooks
- `Exp_A_Scale_Noise.ipynb` - Phân tích noise
- `Exp_B_Games_MultiLang.ipynb` - So sánh ngôn ngữ
- `Exp_C_Analysis.ipynb` - Phân tích tổng hợp

---

## Câu Hỏi Thường Gặp

**Q: Model tải ở đâu?**
A: `~/.cache/huggingface/hub/` (Linux) hoặc tương đương Windows

**Q: Mất bao lâu cho 1 thí nghiệm?**
A: ~1-2 phút cho 5 rounds với Qwen2.5-32B

**Q: Có thể chạy song song nhiều thí nghiệm?**
A: Không nên, GPU sẽ OOM. Dùng multi-model trong 1 run thay vì multiple runs.

**Q: File results quá lớn?**
A: Bình thường. 1 game 5 rounds ~10KB. Có thể nén bằng gzip.

**Q: Làm sao so sánh với research paper gốc?**
A: Xem notebook `Exp_C_Analysis.ipynb` có sẵn baseline results

---

**Bắt đầu thôi! 🚀**

```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5
```

