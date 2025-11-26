#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Standalone AI Model Training Script for FixHR GPT Local
This script can be run independently to train the AI model.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from core.train_model import *
def main():
    print("🚀 FixHR AI Model Training Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("core/train_model.py"):
        print("❌ Error: Please run this script from the project root directory")
        print("   Expected to find: core/train_model.py")
        sys.exit(1)
    
    # Check if data files exist
    data_files = [
        "dataset/general_data.json",
        "dataset/fix_hr_data.json"
    ]
    
    missing_files = []
    for file_path in data_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        print("   Please ensure all training data files are present")
        sys.exit(1)
    
    print("✅ Data files found")
    
    # Check Python dependencies
    required_packages = [
        'torch', 'transformers', 'datasets', 'peft', 'accelerate'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Install them with: pip install torch transformers datasets peft accelerate")
        sys.exit(1)
    
    print("✅ All dependencies are installed")
    
    # Run the training
    print("\n🎯 Starting model training...")
    print("   This may take 2-4 hours depending on your hardware")
    print("   Training progress will be shown below:")
    print("-" * 50)
    
    try:
        # Import and run the training script
        sys.path.insert(0, os.getcwd())
        
        
        print("\n✅ Training completed successfully!")
        print("   Model saved to: fixhr_model/")
        print("   You can now use the AI features in the application")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        print("   Check the error message above for details")
        sys.exit(1)

if __name__ == "__main__":
    main()
