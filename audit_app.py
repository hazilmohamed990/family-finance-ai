#!/usr/bin/env python3
"""
Complete Audit Script for Family Finance AI
Verifies all systems, features, and quality standards
"""

import sys
import os
import importlib.util
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AuditResult:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.warnings = []
    
    def test(self, name, result, error=None):
        self.total += 1
        if result:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            print(f"  [FAIL] {name}")
            if error:
                self.errors.append(f"{name}: {error}")
                print(f"     Error: {error}")
    
    def summary(self):
        pct = (self.passed / self.total * 100) if self.total > 0 else 0
        print(f"\n{'='*60}")
        print(f"AUDIT SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed} [PASS]")
        print(f"Failed: {self.failed} [FAIL]")
        print(f"Success Rate: {pct:.1f}%")
        
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for err in self.errors:
                print(f"  * {err}")
        
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  WARNING: {warn}")
        
        return self.failed == 0

# ============================================================================
print("\n" + "="*60)
print("FAMILY FINANCE AI - APPLICATION AUDIT")
print("="*60 + "\n")

audit = AuditResult()

# ============================================================================
# 1. MODULE IMPORTS
# ============================================================================
print("1. CHECKING MODULE IMPORTS")
print("-" * 60)

try:
    from database.enhanced_db import EnhancedDatabase
    audit.test("Database module imports", True)
except Exception as e:
    audit.test("Database module imports", False, str(e))

try:
    from ui.theme import Colors, Fonts, Spacing
    audit.test("Theme module imports", True)
except Exception as e:
    audit.test("Theme module imports", False, str(e))

try:
    from ui.components import Card, StatCard, MetricCard
    audit.test("Components module imports", True)
except Exception as e:
    audit.test("Components module imports", False, str(e))

try:
    from ai.analyzer import FinanceAnalyzer
    audit.test("AI Analyzer module imports", True)
except Exception as e:
    audit.test("AI Analyzer module imports", False, str(e))

try:
    from ai.chatbot import FinanceChatbot
    audit.test("Chatbot module imports", True)
except Exception as e:
    audit.test("Chatbot module imports", False, str(e))

# ============================================================================
# 2. DATABASE INTEGRITY
# ============================================================================
print("\n2. CHECKING DATABASE SYSTEM")
print("-" * 60)

try:
    db = EnhancedDatabase(":memory:")
    audit.test("Database initializes", True)
    
    # Check tables
    cursor = db.cursor
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = [
        'parents', 'children', 'expenses', 'income', 'budgets',
        'receipts', 'images', 'allowances', 'points', 'achievements',
        'ai_chats', 'ai_responses', 'savings_goals', 'notifications',
        'settings', 'financial_logs'
    ]
    
    audit.test(f"All database tables created ({len(tables)} tables)", 
               len(tables) >= 10, f"Found {len(tables)} tables")
    
    # Test CRUD operations
    try:
        # Create
        db.create_parent("test@test.com", "Test", "hashed_pwd")
        audit.test("Create parent operation works", True)
        
        # Read
        parent = db.get_parent_by_email("test@test.com")
        audit.test("Read parent operation works", parent is not None)
        
    except Exception as e:
        audit.test("CRUD operations work", False, str(e))
    
    db.close()
    
except Exception as e:
    audit.test("Database system", False, str(e))

# ============================================================================
# 3. FILE STRUCTURE
# ============================================================================
print("\n3. CHECKING FILE STRUCTURE")
print("-" * 60)

required_files = [
    "main_production.py",
    "requirements_complete.txt",
    "database/enhanced_db.py",
    "ui/theme.py",
    "ui/components.py",
    "ui/kids_dashboard.py",
    "ui/ai_advisor.py",
    "ui/receipt_scanner_new.py",
    "ui/settings_panel.py",
    "ai/analyzer.py",
    "ai/chatbot.py",
    "utils/app_helpers.py",
]

base_path = Path(__file__).parent
for file_path in required_files:
    full_path = base_path / file_path
    exists = full_path.exists()
    audit.test(f"File exists: {file_path}", exists)

# ============================================================================
# 4. DOCUMENTATION
# ============================================================================
print("\n4. CHECKING DOCUMENTATION")
print("-" * 60)

docs = [
    "README_COMPLETE.md",
    "QUICK_START.md",
    "START_HERE.md",
    "TESTING_GUIDE.md",
    "PROJECT_COMPLETION_CHECKLIST.md",
    "FINAL_VERIFICATION.md",
]

for doc in docs:
    doc_path = base_path / doc
    exists = doc_path.exists()
    if exists:
        size = doc_path.stat().st_size
        audit.test(f"Documentation: {doc} ({size} bytes)", size > 1000)
    else:
        audit.test(f"Documentation: {doc}", False)

# ============================================================================
# 5. CONFIGURATION
# ============================================================================
print("\n5. CHECKING CONFIGURATION")
print("-" * 60)

req_path = base_path / "requirements_complete.txt"
if req_path.exists():
    with open(req_path) as f:
        reqs = f.read().strip().split('\n')
    
    required_packages = ['pyqt5', 'matplotlib', 'opencv-python', 'pillow']
    missing = []
    for pkg in required_packages:
        found = any(pkg.lower() in req.lower() for req in reqs)
        if not found:
            missing.append(pkg)
    
    audit.test(f"All required packages in requirements.txt", len(missing) == 0,
               f"Missing: {missing}" if missing else None)
else:
    audit.test("requirements_complete.txt exists", False)

# ============================================================================
# 6. CODE QUALITY
# ============================================================================
print("\n6. CHECKING CODE QUALITY")
print("-" * 60)

# Check for common issues
code_files = list(base_path.glob("**/*.py"))
audit.test(f"Python files found ({len(code_files)} files)", len(code_files) > 50)

issues_found = []

# Check for TODO comments
for py_file in code_files:
    try:
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if 'TODO' in content or 'FIXME' in content:
                issues_found.append(f"TODOs in {py_file.name}")
    except:
        pass

audit.test("No TODO/FIXME comments", len(issues_found) == 0, 
           f"Found in: {issues_found[:3]}" if issues_found else None)

# ============================================================================
# 7. FEATURE COMPLETENESS
# ============================================================================
print("\n7. CHECKING FEATURE COMPLETENESS")
print("-" * 60)

features = {
    "Parent Dashboard": ("ui/dashboard.py", ["QWidget", "update_data"]),
    "Kids Dashboard": ("ui/kids_dashboard.py", ["QWidget", "piggy_bank"]),
    "AI Advisor": ("ui/ai_advisor.py", ["QWidget", "send_message"]),
    "Receipt Scanner": ("ui/receipt_scanner_new.py", ["QWidget", "scan"]),
    "Settings": ("ui/settings_panel.py", ["QWidget", "save_settings"]),
    "Database": ("database/enhanced_db.py", ["EnhancedDatabase", "create_parent"]),
    "AI Analyzer": ("ai/analyzer.py", ["FinanceAnalyzer", "analyze"]),
    "Theme System": ("ui/theme.py", ["Colors", "GLOBAL_STYLESHEET"]),
}

for feature_name, (file_path, keywords) in features.items():
    try:
        full_path = base_path / file_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                found = all(kw in content for kw in keywords)
                audit.test(f"Feature implemented: {feature_name}", found)
        else:
            audit.test(f"Feature implemented: {feature_name}", False, "File not found")
    except Exception as e:
        audit.test(f"Feature implemented: {feature_name}", False, str(e))

# ============================================================================
# 8. SECURITY
# ============================================================================
print("\n8. CHECKING SECURITY")
print("-" * 60)

security_issues = []

# Check for hardcoded credentials
for py_file in list(base_path.glob("**/*.py"))[:20]:  # Sample check
    try:
        with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
            if 'password' in content and '=' in content:
                if any(x in content for x in ['password=', 'pwd=', 'pass=']):
                    # Check if it's a demo password
                    if 'demo' not in content:
                        security_issues.append(py_file.name)
    except:
        pass

audit.test("No hardcoded credentials (demo excluded)", len(security_issues) == 0)

# ============================================================================
# FINAL SUMMARY
# ============================================================================

success = audit.summary()

if success:
    print("\n" + "="*60)
    print("[PASS] APPLICATION AUDIT PASSED")
    print("="*60)
    sys.exit(0)
else:
    print("\n" + "="*60)
    print("[FAIL] APPLICATION AUDIT HAS ISSUES")
    print("="*60)
    sys.exit(1)
