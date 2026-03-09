#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════
IELTS Writing Task 2 - Dataset Generator với Groq API (Llama 3.3)
═══════════════════════════════════════════════════════════════════════════

Script này tạo dataset fine-tuning JSONL từ CSV bằng cách:
1. Gọi Groq API (Llama 3.3) để chấm bài IELTS
2. Post-process để FIX TỌA ĐỘ ký tự (startIndex/endIndex) bằng Python
3. Lưu thành format ChatML chuẩn cho fine-tuning

Author: Senior AI Engineer
Date: March 12, 2026
Version: 1.0
═══════════════════════════════════════════════════════════════════════════
"""

import os
import json
import time
import pandas as pd
from groq import Groq
from tqdm import tqdm
from typing import Dict, List, Any, Optional

# ═══════════════════════════════════════════════════════════════════════════
# 📋 CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

# Groq API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Set environment variable
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.1
MAX_TOKENS = 4096

# Batch Configuration (Chọn khoảng dòng muốn chạy)
START_INDEX = 0      # Dòng bắt đầu (0-indexed)
END_INDEX = 10       # Dòng kết thúc (exclusive) - Chỉnh số này để chạy nhiều hơn

# File Paths
INPUT_CSV = "train_dataset.csv"
OUTPUT_JSONL = f"dataset_batch_{START_INDEX}_to_{END_INDEX}_fixed.jsonl"

# Rate Limiting
SLEEP_BETWEEN_REQUESTS = 2.5  # seconds

# ═══════════════════════════════════════════════════════════════════════════
# 🎯 SYSTEM PROMPT (Đã tối ưu để AI chỉ trích xuất originalText chính xác)
# ═══════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """Bạn là một giám khảo IELTS Writing chuyên nghiệp với hơn 10 năm kinh nghiệm. Nhiệm vụ của bạn là chấm điểm bài viết IELTS Writing Task 2 theo đúng tiêu chuẩn IELTS và đưa ra feedback chi tiết, xây dựng.

📊 YÊU CẦU CHẤM ĐIỂM
1. Task Response (TR): Đánh giá mức độ trả lời đúng đề, phát triển ý tưởng
2. Coherence & Cohesion (CC): Đánh giá tính mạch lạc, liên kết ý
3. Lexical Resource (LR): Đánh giá từ vựng, collocations, word choice
4. Grammatical Range & Accuracy (GRA): Đánh giá cấu trúc ngữ pháp, độ chính xác

Thang điểm: 0 - 9 (bước 0.5)

🎯 BAND DESCRIPTORS (Hướng dẫn chấm điểm):
- Band 5.0-5.5: Nhiều lỗi grammar/vocab, ý tưởng chưa phát triển đầy đủ (8-12 errors)
- Band 6.0-6.5: Có lỗi nhưng không ảnh hưởng nhiều đến hiểu, trả lời đề tương đối tốt (5-8 errors)
- Band 7.0-7.5: Ít lỗi, từ vựng tốt, ý tưởng rõ ràng (3-5 errors)
- Band 8.0+: Rất ít lỗi, từ vựng sophisticated, mạch lạc xuất sắc (0-2 errors)

📝 ERROR CATEGORIES (Phân loại lỗi):
- GRAMMAR: Subject-verb agreement, tense, articles, prepositions, sentence structure
- VOCABULARY: Word choice, collocation, spelling, register/formality
- COHERENCE: Linking words, pronoun reference, paragraph organization, logical flow
- TASK_RESPONSE: Off-topic, irrelevant examples, underdeveloped arguments

⚠️ SEVERITY LEVELS (Mức độ nghiêm trọng):
- "minor": Lỗi nhỏ, không ảnh hưởng comprehension (VD: thiếu article, lỗi spelling nhỏ)
- "moderate": Ảnh hưởng một phần đến clarity (VD: subject-verb agreement, wrong preposition)
- "critical": Làm câu khó hiểu hoặc sai nghĩa (VD: missing verb, wrong word order)

🎯 OUTPUT FORMAT (BẮT BUỘC)
Bạn PHẢI trả về ĐÚNG JSON format dưới đây:
{
  "taskResponseScore": 6.5,
  "coherenceScore": 6.0,
  "lexicalScore": 6.5,
  "grammarScore": 6.0,
  "overallBand": 6.0,
  "errors": [
    {
      "startIndex": 0,
      "endIndex": 0,
      "category": "GRAMMAR",
      "originalText": "in young generation",
      "suggestion": "among the younger generation",
      "explanation": "Cần sử dụng giới từ 'among' khi nói về một tập thể lớn. Mạo từ 'the' là bắt buộc trước cụm danh từ cụ thể 'younger generation'.",
      "severity": "moderate"
    },
    {
      "startIndex": 0,
      "endIndex": 0,
      "category": "VOCABULARY",
      "originalText": "very good",
      "suggestion": "highly beneficial",
      "explanation": "Để đạt band cao, nên dùng từ vựng học thuật như 'highly beneficial' thay vì 'very good'.",
      "severity": "minor"
    }
  ],
  "generalFeedback": "Bài viết của bạn đã giải quyết được yêu cầu cơ bản của đề bài và thể hiện khả năng diễn đạt ở mức trung bình khá. Tuy nhiên, còn một số lỗi ngữ pháp và từ vựng cần cải thiện để đạt band cao hơn.",
  "strengths": "Cấu trúc bài viết rõ ràng với phần mở bài, thân bài và kết luận đầy đủ. Bạn đã trả lời được cả hai khía cạnh của đề bài và đưa ra ví dụ minh họa cụ thể.",
  "improvements": "Cần chú ý sự hòa hợp chủ ngữ - động từ (subject-verb agreement). Nên mở rộng vốn từ vựng học thuật để thay thế các cụm từ đơn giản. Sử dụng thêm linking words để tăng tính mạch lạc."
}

⚠️ QUY TẮC BẮT BUỘC:
1. Giá trị "startIndex" và "endIndex" BẠN CỨ ĐIỀN LÀ 0 (Python sẽ tự động tính sau).
2. "originalText" PHẢI LÀ TRÍCH ĐOẠN ĐƯỢC COPY CHÍNH XÁC 100% TỪ BÀI VIẾT. KHÔNG được tự ý sửa lỗi chính tả, thêm/bớt dấu cách, hoặc đổi in hoa/thường.
3. "severity" CHỈ được dùng 3 giá trị: "minor", "moderate", "critical" (viết thường, KHÔNG dùng "medium").
4. "category" CHỈ được dùng 4 giá trị: "GRAMMAR", "VOCABULARY", "COHERENCE", "TASK_RESPONSE" (viết HOA).
5. Số lượng errors phải HỢP LÝ với band score (Band 5.0: 8-12 lỗi, Band 6.0: 5-8 lỗi, Band 7.0+: 2-5 lỗi).
6. "overallBand" là trung bình của 4 scores, làm tròn xuống nếu .25 hoặc .75 (VD: 6.25 → 6.0, 6.75 → 6.5).
7. Toàn bộ "explanation", "generalFeedback", "strengths", "improvements" phải viết bằng TIẾNG VIỆT."""


# ═══════════════════════════════════════════════════════════════════════════
# 🔧 CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def post_process_coordinates(ai_json: Dict[str, Any], essay_text: str) -> Dict[str, Any]:
    """
    🎯 HÀM POST-PROCESS QUAN TRỌNG NHẤT

    LLM rất kém trong việc đếm index ký tự, do đó hàm này sẽ:
    1. Lấy `originalText` từ AI output (AI chỉ cần trích xuất đúng cụm từ sai)
    2. Dùng Python `str.find()` để tìm vị trí thực tế trong essay
    3. Ghi đè `startIndex` và `endIndex` chính xác
    4. Loại bỏ các errors mà AI bịa ra text không có trong bài (hallucination)

    Args:
        ai_json: JSON output từ LLM
        essay_text: Nội dung bài viết gốc

    Returns:
        Dict với tọa độ đã được fix
    """
    if "errors" not in ai_json or not isinstance(ai_json["errors"], list):
        return ai_json

    fixed_errors = []

    for error in ai_json["errors"]:
        original_text = error.get("originalText", "")

        if not original_text:
            # Bỏ qua error không có originalText
            continue

        # Tìm vị trí đầu tiên của originalText trong essay
        start_idx = essay_text.find(original_text)

        if start_idx == -1:
            # ⚠️ HALLUCINATION DETECTED - AI bịa ra text không có trong bài
            # → Bỏ qua error này
            print(f"⚠️  Skipped hallucination: '{original_text[:50]}...'")
            continue

        # Tính endIndex (vị trí sau ký tự cuối cùng)
        end_idx = start_idx + len(original_text)

        # Ghi đè tọa độ chính xác
        error["startIndex"] = start_idx
        error["endIndex"] = end_idx

        fixed_errors.append(error)

    # Cập nhật lại mảng errors
    ai_json["errors"] = fixed_errors

    return ai_json


def call_groq_api(client: Groq, prompt: str, essay: str) -> Optional[Dict[str, Any]]:
    """
    Gọi Groq API để chấm bài IELTS

    Args:
        client: Groq client instance
        prompt: Đề bài IELTS
        essay: Bài viết của học viên

    Returns:
        Dict chứa AI output hoặc None nếu lỗi
    """
    user_message = f"""ĐỀ BÀI:
{prompt}

BÀI VIẾT CỦA HỌC VIÊN:
{essay}

Hãy chấm điểm bài viết trên theo đúng format JSON đã yêu cầu."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            response_format={"type": "json_object"}  # Bắt buộc trả về JSON
        )

        # Parse JSON từ response
        ai_output = response.choices[0].message.content
        ai_json = json.loads(ai_output)

        return ai_json

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return None


def create_chatml_message(prompt: str, essay: str, ai_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tạo message theo format ChatML chuẩn cho fine-tuning

    Format:
    {
        "messages": [
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "{JSON}"}
        ]
    }

    Args:
        prompt: Đề bài IELTS
        essay: Bài viết
        ai_json: JSON đã được post-process

    Returns:
        Dict theo format ChatML
    """
    user_message = f"""ĐỀ BÀI:
{prompt}

BÀI VIẾT CỦA HỌC VIÊN:
{essay}

Hãy chấm điểm bài viết trên theo đúng format JSON đã yêu cầu."""

    # Assistant content phải là JSON string (không phải dict)
    assistant_content = json.dumps(ai_json, ensure_ascii=False, indent=2)

    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": assistant_content}
        ]
    }


def validate_ai_output(ai_json: Dict[str, Any]) -> bool:
    """
    Validate AI output có đầy đủ fields cần thiết

    Args:
        ai_json: JSON từ AI

    Returns:
        True nếu hợp lệ, False nếu thiếu fields
    """
    required_fields = [
        "taskResponseScore",
        "coherenceScore",
        "lexicalScore",
        "grammarScore",
        "overallBand"
    ]

    for field in required_fields:
        if field not in ai_json:
            print(f"❌ Missing required field: {field}")
            return False

    return True


# ═══════════════════════════════════════════════════════════════════════════
# 🚀 MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """
    Main function - Orchestrate toàn bộ pipeline
    """
    print("═" * 80)
    print("  🤖 IELTS DATASET GENERATOR - GROQ API (LLAMA 3.3)")
    print("═" * 80)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. VALIDATE CONFIGURATION
    # ─────────────────────────────────────────────────────────────────────────

    if not GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY environment variable not set!")
        print("   Set it with: export GROQ_API_KEY='your_api_key_here'")
        return

    if not os.path.exists(INPUT_CSV):
        print(f"❌ ERROR: Input file '{INPUT_CSV}' not found!")
        return

    # ─────────────────────────────────────────────────────────────────────────
    # 2. LOAD CSV DATA
    # ─────────────────────────────────────────────────────────────────────────

    print(f"\n📂 Loading CSV: {INPUT_CSV}")
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"✅ Loaded {len(df)} rows")

        # Validate columns
        if "prompt" not in df.columns or "essay" not in df.columns:
            print("❌ ERROR: CSV must have 'prompt' and 'essay' columns!")
            return

    except Exception as e:
        print(f"❌ ERROR loading CSV: {e}")
        return

    # ─────────────────────────────────────────────────────────────────────────
    # 3. SELECT BATCH
    # ─────────────────────────────────────────────────────────────────────────

    # Adjust END_INDEX nếu vượt quá số dòng
    actual_end = min(END_INDEX, len(df))
    batch_df = df.iloc[START_INDEX:actual_end]

    print(f"\n🎯 Processing batch: rows {START_INDEX} to {actual_end} ({len(batch_df)} items)")
    print(f"📤 Output file: {OUTPUT_JSONL}")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. INITIALIZE GROQ CLIENT
    # ─────────────────────────────────────────────────────────────────────────

    print(f"\n🔌 Connecting to Groq API...")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Temperature: {TEMPERATURE}")

    client = Groq(api_key=GROQ_API_KEY)

    # ─────────────────────────────────────────────────────────────────────────
    # 5. PROCESS EACH ROW
    # ─────────────────────────────────────────────────────────────────────────

    results = []
    failed_count = 0

    print(f"\n🚀 Starting generation...\n")

    for idx, row in tqdm(batch_df.iterrows(), total=len(batch_df), desc="Processing"):
        prompt = row["prompt"]
        essay = row["essay"]

        print(f"\n{'─' * 80}")
        print(f"📝 Row {idx + 1}/{len(df)}: Processing...")
        print(f"   Prompt: {prompt[:60]}...")
        print(f"   Essay length: {len(essay)} chars")

        # ─────────────────────────────────────────────────────────────────────
        # 5.1. Call Groq API
        # ─────────────────────────────────────────────────────────────────────

        ai_json = call_groq_api(client, prompt, essay)

        if ai_json is None:
            print(f"❌ Failed to get AI response for row {idx}")
            failed_count += 1
            continue

        # ─────────────────────────────────────────────────────────────────────
        # 5.2. Validate Output
        # ─────────────────────────────────────────────────────────────────────

        if not validate_ai_output(ai_json):
            print(f"❌ Invalid AI output for row {idx}")
            failed_count += 1
            continue

        # ─────────────────────────────────────────────────────────────────────
        # 5.3. POST-PROCESS: Fix Coordinates (QUAN TRỌNG NHẤT!)
        # ─────────────────────────────────────────────────────────────────────

        print(f"🔧 Post-processing coordinates...")
        original_error_count = len(ai_json.get("errors", []))

        ai_json = post_process_coordinates(ai_json, essay)

        fixed_error_count = len(ai_json.get("errors", []))
        removed_count = original_error_count - fixed_error_count

        print(f"   ✅ Fixed {fixed_error_count} errors")
        if removed_count > 0:
            print(f"   ⚠️  Removed {removed_count} hallucinated errors")

        # ─────────────────────────────────────────────────────────────────────
        # 5.4. Create ChatML Message
        # ─────────────────────────────────────────────────────────────────────

        chatml_message = create_chatml_message(prompt, essay, ai_json)
        results.append(chatml_message)

        print(f"   ✅ Row {idx + 1} completed successfully")

        # ─────────────────────────────────────────────────────────────────────
        # 5.5. Rate Limiting
        # ─────────────────────────────────────────────────────────────────────

        if idx < len(batch_df) - 1:  # Không sleep ở dòng cuối
            print(f"   ⏳ Sleeping {SLEEP_BETWEEN_REQUESTS}s to avoid rate limit...")
            time.sleep(SLEEP_BETWEEN_REQUESTS)

    # ─────────────────────────────────────────────────────────────────────────
    # 6. SAVE TO JSONL
    # ─────────────────────────────────────────────────────────────────────────

    print(f"\n{'═' * 80}")
    print(f"💾 Saving results to {OUTPUT_JSONL}...")

    try:
        with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
            for result in results:
                json_line = json.dumps(result, ensure_ascii=False)
                f.write(json_line + "\n")

        print(f"✅ Successfully saved {len(results)} examples to JSONL")

    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return

    # ─────────────────────────────────────────────────────────────────────────
    # 7. SUMMARY
    # ─────────────────────────────────────────────────────────────────────────

    print(f"\n{'═' * 80}")
    print("📊 GENERATION SUMMARY")
    print(f"{'═' * 80}")
    print(f"Total rows processed:  {len(batch_df)}")
    print(f"Successful:           {len(results)} ✅")
    print(f"Failed:               {failed_count} ❌")
    print(f"Success rate:         {len(results)/len(batch_df)*100:.1f}%")
    print(f"\nOutput file:          {OUTPUT_JSONL}")
    print(f"File size:            {os.path.getsize(OUTPUT_JSONL) / 1024:.2f} KB")
    print(f"{'═' * 80}\n")

    # ─────────────────────────────────────────────────────────────────────────
    # 8. PREVIEW FIRST EXAMPLE
    # ─────────────────────────────────────────────────────────────────────────

    if results:
        print("📄 PREVIEW FIRST EXAMPLE:")
        print("─" * 80)
        first_example = results[0]

        # Parse assistant content to show scores
        assistant_json = json.loads(first_example["messages"][2]["content"])

        print(f"Scores:")
        print(f"  - Task Response: {assistant_json['taskResponseScore']}")
        print(f"  - Coherence:     {assistant_json['coherenceScore']}")
        print(f"  - Lexical:       {assistant_json['lexicalScore']}")
        print(f"  - Grammar:       {assistant_json['grammarScore']}")
        print(f"  - Overall Band:  {assistant_json['overallBand']}")
        print(f"\nErrors detected: {len(assistant_json['errors'])}")

        if assistant_json['errors']:
            print(f"\nFirst error example:")
            first_error = assistant_json['errors'][0]
            print(f"  - Position: [{first_error['startIndex']}:{first_error['endIndex']}]")
            print(f"  - Text: '{first_error['originalText']}'")
            print(f"  - Category: {first_error['category']}")
            print(f"  - Suggestion: '{first_error['suggestion']}'")

        print("─" * 80)


# ═══════════════════════════════════════════════════════════════════════════
# 🎯 ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
