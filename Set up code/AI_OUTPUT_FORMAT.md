# 🤖 AI GRADING OUTPUT FORMAT SPECIFICATION

## 📋 MỤC ĐÍCH
Document này định nghĩa **format đầu ra chuẩn** mà AI model (Google Gemini) phải tuân thủ khi chấm điểm bài viết IELTS Writing Task 2.

---

## 📊 JSON SCHEMA DEFINITION

### **Cấu trúc tổng quan (Flat structure - Không nested)**

```json
{
  "taskResponseScore": number,      // Điểm Task Response (0-9, bước 0.5)
  "coherenceScore": number,         // Điểm Coherence & Cohesion (0-9, bước 0.5)
  "lexicalScore": number,           // Điểm Lexical Resource (0-9, bước 0.5)
  "grammarScore": number,           // Điểm Grammar (0-9, bước 0.5)
  "overallBand": number,            // Điểm tổng (0-9, bước 0.5)
  "errors": [                       // Mảng các lỗi phát hiện
    {
      "startIndex": number,         // Vị trí bắt đầu lỗi (character index)
      "endIndex": number,           // Vị trí kết thúc lỗi (character index)
      "category": string,           // Loại lỗi: GRAMMAR | VOCABULARY | COHERENCE | TASK_RESPONSE | SPELLING | PUNCTUATION
      "originalText": string,       // Đoạn text bị lỗi (copy từ bài viết)
      "suggestion": string,         // Gợi ý sửa lỗi
      "explanation": string,        // Giải thích lỗi bằng tiếng Việt
      "severity": string            // Mức độ nghiêm trọng: low | medium | high
    }
  ],
  "generalFeedback": string,        // Nhận xét chung (tiếng Việt)
  "strengths": string,              // Điểm mạnh của bài viết (tiếng Việt)
  "improvements": string            // Gợi ý cải thiện (tiếng Việt)
}
```

---

## ✅ VALIDATION RULES

### **1. Scores (taskResponseScore, coherenceScore, lexicalScore, grammarScore, overallBand)**

- **Type:** `number`
- **Range:** `0 - 9`
- **Increment:** `0.5` (các giá trị hợp lệ: 0, 0.5, 1.0, 1.5, 2.0, ..., 8.5, 9.0)
- **Required:** Yes
- **Examples:**
  ```json
  ✅ "taskResponseScore": 6.5
  ✅ "coherenceScore": 7.0
  ❌ "lexicalScore": 6.75    // Không hợp lệ (phải bước 0.5)
  ❌ "grammarScore": 10.0    // Vượt quá 9.0
  ❌ "overallBand": "6.5"    // Phải là number, không phải string
  ```

### **2. Errors Array**

- **Type:** `Array<ErrorObject>`
- **Required:** No (có thể là mảng rỗng `[]` nếu không có lỗi)
- **Max items:** Không giới hạn (nhưng khuyến nghị < 50 errors cho trải nghiệm tốt)

#### **2.1. startIndex & endIndex**

- **Type:** `number` (integer)
- **Range:** `>= 0`
- **Rule:** `endIndex > startIndex`
- **Cách tính:** Character index (bắt đầu từ 0) trong `essayContent` string
  ```javascript
  const essay = "Technology is changing the world.";
  //             0123456789...
  // Ví dụ: "Technology" → startIndex: 0, endIndex: 10
  ```

#### **2.2. category**

- **Type:** `string` (enum)
- **Allowed values:**
  - `"GRAMMAR"` - Lỗi ngữ pháp
  - `"VOCABULARY"` - Lỗi từ vựng (sai nghĩa, word choice)
  - `"COHERENCE"` - Lỗi mạch lạc, liên kết ý
  - `"TASK_RESPONSE"` - Lỗi không trả lời đúng đề
  - `"SPELLING"` - Lỗi chính tả
  - `"PUNCTUATION"` - Lỗi dấu câu
- **Required:** Yes
- **Examples:**
  ```json
  ✅ "category": "GRAMMAR"
  ❌ "category": "grammar"        // Phải UPPERCASE
  ❌ "category": "WORD_CHOICE"    // Không có trong enum (dùng VOCABULARY)
  ```

#### **2.3. originalText**

- **Type:** `string`
- **Required:** Yes
- **Rule:** Phải khớp chính xác với đoạn text trong bài viết từ `startIndex` đến `endIndex`
- **Examples:**
  ```json
  // Essay: "I goes to school every day."
  // Error at "goes" (index 2-6)
  ✅ "originalText": "goes"
  ❌ "originalText": "go"          // Không khớp với text gốc
  ```

#### **2.4. suggestion**

- **Type:** `string`
- **Required:** Yes
- **Rule:** Đưa ra text sửa lỗi, có thể là:
  - Từ/cụm từ thay thế
  - Cấu trúc câu sửa lại
  - Dấu câu đúng
- **Examples:**
  ```json
  ✅ "suggestion": "go"
  ✅ "suggestion": "in the younger generation"
  ✅ "suggestion": "However,"
  ```

#### **2.5. explanation**

- **Type:** `string`
- **Required:** Yes
- **Language:** Tiếng Việt
- **Max length:** 500 characters (khuyến nghị)
- **Content:** Giải thích rõ ràng tại sao bị lỗi và cách sửa
- **Examples:**
  ```json
  ✅ "explanation": "Chủ ngữ 'I' là ngôi thứ nhất số ít, động từ phải dùng 'go' không chia thêm 's'."
  ❌ "explanation": "Wrong verb form"  // Quá ngắn, không rõ ràng
  ```

#### **2.6. severity**

- **Type:** `string` (enum)
- **Allowed values:**
  - `"low"` - Lỗi nhỏ, không ảnh hưởng nhiều đến điểm
  - `"medium"` - Lỗi trung bình, ảnh hưởng đến điểm
  - `"high"` - Lỗi nghiêm trọng, ảnh hưởng lớn đến điểm
- **Required:** No (default: `"medium"`)
- **Case:** **lowercase** (quan trọng!)
- **Examples:**
  ```json
  ✅ "severity": "low"
  ✅ "severity": "medium"
  ✅ "severity": "high"
  ❌ "severity": "LOW"       // Phải lowercase
  ❌ "severity": "critical"  // Không có trong enum
  ```

### **3. Feedback Fields (generalFeedback, strengths, improvements)**

- **Type:** `string`
- **Required:** No (nhưng khuyến nghị có để tăng chất lượng feedback)
- **Language:** Tiếng Việt
- **Max length:**
  - `generalFeedback`: 1000 characters
  - `strengths`: 500 characters
  - `improvements`: 500 characters
- **Content:**
  - `generalFeedback`: Nhận xét tổng quan về bài viết
  - `strengths`: Điểm mạnh cụ thể (ví dụ: từ vựng tốt, cấu trúc rõ ràng)
  - `improvements`: Gợi ý cải thiện cụ thể (ví dụ: cần luyện ngữ pháp X, thêm ví dụ)

---

## 📚 FULL EXAMPLES

### **Example 1: Bài viết tốt (Band 7.5+) với ít lỗi**

```json
{
  "taskResponseScore": 8.0,
  "coherenceScore": 7.5,
  "lexicalScore": 8.0,
  "grammarScore": 7.5,
  "overallBand": 7.5,
  "errors": [
    {
      "startIndex": 245,
      "endIndex": 253,
      "category": "VOCABULARY",
      "originalText": "very big",
      "suggestion": "substantial",
      "explanation": "Trong văn phong học thuật, nên dùng từ vựng chính thức hơn như 'substantial', 'significant' thay vì 'very big'.",
      "severity": "low"
    }
  ],
  "generalFeedback": "Bài viết rất tốt với luận điểm rõ ràng và ví dụ cụ thể. Cấu trúc bài chặt chẽ, sử dụng linking words hiệu quả.",
  "strengths": "Từ vựng phong phú với các collocations tốt như 'mitigate the impact', 'sustainable development'. Ngữ pháp chính xác với cấu trúc câu phức đa dạng.",
  "improvements": "Có thể cải thiện thêm bằng cách sử dụng từ vựng học thuật hơn thay vì các từ đơn giản như 'very big', 'a lot of'."
}
```

### **Example 2: Bài viết trung bình (Band 6.0) với nhiều lỗi**

```json
{
  "taskResponseScore": 6.0,
  "coherenceScore": 6.0,
  "lexicalScore": 6.0,
  "grammarScore": 5.5,
  "overallBand": 6.0,
  "errors": [
    {
      "startIndex": 45,
      "endIndex": 64,
      "category": "GRAMMAR",
      "originalText": "in young generation",
      "suggestion": "among the younger generation",
      "explanation": "Cần sử dụng giới từ 'among' khi nói về một tập thể lớn. Mạo từ 'the' là bắt buộc trước cụm danh từ cụ thể 'younger generation'.",
      "severity": "medium"
    },
    {
      "startIndex": 152,
      "endIndex": 173,
      "category": "VOCABULARY",
      "originalText": "earn bread and butter",
      "suggestion": "make a living",
      "explanation": "Thành ngữ 'earn bread and butter' mang sắc thái quá thân mật (informal) cho một bài luận học thuật (IELTS Writing). Hãy dùng các cụm từ trung lập hơn như 'make a living' hoặc 'earn an income'.",
      "severity": "low"
    },
    {
      "startIndex": 310,
      "endIndex": 317,
      "category": "SPELLING",
      "originalText": "goverment",
      "suggestion": "government",
      "explanation": "Lỗi chính tả: 'goverment' → 'government' (có chữ 'n' giữa 'r' và 'm').",
      "severity": "high"
    },
    {
      "startIndex": 420,
      "endIndex": 427,
      "category": "GRAMMAR",
      "originalText": "was many",
      "suggestion": "were many",
      "explanation": "Chủ ngữ 'many problems' là số nhiều, cần dùng động từ 'were' thay vì 'was'.",
      "severity": "high"
    },
    {
      "startIndex": 550,
      "endIndex": 570,
      "category": "COHERENCE",
      "originalText": "On the other hand,",
      "suggestion": "However,",
      "explanation": "Linking word 'On the other hand' dùng để đối lập hai lựa chọn ngang bằng nhau. Trong ngữ cảnh này nên dùng 'However' hoặc 'Nevertheless' để nối ý.",
      "severity": "medium"
    }
  ],
  "generalFeedback": "Bài viết đã giải quyết được yêu cầu cơ bản của đề bài và đưa ra được một số luận điểm rõ ràng. Tuy nhiên, văn phong đôi chỗ còn thiếu tính học thuật và mắc một số lỗi ngữ pháp cơ bản về chia động từ và giới từ.",
  "strengths": "Cấu trúc bài viết rõ ràng, có chia đoạn hợp lý. Đã sử dụng được một số từ vựng tốt như 'unavailability', 'juvenile delinquency'.",
  "improvements": "Cần kiểm tra kỹ sự hòa hợp giữa chủ ngữ và động từ (Subject-Verb Agreement). Cố gắng tránh các idiom dùng trong văn nói hằng ngày. Luyện tập chính tả các từ phổ biến như 'government', 'environment'."
}
```

### **Example 3: Bài viết yếu (Band 5.0) với nhiều lỗi nghiêm trọng**

```json
{
  "taskResponseScore": 5.0,
  "coherenceScore": 5.0,
  "lexicalScore": 5.5,
  "grammarScore": 4.5,
  "overallBand": 5.0,
  "errors": [
    {
      "startIndex": 0,
      "endIndex": 50,
      "category": "TASK_RESPONSE",
      "originalText": "Nowadays, many people use technology every day.",
      "suggestion": "In my opinion, the advantages of remote work outweigh the disadvantages because...",
      "explanation": "Câu mở đầu chưa giới thiệu đề bài cụ thể. Với đề 'Discuss advantages and disadvantages of remote work', bạn cần statement rõ ràng về quan điểm của mình ngay từ đầu.",
      "severity": "high"
    },
    {
      "startIndex": 120,
      "endIndex": 135,
      "category": "GRAMMAR",
      "originalText": "peoples is happy",
      "suggestion": "people are happy",
      "explanation": "Lỗi nghiêm trọng: 'people' là danh từ số nhiều không thêm 's', và phải dùng 'are' không phải 'is'.",
      "severity": "high"
    }
  ],
  "generalFeedback": "Bài viết còn yếu về mặt nội dung và ngữ pháp. Chưa trả lời đúng yêu cầu đề bài. Mắc nhiều lỗi ngữ pháp cơ bản về chia động từ và danh từ số nhiều/số ít.",
  "strengths": "Có cố gắng viết đủ số từ yêu cầu. Ý tưởng có tiềm năng nhưng cần phát triển rõ ràng hơn.",
  "improvements": "Cần học kỹ cấu trúc bài IELTS Writing Task 2 (introduction, body paragraphs, conclusion). Luyện tập ngữ pháp cơ bản về subject-verb agreement và plural nouns. Đọc đề bài cẩn thận và đảm bảo trả lời đúng câu hỏi."
}
```

### **Example 4: Bài viết hoàn hảo (Band 9.0) không có lỗi**

```json
{
  "taskResponseScore": 9.0,
  "coherenceScore": 9.0,
  "lexicalScore": 9.0,
  "grammarScore": 9.0,
  "overallBand": 9.0,
  "errors": [],
  "generalFeedback": "Bài viết xuất sắc với luận điểm sâu sắc, ví dụ cụ thể và thuyết phục. Ngôn ngữ học thuật cao, không có lỗi ngữ pháp hay từ vựng. Cấu trúc hoàn hảo với sự liên kết mạch lạc giữa các ý.",
  "strengths": "Từ vựng phức tạp và chính xác với các collocations như 'mitigate adverse effects', 'pervasive influence', 'sustainable paradigm'. Cấu trúc câu đa dạng với mix của simple, compound và complex sentences. Linking words được sử dụng tinh tế và tự nhiên.",
  "improvements": "Bài viết đã ở mức xuất sắc. Để duy trì trình độ này, hãy tiếp tục đọc nhiều tài liệu học thuật và luyện tập thường xuyên."
}
```

---

## 🎯 TYPESCRIPT TYPE DEFINITION

Để tham khảo khi code backend:

```typescript
// Backend TypeScript types
export enum ErrorCategory {
  GRAMMAR = 'GRAMMAR',
  VOCABULARY = 'VOCABULARY',
  COHERENCE = 'COHERENCE',
  TASK_RESPONSE = 'TASK_RESPONSE',
  SPELLING = 'SPELLING',
  PUNCTUATION = 'PUNCTUATION',
}

export enum ErrorSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
}

export interface AIError {
  startIndex: number;
  endIndex: number;
  category: ErrorCategory;
  originalText: string;
  suggestion: string;
  explanation: string;
  severity: ErrorSeverity;
}

export interface AIGradingOutput {
  taskResponseScore: number;      // 0-9, step 0.5
  coherenceScore: number;         // 0-9, step 0.5
  lexicalScore: number;           // 0-9, step 0.5
  grammarScore: number;           // 0-9, step 0.5
  overallBand: number;            // 0-9, step 0.5
  errors: AIError[];
  generalFeedback?: string;
  strengths?: string;
  improvements?: string;
}
```

---

## 📝 PROMPT TEMPLATE CHO GEMINI

Sử dụng prompt sau để hướng dẫn Gemini tạo đúng format:

```
Bạn là một giám khảo IELTS Writing chuyên nghiệp. Nhiệm vụ của bạn là chấm điểm bài viết IELTS Writing Task 2 và đưa ra feedback chi tiết.

**ĐỀ BÀI:**
{question_prompt}

**BÀI VIẾT CỦA HỌC VIÊN:**
{essay_content}

**YÊU CẦU:**
1. Chấm điểm theo 4 tiêu chí IELTS: Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy (thang điểm 0-9, bước 0.5)
2. Tính điểm tổng overallBand (trung bình 4 điểm trên)
3. Phát hiện các lỗi trong bài viết (ngữ pháp, từ vựng, chính tả, mạch lạc, v.v.)
4. Đưa ra feedback bằng tiếng Việt

**OUTPUT FORMAT (BẮT BUỘC):**
Trả về ĐÚNG JSON format sau (không thêm text hay explanation khác):

{
  "taskResponseScore": <number 0-9, bước 0.5>,
  "coherenceScore": <number 0-9, bước 0.5>,
  "lexicalScore": <number 0-9, bước 0.5>,
  "grammarScore": <number 0-9, bước 0.5>,
  "overallBand": <number 0-9, bước 0.5>,
  "errors": [
    {
      "startIndex": <số nguyên - vị trí ký tự bắt đầu lỗi>,
      "endIndex": <số nguyên - vị trí ký tự kết thúc lỗi>,
      "category": <string - một trong: GRAMMAR | VOCABULARY | COHERENCE | TASK_RESPONSE | SPELLING | PUNCTUATION>,
      "originalText": <string - đoạn text bị lỗi>,
      "suggestion": <string - gợi ý sửa lỗi>,
      "explanation": <string - giải thích bằng tiếng Việt>,
      "severity": <string - một trong: low | medium | high (PHẢI LOWERCASE)>
    }
  ],
  "generalFeedback": <string - nhận xét chung bằng tiếng Việt>,
  "strengths": <string - điểm mạnh bằng tiếng Việt>,
  "improvements": <string - gợi ý cải thiện bằng tiếng Việt>
}

**LƯU Ý QUAN TRỌNG:**
- Tất cả scores phải là NUMBER, không phải string
- category phải UPPERCASE: "GRAMMAR" không phải "grammar"
- severity phải lowercase: "low" không phải "LOW"
- startIndex và endIndex tính từ 0, theo vị trí ký tự trong essay_content
- Nếu không có lỗi, errors = []
- Tất cả feedback phải bằng tiếng Việt
- Chỉ trả về JSON, không thêm text giải thích nào khác
```

---

## 🔍 VALIDATION CHECKLIST

Trước khi lưu output vào database, validate:

```typescript
// Validation function example
function validateAIOutput(output: any): boolean {
  // 1. Check required fields
  if (!output.taskResponseScore || !output.coherenceScore ||
      !output.lexicalScore || !output.grammarScore || !output.overallBand) {
    return false;
  }

  // 2. Check score range và increment
  const scores = [
    output.taskResponseScore,
    output.coherenceScore,
    output.lexicalScore,
    output.grammarScore,
    output.overallBand
  ];

  for (const score of scores) {
    if (typeof score !== 'number' || score < 0 || score > 9) {
      return false;
    }
    // Check bước 0.5
    if ((score * 10) % 5 !== 0) {
      return false;
    }
  }

  // 3. Check errors array
  if (!Array.isArray(output.errors)) {
    return false;
  }

  // 4. Validate each error
  for (const error of output.errors) {
    if (error.endIndex <= error.startIndex) {
      return false;
    }
    if (!['GRAMMAR', 'VOCABULARY', 'COHERENCE', 'TASK_RESPONSE', 'SPELLING', 'PUNCTUATION'].includes(error.category)) {
      return false;
    }
    if (!['low', 'medium', 'high'].includes(error.severity)) {
      return false;
    }
  }

  return true;
}
```

---

## 🚨 COMMON MISTAKES TO AVOID

### ❌ Sai format:
```json
{
  "scores": {                          // ← KHÔNG nested
    "taskResponseScore": 6.5
  },
  "severity": "MEDIUM"                 // ← Phải lowercase "medium"
}
```

### ✅ Đúng format:
```json
{
  "taskResponseScore": 6.5,            // ← Flat structure
  "severity": "medium"                 // ← lowercase
}
```

---

## 📊 SUMMARY

| Field | Type | Range | Required | Format |
|-------|------|-------|----------|--------|
| taskResponseScore | number | 0-9, step 0.5 | ✅ | `6.5` |
| coherenceScore | number | 0-9, step 0.5 | ✅ | `7.0` |
| lexicalScore | number | 0-9, step 0.5 | ✅ | `6.5` |
| grammarScore | number | 0-9, step 0.5 | ✅ | `6.0` |
| overallBand | number | 0-9, step 0.5 | ✅ | `6.5` |
| errors | Array | - | ❌ | `[...]` hoặc `[]` |
| errors[].category | string | enum | ✅ | `"GRAMMAR"` (uppercase) |
| errors[].severity | string | enum | ✅ | `"medium"` (lowercase) |
| generalFeedback | string | - | ❌ | Tiếng Việt |
| strengths | string | - | ❌ | Tiếng Việt |
| improvements | string | - | ❌ | Tiếng Việt |

---

## 📚 REFERENCE

- Backend Schema: `backend/src/schemas/submission.schema.ts`
- Enums Definition: `backend/src/common/enums/index.ts`
- Transform Utility: `backend/src/ai/utils/transform-ai-output.ts` (sẽ tạo)

---

**Document Version:** 1.0
**Last Updated:** March 11, 2026
**Author:** IELTS Writing Platform Team
