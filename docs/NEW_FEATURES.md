# New Features: Reasoning Extraction & Meta-Prompting

## Tổng Quan

Đã thêm 2 features mới theo paper **"Nicer than Human"**:

1. **Reasoning Extraction** - Lưu lý do suy nghĩ của agent vào JSON
2. **Meta-Prompting** - Test xem agent có hiểu luật chơi không

---

## Feature 1: Reasoning Extraction

### Mô Tả
Sau khi agent chọn strategy (Cooperate/Defect), hệ thống sẽ hỏi thêm một câu riêng để agent giải thích **TẠI SAO** họ chọn như vậy.

### Cách Hoạt Động
1. Agent chọn strategy (prompt ngắn, max_new_tokens=10)
2. Sau khi parse strategy, hệ thống gửi thêm reasoning prompt
3. Agent trả lời reasoning (max_new_tokens tăng lên)
4. Reasoning được lưu vào JSON output

### Reasoning Prompt Example
```
You just chose to Cooperate in round 3 while playing with Bob, Charlie.
In 1-2 short sentences, explain WHY you made this choice. What factors influenced your decision?

Your reasoning:
```

### Output JSON Format
```json
{
  "round_1": [
    {
      "agent": "Alice",
      "strategy": "Cooperate",
      "intended_strategy": "Cooperate",
      "is_noise": false,
      "score": 7,
      "reasoning": "I cooperated because both opponents cooperated in the previous round, indicating a cooperative environment."
    }
  ]
}
```

### Kích Hoạt
```bash
# Bật reasoning extraction
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5 --reasoning
```

### Lưu Ý
- Reasoning bị limit ở 300 ký tự
- Nếu không bật `--reasoning`, reasoning field sẽ là "Reasoning extraction disabled"
- Reasoning extraction làm tăng thời gian chạy (thêm 1 LLM call per agent per round)

---

## Feature 2: Meta-Prompting (Comprehension Validation)

### Mô Tả
Định kỳ (ở các round cụ thể), hệ thống sẽ hỏi agent các câu hỏi để **kiểm tra xem agent có hiểu luật chơi không**.

Theo paper "Nicer than Human", việc validate comprehension rất quan trọng để đảm bảo agent thực sự hiểu game chứ không phải random guess.

### 3 Loại Validation Questions

#### 1. Payoff Understanding
```
You are playing a game with payoffs. Answer briefly:
If you Cooperate and your opponent Defects, what happens to your score 
compared to if you both Cooperate?
Answer in one short sentence.
```

**Mục đích**: Test xem agent có hiểu payoff structure không

#### 2. History Recall
```
Based on the game history so far, which opponent has defected the most?
Answer with just the name or 'None'.
```

**Mục đích**: Test xem agent có theo dõi được history không

#### 3. Strategy Understanding
```
What is your main goal in this game? Answer in one short sentence.
```

**Mục đích**: Test xem agent có hiểu objective của game không

### Output JSON Format
```json
{
  "round_3": [
    {
      "agent": "Alice",
      "strategy": "Cooperate",
      "score": 7,
      "reasoning": "Bob always cooperates, so I trust him.",
      "meta_prompt_validation": {
        "payoff_understanding": "If I cooperate and opponent defects, I get lower score (sucker's payoff).",
        "history_recall": "Bob has not defected yet.",
        "strategy_understanding": "My goal is to maximize total points over all rounds."
      }
    }
  ]
}
```

### Kích Hoạt

**Mặc định**: Tắt

```bash
# Bật meta-prompting ở round 1, 3, 5
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --meta-prompt

# Tùy chỉnh rounds cho meta-prompting
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --meta-prompt --meta-rounds "1,5,10"

# Kết hợp cả reasoning và meta-prompting
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --reasoning --meta-prompt
```

### Lưu Ý
- Meta-prompting chỉ chạy ở các round được chỉ định
- Mỗi agent được hỏi 3 câu hỏi
- Các câu trả lời bị limit ở 100 ký tự
- History recall chỉ được hỏi từ round 2 trở đi

---

## So Sánh Với Paper "Nicer than Human"

| Feature | Paper "Nicer than Human" | Implementation Này |
|---------|-------------------------|-------------------|
| **Meta-Prompting** | ✅ Có | ✅ Có (`--meta-prompt`) |
| **Payoff Understanding** | ✅ Test | ✅ Test |
| **History Parsing** | ✅ Test | ✅ Test (History Recall) |
| **Strategy Understanding** | ✅ Implicit | ✅ Explicit question |
| **Reasoning Extraction** | ❌ Không có | ✅ Có (`--reasoning`) |
| **100-round games** | ✅ Có | ✅ Có (tùy `--rounds`) |
| **Behavioral Dimensions** | ✅ Phân tích | ⏳ Chưa (future work) |

---

## Ví Dụ Sử Dụng

### Experiment 1: Chỉ Reasoning
```bash
python triad_experiment.py \
  --game PD \
  --models Qwen2.5-32B \
  --rounds 10 \
  --languages en \
  --reasoning
```

**Output**: JSON với reasoning cho mỗi round

---

### Experiment 2: Chỉ Meta-Prompting
```bash
python triad_experiment.py \
  --game PD \
  --models "Qwen2.5-32B,Llama3-70B" \
  --rounds 20 \
  --meta-prompt \
  --meta-rounds "1,5,10,15,20"
```

**Output**: JSON với validation results ở round 1, 5, 10, 15, 20

---

### Experiment 3: Full Package (Giống Paper)
```bash
python triad_experiment.py \
  --game PD \
  --models Qwen2.5-32B \
  --rounds 100 \
  --reasoning \
  --meta-prompt \
  --meta-rounds "1,10,25,50,75,100"
```

**Output**: 
- Reasoning cho tất cả 100 rounds
- Validation questions ở 6 checkpoints
- Phân tích đầy đủ behavior patterns

---

### Experiment 4: Test Comprehension Nhanh
```bash
# Test với MockModel (không cần GPU)
python triad_experiment.py \
  --game PGG \
  --models MockModel \
  --rounds 5 \
  --meta-prompt \
  --meta-rounds "1,3,5"
```

**Mục đích**: Test nhanh xem meta-prompting có hoạt động không

---

## Phân Tích Kết Quả

### Python Script Để Phân Tích
```python
import json

with open('experiment_results_PD_1738014589.json', 'r') as f:
    data = json.load(f)

for exp_name, exp_data in data.items():
    print(f"\n{'='*60}")
    print(f"Experiment: {exp_name}")
    print(f"{'='*60}")
    
    history = exp_data['history']
    
    # Analyze reasoning patterns
    print("\n--- Reasoning Analysis ---")
    for round_key in sorted(history.keys()):
        round_data = history[round_key]
        print(f"\n{round_key}:")
        for agent_data in round_data:
            agent = agent_data['agent']
            strategy = agent_data['strategy']
            reasoning = agent_data.get('reasoning', 'N/A')
            print(f"  {agent} chose {strategy}")
            print(f"    Reasoning: {reasoning[:80]}...")
    
    # Analyze meta-prompt validations
    print("\n--- Meta-Prompt Validation ---")
    for round_key in sorted(history.keys()):
        round_data = history[round_key]
        for agent_data in round_data:
            if 'meta_prompt_validation' in agent_data:
                agent = agent_data['agent']
                meta = agent_data['meta_prompt_validation']
                print(f"\n{round_key} - {agent}:")
                print(f"  Payoff Understanding: {meta['payoff_understanding'][:60]}...")
                print(f"  History Recall: {meta['history_recall']}")
                print(f"  Strategy Understanding: {meta['strategy_understanding'][:60]}...")
```

---

## Performance Impact

| Feature | Extra LLM Calls per Round | Time Impact |
|---------|-------------------------|-------------|
| **Reasoning** | +3 (1 per agent) | ~3-5s extra |
| **Meta-Prompting** | +9 (3 questions × 3 agents) | ~10-15s extra |
| **Both** | +12 | ~15-20s extra |

**Lưu ý**: Chỉ áp dụng cho rounds có meta-prompting enabled

---

## Troubleshooting

### Q: Reasoning quá ngắn hoặc không có ý nghĩa?
**A**: Model có thể cần temperature cao hơn. Hiện tại set `temperature=0.1` cho strategy nhưng reasoning prompt có thể cần điều chỉnh.

### Q: Meta-prompt validation fail?
**A**: Agent có thể không hiểu game. Xem output validation để debug:
```python
# Check validation quality
meta = agent_data['meta_prompt_validation']
if 'lower' in meta['payoff_understanding'].lower():
    print("✓ Agent understands payoff correctly")
else:
    print("✗ Agent may not understand payoff")
```

### Q: Có thể extract reasoning mà không cần separate prompt không?
**A**: Có, nhưng sẽ làm giảm accuracy của strategy parsing. Separate prompt đảm bảo:
1. Strategy parsing không bị nhiễu
2. Reasoning đầy đủ hơn (không bị limit bởi max_new_tokens=10)

---

## Next Steps

Các features có thể thêm tiếp theo:

1. **Behavioral Dimension Analysis**
   - Tính cooperation rate
   - Detect strategy types (TFT, Always Defect, etc.)
   - Measure forgiveness, retaliation

2. **Adversarial Validation**
   - Test với adversarial prompts
   - Check consistency across paraphrased questions

3. **Visualization**
   - Plot reasoning patterns over time
   - Visualize strategy evolution
   - Heatmap of cooperation/defection

4. **Auto Analysis**
   - Tự động phân loại reasoning (rule-based, reciprocal, etc.)
   - Tự động grade meta-prompt answers

---

## Tài Liệu Tham Khảo

- **Paper**: "Nicer than Human: How Do Large Language Models Behave in the Prisoner's Dilemma?" (ICWSM 2025)
- **Code**: `triad_experiment.py` (dòng 538-596 cho meta-prompting, dòng 606-674 cho reasoning)

---

**Happy Experimenting! 🎯**

