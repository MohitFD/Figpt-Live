#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Training Data Validation Script
This script validates and analyzes the comprehensive training dataset.
"""

import json
import os
from collections import Counter, defaultdict

def load_training_data(file_path):
    """Load and parse training data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def validate_data_structure(data):
    """Validate the structure of training data"""
    print("🔍 Validating data structure...")
    
    if not isinstance(data, dict):
        print("❌ Root data should be a dictionary")
        return False
    
    if "train" not in data:
        print("❌ Missing 'train' key")
        return False
    
    if not isinstance(data["train"], list):
        print("❌ 'train' should be a list")
        return False
    
    if len(data["train"]) == 0:
        print("❌ 'train' list is empty")
        return False
    
    print(f"✅ Data structure valid with {len(data['train'])} training examples")
    return True

def analyze_training_examples(examples):
    """Analyze individual training examples"""
    print("\n📊 Analyzing training examples...")
    
    required_fields = ["instruction", "output"]
    optional_fields = ["category", "language"]
    
    valid_examples = 0
    invalid_examples = 0
    categories = Counter()
    languages = Counter()
    instruction_lengths = []
    output_lengths = []
    
    for i, example in enumerate(examples):
        # Check required fields
        if not all(field in example for field in required_fields):
            print(f"❌ Example {i+1}: Missing required fields")
            invalid_examples += 1
            continue
        
        # Check field types
        if not isinstance(example["instruction"], str) or not isinstance(example["output"], str):
            print(f"❌ Example {i+1}: Fields should be strings")
            invalid_examples += 1
            continue
        
        # Check empty fields
        if not example["instruction"].strip() or not example["output"].strip():
            print(f"❌ Example {i+1}: Empty instruction or output")
            invalid_examples += 1
            continue
        
        valid_examples += 1
        
        # Collect statistics
        if "category" in example:
            categories[example["category"]] += 1
        
        if "language" in example:
            languages[example["language"]] += 1
        
        instruction_lengths.append(len(example["instruction"]))
        output_lengths.append(len(example["output"]))
    
    print(f"✅ Valid examples: {valid_examples}")
    print(f"❌ Invalid examples: {invalid_examples}")
    
    # Print category distribution
    if categories:
        print(f"\n📂 Category distribution:")
        for category, count in categories.most_common():
            print(f"   {category}: {count} examples")
    
    # Print language distribution
    if languages:
        print(f"\n🌐 Language distribution:")
        for language, count in languages.most_common():
            print(f"   {language}: {count} examples")
    
    # Print length statistics
    if instruction_lengths:
        print(f"\n📏 Instruction length statistics:")
        print(f"   Average: {sum(instruction_lengths)/len(instruction_lengths):.1f} characters")
        print(f"   Min: {min(instruction_lengths)} characters")
        print(f"   Max: {max(instruction_lengths)} characters")
    
    if output_lengths:
        print(f"\n📏 Output length statistics:")
        print(f"   Average: {sum(output_lengths)/len(output_lengths):.1f} characters")
        print(f"   Min: {min(output_lengths)} characters")
        print(f"   Max: {max(output_lengths)} characters")
    
    return valid_examples, invalid_examples

def check_data_quality(examples):
    """Check data quality and consistency"""
    print("\n🔍 Checking data quality...")
    
    # Check for duplicate instructions
    instructions = [ex["instruction"].lower().strip() for ex in examples if "instruction" in ex]
    duplicates = len(instructions) - len(set(instructions))
    
    if duplicates > 0:
        print(f"⚠️  Found {duplicates} duplicate instructions")
    else:
        print("✅ No duplicate instructions found")
    
    # Check for very short or very long examples
    short_instructions = sum(1 for ex in examples if len(ex.get("instruction", "")) < 10)
    long_instructions = sum(1 for ex in examples if len(ex.get("instruction", "")) > 500)
    
    short_outputs = sum(1 for ex in examples if len(ex.get("output", "")) < 10)
    long_outputs = sum(1 for ex in examples if len(ex.get("output", "")) > 2000)
    
    if short_instructions > 0:
        print(f"⚠️  {short_instructions} very short instructions (< 10 chars)")
    
    if long_instructions > 0:
        print(f"⚠️  {long_instructions} very long instructions (> 500 chars)")
    
    if short_outputs > 0:
        print(f"⚠️  {short_outputs} very short outputs (< 10 chars)")
    
    if long_outputs > 0:
        print(f"⚠️  {long_outputs} very long outputs (> 2000 chars)")
    
    if short_instructions == 0 and long_instructions == 0 and short_outputs == 0 and long_outputs == 0:
        print("✅ All examples have reasonable lengths")

def generate_training_summary(data):
    """Generate a comprehensive training summary"""
    print("\n📋 Training Data Summary")
    print("=" * 50)
    
    if "metadata" in data:
        metadata = data["metadata"]
        print(f"Description: {metadata.get('description', 'N/A')}")
        print(f"Total examples: {len(data['train'])}")
        print(f"Categories: {len(metadata.get('categories', {}))}")
        print(f"Languages: {', '.join(metadata.get('languages', []))}")
        print(f"Created: {metadata.get('created_date', 'N/A')}")
    
    print(f"\nTraining examples: {len(data['train'])}")
    
    # Category breakdown
    categories = Counter()
    for example in data["train"]:
        if "category" in example:
            categories[example["category"]] += 1
    
    if categories:
        print(f"\nCategory breakdown:")
        for category, count in categories.most_common():
            percentage = (count / len(data['train'])) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")
    
    # Language breakdown
    languages = Counter()
    for example in data["train"]:
        if "language" in example:
            languages[example["language"]] += 1
    
    if languages:
        print(f"\nLanguage breakdown:")
        for language, count in languages.most_common():
            percentage = (count / len(data['train'])) * 100
            print(f"  {language}: {count} ({percentage:.1f}%)")

def main():
    print("🧪 FixHR Training Data Validation")
    print("=" * 50)
    
    # Check if comprehensive data exists
    comprehensive_file = "dataset/comprehensive_training_data.json"
    if not os.path.exists(comprehensive_file):
        print(f"❌ Comprehensive training data not found: {comprehensive_file}")
        return
    
    # Load and validate data
    data = load_training_data(comprehensive_file)
    if not data:
        return
    
    # Validate structure
    if not validate_data_structure(data):
        return
    
    # Analyze examples
    valid_count, invalid_count = analyze_training_examples(data["train"])
    
    # Check data quality
    check_data_quality(data["train"])
    
    # Generate summary
    generate_training_summary(data)
    
    # Final assessment
    print(f"\n🎯 Final Assessment:")
    if invalid_count == 0:
        print("✅ All training examples are valid!")
        print("✅ Data is ready for training!")
    else:
        print(f"⚠️  {invalid_count} examples need attention")
        print("⚠️  Please fix issues before training")
    
    print(f"\n📊 Total valid examples for training: {valid_count}")

if __name__ == "__main__":
    main()
