# Quick Start Guide - Family Finance AI

## 🚀 Get Started in 2 Minutes

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

#### Option 1: Automated Setup (Recommended)
```bash
cd family-finance-ai
python setup.py
```

The setup script will:
- Create a virtual environment
- Install all dependencies
- Initialize the database with demo data
- Configure environment variables

#### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements_complete.txt

# 4. Run application
python main_production.py
```

---

## 📝 Demo Credentials

```
Email:    parent@family.local
Password: demo1234
```

**First Login**: The app automatically creates:
- Demo parent account
- 2 sample children (Alice, age 8 & Bob, age 10)
- Sample financial data
- Demo transactions

---

## 🎯 Quick Navigation

### Parent Dashboard
- **View Financial Overview**: See total income, expenses, savings on home screen
- **Add Expense**: Click "Add Expense" button → Select category → Enter amount
- **Add Income**: Click "Add Income" button → Enter source and amount
- **View Recent Expenses**: Displayed automatically on dashboard

### Kids Dashboard
- **Switch to Kids View**: Click child name in left sidebar
- **View Piggy Bank**: Shows total savings with emoji piggy
- **Check Points**: Star icon displays current points
- **See Goals**: Progress bars show savings goal status
- **Read Tips**: Financial education tips with navigation

### Features

#### Receipt Scanner
1. Go to Receipts tab (in menu)
2. Click "Choose Image" or "Take Photo"
3. Select receipt image
4. Confirm extracted data
5. Click "Save Expense"

#### AI Advisor
1. Open AI Advisor
2. Type your question about finances
3. Click Send or press Enter
4. AI provides response
5. Conversation saved automatically

#### Settings
1. Click Settings in left sidebar
2. Choose tab: App Settings, Notifications, Privacy, About
3. Make changes
4. Click "Save Settings"

---

## 📊 Understanding the Dashboard

### Parent Dashboard Metrics

**Total Income**
- Sum of all income this month
- Shows month-to-date (MTD)
- Updated automatically

**Total Expenses**
- Sum of all expenses this month
- Broken down by category
- Shows spending trends

**Net Savings**
- Income minus expenses (YTD)
- Indicates financial health
- Green if positive

**Kids Allowances**
- Total allowance paid this month
- Sum across all children
- Tracks family budget

### Kids Dashboard Metrics

**Piggy Bank**
- Total savings balance
- Visual representation
- Updates with transactions

**Points**
- Current point total
- Earned through actions
- Can be redeemed

**Achievements**
- Earned badges
- Shows milestones hit
- Unlock criteria visible

---

## 💡 Common Tasks

### Add an Expense

1. Click "Add Expense"
2. Select category:
   - Groceries
   - Utilities
   - Transport
   - Entertainment
   - Health
   - Other
3. Enter amount (e.g., 45.99)
4. Add description (optional)
5. Click "Save"

### Add Income

1. Click "Add Income"
2. Enter income source (e.g., "Salary")
3. Enter amount
4. Click "Save"

### Give Child Allowance

1. Go to parent dashboard
2. Click "Add Allowance" (when implemented)
3. Select child
4. Enter amount
5. Click "Save"

Child's savings auto-update!

### Create Savings Goal

1. Switch to child's dashboard
2. Click "Add Goal" (when implemented)
3. Set goal name (e.g., "Bike")
4. Enter target amount
5. Set deadline (optional)
6. Click "Create"

Progress updates automatically as savings increase!

### View Budget Status

1. Go to Budgets section
2. Check spending vs limit
3. See alert status:
   - ✓ OK (green) - Under 80%
   - ⚠ Warning (yellow) - 80-100%
   - ✗ Over (red) - Exceeded

---

## 🎓 Financial Tips

### For Parents

1. **Track All Spending**: Log expenses regularly for accurate analysis
2. **Set Realistic Budgets**: Base on actual spending patterns
3. **Review Monthly**: Check dashboard at month end
4. **Plan Allowances**: Consider income when setting kids' allowances
5. **Use AI Advisor**: Ask for budgeting recommendations

### For Kids

1. **Save First**: Set aside savings before spending
2. **Track Goals**: Create realistic savings targets
3. **Earn Points**: Good financial decisions earn rewards
4. **Learn Patterns**: Understand where money goes
5. **Ask Questions**: Use chat to learn about money

---

## ⚙️ Customization

### Change Theme

1. Go to Settings
2. Select "App Settings" tab
3. Choose theme: Light, Dark, or Auto
4. Click "Save Settings"

### Choose Currency

1. Go to Settings
2. Select "App Settings" tab
3. Choose currency: USD, EUR, GBP, JPY
4. Click "Save Settings"

### Set Accent Color

1. Go to Settings
2. Select "App Settings" tab
3. Click "Choose Color"
4. Select desired color
5. Click "Save Settings"

---

## 🐛 Troubleshooting

### App Won't Start
- Check Python version: `python --version` (should be 3.8+)
- Try deleting `finance.db` and restarting
- Check for error messages in console

### Demo Data Missing
- Delete `finance.db`
- Restart application
- Login with demo credentials again

### Database Error
- Close all instances
- Delete `finance.db`
- Run setup again: `python setup.py`

### Import Errors
- Reinstall dependencies: `pip install -r requirements_complete.txt`
- Check virtual environment is activated

### UI Looks Wrong
- SF Pro Display font may not be installed
- Falls back to Segoe UI on Windows automatically
- Install SF Pro from Apple for best appearance

---

## 📚 Learning More

### Full Documentation
See `README_COMPLETE.md` for comprehensive guide

### Testing Guide
See `TESTING_GUIDE.md` for feature testing

### Setup Help
See `setup.py` for installation details

### Code Documentation
Check docstrings in source files for details

---

## 🎉 Have Fun!

Family Finance AI is designed to make managing family finances fun and educational!

- **Parents**: Get insights and control
- **Kids**: Learn financial responsibility
- **Family**: Build healthy money habits together

---

## 💬 Support

For issues:
1. Check TESTING_GUIDE.md troubleshooting section
2. Review README_COMPLETE.md FAQ
3. Check error logs in console
4. Verify database hasn't been corrupted

---

**Enjoy managing your family finances! 💰**

Version 1.0.0 | 2024
