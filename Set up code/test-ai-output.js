/**
 * TEST SCRIPT - Validate Gemini AI Output
 * File này dùng để test và validate output từ Gemini AI
 * Chạy: node test-ai-output.js
 */

// ============================================================================
// MOCK AI OUTPUT (Copy từ Gemini response)
// ============================================================================

const mockGeminiOutput = {
  "taskResponseScore": 6.5,
  "coherenceScore": 6.0,
  "lexicalScore": 6.5,
  "grammarScore": 6.0,
  "overallBand": 6.0,
  "errors": [
    {
      "startIndex": 45,
      "endIndex": 64,
      "category": "GRAMMAR",
      "originalText": "in young generation",
      "suggestion": "among the younger generation",
      "explanation": "Cần sử dụng giới từ 'among' khi nói về một tập thể lớn.",
      "severity": "medium"
    },
    {
      "startIndex": 152,
      "endIndex": 173,
      "category": "VOCABULARY",
      "originalText": "earn bread and butter",
      "suggestion": "make a living",
      "explanation": "Thành ngữ 'earn bread and butter' mang sắc thái quá thân mật.",
      "severity": "low"
    }
  ],
  "generalFeedback": "Bài viết của bạn đã giải quyết được yêu cầu cơ bản...",
  "strengths": "Cấu trúc bài viết rõ ràng...",
  "improvements": "Cần kiểm tra kỹ sự hòa hợp giữa chủ ngữ và động từ..."
};

// ============================================================================
// VALIDATION FUNCTIONS
// ============================================================================

const ErrorCategory = ['GRAMMAR', 'VOCABULARY', 'COHERENCE', 'TASK_RESPONSE', 'SPELLING', 'PUNCTUATION'];
const ErrorSeverity = ['low', 'medium', 'high'];

function validateScore(score, fieldName) {
  const errors = [];

  // Check type
  if (typeof score !== 'number') {
    errors.push(`${fieldName}: Phải là number, nhận được ${typeof score}`);
    return errors;
  }

  // Check range
  if (score < 0 || score > 9) {
    errors.push(`${fieldName}: Phải trong khoảng 0-9, nhận được ${score}`);
  }

  // Check increment (bước 0.5)
  if ((score * 10) % 5 !== 0) {
    errors.push(`${fieldName}: Phải là bước 0.5 (ví dụ: 6.0, 6.5, 7.0), nhận được ${score}`);
  }

  return errors;
}

function validateError(error, index) {
  const errors = [];

  // Check required fields
  if (typeof error.startIndex !== 'number') {
    errors.push(`errors[${index}].startIndex: Phải là number`);
  }
  if (typeof error.endIndex !== 'number') {
    errors.push(`errors[${index}].endIndex: Phải là number`);
  }
  if (error.endIndex <= error.startIndex) {
    errors.push(`errors[${index}]: endIndex (${error.endIndex}) phải > startIndex (${error.startIndex})`);
  }

  // Check category
  if (!ErrorCategory.includes(error.category)) {
    errors.push(`errors[${index}].category: Phải là một trong [${ErrorCategory.join(', ')}], nhận được "${error.category}"`);
  }

  // Check severity
  if (error.severity && !ErrorSeverity.includes(error.severity)) {
    errors.push(`errors[${index}].severity: Phải là một trong [${ErrorSeverity.join(', ')}], nhận được "${error.severity}"`);
  }

  // Check strings
  if (!error.originalText || typeof error.originalText !== 'string') {
    errors.push(`errors[${index}].originalText: Bắt buộc và phải là string`);
  }
  if (!error.suggestion || typeof error.suggestion !== 'string') {
    errors.push(`errors[${index}].suggestion: Bắt buộc và phải là string`);
  }
  if (!error.explanation || typeof error.explanation !== 'string') {
    errors.push(`errors[${index}].explanation: Bắt buộc và phải là string`);
  }

  return errors;
}

function validateAIOutput(output) {
  const validationErrors = [];

  console.log('\n🔍 BẮT ĐẦU VALIDATION...\n');

  // 1. Check required score fields
  console.log('1️⃣  Kiểm tra scores...');
  const scoreFields = ['taskResponseScore', 'coherenceScore', 'lexicalScore', 'grammarScore', 'overallBand'];

  for (const field of scoreFields) {
    if (!(field in output)) {
      validationErrors.push(`Thiếu field bắt buộc: ${field}`);
      continue;
    }
    const scoreErrors = validateScore(output[field], field);
    validationErrors.push(...scoreErrors);
  }

  if (validationErrors.length === 0) {
    console.log('   ✅ Tất cả scores hợp lệ');
  } else {
    console.log(`   ❌ Có ${validationErrors.length} lỗi trong scores`);
  }

  // 2. Check errors array
  console.log('\n2️⃣  Kiểm tra errors array...');
  if (!Array.isArray(output.errors)) {
    validationErrors.push('errors: Phải là array');
    console.log('   ❌ errors không phải array');
  } else {
    console.log(`   ℹ️  Tìm thấy ${output.errors.length} errors`);

    output.errors.forEach((error, index) => {
      const errorErrors = validateError(error, index);
      validationErrors.push(...errorErrors);
    });

    if (validationErrors.length === 0 || output.errors.length === 0) {
      console.log('   ✅ Tất cả errors hợp lệ');
    }
  }

  // 3. Check feedback fields (optional but recommended)
  console.log('\n3️⃣  Kiểm tra feedback fields...');
  const feedbackFields = ['generalFeedback', 'strengths', 'improvements'];
  const missingFeedback = [];

  for (const field of feedbackFields) {
    if (!output[field]) {
      missingFeedback.push(field);
    }
  }

  if (missingFeedback.length === 0) {
    console.log('   ✅ Có đầy đủ feedback fields');
  } else {
    console.log(`   ⚠️  Thiếu feedback fields (optional): ${missingFeedback.join(', ')}`);
  }

  // 4. Overall result
  console.log('\n' + '='.repeat(70));
  if (validationErrors.length === 0) {
    console.log('✅ VALIDATION THÀNH CÔNG - Output hợp lệ!');
    console.log('='.repeat(70));
    return { valid: true, errors: [] };
  } else {
    console.log('❌ VALIDATION THẤT BẠI - Tìm thấy lỗi:');
    console.log('='.repeat(70));
    validationErrors.forEach((error, index) => {
      console.log(`   ${index + 1}. ${error}`);
    });
    console.log('='.repeat(70));
    return { valid: false, errors: validationErrors };
  }
}

// ============================================================================
// TRANSFORM FUNCTION (Nếu cần transform nested structure)
// ============================================================================

function transformNestedToFlat(nestedOutput) {
  console.log('\n🔄 TRANSFORM NESTED → FLAT STRUCTURE...\n');

  // Check if already flat
  if ('taskResponseScore' in nestedOutput && !('scores' in nestedOutput)) {
    console.log('   ℹ️  Output đã ở dạng flat, không cần transform');
    return nestedOutput;
  }

  // Transform
  const flat = {
    taskResponseScore: nestedOutput.scores?.taskResponseScore,
    coherenceScore: nestedOutput.scores?.coherenceScore,
    lexicalScore: nestedOutput.scores?.lexicalScore,
    grammarScore: nestedOutput.scores?.grammarScore,
    overallBand: nestedOutput.scores?.overallBand,
    errors: (nestedOutput.feedback?.errors || []).map(error => ({
      ...error,
      severity: error.severity ? error.severity.toLowerCase() : 'medium',
    })),
    generalFeedback: nestedOutput.feedback?.generalFeedback,
    strengths: nestedOutput.feedback?.strengths,
    improvements: nestedOutput.feedback?.improvements,
  };

  console.log('   ✅ Transform thành công');
  return flat;
}

// ============================================================================
// TEST CASES
// ============================================================================

function runTests() {
  console.log('\n' + '═'.repeat(70));
  console.log('  TEST GEMINI AI OUTPUT VALIDATION');
  console.log('═'.repeat(70));

  // Test 1: Valid output
  console.log('\n📝 TEST 1: Valid output (flat structure)');
  console.log('-'.repeat(70));
  const result1 = validateAIOutput(mockGeminiOutput);

  // Test 2: Nested structure (cần transform)
  console.log('\n\n📝 TEST 2: Nested structure (scores/feedback objects)');
  console.log('-'.repeat(70));
  const nestedOutput = {
    scores: {
      taskResponseScore: 6.5,
      coherenceScore: 6.0,
      lexicalScore: 6.5,
      grammarScore: 6.0,
      overallBand: 6.0,
    },
    feedback: {
      errors: [
        {
          startIndex: 10,
          endIndex: 20,
          category: "GRAMMAR",
          originalText: "test error",
          suggestion: "correction",
          explanation: "Giải thích lỗi",
          severity: "MEDIUM" // ← UPPERCASE, cần lowercase
        }
      ],
      generalFeedback: "Feedback...",
      strengths: "Strengths...",
      improvements: "Improvements..."
    }
  };

  const transformed = transformNestedToFlat(nestedOutput);
  const result2 = validateAIOutput(transformed);

  // Test 3: Invalid output (nhiều lỗi)
  console.log('\n\n📝 TEST 3: Invalid output (nhiều lỗi)');
  console.log('-'.repeat(70));
  const invalidOutput = {
    taskResponseScore: "6.5", // ← String, phải number
    coherenceScore: 6.75, // ← Không đúng bước 0.5
    lexicalScore: 10.0, // ← Vượt quá 9.0
    grammarScore: 6.0,
    overallBand: 6.0,
    errors: [
      {
        startIndex: 20,
        endIndex: 10, // ← endIndex <= startIndex
        category: "grammar", // ← Lowercase, phải UPPERCASE
        originalText: "test",
        suggestion: "correction",
        explanation: "Explanation",
        severity: "CRITICAL" // ← Không có trong enum
      }
    ]
  };

  const result3 = validateAIOutput(invalidOutput);

  // Summary
  console.log('\n\n' + '═'.repeat(70));
  console.log('  📊 SUMMARY');
  console.log('═'.repeat(70));
  console.log(`Test 1 (Valid flat): ${result1.valid ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Test 2 (Nested): ${result2.valid ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Test 3 (Invalid): ${result3.valid ? '❌ FAIL (expected)' : '✅ PASS'}`);
  console.log('═'.repeat(70) + '\n');
}

// ============================================================================
// HELPER: Print pretty JSON
// ============================================================================

function printJSON(obj, title) {
  console.log(`\n${title}:`);
  console.log('-'.repeat(70));
  console.log(JSON.stringify(obj, null, 2));
  console.log('-'.repeat(70));
}

// ============================================================================
// RUN
// ============================================================================

// Chạy tests
runTests();

// Export cho sử dụng trong code khác
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    validateAIOutput,
    transformNestedToFlat,
    validateScore,
    validateError,
    ErrorCategory,
    ErrorSeverity,
  };
}

// ============================================================================
// HƯỚNG DẪN SỬ DỤNG
// ============================================================================

/*

1. Copy Gemini response vào biến mockGeminiOutput (dòng 8)

2. Chạy file:
   node test-ai-output.js

3. Xem kết quả validation:
   - ✅ = Hợp lệ
   - ❌ = Có lỗi
   - ⚠️  = Warning (không bắt buộc)

4. Nếu có lỗi, sửa prompt Gemini theo errors hiển thị

5. Test lại cho đến khi validation pass

6. Khi validation pass, copy code vào backend AI service:

   import { validateAIOutput, transformNestedToFlat } from './test-ai-output';

   const geminiResponse = await callGeminiAPI(...);
   const flat = transformNestedToFlat(geminiResponse);
   const validation = validateAIOutput(flat);

   if (validation.valid) {
     // Save to database
     submission.aiResult = flat;
     await submission.save();
   } else {
     console.error('AI Output invalid:', validation.errors);
   }

*/
