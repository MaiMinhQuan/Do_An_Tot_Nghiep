# Database Schema - IELTS Writing Backend (For AI Understanding)

## Context
This is a NestJS backend application for an IELTS Writing learning platform using MongoDB with Mongoose ODM.

## Collections Overview (11 total)

### 1. **users** - User Management
Stores student and admin accounts.
```
Fields: _id, email*, passwordHash, fullName, role (STUDENT|ADMIN), isActive, avatarUrl, lastLoginAt
Relationships: Has many → submissions, favoriteessays, notebooknotes, flashcardsets
```

### 2. **topics** - IELTS Writing Topics
Categories like "Education", "Environment", "Technology"
```
Fields: _id, name*, slug*, description, iconUrl, orderIndex, isActive
Relationships: Has many → courses, sampleessays, examquestions
```

### 3. **courses** - Learning Courses
Structured courses for different topics
```
Fields: _id, title, description, topicId→, thumbnailUrl, orderIndex, isPublished, totalLessons, instructorName
Relationships: Belongs to → topics, Has many → lessons
```

### 4. **lessons** - Course Lessons
Contains videos, vocabulary, and grammar content
```
Fields: _id, title, courseId→, targetBand (5.0|6.0|7.0+), description, orderIndex, isPublished, notesContent
Embedded: videos[], vocabularies[], grammars[]
Relationships: Belongs to → courses
```

### 5. **sampleessays** - Model Essays
High-quality example essays with annotations
```
Fields: _id, title, topicId→, questionPrompt, targetBand, outlineContent, fullEssayContent, viewCount, favoriteCount, isPublished, authorName, overallBandScore (0-9)
Embedded: highlightAnnotations[] (vocabulary, grammar, structure, argument highlights)
Relationships: Belongs to → topics, Has many → favoriteessays
```

### 6. **favoriteessays** - User's Favorite Essays
Junction table for users bookmarking sample essays
```
Fields: _id, userId→, essayId→, personalNote
Unique: (userId, essayId) combination
Relationships: Belongs to → users, sampleessays
```

### 7. **notebooknotes** - User's Personal Notes
Free-form notes created by students
```
Fields: _id, userId→, userDraftNote, title
Relationships: Belongs to → users
```

### 8. **flashcardsets** - Flashcard Collections
User-created flashcard sets for vocabulary/grammar practice
```
Fields: _id, userId→, title, description
Relationships: Belongs to → users, Has many → flashcards
```

### 9. **flashcards** - Individual Flashcards
Flashcards with spaced repetition support
```
Fields: _id, setId→, frontContent, backContent, nextReviewDate, reviewCount
Relationships: Belongs to → flashcardsets
```

### 10. **examquestions** - Exam Question Bank
IELTS Writing Task 2 questions for practice
```
Fields: _id, title, topicId→, questionPrompt, suggestedOutline, difficultyLevel (1-5), isPublished, attemptCount, sourceReference, tags[]
Relationships: Belongs to → topics (optional), Has many → submissions
```

### 11. **submissions** - Student Submissions
Student essays with AI grading results
```
Fields: _id, userId→, questionId→, essayContent, wordCount, timeSpentSeconds, status (DRAFT|SUBMITTED|PROCESSING|COMPLETED|FAILED), submittedAt, attemptNumber
Embedded: aiResult {
  scores: taskResponseScore, coherenceScore, lexicalScore, grammarScore, overallBand (all 0-9)
  feedback: errors[], generalFeedback, strengths, improvements, processedAt
  error detail: {startIndex, endIndex, category, originalText, suggestion, explanation, severity}
}
Relationships: Belongs to → users, examquestions
```

## Key Relationships
```
User → creates → Submissions (for ExamQuestions)
User → favorites → SampleEssays (via FavoriteEssays)
User → writes → NotebookNotes
User → creates → FlashcardSets → contains → Flashcards

Topic → categorizes → Courses → contains → Lessons
Topic → categorizes → SampleEssays
Topic → categorizes → ExamQuestions

ExamQuestion → has → Submissions (with AI grading)
```

## Important Enums

**UserRole**: STUDENT, ADMIN

**TargetBand**: BAND_5_0, BAND_6_0, BAND_7_PLUS

**SubmissionStatus**: DRAFT, SUBMITTED, PROCESSING, COMPLETED, FAILED

**HighlightType**: VOCABULARY, GRAMMAR, STRUCTURE, ARGUMENT

**ErrorCategory**: GRAMMAR, VOCABULARY, COHERENCE, TASK_RESPONSE, SPELLING, PUNCTUATION

## AI Grading Flow
1. Student creates submission (status: DRAFT)
2. Student submits essay (status: SUBMITTED → PROCESSING)
3. AI (Gemini/Mistral) analyzes essay
4. System saves aiResult with scores and detailed feedback (status: COMPLETED)
5. Student views detailed feedback with error highlights and suggestions

## Special Features
- **Auto-generated fields**: topics.slug (from name), submissions.wordCount (from essayContent)
- **Timestamps**: All collections have createdAt/updatedAt
- **Unique constraints**: users.email, topics.name/slug, (userId+essayId) in favoriteessays
- **Indexes**: Optimized for common queries (userId, topicId, status, dates, popularity)
- **Embedded documents**: Lessons have nested videos/vocab/grammar, Submissions have nested AI results
- **Spaced repetition**: Flashcards track nextReviewDate and reviewCount

## Use Cases
1. **Learning Path**: User → enrolls in Course → completes Lessons → practices with ExamQuestions
2. **Essay Practice**: User → selects ExamQuestion → writes Submission → receives AI feedback
3. **Study Materials**: User → reads SampleEssays → bookmarks favorites → takes notes → creates flashcards
4. **Progress Tracking**: Count submissions, track scores over time, monitor learning activity

This schema supports a complete IELTS Writing learning ecosystem with AI-powered feedback.
