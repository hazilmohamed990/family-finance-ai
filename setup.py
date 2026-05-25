"""
Setup Script for Family Finance AI
Automatic installation and configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_step(number, text):
    """Print step"""
    print(f"\n[{number}] {text}")


def check_python_version():
    """Check Python version"""
    print_step(1, "Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ✗ ERROR: Python 3.8+ required!")
        return False
    
    print("   ✓ Python version OK")
    return True


def check_directory():
    """Check project directory"""
    print_step(2, "Checking project directory...")
    
    required_dirs = [
        'ui', 'database', 'ai', 'utils', 'assets',
        'tests', 'data', 'styles'
    ]
    
    for dir_name in required_dirs:
        if not os.path.isdir(dir_name):
            print(f"   ✗ Missing directory: {dir_name}")
            return False
    
    print("   ✓ All required directories present")
    return True


def create_virtual_env():
    """Create virtual environment"""
    print_step(3, "Creating virtual environment...")
    
    if os.path.exists('venv'):
        print("   ✓ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("   ✓ Virtual environment created")
        return True
    except Exception as e:
        print(f"   ✗ Error creating venv: {e}")
        return False


def get_pip_command():
    """Get pip command for current OS"""
    if platform.system() == 'Windows':
        return ['venv\\Scripts\\pip']
    else:
        return ['venv/bin/pip']


def install_dependencies():
    """Install dependencies"""
    print_step(4, "Installing dependencies...")
    
    pip_cmd = get_pip_command()
    requirements = 'requirements_complete.txt'
    
    if not os.path.exists(requirements):
        print(f"   ⚠ {requirements} not found, using fallback")
        requirements = 'requirements.txt'
    
    try:
        subprocess.run(pip_cmd + ['install', '-r', requirements], check=True)
        print("   ✓ Dependencies installed")
        return True
    except Exception as e:
        print(f"   ✗ Error installing dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print_step(5, "Creating required directories...")
    
    dirs = [
        'assets/images',
        'assets/icons',
        'assets/receipts',
        'data',
    ]
    
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"   ✓ {dir_name}")


def create_env_file():
    """Create .env file if not exists"""
    print_step(6, "Setting up environment file...")
    
    env_file = '.env'
    if os.path.exists(env_file):
        print("   ✓ .env file already exists")
        return
    
    env_content = """# Family Finance AI Configuration

# OpenAI API Key (optional - for AI advisor)
# OPENAI_API_KEY=your_key_here

# Database
DATABASE_PATH=./finance.db

# App Settings
APP_THEME=light
ENABLE_NOTIFICATIONS=true
ENABLE_OCR=false
ENABLE_CAMERA=false

# Tesseract OCR (if using OCR)
# TESSERACT_PATH=/usr/share/tesseract-ocr/tessdata (Linux)
# TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR (Windows)
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("   ✓ .env file created")


def create_test_data():
    """Create test database"""
    print_step(7, "Initializing database...")
    
    try:
        from database.enhanced_db import EnhancedDatabase
        db = EnhancedDatabase("finance.db")
        
        # Create demo parent and children
        parent_id = db.add_parent(
            "parent@family.local",
            "Demo Parent",
            "demo1234"
        )
        
        # Create demo children
        alice_id = db.add_child(parent_id, "Alice", age=8, monthly_allowance=15)
        bob_id = db.add_child(parent_id, "Bob", age=10, monthly_allowance=20)
        
        # Add initial savings
        db.add_to_child_savings(alice_id, 50)
        db.add_to_child_savings(bob_id, 75)
        
        # Add sample points
        db.add_points(alice_id, 150, "Welcome bonus")
        db.add_points(bob_id, 200, "Welcome bonus")
        
        # Add sample achievements
        db.add_achievement(alice_id, "badge", "First Step", "Made your first transaction")
        db.add_achievement(bob_id, "badge", "Saver", "Saved $50")
        
        # Add sample expenses
        db.add_parent_expense(parent_id, "Groceries", 75.50, "Weekly shopping", "2024-05-20")
        db.add_parent_expense(parent_id, "Utilities", 120.00, "Electric bill", "2024-05-19")
        
        # Add sample income
        db.add_parent_income(parent_id, "Salary", 4000, "2024-05-15", True, "monthly")
        
        db.close()
        print("   ✓ Database initialized with demo data")
        return True
    except Exception as e:
        print(f"   ⚠ Could not create demo data: {e}")
        return False


def verify_imports():
    """Verify critical imports"""
    print_step(8, "Verifying imports...")
    
    imports = [
        ('PyQt5.QtWidgets', 'PyQt5'),
        ('PyQt5.QtCore', 'PyQt5'),
        ('database.enhanced_db', 'Database module'),
        ('ui.theme', 'Theme module'),
        ('ui.components', 'Components module'),
    ]
    
    all_ok = True
    for module, name in imports:
        try:
            __import__(module)
            print(f"   ✓ {name}")
        except ImportError:
            print(f"   ✗ {name} - NOT FOUND")
            all_ok = False
    
    return all_ok


def print_instructions():
    """Print final instructions"""
    print_header("SETUP COMPLETE!")
    print("\n✓ Family Finance AI is ready to use!\n")
    
    print("To start the application, run:\n")
    
    if platform.system() == 'Windows':
        print("   venv\\Scripts\\activate")
        print("   python main_production.py\n")
    else:
        print("   source venv/bin/activate")
        print("   python main_production.py\n")
    
    print("Default Login Credentials:")
    print("   Email: parent@family.local")
    print("   Password: demo1234\n")
    
    print("Quick Links:")
    print("   • Documentation: README_COMPLETE.md")
    print("   • Testing Guide: TESTING_GUIDE.md")
    print("   • API Reference: docs/")
    print()


def main():
    """Main setup flow"""
    print_header("FAMILY FINANCE AI - SETUP WIZARD")
    
    print(f"\nOperating System: {platform.system()}")
    print(f"Python Version: {sys.version}")
    
    # Run checks
    if not check_python_version():
        return False
    
    if not check_directory():
        print("\n✗ Please run setup from project root directory!")
        return False
    
    if not create_virtual_env():
        return False
    
    if not install_dependencies():
        print("\n⚠ Dependency installation failed. You may need to:")
        print("  - Manually install: pip install -r requirements_complete.txt")
        print("  - Check internet connection")
        print("  - Check Python version compatibility")
    
    create_directories()
    create_env_file()
    
    print_step(7, "Initializing database...")
    if create_test_data():
        pass
    
    if verify_imports():
        print_instructions()
        return True
    else:
        print("\n✗ Import verification failed!")
        print("   Please check installation and try again.")
        return False


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
