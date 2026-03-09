hãy đọc qua schema của dự án rồi hướng dẫn tôi làm các ý sau 1 cách chi tiết (chỉ hướng dẫn, không tự ý tạo và code trực tiếp vào các file):
# 🗺️ ROADMAP PHÁT TRIỂN DỰ ÁN
## IELTS Writing Task 2 E-Learning Platform

---

## ✅ **GIAI ĐOẠN 1: THIẾT LẬP DỰ ÁN & DATABASE SCHEMA**
### Status: **HOÀN THÀNH** ✓

**Đã thực hiện:**
- ✅ Setup NestJS project structure
- ✅ Cấu hình TypeScript, Mongoose, Redis
- ✅ Định nghĩa 11 Database Schemas cho 4 modules
- ✅ Tạo Enums & Common utilities
- ✅ Cấu hình môi trường (.env)

**Kết quả:**
- 11 schemas hoàn chỉnh: User, Topic, Course, Lesson, SampleEssay, FavoriteEssay, NotebookNote, FlashcardSet, Flashcard, ExamQuestion, Submission
- Embedded documents đã được sử dụng đúng chỗ
- Indexes và hooks đã được thiết lập

---

## 🚧 **GIAI ĐOẠN 2: CORE INFRASTRUCTURE & AUTHENTICATION**
### Ước tính: 2-3 giờ

### 2.1. Database Module Setup
- [ ] Tạo `database.module.ts` - Kết nối MongoDB
- [ ] Tạo `database.providers.ts` - Export tất cả Models
- [ ] Test connection với MongoDB

### 2.2. Authentication & Authorization
- [ ] Tạo `auth` module với JWT strategy
- [ ] Implement `AuthService`: register, login, validateUser
- [ ] Implement `AuthController`: POST /api/auth/register, /api/auth/login
- [ ] Tạo `JwtAuthGuard` & `RolesGuard` (STUDENT/ADMIN)
- [ ] Hash password với bcrypt

### 2.3. Users Module (Core)
- [ ] Tạo `users` module
- [ ] Implement `UsersService`: CRUD operations
- [ ] Implement `UsersController`: GET /api/users/profile, PATCH /api/users/profile
- [ ] Validation DTOs cho User operations

### 2.4. Topics Module (Core)
- [ ] Tạo `topics` module
- [ ] Implement `TopicsService`: CRUD operations
- [ ] Implement `TopicsController`: GET /api/topics, POST /api/topics (Admin only)
- [ ] Validation DTOs

**Output Giai đoạn 2:**
- ✅ User có thể đăng ký/đăng nhập
- ✅ JWT token authentication hoạt động
- ✅ Admin có thể quản lý Topics
- ✅ Protected routes với Guards

---

## 🚧 **GIAI ĐOẠN 3: MODULE 1 - COURSE SYSTEM**
### Ước tính: 2-3 giờ

### 3.1. Courses Module
- [ ] Tạo `courses` module
- [ ] Implement `CoursesService`:
  - `findAll(topicId?, isPublished?)` - Lọc theo topic, status
  - `findOne(id)` - Chi tiết khóa học
  - `create()`, `update()`, `delete()` - Admin only
- [ ] Implement `CoursesController`:
  - GET /api/courses (Public)
  - GET /api/courses/:id (Public)
  - POST /api/courses (Admin)
  - PATCH /api/courses/:id (Admin)
  - DELETE /api/courses/:id (Admin)
- [ ] Validation DTOs (CreateCourseDto, UpdateCourseDto)

### 3.2. Lessons Module
- [ ] Tạo `lessons` module
- [ ] Implement `LessonsService`:
  - `findByCourse(courseId, targetBand?)` - Lọc theo Band
  - `findOne(id)` - Chi tiết bài học (bao gồm videos, vocabularies, grammars)
  - `create()`, `update()`, `delete()` - Admin only
  - `addVideo()`, `addVocabulary()`, `addGrammar()` - Thêm embedded items
- [ ] Implement `LessonsController`:
  - GET /api/lessons?courseId=xxx&targetBand=BAND_6_0
  - GET /api/lessons/:id
  - POST /api/lessons (Admin)
  - PATCH /api/lessons/:id (Admin)
  - POST /api/lessons/:id/videos (Admin)
  - POST /api/lessons/:id/vocabularies (Admin)
- [ ] Validation DTOs

**Output Giai đoạn 3:**
- ✅ Admin có thể tạo Courses & Lessons
- ✅ Học viên có thể xem danh sách và chi tiết khóa học
- ✅ Lọc bài học theo targetBand (cá nhân hóa)

---

## 🚧 **GIAI ĐOẠN 4: MODULE 2 - SAMPLE ESSAYS**
### Ước tính: 2 giờ

### 4.1. Sample Essays Module
- [ ] Tạo `sample-essays` module
- [ ] Implement `SampleEssaysService`:
  - `findAll(topicId?, targetBand?)` - Lọc bài mẫu
  - `findOne(id)` - Chi tiết bài mẫu (bao gồm highlightAnnotations)
  - `incrementViewCount(id)` - Tăng lượt xem
  - `create()`, `update()`, `delete()` - Admin only
- [ ] Implement `SampleEssaysController`:
  - GET /api/sample-essays
  - GET /api/sample-essays/:id
  - POST /api/sample-essays (Admin)
  - PATCH /api/sample-essays/:id (Admin)
- [ ] Validation DTOs (bao gồm HighlightAnnotationDto)

### 4.2. Favorite Essays Module
- [ ] Tạo `favorite-essays` module
- [ ] Implement `FavoriteEssaysService`:
  - `addFavorite(userId, essayId)` - Thả tim bài mẫu
  - `removeFavorite(userId, essayId)` - Bỏ tim
  - `getFavorites(userId)` - Danh sách bài yêu thích
  - `isFavorite(userId, essayId)` - Kiểm tra đã thả tim chưa
- [ ] Implement `FavoriteEssaysController`:
  - GET /api/favorite-essays (Student)
  - POST /api/favorite-essays (Student)
  - DELETE /api/favorite-essays/:essayId (Student)
- [ ] Validation DTOs

**Output Giai đoạn 4:**
- ✅ Admin có thể upload bài mẫu với highlight annotations
- ✅ Học viên xem bài mẫu với bôi màu phân tích
- ✅ Học viên có thể lưu bài mẫu yêu thích

---

## 🚧 **GIAI ĐOẠN 5: MODULE 3 - NOTEBOOK & FLASHCARDS**
### Ước tính: 2 giờ

### 5.1. Notebook Module
- [ ] Tạo `notebook` module
- [ ] Implement `NotebookService`:
  - `findAll(userId)` - Danh sách ghi chú
  - `findOne(id, userId)` - Chi tiết 1 ghi chú
  - `create(userId, content)` - Tạo ghi chú mới
  - `update(id, userId, content)` - Sửa ghi chú
  - `delete(id, userId)` - Xóa ghi chú
- [ ] Implement `NotebookController`:
  - GET /api/notebook (Student)
  - GET /api/notebook/:id (Student)
  - POST /api/notebook (Student)
  - PATCH /api/notebook/:id (Student)
  - DELETE /api/notebook/:id (Student)
- [ ] Validation DTOs

### 5.2. Flashcards Module
- [ ] Tạo `flashcards` module
- [ ] Implement `FlashcardsService`:
  - `findAllSets(userId)` - Danh sách các bộ thẻ
  - `findSetWithCards(setId, userId)` - Chi tiết bộ thẻ + cards
  - `createSet()`, `updateSet()`, `deleteSet()` - Quản lý Set
  - `addCard(setId)`, `updateCard()`, `deleteCard()` - Quản lý Card
  - `updateReviewSchedule(cardId)` - Cập nhật lịch ôn tập (spaced repetition)
- [ ] Implement `FlashcardsController`:
  - GET /api/flashcard-sets (Student)
  - GET /api/flashcard-sets/:id (Student)
  - POST /api/flashcard-sets (Student)
  - POST /api/flashcard-sets/:id/cards (Student)
  - PATCH /api/flashcards/:cardId (Student)
- [ ] Validation DTOs

**Output Giai đoạn 5:**
- ✅ Học viên có sổ tay nháp cá nhân
- ✅ Học viên tạo và ôn tập flashcards (giống Quizlet)
- ✅ Spaced repetition scheduling

---

## 🚧 **GIAI ĐOẠN 6: MODULE 4 - PRACTICE & AI ENGINE (CORE USP)**
### Ước tính: 4-5 giờ (Phần quan trọng nhất!)

### 6.1. Exam Questions Module
- [ ] Tạo `exam-questions` module
- [ ] Implement `ExamQuestionsService`:
  - `findAll(topicId?, difficultyLevel?)` - Danh sách đề thi
  - `findOne(id)` - Chi tiết đề thi (bao gồm suggestedOutline)
  - `getRandomQuestion(topicId?)` - Random 1 đề cho học viên luyện tập
  - `create()`, `update()`, `delete()` - Admin only
- [ ] Implement `ExamQuestionsController`:
  - GET /api/exam-questions
  - GET /api/exam-questions/random
  - GET /api/exam-questions/:id
  - POST /api/exam-questions (Admin)
- [ ] Validation DTOs

### 6.2. AI Grading Service (Strategy Pattern)
- [ ] Tạo `ai-grading` module
- [ ] **Interface & Strategy Pattern:**
  ```typescript
  interface IAIGradingService {
    gradeEssay(content: string, questionPrompt: string): Promise<AIResultDto>;
  }
  ```
- [ ] Implement `GeminiGradingService` (MVP):
  - Gọi Google Gemini API
  - Parse JSON response thành AIResult structure
  - Prompt engineering để nhận điểm chính xác + errors array
- [ ] Implement `MistralGradingService` (Future - Stub):
  - Placeholder cho Mistral 7B GPU Node
  - Sẽ implement sau khi có GPU Node
- [ ] Factory pattern để chọn provider (Gemini/Mistral)
- [ ] Error handling & retry logic

### 6.3. BullMQ Queue Setup
- [ ] Cấu hình BullMQ với Redis
- [ ] Tạo `submission.queue.ts` - Queue cho AI grading jobs
- [ ] Tạo `submission.processor.ts` - Worker xử lý jobs:
  - Nhận Job từ Queue
  - Gọi AI Grading Service
  - Cập nhật Submission với aiResult
  - Update status: PROCESSING → COMPLETED/FAILED
  - Emit WebSocket event (sẽ làm ở Giai đoạn 7)

### 6.4. Submissions Module
- [ ] Tạo `submissions` module
- [ ] Implement `SubmissionsService`:
  - `create(userId, questionId, content, timeSpent)` - Tạo bài nộp mới
  - `submit(id, userId)` - Nộp bài để chấm:
    - Update status: DRAFT → SUBMITTED
    - Push Job vào BullMQ Queue
    - Return HTTP 202 Accepted
  - `findByUser(userId)` - Danh sách bài đã làm
  - `findOne(id, userId)` - Chi tiết bài + kết quả AI (nếu có)
  - `updateDraft(id, userId, content)` - Sửa bản nháp
- [ ] Implement `SubmissionsController`:
  - POST /api/submissions - Tạo bài nháp
  - POST /api/submissions/:id/submit - Nộp bài chấm
  - GET /api/submissions - Lịch sử bài làm
  - GET /api/submissions/:id - Chi tiết + kết quả
  - PATCH /api/submissions/:id - Sửa nháp
- [ ] Validation DTOs

**Output Giai đoạn 6:**
- ✅ Học viên có thể chọn đề thi và làm bài
- ✅ Nộp bài → Job vào Queue → AI chấm tự động
- ✅ Kết quả AI với điểm + errors array (tọa độ bôi màu)
- ✅ Strategy Pattern sẵn sàng để swap Gemini → Mistral

---

## 🚧 **GIAI ĐOẠN 7: WEBSOCKET & REAL-TIME NOTIFICATIONS**
### Ước tính: 2 giờ

### 7.1. WebSocket Gateway Setup
- [ ] Tạo `websocket` module
- [ ] Implement `SubmissionsGateway`:
  - Socket.io server với namespace `/ws/submissions`
  - Client join room theo `userId`
  - Handle connection/disconnect
- [ ] Emit events:
  - `submission_status_updated` khi AI chấm xong
  - Payload: `{ submissionId, status, hasResult }`

### 7.2. Integrate với Submission Processor
- [ ] Trong `submission.processor.ts`:
  - Sau khi AI chấm xong
  - Emit WebSocket event về đúng user room
  - Client tự động gọi GET /api/submissions/:id

### 7.3. Frontend Integration Guide
- [ ] Tài liệu hướng dẫn Frontend kết nối WebSocket
- [ ] Sample client code (React/Next.js)

**Output Giai đoạn 7:**
- ✅ Real-time thông báo khi AI chấm xong
- ✅ Frontend tự động cập nhật kết quả không cần refresh

---

## 🚧 **GIAI ĐOẠN 8: TESTING, OPTIMIZATION & DOCUMENTATION**
### Ước tính: 2-3 giờ

### 8.1. Error Handling & Validation
- [ ] Global Exception Filter
- [ ] Custom API error responses
- [ ] Validation pipes cho tất cả DTOs

### 8.2. API Documentation
- [ ] Cài đặt Swagger/OpenAPI
- [ ] Document tất cả endpoints
- [ ] Tạo API collection (Postman/Thunder Client)

### 8.3. Database Seeding
- [ ] Tạo seed scripts:
  - Sample Topics
  - Sample Courses & Lessons
  - Sample Essays
  - Sample Exam Questions
- [ ] Script để import vào MongoDB

### 8.4. Testing
- [ ] Unit tests cho critical services (AI Grading, Submissions)
- [ ] E2E test cho AI grading flow
- [ ] Load testing cho Queue system

### 8.5. Deployment Guide
- [ ] Docker Compose setup (NestJS + MongoDB + Redis)
- [ ] Environment configuration
- [ ] Production checklist

**Output Giai đoạn 8:**
- ✅ API documentation đầy đủ
- ✅ Sample data để test
- ✅ Sẵn sàng deploy production

---

## 📊 TỔNG KẾT

| Giai đoạn | Nội dung | Ước tính | Status |
|-----------|----------|----------|--------|
| **1** | Setup & Database Schema | 2h | ✅ HOÀN THÀNH |
| **2** | Core Infrastructure & Auth | 2-3h | 🔜 Tiếp theo |
| **3** | Module 1: Course System | 2-3h | ⏳ Chờ |
| **4** | Module 2: Sample Essays | 2h | ⏳ Chờ |
| **5** | Module 3: Notebook & Flashcards | 2h | ⏳ Chờ |
| **6** | Module 4: Practice & AI (Core) | 4-5h | ⏳ Chờ |
| **7** | WebSocket & Real-time | 2h | ⏳ Chờ |
| **8** | Testing & Deployment | 2-3h | ⏳ Chờ |
| **TỔNG** | | **18-23 giờ** | **6% done** |

---

## 🎯 CHIẾN LƯỢC THỰC HIỆN

### Phương pháp làm việc:
1. **Từng giai đoạn một** - Hoàn thành 100% trước khi chuyển sang giai đoạn tiếp
2. **Test ngay** - Mỗi module phải test endpoints ngay sau khi code xong
3. **Commit thường xuyên** - Mỗi feature nhỏ = 1 commit
4. **Documentation inline** - Comment code rõ ràng ngay khi viết

### Câu hỏi quan trọng trước khi bắt đầu Giai đoạn 2:
- Bạn đã có **Gemini API Key** chưa? (Cần cho Giai đoạn 6)
- Bạn có muốn tôi tạo **seed data mẫu** ngay từ đầu không?
- Frontend (Next.js) bạn muốn làm song song hay sau khi backend xong?

---

## 🚀 BẮT ĐẦU GIAI ĐOẠN 2?

Sẵn sàng bắt đầu **Giai đoạn 2: Core Infrastructure & Authentication** chưa?

Giai đoạn 2 sẽ tạo nền tảng cho toàn bộ hệ thống:
- ✅ User đăng ký/đăng nhập
- ✅ JWT authentication
- ✅ Protected routes
- ✅ Admin/Student roles

**Thời gian ước tính:** 2-3 giờ
**Kết quả:** Backend có thể authen/author user

Bạn có muốn tôi bắt đầu **Giai đoạn 2** ngay không? 🚀
