#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FixHR Dataset Summary Script
This script provides a comprehensive summary of all training datasets.
"""

import json
import os
from collections import Counter, defaultdict

def load_json_file(file_path):
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def analyze_dataset(file_path, dataset_name):
    """Analyze a single dataset"""
    print(f"\n📊 {dataset_name}")
    print("=" * 50)
    
    data = load_json_file(file_path)
    if not data:
        return None
    
    if "train" in data:
        examples = data["train"]
        print(f"📝 Total Examples: {len(examples)}")
        
        # Analyze categories if present
        categories = Counter()
        languages = Counter()
        
        for example in examples:
            if "category" in example:
                categories[example["category"]] += 1
            if "language" in example:
                languages[example["language"]] += 1
        
        if categories:
            print(f"📂 Categories: {len(categories)}")
            for cat, count in categories.most_common():
                print(f"   {cat}: {count}")
        
        if languages:
            print(f"🌐 Languages: {len(languages)}")
            for lang, count in languages.most_common():
                print(f"   {lang}: {count}")
        
        # Sample examples
        print(f"\n📋 Sample Examples:")
        for i, example in enumerate(examples[:3]):
            print(f"   {i+1}. {example.get('instruction', 'N/A')[:50]}...")
        
        return {
            "name": dataset_name,
            "file": file_path,
            "total": len(examples),
            "categories": dict(categories),
            "languages": dict(languages)
        }
    
    return None

def main():
    print("📚 FixHR Dataset Summary")
    print("=" * 60)
    
    # Define all dataset files
    datasets = [
        ("dataset/comprehensive_training_data.json", "Comprehensive Training Data (Merged)"),
        ("dataset/general_data.json", "General HR Data"),
        ("dataset/fix_hr_data.json", "FixHR Specific Data"),
        ("dataset/leaves_data.json", "Leave Management Data"),
        ("dataset/attendance_data.json", "Attendance Tracking Data"),
        ("dataset/gatepass_data.json", "Gatepass Management Data"),
        ("dataset/holidays_data.json", "Holiday Management Data"),
        ("dataset/missed_punch_data.json", "Missed Punch Data")
    ]
    
    results = []
    total_examples = 0
    
    # Analyze each dataset
    for file_path, name in datasets:
        if os.path.exists(file_path):
            result = analyze_dataset(file_path, name)
            if result:
                results.append(result)
                total_examples += result["total"]
        else:
            print(f"\n❌ {name}: File not found ({file_path})")
    
    # Summary
    print(f"\n🎯 Overall Summary")
    print("=" * 60)
    print(f"📊 Total Datasets: {len(results)}")
    print(f"📝 Total Examples: {total_examples}")
    
    # Category summary
    all_categories = Counter()
    all_languages = Counter()
    
    for result in results:
        for cat, count in result["categories"].items():
            all_categories[cat] += count
        for lang, count in result["languages"].items():
            all_languages[lang] += count
    
    if all_categories:
        print(f"\n📂 All Categories:")
        for cat, count in all_categories.most_common():
            print(f"   {cat}: {count}")
    
    if all_languages:
        print(f"\n🌐 All Languages:")
        for lang, count in all_languages.most_common():
            print(f"   {lang}: {count}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    print("=" * 30)
    
    if "comprehensive_training_data.json" in [r["file"] for r in results]:
        print("✅ Use 'comprehensive_training_data.json' for training")
        print("   - Contains all merged data")
        print("   - Properly categorized")
        print("   - Multi-language support")
    else:
        print("⚠️  Comprehensive dataset not found")
        print("   - Consider merging individual datasets")
    
    # Training readiness
    comprehensive_result = next((r for r in results if "comprehensive" in r["name"].lower()), None)
    if comprehensive_result:
        if comprehensive_result["total"] >= 50:
            print("✅ Dataset size is adequate for training")
        else:
            print("⚠️  Dataset might be too small for effective training")
        
        if len(comprehensive_result["categories"]) >= 5:
            print("✅ Good category diversity")
        else:
            print("⚠️  Consider adding more categories")
        
        if len(comprehensive_result["languages"]) >= 2:
            print("✅ Multi-language support available")
        else:
            print("⚠️  Consider adding more languages")
    
    print(f"\n🚀 Next Steps:")
    print("1. Run: python validate_training_data.py")
    print("2. Train model: python train_ai_model.py")
    print("3. Test system: python test_system.py")

if __name__ == "__main__":
    main()
