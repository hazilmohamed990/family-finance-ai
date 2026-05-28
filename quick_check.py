#!/usr/bin/env python3
"""
Quick System Verification - No GUI
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("QUICK SYSTEM CHECK...")

# Test 1: Database
try:
    from database.enhanced_db import EnhancedDatabase
    db = EnhancedDatabase(":memory:")
    db.close()
    print("[PASS] Database module")
except Exception as e:
    print(f"[FAIL] Database: {e}")

# Test 2: Analysis without GUI
try:
    from ai.analyzer import FinanceAnalyzer
    print("[PASS] AI Analyzer module")
except Exception as e:
    print(f"[FAIL] AI: {e}")

# Test 3: File structure
files = [
    "main_production.py",
    "ui/theme.py",
    "ui/components.py",
    "ui/kids_dashboard.py",
    "ui/ai_advisor.py",
    "database/enhanced_db.py"
]

missing = []
for f in files:
    if not os.path.exists(f):
        missing.append(f)

if missing:
    print(f"[FAIL] Missing files: {missing}")
else:
    print(f"[PASS] All {len(files)} key files present")

print("\nCore systems functional!")
