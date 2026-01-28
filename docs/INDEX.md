# 📖 Documentation Index

Tất cả tài liệu cho Triad Experiment Project.

---

## 🇻🇳 Tiếng Việt (Vietnamese)

### ⭐ BẮT ĐẦU TẠI ĐÂY
**[SUMMARY_VI.md](SUMMARY_VI.md)** - Tổng quan toàn bộ features
- Reasoning Extraction
- Meta-Prompting
- Cách sử dụng
- Examples
- FAQ

### Các Tài Liệu Khác
- **[TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md)** - Chi tiết các bug fixes đã sửa
- **[QUICK_START.md](QUICK_START.md)** - Các lệnh thường dùng, quick reference

---

## 🇬🇧 English

### Core Documentation
- **[NEW_FEATURES.md](NEW_FEATURES.md)** - Reasoning Extraction & Meta-Prompting
  - Technical implementation
  - Usage examples
  - Analysis scripts
  
- **[FIXES.md](FIXES.md)** - Bug Fixes & Performance Improvements
  - What was fixed
  - How it works now
  - Performance metrics

- **[QUICK_START.md](QUICK_START.md)** - Quick Reference Guide
  - Common commands
  - Examples
  - Troubleshooting

---

## 📚 Mục Lục Chi Tiết

### 1. Bắt Đầu Nhanh
**Chọn 1 trong 3:**
- 🇻🇳 [SUMMARY_VI.md](SUMMARY_VI.md) - Nếu bạn đọc tiếng Việt
- 🇬🇧 [NEW_FEATURES.md](NEW_FEATURES.md) - If you read English
- 📋 [QUICK_START.md](QUICK_START.md) - Chỉ muốn xem commands

### 2. Features Mới
- **Reasoning Extraction** → [NEW_FEATURES.md](NEW_FEATURES.md) hoặc [SUMMARY_VI.md](SUMMARY_VI.md)
- **Meta-Prompting** → [NEW_FEATURES.md](NEW_FEATURES.md) hoặc [SUMMARY_VI.md](SUMMARY_VI.md)

### 3. Bug Fixes
- 🇬🇧 English → [FIXES.md](FIXES.md)
- 🇻🇳 Tiếng Việt → [TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md)

### 4. Quick Reference
- **Commands** → [QUICK_START.md](QUICK_START.md)
- **Examples** → [QUICK_START.md](QUICK_START.md)
- **Troubleshooting** → [FIXES.md](FIXES.md) hoặc [TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md)

---

## 🎯 Tìm Tài Liệu Theo Chủ Đề

### Tôi Muốn...

#### ...học cách sử dụng features mới
→ [SUMMARY_VI.md](SUMMARY_VI.md) (VN) hoặc [NEW_FEATURES.md](NEW_FEATURES.md) (EN)

#### ...xem các lệnh thường dùng
→ [QUICK_START.md](QUICK_START.md)

#### ...hiểu các bug fixes
→ [FIXES.md](FIXES.md) (EN) hoặc [TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md) (VN)

#### ...chạy experiment ngay
→ [QUICK_START.md](QUICK_START.md) - Section "Quick Start"

#### ...phân tích kết quả
→ [NEW_FEATURES.md](NEW_FEATURES.md) - Section "Phân Tích Kết Quả"

#### ...troubleshoot lỗi
→ [FIXES.md](FIXES.md) - Section "Troubleshooting"

#### ...hiểu meta-prompting
→ [NEW_FEATURES.md](NEW_FEATURES.md) - Section "Feature 2: Meta-Prompting"

#### ...hiểu reasoning extraction
→ [NEW_FEATURES.md](NEW_FEATURES.md) - Section "Feature 1: Reasoning Extraction"

---

## 📊 So Sánh Các Tài Liệu

| File | Language | Length | Focus | Best For |
|------|----------|--------|-------|----------|
| **SUMMARY_VI.md** | 🇻🇳 Vietnamese | Long | Everything | Người Việt, học chi tiết |
| **NEW_FEATURES.md** | 🇬🇧 English | Long | New features | Technical deep-dive |
| **QUICK_START.md** | 🇻🇳🇬🇧 Both | Medium | Commands | Quick reference |
| **FIXES.md** | 🇬🇧 English | Long | Bug fixes | Understanding fixes |
| **TOM_TAT_SUA_LOI.md** | 🇻🇳 Vietnamese | Medium | Bug fixes | Người Việt |

---

## 🚀 Recommended Reading Order

### Người Mới Bắt Đầu (Beginners)
1. [SUMMARY_VI.md](SUMMARY_VI.md) hoặc [NEW_FEATURES.md](NEW_FEATURES.md) - Đọc overview
2. [QUICK_START.md](QUICK_START.md) - Xem commands
3. Chạy test: `python test_new_features.py`
4. Chạy experiment đầu tiên

### Người Đã Biết (Advanced)
1. [QUICK_START.md](QUICK_START.md) - Xem commands mới
2. [NEW_FEATURES.md](NEW_FEATURES.md) - Technical details
3. Chạy thử với `--reasoning --meta-prompt`

### Troubleshooting
1. [FIXES.md](FIXES.md) hoặc [TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md)
2. Check test results
3. Review error logs

---

## 📝 Quick Examples

### Example 1: Basic Usage
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10
```
**Docs**: [QUICK_START.md](QUICK_START.md)

### Example 2: With Reasoning
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --reasoning
```
**Docs**: [NEW_FEATURES.md](NEW_FEATURES.md) - Feature 1

### Example 3: With Meta-Prompting
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --meta-prompt
```
**Docs**: [NEW_FEATURES.md](NEW_FEATURES.md) - Feature 2

### Example 4: Full Package
```bash
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 20 --reasoning --meta-prompt
```
**Docs**: [SUMMARY_VI.md](SUMMARY_VI.md) - Example 3

---

## 🔗 External Links

- **Paper**: "Nicer than Human" (ICWSM 2025)
- **Main README**: [../README.md](../README.md)
- **Test Scripts**: 
  - `../test_fixes.py`
  - `../test_new_features.py`

---

## ❓ FAQ - Which Doc Should I Read?

**Q: Tôi mới hoàn toàn, nên đọc gì?**
A: [SUMMARY_VI.md](SUMMARY_VI.md) - Đầy đủ nhất bằng tiếng Việt

**Q: I want technical details in English?**
A: [NEW_FEATURES.md](NEW_FEATURES.md) - Comprehensive technical guide

**Q: Chỉ muốn xem commands?**
A: [QUICK_START.md](QUICK_START.md) - Quick reference

**Q: Làm sao biết bug gì đã fix?**
A: [FIXES.md](FIXES.md) hoặc [TOM_TAT_SUA_LOI.md](TOM_TAT_SUA_LOI.md)

**Q: Có example code không?**
A: [NEW_FEATURES.md](NEW_FEATURES.md) - Section "Phân Tích Kết Quả"

---

## 📌 File Descriptions

### SUMMARY_VI.md (⭐ RECOMMENDED)
- **Language**: Vietnamese
- **Length**: ~280 lines
- **Content**: 
  - Overview of all features
  - Reasoning extraction guide
  - Meta-prompting guide
  - Examples
  - FAQ
  - Tips & Tricks
- **Best for**: Vietnamese speakers wanting complete understanding

### NEW_FEATURES.md
- **Language**: English
- **Length**: ~350 lines
- **Content**:
  - Technical implementation details
  - Reasoning extraction
  - Meta-prompting validation
  - Python analysis scripts
  - Comparison with "Nicer than Human" paper
- **Best for**: Technical deep-dive, English speakers

### QUICK_START.md
- **Language**: Vietnamese + English
- **Length**: ~200 lines
- **Content**:
  - 10 common commands
  - Game comparisons
  - Output format examples
  - Troubleshooting table
- **Best for**: Quick reference, copy-paste commands

### FIXES.md
- **Language**: English
- **Length**: ~300 lines
- **Content**:
  - Detailed bug fixes
  - Before/after comparisons
  - Performance metrics
  - Troubleshooting guide
- **Best for**: Understanding what was fixed

### TOM_TAT_SUA_LOI.md
- **Language**: Vietnamese
- **Length**: ~250 lines
- **Content**:
  - Bug fixes explained in Vietnamese
  - Examples
  - Performance improvements
- **Best for**: Vietnamese speakers wanting to understand fixes

---

**Quay lại**: [Main README](../README.md)

