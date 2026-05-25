# Family Finance AI - Premium Desktop Application

A sophisticated, production-ready PyQt5 family finance management application with AI-powered insights, dual interfaces for parents and kids, gamification, and modern fintech design.

## Features

### 🎯 Core Features

- **Dual Interface System**
  - Parent Dashboard: Comprehensive financial overview and analytics
  - Kids Dashboard: Gamified, child-friendly financial education
  - Multi-child support with individual profiles

- **Financial Management**
  - Income tracking with recurring income support
  - Expense management with categorization
  - Budget planning and monitoring
  - Monthly expense analytics
  - Net savings calculation

- **Allowance System**
  - Set monthly allowances per child
  - Track allowance payments
  - Automatic savings updates
  - Spending limits per child

- **Gamification (Kids)**
  - Virtual piggy bank with savings display
  - Points system with visual rewards
  - Achievement badges and milestones
  - Savings goals with progress tracking
  - Financial education tips and tips rotation

- **Receipt & Grocery Scanning**
  - Image upload and preview
  - OCR text extraction (pytesseract)
  - Automatic expense categorization
  - Receipt history tracking
  - Quick expense form population

- **AI Financial Advisor**
  - Chat-based financial guidance
  - Spending pattern analysis
  - Budget recommendations
  - Child-friendly or parent-level advice
  - Conversation history storage

- **Premium UI/UX**
  - Apple-like design aesthetic
  - Glassmorphism and neumorphism effects
  - Smooth animations and transitions
  - SF Pro Display font styling
  - Responsive layouts
  - Dark/Light theme support

- **Database System**
  - SQLite with normalized schema
  - Parent and child profiles
  - Complete transaction history
  - AI conversation storage
  - Achievements and points tracking
  - Budget and notification system

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB for application and data

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hazilmohamed990/family-finance-ai.git
cd family-finance-ai
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Optional Dependencies

For OCR support (receipt scanning):
```bash
# Windows
# Download pytesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Add Tesseract to PATH or set in code

# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr
```

## Configuration

### API Keys

Create a `.env` file in the project root:

```env
# OpenAI API Key for AI Advisor (optional)
OPENAI_API_KEY=your_key_here

# Database
DATABASE_PATH=./finance.db

# App Settings
APP_THEME=light
ENABLE_NOTIFICATIONS=true
ENABLE_OCR=true
```

### Font Setup

The app uses SF Pro Display font (Apple-designed). If not available:
- macOS: Automatically available
- Windows: Download from Apple Typography or use Segoe UI (default fallback)
- Linux: Install from font repository

## Usage

### Running the Application

```bash
python main_production.py
```

### Default Demo Account

```
Email: parent@family.local
Password: demo1234
```

The first login automatically creates:
- Demo parent account
- Two sample children: Alice (age 8) and Bob (age 9)
- Sample transactions and data

### Features Walkthrough

#### Parent Dashboard
1. **View Financial Overview**
   - Total income and expenses (current month)
   - Net savings calculation
   - Kids allowance total

2. **Add Expenses**
   - Click "Add Expense" button
   - Select category
   - Enter amount and description
   - Auto-saves to database

3. **Add Income**
   - Click "Add Income" button
   - Enter income source and amount
   - Optional: Set as recurring

4. **View Recent Expenses**
   - Automatically displayed on dashboard
   - Click to view details
   - Edit or delete as needed

5. **Receipt Scanning**
   - Upload receipt image
   - OCR extracts merchant and amount
   - Confirm details and save

6. **AI Financial Advisor**
   - Chat with AI for financial advice
   - Ask about budgeting, spending, goals
   - View conversation history

#### Kids Dashboard
1. **Virtual Piggy Bank**
   - Visual display of current savings
   - Automatic updates when money added/spent
   - Encouraging animations

2. **Points & Achievements**
   - View current points
   - Browse achievement badges
   - Unlock badges through financial goals

3. **Savings Goals**
   - Create personal savings goals
   - Set target amounts
   - Track progress with visual bars
   - Set deadlines

4. **Financial Tips**
   - Rotate through 4 educational tips
   - Learn about saving, budgeting, goals
   - Age-appropriate advice

5. **Quick Actions**
   - View allowance information
   - See spending history
   - Redeem points (placeholder)

## Database Schema

### Main Tables

- **parents**: Parent account information
- **children**: Child profiles and basic info
- **parent_expenses**: Expense records
- **parent_income**: Income records
- **child_savings**: Current and total savings per child
- **child_spending**: Child expense records
- **allowances**: Allowance payment history
- **points**: Points awarded to children
- **achievements**: Achievement badges earned
- **savings_goals**: Savings goals per child
- **receipts**: Scanned receipt information
- **ai_conversations**: Chat history with AI
- **budgets**: Budget limits per category
- **notifications**: System notifications

## Project Structure

```
family-finance-ai/
├── main_production.py              # Main application entry point
├── database/
│   ├── enhanced_db.py             # Complete database system
│   ├── db.py                      # Original database (legacy)
│   └── queries.py                 # Database queries
├── ui/
│   ├── theme.py                   # Color, font, and style system
│   ├── components.py              # Reusable UI components
│   ├── kids_dashboard.py          # Kids gamified interface
│   ├── ai_advisor.py              # AI chat interface
│   ├── receipt_scanner_new.py     # Receipt scanning UI
│   ├── sidebar.py                 # Navigation sidebar
│   ├── dashboard.py               # Parent dashboard
│   └── [other UI files]           # Additional pages
├── ai/
│   ├── chatbot.py                 # AI advisor chatbot
│   ├── analyzer.py                # Financial analysis
│   └── [other AI modules]         # ML and AI features
├── utils/
│   ├── app_helpers.py             # Helper functions and utilities
│   ├── validators.py              # Input validation
│   ├── constants.py               # App constants
│   └── [other utilities]          # Additional helpers
├── assets/
│   ├── images/                    # Logo and images
│   ├── icons/                     # UI icons
│   └── receipts/                  # Scanned receipts
├── data/                          # Data files
├── tests/                         # Unit tests
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── finance.db                    # SQLite database
```

## Code Quality

- **Architecture**: Modular, scalable design with clear separation of concerns
- **Styling**: Global QSS stylesheet with component-specific overrides
- **Database**: Normalized SQLite with proper foreign keys and indexing
- **Error Handling**: Try-catch blocks with user-friendly error messages
- **Documentation**: Docstrings on all classes and methods
- **Type Hints**: Python type annotations for clarity

## Customization

### Change Color Scheme

Edit `ui/theme.py`:

```python
class Colors:
    ACCENT = "#YourColorHere"  # Change primary color
    INCOME = "#GreenColor"      # Change income color
    EXPENSE = "#RedColor"       # Change expense color
    # ... more colors
```

### Add New Categories

Edit `ParentDashboard.add_expense_dialog()`:

```python
category, ok = QInputDialog.getItem(
    self, "Add Expense", "Category:",
    ["YourCategory", "Another", ...],  # Add here
    editable=False
)
```

### Customize Child Achievements

Edit `PointsHelper.get_achievement_badges()` in `utils/app_helpers.py`:

```python
"your_badge": {
    "name": "Badge Name",
    "description": "How to earn it",
    "icon": "🏆",
}
```

## Troubleshooting

### Issue: Application won't start

**Solution**: Check Python version and dependencies
```bash
python --version  # Should be 3.8+
pip list          # Verify PyQt5 is installed
```

### Issue: Database errors

**Solution**: Delete `finance.db` and restart (creates fresh database)
```bash
rm finance.db
python main_production.py
```

### Issue: Font looks wrong

**Solution**: Install SF Pro font or check fallback fonts in `ui/theme.py`

### Issue: OCR not working

**Solution**: Install tesseract-ocr and set path in environment

## Contributing

To extend the application:

1. Add new features in appropriate modules
2. Update database schema in `database/enhanced_db.py` if needed
3. Add UI components in `ui/` directory
4. Update README and documentation
5. Test thoroughly before committing

## Performance Optimization

- Database queries are optimized with proper indexing
- UI renders efficiently with lazy loading
- Charts use lightweight rendering
- Image scaling done at display time
- Smooth animations use Qt's built-in animation framework

## Security Considerations

- Passwords hashed with SHA-256 (production: use bcrypt)
- Input validation on all user data
- SQL injection prevention with parameterized queries
- Sensitive data stored securely in database
- No credentials hardcoded in source

## Future Enhancements

- [ ] Multi-family support
- [ ] Cloud synchronization
- [ ] Mobile app companion
- [ ] Advanced ML predictions
- [ ] Real receipt OCR integration
- [ ] Multi-language support
- [ ] Charts with PyQtGraph
- [ ] Email/SMS notifications
- [ ] Parent approval workflow for large purchases
- [ ] Automatic category suggestions

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@familyfinanceai.local
- Documentation: [Full Wiki](docs/)

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- Designed with modern fintech best practices
- UI inspired by Apple's design language
- Educational features for financial literacy
- Built with PyQt5 for desktop excellence

---

**Made with ❤️ for families managing finances together**

Version 1.0.0 | Last Updated: 2024
