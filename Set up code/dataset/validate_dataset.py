#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════
JSONL Dataset Validator - Kiểm tra chất lượng dataset sau khi generate
═══════════════════════════════════════════════════════════════════════════

Script này validate:
1. Format JSONL đúng chuẩn ChatML
2. Tọa độ startIndex/endIndex chính xác
3. Scores trong range hợp lệ
4. Statistics về distribution

Usage:
    python validate_dataset.py dataset_batch_0_to_10_fixed.jsonl

Author: Senior AI Engineer
Date: March 12, 2026
═══════════════════════════════════════════════════════════════════════════
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# VALIDATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def validate_scores(ai_json: Dict) -> List[str]:
    """Validate scores trong range 0-9, bước 0.5"""
    errors = []
    score_fields = ['taskResponseScore', 'coherenceScore', 'lexicalScore',
                   'grammarScore', 'overallBand']

    for field in score_fields:
        if field not in ai_json:
            errors.append(f"Missing field: {field}")
            continue

        score = ai_json[field]

        # Check type
        if not isinstance(score, (int, float)):
            errors.append(f"{field}: Must be number, got {type(score)}")
            continue

        # Check range
        if score < 0 or score > 9:
            errors.append(f"{field}: Out of range [0-9], got {score}")

        # Check increment (bước 0.5)
        if (score * 10) % 5 != 0:
            errors.append(f"{field}: Must be 0.5 increment, got {score}")

    return errors


def validate_coordinates(ai_json: Dict, essay_text: str) -> List[str]:
    """Validate tọa độ startIndex/endIndex khớp với originalText"""
    errors = []

    if 'errors' not in ai_json:
        return errors

    for i, error in enumerate(ai_json['errors']):
        start = error.get('startIndex')
        end = error.get('endIndex')
        original = error.get('originalText', '')

        # Check required fields
        if start is None or end is None:
            errors.append(f"Error {i}: Missing startIndex or endIndex")
            continue

        # Check range
        if end <= start:
            errors.append(f"Error {i}: endIndex ({end}) <= startIndex ({start})")
            continue

        if start < 0 or end < 0:
            errors.append(f"Error {i}: Negative index")
            continue

        if end > len(essay_text):
            errors.append(f"Error {i}: endIndex ({end}) > essay length ({len(essay_text)})")
            continue

        # Verify coordinates match originalText
        extracted = essay_text[start:end]
        if extracted != original:
            errors.append(
                f"Error {i}: Coordinate mismatch\n"
                f"  originalText: '{original}'\n"
                f"  essay[{start}:{end}]: '{extracted}'"
            )

    return errors


def validate_chatml_format(data: Dict) -> List[str]:
    """Validate format ChatML"""
    errors = []

    if 'messages' not in data:
        return ["Missing 'messages' key"]

    messages = data['messages']

    if not isinstance(messages, list):
        return ["'messages' must be array"]

    if len(messages) != 3:
        errors.append(f"Expected 3 messages, got {len(messages)}")

    expected_roles = ['system', 'user', 'assistant']
    for i, msg in enumerate(messages[:3]):
        if 'role' not in msg:
            errors.append(f"Message {i}: Missing 'role'")
        elif msg['role'] != expected_roles[i]:
            errors.append(
                f"Message {i}: Expected role '{expected_roles[i]}', "
                f"got '{msg['role']}'"
            )

        if 'content' not in msg:
            errors.append(f"Message {i}: Missing 'content'")

    return errors


# ═══════════════════════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

def collect_statistics(jsonl_file: str) -> Dict:
    """Collect statistics về dataset"""
    stats = {
        'total_examples': 0,
        'valid_examples': 0,
        'total_errors_detected': 0,
        'band_distribution': defaultdict(int),
        'error_category_distribution': defaultdict(int),
        'error_severity_distribution': defaultdict(int),
        'avg_errors_per_essay': 0,
        'coordinate_accuracy': 0,
    }

    coordinate_correct = 0
    coordinate_total = 0

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                stats['total_examples'] += 1

                # Parse assistant message
                assistant_content = data['messages'][2]['content']
                ai_json = json.loads(assistant_content)

                # Band distribution
                band = ai_json.get('overallBand')
                if band:
                    stats['band_distribution'][band] += 1

                # Error statistics
                errors = ai_json.get('errors', [])
                stats['total_errors_detected'] += len(errors)

                for error in errors:
                    # Category distribution
                    category = error.get('category')
                    if category:
                        stats['error_category_distribution'][category] += 1

                    # Severity distribution
                    severity = error.get('severity')
                    if severity:
                        stats['error_severity_distribution'][severity] += 1

                    # Coordinate accuracy
                    coordinate_total += 1

                    # Extract essay from user message
                    user_content = data['messages'][1]['content']
                    essay_part = user_content.split('BÀI VIẾT CỦA HỌC VIÊN:')
                    if len(essay_part) > 1:
                        essay = essay_part[1].strip().split('\n\n')[0]

                        start = error.get('startIndex')
                        end = error.get('endIndex')
                        original = error.get('originalText', '')

                        if start is not None and end is not None:
                            extracted = essay[start:end]
                            if extracted == original:
                                coordinate_correct += 1

                stats['valid_examples'] += 1

            except Exception as e:
                print(f"❌ Error parsing line {line_num}: {e}")

    # Calculate averages
    if stats['total_examples'] > 0:
        stats['avg_errors_per_essay'] = stats['total_errors_detected'] / stats['total_examples']

    if coordinate_total > 0:
        stats['coordinate_accuracy'] = (coordinate_correct / coordinate_total) * 100

    return stats


# ═══════════════════════════════════════════════════════════════════════════
# MAIN VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

def validate_jsonl(jsonl_file: str, verbose: bool = False) -> Tuple[int, int]:
    """
    Validate JSONL file

    Returns:
        (valid_count, invalid_count)
    """
    print("═" * 80)
    print("  🔍 DATASET VALIDATION")
    print("═" * 80)
    print(f"\n📂 File: {jsonl_file}\n")

    valid_count = 0
    invalid_count = 0
    all_errors = []

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line_errors = []

            # ─────────────────────────────────────────────────────────────────
            # 1. Parse JSON
            # ─────────────────────────────────────────────────────────────────

            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                line_errors.append(f"Invalid JSON: {e}")
                invalid_count += 1
                all_errors.append((line_num, line_errors))
                continue

            # ─────────────────────────────────────────────────────────────────
            # 2. Validate ChatML format
            # ─────────────────────────────────────────────────────────────────

            format_errors = validate_chatml_format(data)
            line_errors.extend(format_errors)

            if format_errors:
                invalid_count += 1
                all_errors.append((line_num, line_errors))
                continue

            # ─────────────────────────────────────────────────────────────────
            # 3. Parse assistant message
            # ─────────────────────────────────────────────────────────────────

            try:
                assistant_content = data['messages'][2]['content']
                ai_json = json.loads(assistant_content)
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                line_errors.append(f"Invalid assistant message: {e}")
                invalid_count += 1
                all_errors.append((line_num, line_errors))
                continue

            # ─────────────────────────────────────────────────────────────────
            # 4. Validate scores
            # ─────────────────────────────────────────────────────────────────

            score_errors = validate_scores(ai_json)
            line_errors.extend(score_errors)

            # ─────────────────────────────────────────────────────────────────
            # 5. Validate coordinates
            # ─────────────────────────────────────────────────────────────────

            # Extract essay from user message
            user_content = data['messages'][1]['content']
            essay_parts = user_content.split('BÀI VIẾT CỦA HỌC VIÊN:')

            if len(essay_parts) > 1:
                essay = essay_parts[1].strip().split('\n\n')[0]
                coord_errors = validate_coordinates(ai_json, essay)
                line_errors.extend(coord_errors)

            # ─────────────────────────────────────────────────────────────────
            # 6. Summary
            # ─────────────────────────────────────────────────────────────────

            if line_errors:
                invalid_count += 1
                all_errors.append((line_num, line_errors))

                if verbose:
                    print(f"❌ Line {line_num}: {len(line_errors)} error(s)")
                    for err in line_errors:
                        print(f"   - {err}")
            else:
                valid_count += 1
                if verbose:
                    print(f"✅ Line {line_num}: OK")

    # ─────────────────────────────────────────────────────────────────────────
    # Print Summary
    # ─────────────────────────────────────────────────────────────────────────

    print("\n" + "═" * 80)
    print("📊 VALIDATION SUMMARY")
    print("═" * 80)
    print(f"Total lines:    {valid_count + invalid_count}")
    print(f"Valid:          {valid_count} ✅")
    print(f"Invalid:        {invalid_count} ❌")
    print(f"Success rate:   {valid_count/(valid_count + invalid_count)*100:.1f}%")

    if all_errors and not verbose:
        print(f"\n⚠️  Found errors in {len(all_errors)} lines")
        print("Run with --verbose flag to see details")

    return valid_count, invalid_count


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_dataset.py <jsonl_file> [--verbose] [--stats]")
        print("\nOptions:")
        print("  --verbose    Show detailed errors for each line")
        print("  --stats      Show dataset statistics")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    verbose = '--verbose' in sys.argv
    show_stats = '--stats' in sys.argv

    # Validate
    valid, invalid = validate_jsonl(jsonl_file, verbose=verbose)

    # Statistics
    if show_stats or invalid == 0:
        print("\n" + "═" * 80)
        print("📈 DATASET STATISTICS")
        print("═" * 80)

        stats = collect_statistics(jsonl_file)

        print(f"\n📊 Overview:")
        print(f"  Total examples:        {stats['total_examples']}")
        print(f"  Valid examples:        {stats['valid_examples']}")
        print(f"  Total errors detected: {stats['total_errors_detected']}")
        print(f"  Avg errors/essay:      {stats['avg_errors_per_essay']:.2f}")
        print(f"  Coordinate accuracy:   {stats['coordinate_accuracy']:.1f}%")

        print(f"\n🎯 Band Distribution:")
        for band in sorted(stats['band_distribution'].keys()):
            count = stats['band_distribution'][band]
            percentage = (count / stats['total_examples']) * 100
            bar = '█' * int(percentage / 2)
            print(f"  Band {band:3.1f}: {bar} {count:3d} ({percentage:5.1f}%)")

        print(f"\n📝 Error Category Distribution:")
        for category, count in sorted(stats['error_category_distribution'].items()):
            percentage = (count / stats['total_errors_detected']) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {category:15s}: {bar} {count:3d} ({percentage:5.1f}%)")

        print(f"\n⚠️  Error Severity Distribution:")
        for severity, count in sorted(stats['error_severity_distribution'].items()):
            percentage = (count / stats['total_errors_detected']) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {severity:6s}: {bar} {count:3d} ({percentage:5.1f}%)")

        print("═" * 80)

    # Exit code
    sys.exit(0 if invalid == 0 else 1)


if __name__ == "__main__":
    main()
