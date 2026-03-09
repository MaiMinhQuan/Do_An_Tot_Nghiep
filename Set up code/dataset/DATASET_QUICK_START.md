# 🚀 Dataset Generation - Quick Start Guide

**Mục tiêu**: Tạo training dataset từ CSV essays để fine-tune Mistral/Llama model cho AI grading engine.

---

## 📋 Prerequisites

```bash
# 1. Python 3.8+ installed
python --version

# 2. Groq API Key
# Lấy tại: https://console.groq.com/keys
```

---

## ⚡ Quick Start (5 phút)

### Step 1: Setup Environment

```bash
# Tạo virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements-dataset.txt
```

### Step 2: Prepare CSV File

Tạo file `train_dataset.csv` với format:

```csv
prompt,essay
"Some people think...",Nowadays, education is very important for...
"Many people believe...",In modern society, technology has changed...
```

**Yêu cầu**:
- Có đúng 2 cột: `prompt`, `essay`
- Encoding: UTF-8
- No extra spaces trong column names

### Step 3: Configure API Key

Mở `create_dataset_groq.py`, tìm dòng 35:

```python
groq_api_key = "YOUR_GROQ_API_KEY_HERE"  # ← Thay bằng key của bạn
```

### Step 4: Generate Dataset (Batch Processing)

```bash
# Batch 1: Rows 0-10 (test run)
python create_dataset_groq.py

# Kiểm tra output
python validate_dataset.py dataset_batch_0_to_10_fixed.jsonl --stats

# Nếu OK, continue với batch tiếp theo
# Edit START_INDEX và END_INDEX trong script
```

**Workflow:**
```
START_INDEX = 0  → END_INDEX = 10   (rows 0-9)
START_INDEX = 10 → END_INDEX = 20   (rows 10-19)
START_INDEX = 20 → END_INDEX = 30   (rows 20-29)
...
```

---

## 🔍 Validation

### Quick Check

```bash
# Basic validation
python validate_dataset.py dataset_batch_0_to_10_fixed.jsonl

# Verbose (show all errors)
python validate_dataset.py dataset_batch_0_to_10_fixed.jsonl --verbose

# With statistics
python validate_dataset.py dataset_batch_0_to_10_fixed.jsonl --stats
```

### Expected Output

```
═══════════════════════════════════════════════════════════════════════════
📊 VALIDATION SUMMARY
═══════════════════════════════════════════════════════════════════════════
Total lines:    10
Valid:          10 ✅
Invalid:        0 ❌
Success rate:   100.0%

═══════════════════════════════════════════════════════════════════════════
📈 DATASET STATISTICS
═══════════════════════════════════════════════════════════════════════════
📊 Overview:
  Total examples:        10
  Valid examples:        10
  Total errors detected: 45
  Avg errors/essay:      4.50
  Coordinate accuracy:   100.0%

🎯 Band Distribution:
  Band 5.0: ████ 3 (30.0%)
  Band 6.0: ████ 4 (40.0%)
  Band 7.0: ██   2 (20.0%)
  Band 8.0: █    1 (10.0%)
```

**✅ Good signs:**
- ✅ Coordinate accuracy = 100%
- ✅ Band distribution đa dạng (5.0 - 9.0)
- ✅ Error categories balanced (GRAMMAR, VOCABULARY, COHERENCE, TASK_RESPONSE)
- ✅ Avg errors/essay: 3-7 errors (reasonable)

**❌ Warning signs:**
- ❌ Coordinate accuracy < 95% → Check `originalText` extraction
- ❌ Too many "critical" errors → Adjust severity logic
- ❌ Unbalanced bands (all 9.0 or all 5.0) → Review prompts
- ❌ Avg errors > 15 → AI too aggressive, adjust system prompt

---

## 📂 File Structure

```
backend/
├── create_dataset_groq.py           # Main generation script
├── validate_dataset.py              # Validation script
├── requirements-dataset.txt         # Python dependencies
├── DATASET_GENERATOR_GUIDE.txt      # Chi tiết troubleshooting
├── DATASET_QUICK_START.md          # This guide
│
├── train_dataset.csv                # Input CSV (your data)
└── dataset_batch_0_to_10_fixed.jsonl  # Output JSONL (generated)
```

---

## 🎯 Output Format (JSONL / ChatML)

Mỗi dòng trong file `.jsonl`:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "Bạn là trợ lý AI chuyên chấm điểm IELTS Writing Task 2..."
    },
    {
      "role": "user",
      "content": "ĐỀ BÀI: Some people think...\n\nBÀI VIẾT CỦA HỌC VIÊN: Nowadays, education..."
    },
    {
      "role": "assistant",
      "content": "{\"taskResponseScore\":6.0,\"coherenceScore\":5.5,...}"
    }
  ]
}
```

**Key points:**
- 🔹 3 messages: system, user, assistant
- 🔹 Assistant content là JSON string (flat structure, không nested)
- 🔹 Severity: lowercase (`minor`, `moderate`, `critical`)
- 🔹 Category: UPPERCASE (`GRAMMAR`, `VOCABULARY`, `COHERENCE`, `TASK_RESPONSE`)
- 🔹 Coordinates: `startIndex`, `endIndex` (0-based, chính xác 100%)

---

## 🔧 Common Issues

### Issue 1: Rate Limit Error

```
Error 429: Rate limit exceeded
```

**Fix:** Tăng `time.sleep()` trong script (line ~115):

```python
time.sleep(3.0)  # Từ 2.5s → 3.0s
```

### Issue 2: Coordinate Accuracy < 100%

```
Coordinate accuracy: 87.3%
```

**Fix:** Check `originalText` có dấu xuống dòng/tab không:

```python
# In script, line ~88
original_text = error.get('originalText', '').strip()  # ← Add .strip()
```

### Issue 3: JSON Decode Error

```
Error parsing line 5: json.decoder.JSONDecodeError
```

**Fix:** Groq API trả về incomplete JSON, giảm `max_tokens`:

```python
max_tokens=4096,  # Từ 8000 → 4096
```

---

## 🚀 Next Steps

### 1. Generate Full Dataset

```bash
# Script batch processing
for i in {0..100..10}; do
    # Edit START_INDEX và END_INDEX
    python create_dataset_groq.py
    sleep 5
done
```

### 2. Merge All Batches

```bash
# Windows PowerShell
Get-Content dataset_batch_*.jsonl > train_dataset_full.jsonl

# Linux/Mac
cat dataset_batch_*.jsonl > train_dataset_full.jsonl
```

### 3. Validate Final Dataset

```bash
python validate_dataset.py train_dataset_full.jsonl --stats
```

### 4. Fine-tune Model

```bash
# Upload to Hugging Face / Mistral Fine-tuning Platform
# Follow platform-specific instructions
```

### 5. Integrate to Backend

```typescript
// backend/src/ai/services/mistral-grading.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class MistralGradingService {
  async gradeEssay(prompt: string, essay: string) {
    // Call your fine-tuned model endpoint
    const response = await this.mistralClient.chat({
      model: 'your-fine-tuned-model',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: `ĐỀ BÀI: ${prompt}\n\nBÀI VIẾT: ${essay}` }
      ]
    });

    return JSON.parse(response.choices[0].message.content);
  }
}
```

---

## 📞 Support

Chi tiết troubleshooting: Xem `DATASET_GENERATOR_GUIDE.txt`

Format specification: Xem `backend/AI_OUTPUT_FORMAT.md`

---

## ✅ Checklist

Pre-generation:
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements-dataset.txt`)
- [ ] Groq API key configured
- [ ] CSV file prepared (correct format)

Post-generation:
- [ ] All batches generated successfully
- [ ] Validation passed (100% coordinate accuracy)
- [ ] Band distribution diverse (5.0 - 9.0)
- [ ] Error categories balanced
- [ ] Batches merged to single JSONL
- [ ] Ready for fine-tuning upload

---

**Estimated Time:**
- Setup: 5 minutes
- Generate 100 essays (10 batches): ~45 minutes (with 2.5s delay)
- Validation: 2 minutes
- **Total: ~1 hour** for 100 training examples

**Recommended batch size:** 10 rows (balance between safety and efficiency)

**Pro tip:** Chạy batch đầu tiên (0-10), validate kỹ, nếu OK thì mới chạy toàn bộ dataset! 🎯
