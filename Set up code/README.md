# IELTS Writing Task 2 E-Learning Platform - Backend

## 📋 Tổng Quan

Backend NestJS cho nền tảng E-learning rèn luyện IELTS Writing Task 2 tích hợp AI chấm chữa tự động.

## 🏗️ Tech Stack

- **Framework**: NestJS
- **Database**: MongoDB (Mongoose ODM)
- **Queue**: BullMQ + Redis
- **AI Engine**: Google Gemini API (MVP) → Mistral 7B (Phase 2)
- **WebSockets**: Socket.io
- **Language**: TypeScript

## 📁 Cấu Trúc Database Schemas

### Core Entities
- **User**: Quản lý người dùng (STUDENT, ADMIN)
- **Topic**: Chủ đề dùng chung để phân loại

### Module 1: Course System
- **Course**: Khóa học liên kết với Topic
- **Lesson**: Bài học với `targetBand`, nhúng videos, vocabularies, grammars

### Module 2: Sample Essays
- **SampleEssay**: Bài mẫu với outline, full essay, và highlight annotations
- **FavoriteEssay**: Lưu bài mẫu yêu thích của học viên

### Module 3: Global Notebook & Flashcards
- **NotebookNote**: Sổ tay nháp tự do
- **FlashcardSet**: Bộ thẻ từ vựng (giống Quizlet), nhúng Flashcards

### Module 4: Practice & AI Engine (Core USP)
- **ExamQuestion**: Đề thi với gợi ý outline
- **Submission**: Bài nộp với trạng thái và `aiResult` embedded document

## 🚀 Cài Đặt & Chạy Dự Án

### Bước 1: Cài đặt dependencies

```bash
cd backend
npm install
```

### Bước 2: Cấu hình môi trường

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Cập nhật các biến môi trường:

```env
NODE_ENV=development
PORT=3000

MONGODB_URI=mongodb://localhost:27017/ielts-writing-db

REDIS_HOST=localhost
REDIS_PORT=6379

GEMINI_API_KEY=your_actual_gemini_api_key
```

### Bước 3: Chạy MongoDB & Redis

**Sử dụng Docker (Recommended):**

```bash
# MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Redis
docker run -d -p 6379:6379 --name redis redis:latest
```

**Hoặc cài đặt local:**
- MongoDB: https://www.mongodb.com/try/download/community
- Redis: https://redis.io/download

### Bước 4: Chạy ứng dụng

```bash
# Development mode
npm run start:dev

# Production build
npm run build
npm run start:prod
```

Server sẽ chạy tại: `http://localhost:3000`

## 📊 Database Schema Highlights

### Submission Schema (Core của AI Grading)

```typescript
{
  userId: ObjectId,
  questionId: ObjectId,
  essayContent: string,
  status: 'DRAFT' | 'SUBMITTED' | 'PROCESSING' | 'COMPLETED' | 'FAILED',
  aiResult: {
    taskResponseScore: number,
    coherenceScore: number,
    lexicalScore: number,
    grammarScore: number,
    overallBand: number,
    errors: [{
      startIndex: number,
      endIndex: number,
      category: ErrorCategory,
      originalText: string,
      suggestion: string,
      explanation: string
    }],
    generalFeedback: string
  }
}
```

### Lesson Schema (Embedded Documents)

```typescript
{
  title: string,
  courseId: ObjectId,
  targetBand: 'BAND_5_0' | 'BAND_6_0' | 'BAND_7_PLUS',
  videos: [{ title, videoUrl, duration }],
  vocabularies: [{ word, definition, examples }],
  grammars: [{ title, explanation, examples }]
}
```

## 🎯 Luồng AI Grading (Sẽ Implement ở Bước Tiếp Theo)

1. **Client** → `POST /api/submissions` → Backend lưu DB (status: SUBMITTED)
2. **Backend** → Đẩy Job vào Redis Queue (BullMQ)
3. **AI Worker** → Bốc Job, gọi Gemini API
4. **Backend** → Cập nhật `aiResult` vào Submission (status: COMPLETED)
5. **WebSocket** → Phát sự kiện `submission_status_updated` về Client
6. **Client** → Gọi `GET /api/submissions/:id` → Render UI với highlight errors

## 🔧 Dependency Injection Pattern cho AI

Backend đã được thiết kế để dễ dàng swap giữa Gemini và Mistral:

```typescript
// Sẽ implement ở bước tiếp theo
interface AIGradingService {
  gradeEssay(content: string): Promise<AIResult>;
}

class GeminiGradingService implements AIGradingService { ... }
class MistralGradingService implements AIGradingService { ... }
```

## 📝 Next Steps

**Bước 1 đã hoàn thành:**
✅ Setup NestJS project
✅ Cấu hình Mongoose
✅ Định nghĩa toàn bộ Database Schemas cho 4 modules

**Bước 2 (Sắp tới):**
- Tạo các Module, Controller, Service cho từng feature
- Implement Authentication & Authorization (JWT)
- Setup BullMQ cho AI grading queue
- Implement AI Grading Service với Strategy Pattern

## 📚 Tài Liệu Tham Khảo

- [NestJS Documentation](https://docs.nestjs.com/)
- [Mongoose Documentation](https://mongoosejs.com/)
- [BullMQ Documentation](https://docs.bullmq.io/)
- [Google Gemini API](https://ai.google.dev/)

---

**Tác giả**: Senior Tech Lead & Full-stack Developer
**Dự án**: IELTS Writing Task 2 E-Learning Platform
