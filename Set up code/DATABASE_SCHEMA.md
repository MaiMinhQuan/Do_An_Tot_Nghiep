# IELTS Writing Backend - Database Schema

## Tổng quan
Dự án sử dụng **MongoDB** với **Mongoose ODM** trong **NestJS Framework**.
Database gồm **11 Collections** chính để quản lý hệ thống học IELTS Writing.

---

## 1. Collection: `users`

**Mục đích**: Quản lý tài khoản người dùng (học viên và admin)

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `email` | String | ✓ | ✓ | - | Email đăng nhập |
| `passwordHash` | String | ✓ | ✗ | - | Mật khẩu đã hash (bcrypt) |
| `fullName` | String | ✓ | ✗ | - | Họ tên đầy đủ |
| `role` | Enum | ✓ | ✗ | STUDENT | Role: STUDENT, ADMIN |
| `isActive` | Boolean | ✓ | ✗ | true | Trạng thái tài khoản |
| `avatarUrl` | String | ✗ | ✗ | - | URL ảnh đại diện |
| `lastLoginAt` | Date | ✗ | ✗ | - | Thời điểm đăng nhập cuối |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `email`: unique index
- `role`: index

### Enums:
```typescript
UserRole {
  STUDENT = 'STUDENT',
  ADMIN = 'ADMIN'
}
```

---

## 2. Collection: `topics`

**Mục đích**: Quản lý các chủ đề IELTS Writing (Education, Environment, Technology...)

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `name` | String | ✓ | ✓ | - | Tên chủ đề |
| `slug` | String | ✓ | ✓ | - | URL-friendly slug (auto-generated) |
| `description` | String | ✗ | ✗ | - | Mô tả chủ đề |
| `iconUrl` | String | ✗ | ✗ | - | URL icon |
| `orderIndex` | Number | ✓ | ✗ | 0 | Thứ tự hiển thị |
| `isActive` | Boolean | ✓ | ✗ | true | Trạng thái kích hoạt |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `slug`: unique index
- `orderIndex`: index

### Hooks:
- **Pre-save**: Auto-generate slug từ name (lowercase, replace spaces with hyphens)

---

## 3. Collection: `courses`

**Mục đích**: Quản lý các khóa học IELTS Writing

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `title` | String | ✓ | ✗ | - | Tiêu đề khóa học |
| `description` | String | ✗ | ✗ | - | Mô tả khóa học |
| `topicId` | ObjectId | ✓ | ✗ | - | Reference → `topics._id` |
| `thumbnailUrl` | String | ✗ | ✗ | - | URL ảnh thumbnail |
| `orderIndex` | Number | ✓ | ✗ | 0 | Thứ tự hiển thị |
| `isPublished` | Boolean | ✓ | ✗ | true | Trạng thái xuất bản |
| `totalLessons` | Number | ✓ | ✗ | 0 | Tổng số bài học |
| `instructorName` | String | ✗ | ✗ | - | Tên giảng viên |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `topicId`: index
- `isPublished, orderIndex`: compound index

### Relations:
- **Belongs to**: `topics` (via `topicId`)
- **Has many**: `lessons`

---

## 4. Collection: `lessons`

**Mục đích**: Quản lý các bài học trong khóa học (bao gồm video, từ vựng, ngữ pháp)

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `title` | String | ✓ | ✗ | - | Tiêu đề bài học |
| `courseId` | ObjectId | ✓ | ✗ | - | Reference → `courses._id` |
| `targetBand` | Enum | ✓ | ✗ | - | Target band: BAND_5_0, BAND_6_0, BAND_7_PLUS |
| `description` | String | ✗ | ✗ | - | Mô tả bài học |
| `orderIndex` | Number | ✓ | ✗ | 0 | Thứ tự trong khóa học |
| `isPublished` | Boolean | ✓ | ✗ | true | Trạng thái xuất bản |
| `videos` | Array | ✓ | ✗ | [] | Array of LessonVideo (embedded) |
| `vocabularies` | Array | ✓ | ✗ | [] | Array of LessonVocabulary (embedded) |
| `grammars` | Array | ✓ | ✗ | [] | Array of LessonGrammar (embedded) |
| `notesContent` | String | ✗ | ✗ | - | Rich text/Markdown notes |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Embedded Sub-documents:

#### LessonVideo:
```typescript
{
  title: String (required),
  videoUrl: String (required),
  duration: Number (seconds, optional),
  thumbnailUrl: String (optional)
}
```

#### LessonVocabulary:
```typescript
{
  word: String (required),
  pronunciation: String (optional),
  definition: String (required),
  examples: Array<String> (default: []),
  translation: String (optional, Vietnamese)
}
```

#### LessonGrammar:
```typescript
{
  title: String (required),
  explanation: String (required),
  examples: Array<String> (default: []),
  structure: String (optional, e.g., "Subject + Verb + Object")
}
```

### Indexes:
- `courseId, orderIndex`: compound index
- `targetBand`: index
- `isPublished`: index

### Relations:
- **Belongs to**: `courses` (via `courseId`)

### Enums:
```typescript
TargetBand {
  BAND_5_0 = 'BAND_5_0',
  BAND_6_0 = 'BAND_6_0',
  BAND_7_PLUS = 'BAND_7_PLUS'
}
```

---

## 5. Collection: `sampleessays`

**Mục đích**: Quản lý các bài viết mẫu IELTS Writing với highlight annotations

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `title` | String | ✓ | ✗ | - | Tiêu đề bài mẫu |
| `topicId` | ObjectId | ✓ | ✗ | - | Reference → `topics._id` |
| `questionPrompt` | String | ✓ | ✗ | - | Đề bài IELTS |
| `targetBand` | Enum | ✓ | ✗ | - | Target band score |
| `outlineContent` | String | ✓ | ✗ | - | Dàn ý (markdown/plain text) |
| `fullEssayContent` | String | ✓ | ✗ | - | Bài viết mẫu hoàn chỉnh |
| `highlightAnnotations` | Array | ✓ | ✗ | [] | Array of HighlightAnnotation (embedded) |
| `viewCount` | Number | ✓ | ✗ | 0 | Số lượt xem |
| `favoriteCount` | Number | ✓ | ✗ | 0 | Số lượt yêu thích |
| `isPublished` | Boolean | ✓ | ✗ | true | Trạng thái xuất bản |
| `authorName` | String | ✗ | ✗ | - | Tên tác giả |
| `overallBandScore` | Number | ✗ | ✗ | - | Điểm band tổng (0-9) |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Embedded Sub-document:

#### HighlightAnnotation:
```typescript
{
  startIndex: Number (required),
  endIndex: Number (required),
  highlightType: Enum (required, HighlightType),
  explanation: String (required, tiếng Việt/Anh),
  color: String (optional, hex color code)
}
```

### Indexes:
- `topicId`: index
- `targetBand`: index
- `isPublished`: index
- `favoriteCount`: index (descending, for sorting by popularity)

### Relations:
- **Belongs to**: `topics` (via `topicId`)
- **Has many**: `favoriteessays`

### Enums:
```typescript
HighlightType {
  VOCABULARY = 'VOCABULARY',
  GRAMMAR = 'GRAMMAR',
  STRUCTURE = 'STRUCTURE',
  ARGUMENT = 'ARGUMENT'
}
```

---

## 6. Collection: `favoriteessays`

**Mục đích**: Quản lý bài mẫu yêu thích của học viên (Many-to-Many relationship)

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `userId` | ObjectId | ✓ | ✗ | - | Reference → `users._id` |
| `essayId` | ObjectId | ✓ | ✗ | - | Reference → `sampleessays._id` |
| `personalNote` | String | ✗ | ✗ | - | Ghi chú cá nhân của học viên |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `userId, essayId`: unique compound index
- `userId`: index

### Relations:
- **Belongs to**: `users` (via `userId`)
- **Belongs to**: `sampleessays` (via `essayId`)

---

## 7. Collection: `notebooknotes`

**Mục đích**: Quản lý ghi chú tự do của học viên

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `userId` | ObjectId | ✓ | ✗ | - | Reference → `users._id` |
| `userDraftNote` | String | ✓ | ✗ | - | Nội dung ghi chú (plain text/markdown) |
| `title` | String | ✗ | ✗ | - | Tiêu đề ghi chú (optional) |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `userId, createdAt`: compound index (descending on createdAt)

### Relations:
- **Belongs to**: `users` (via `userId`)

---

## 8. Collection: `flashcardsets`

**Mục đích**: Quản lý bộ flashcard của học viên

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `userId` | ObjectId | ✓ | ✗ | - | Reference → `users._id` |
| `title` | String | ✓ | ✗ | - | Tiêu đề bộ flashcard |
| `description` | String | ✗ | ✗ | - | Mô tả |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `userId`: index

### Relations:
- **Belongs to**: `users` (via `userId`)
- **Has many**: `flashcards`

---

## 9. Collection: `flashcards`

**Mục đích**: Quản lý các flashcard trong bộ (hỗ trợ spaced repetition)

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `setId` | ObjectId | ✓ | ✗ | - | Reference → `flashcardsets._id` |
| `frontContent` | String | ✓ | ✗ | - | Mặt trước (từ vựng/câu hỏi) |
| `backContent` | String | ✓ | ✗ | - | Mặt sau (nghĩa/giải thích) |
| `nextReviewDate` | Date | ✗ | ✗ | - | Ngày ôn tập tiếp theo (spaced repetition) |
| `reviewCount` | Number | ✓ | ✗ | 0 | Số lần đã ôn tập |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `setId`: index
- `nextReviewDate`: index

### Relations:
- **Belongs to**: `flashcardsets` (via `setId`)

---

## 10. Collection: `examquestions`

**Mục đích**: Quản lý ngân hàng đề thi IELTS Writing Task 2

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `title` | String | ✓ | ✗ | - | Tiêu đề đề thi |
| `topicId` | ObjectId | ✗ | ✗ | - | Reference → `topics._id` (optional) |
| `questionPrompt` | String | ✓ | ✗ | - | Đề bài IELTS Writing Task 2 |
| `suggestedOutline` | String | ✗ | ✗ | - | Gợi ý dàn ý (markdown/plain text) |
| `difficultyLevel` | Number | ✓ | ✗ | 0 | Độ khó (1-5) |
| `isPublished` | Boolean | ✓ | ✗ | true | Trạng thái xuất bản |
| `attemptCount` | Number | ✓ | ✗ | 0 | Số lượt làm bài |
| `sourceReference` | String | ✗ | ✗ | - | Nguồn đề thi |
| `tags` | Array | ✓ | ✗ | [] | Tags phân loại (e.g., ["education", "technology"]) |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Indexes:
- `topicId`: index
- `isPublished`: index
- `difficultyLevel`: index
- `tags`: index (array index)

### Relations:
- **Belongs to**: `topics` (via `topicId`, optional)
- **Has many**: `submissions`

---

## 11. Collection: `submissions`

**Mục đích**: Quản lý bài làm của học viên và kết quả chấm AI

### Fields:
| Field | Type | Required | Unique | Default | Description |
|-------|------|----------|--------|---------|-------------|
| `_id` | ObjectId | ✓ | ✓ | Auto | ID tự động |
| `userId` | ObjectId | ✓ | ✗ | - | Reference → `users._id` |
| `questionId` | ObjectId | ✓ | ✗ | - | Reference → `examquestions._id` |
| `essayContent` | String | ✓ | ✗ | - | Nội dung bài viết của học viên |
| `wordCount` | Number | ✗ | ✗ | - | Số từ (auto-calculated) |
| `timeSpentSeconds` | Number | ✗ | ✗ | - | Thời gian làm bài (giây) |
| `status` | Enum | ✓ | ✗ | DRAFT | Status: DRAFT, SUBMITTED, PROCESSING, COMPLETED, FAILED |
| `aiResult` | Object | ✗ | ✗ | - | AIResult (embedded, chỉ có khi COMPLETED) |
| `errorMessage` | String | ✗ | ✗ | - | Lỗi nếu status = FAILED |
| `submittedAt` | Date | ✗ | ✗ | - | Thời điểm nộp bài |
| `attemptNumber` | Number | ✓ | ✗ | 1 | Lần làm thứ mấy |
| `createdAt` | Date | ✓ | ✗ | Auto | Thời điểm tạo |
| `updatedAt` | Date | ✓ | ✗ | Auto | Thời điểm cập nhật |

### Embedded Sub-documents:

#### AIResult:
```typescript
{
  taskResponseScore: Number (required, 0-9),
  coherenceScore: Number (required, 0-9),
  lexicalScore: Number (required, 0-9),
  grammarScore: Number (required, 0-9),
  overallBand: Number (required, 0-9),
  errors: Array<AIError> (default: []),
  generalFeedback: String (optional, tiếng Việt),
  strengths: String (optional),
  improvements: String (optional),
  processedAt: Date (optional)
}
```

#### AIError:
```typescript
{
  startIndex: Number (required),
  endIndex: Number (required),
  category: Enum (required, ErrorCategory),
  originalText: String (required),
  suggestion: String (required),
  explanation: String (required, tiếng Việt),
  severity: String (default: 'medium', values: 'low'|'medium'|'high')
}
```

### Indexes:
- `userId, createdAt`: compound index (descending on createdAt)
- `questionId`: index
- `status`: index
- `userId, questionId, attemptNumber`: compound index

### Relations:
- **Belongs to**: `users` (via `userId`)
- **Belongs to**: `examquestions` (via `questionId`)

### Hooks:
- **Pre-save**: Auto-calculate `wordCount` from `essayContent`

### Enums:
```typescript
SubmissionStatus {
  DRAFT = 'DRAFT',
  SUBMITTED = 'SUBMITTED',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED'
}

ErrorCategory {
  GRAMMAR = 'GRAMMAR',
  VOCABULARY = 'VOCABULARY',
  COHERENCE = 'COHERENCE',
  TASK_RESPONSE = 'TASK_RESPONSE',
  SPELLING = 'SPELLING',
  PUNCTUATION = 'PUNCTUATION'
}
```

---

## Entity Relationship Diagram (ERD)

```
users (1) ──────< (N) submissions
users (1) ──────< (N) favoriteessays
users (1) ──────< (N) notebooknotes
users (1) ──────< (N) flashcardsets

topics (1) ──────< (N) courses
topics (1) ──────< (N) sampleessays
topics (1) ──────< (N) examquestions (optional)

courses (1) ──────< (N) lessons

sampleessays (1) ──────< (N) favoriteessays

flashcardsets (1) ──────< (N) flashcards

examquestions (1) ──────< (N) submissions
```

---

## Tổng kết các Enums

### UserRole
- `STUDENT`: Học viên
- `ADMIN`: Quản trị viên

### TargetBand
- `BAND_5_0`: Target band 5.0
- `BAND_6_0`: Target band 6.0
- `BAND_7_PLUS`: Target band 7.0+

### SubmissionStatus
- `DRAFT`: Bản nháp
- `SUBMITTED`: Đã nộp bài
- `PROCESSING`: Đang xử lý bởi AI
- `COMPLETED`: Đã chấm xong
- `FAILED`: Chấm thất bại

### HighlightType
- `VOCABULARY`: Highlight từ vựng
- `GRAMMAR`: Highlight ngữ pháp
- `STRUCTURE`: Highlight cấu trúc câu
- `ARGUMENT`: Highlight lập luận

### ErrorCategory
- `GRAMMAR`: Lỗi ngữ pháp
- `VOCABULARY`: Lỗi từ vựng
- `COHERENCE`: Lỗi mạch lạc
- `TASK_RESPONSE`: Lỗi trả lời đề bài
- `SPELLING`: Lỗi chính tả
- `PUNCTUATION`: Lỗi dấu câu

### AIProvider
- `GEMINI`: Google Gemini AI
- `MISTRAL`: Mistral AI

---

## Ghi chú kỹ thuật

1. **Timestamps**: Tất cả collections đều có `createdAt` và `updatedAt` (auto-managed by Mongoose)

2. **Indexes**: Được thiết kế để tối ưu query performance cho:
   - Lookup by user
   - Lookup by relationships (topicId, courseId, etc.)
   - Sorting by order, date, popularity

3. **Embedded Documents**:
   - `lessons` chứa arrays của videos, vocabularies, grammars
   - `sampleessays` chứa array của highlightAnnotations
   - `submissions` chứa nested AIResult với array of AIErrors

4. **Pre-save Hooks**:
   - `topics`: Auto-generate slug từ name
   - `submissions`: Auto-calculate wordCount từ essayContent

5. **Unique Constraints**:
   - `users.email`: Unique
   - `topics.name`, `topics.slug`: Unique
   - `favoriteessays`: Unique compound (userId + essayId)

6. **Soft Delete**: Không implement (dùng `isActive`, `isPublished` flags thay thế)

7. **AI Integration**:
   - Collection `submissions` lưu kết quả AI grading
   - Support multi-provider (Gemini, Mistral)
