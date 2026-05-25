"""
Testing Guide for Family Finance AI
Complete QA checklist and test scenarios
"""

# ====================================================================================
# TESTING GUIDE - FAMILY FINANCE AI
# ====================================================================================

## Getting Started with Testing

### Prerequisites
- Python 3.8+
- All dependencies installed (see requirements_complete.txt)
- Fresh finance.db or test database
- Test accounts available

### Test Environment Setup

```bash
# Create test database
python -c "from database.enhanced_db import EnhancedDatabase; db = EnhancedDatabase('test_finance.db'); db.close()"

# Run test data generator
python scripts/generate_test_data.py

# Start application
python main_production.py
```

---

## TEST SCENARIOS

### 1. AUTHENTICATION & LOGIN

#### Test 1.1: Valid Login
- **Steps**:
  1. Start application
  2. Enter demo email: `parent@family.local`
  3. Enter password: `demo1234`
  4. Click Sign In
- **Expected**: 
  - Login page closes
  - Parent dashboard loads
  - Welcome message shows parent name

#### Test 1.2: Invalid Credentials
- **Steps**:
  1. Enter wrong password
  2. Click Sign In
- **Expected**: Error message displayed

#### Test 1.3: Demo Account Creation
- **Steps**:
  1. Login with first-time account
  2. Verify demo data created
- **Expected**:
  - Two sample children created (Alice, Bob)
  - Sample transactions added
  - Demo parent visible in profile

---

### 2. PARENT DASHBOARD

#### Test 2.1: Dashboard Loads
- **Steps**:
  1. Login with parent account
  2. Dashboard tab selected by default
- **Expected**:
  - Title: "Dashboard" visible
  - Welcome message: "Welcome, [Name]!"
  - Stats cards displayed (Income, Expenses, Savings, Allowances)
  - Recent expenses list shown

#### Test 2.2: Stats Calculate Correctly
- **Steps**:
  1. Check displayed stats
  2. Manually calculate expected values
  3. Compare with display
- **Expected**: All values match calculation

#### Test 2.3: Recent Expenses Display
- **Steps**:
  1. View recent expenses section
  2. Verify top 5 expenses shown
  3. Ordered by date DESC
- **Expected**:
  - Expenses properly formatted
  - Correct amounts displayed
  - Dates in readable format

---

### 3. EXPENSE MANAGEMENT

#### Test 3.1: Add Expense
- **Steps**:
  1. Click "Add Expense" button
  2. Select category: "Groceries"
  3. Enter amount: 45.99
  4. Enter description: "Weekly groceries"
  5. Confirm
- **Expected**:
  - Success message
  - Expense appears in recent list
  - Dashboard updates
  - Database saved correctly

#### Test 3.2: Add Multiple Expenses
- **Steps**:
  1. Add 5 different expenses
  2. Different categories
  3. Various amounts
- **Expected**:
  - All expenses saved
  - Dashboard totals update
  - No duplicates

#### Test 3.3: Edit Expense
- **Steps**:
  1. Add expense
  2. Click to edit
  3. Change amount
  4. Save changes
- **Expected**:
  - Original deleted
  - New values saved
  - Dashboard recalculates

#### Test 3.4: Delete Expense
- **Steps**:
  1. Add expense
  2. Delete it
  3. Confirm deletion
- **Expected**:
  - Removed from list
  - Dashboard totals update
  - Database reflects change

---

### 4. INCOME MANAGEMENT

#### Test 4.1: Add Income
- **Steps**:
  1. Click "Add Income" button
  2. Enter source: "Salary"
  3. Enter amount: 3000.00
  4. Confirm
- **Expected**:
  - Income recorded
  - Total income updates
  - Savings rate recalculates

#### Test 4.2: Monthly Income Calculation
- **Steps**:
  1. Add multiple income sources this month
  2. Check total displayed
- **Expected**: Sum of all incomes shown correctly

---

### 5. RECEIPT SCANNER

#### Test 5.1: Upload Receipt Image
- **Steps**:
  1. Navigate to Receipt Scanner
  2. Click "Choose Image"
  3. Select a receipt image
  4. Verify preview
- **Expected**:
  - Image displayed
  - Merchant extracted (or placeholder)
  - Amount field populated
  - Date shown

#### Test 5.2: Confirm Expense from Receipt
- **Steps**:
  1. Upload receipt
  2. Review extracted data
  3. Click "Save Expense"
- **Expected**:
  - Expense created
  - Linked to receipt
  - Dashboard updates

#### Test 5.3: Receipt History
- **Steps**:
  1. View Receipt History tab
  2. Upload multiple receipts
  3. Check history list
- **Expected**:
  - All receipts listed
  - Most recent first
  - Details show when selected

---

### 6. KID PROFILES & ALLOWANCES

#### Test 6.1: View Children
- **Steps**:
  1. Check left sidebar
  2. Verify all children listed
- **Expected**:
  - Alice and Bob shown
  - Clickable to switch
  - Names match database

#### Test 6.2: Add Allowance
- **Steps**:
  1. Add allowance to child
  2. Amount: $15.00
  3. Confirm
- **Expected**:
  - Child's savings increased
  - Allowance recorded
  - Payment date tracked

#### Test 6.3: Set Monthly Allowance
- **Steps**:
  1. Update child's monthly allowance
  2. Set to $20.00
  3. Save
- **Expected**:
  - Updated in database
  - Affects dashboard calculations
  - Future allowances use new amount

---

### 7. KIDS DASHBOARD

#### Test 7.1: Switch to Child View
- **Steps**:
  1. Click child name in sidebar
  2. Dashboard switches
- **Expected**:
  - Child's dashboard loads
  - Colorful, kid-friendly UI
  - Shows savings and points

#### Test 7.2: Piggy Bank Display
- **Steps**:
  1. View piggy bank widget
  2. Check savings amount
- **Expected**:
  - Correct balance shown
  - Formatted as currency
  - Visual representation clear

#### Test 7.3: Points Display
- **Steps**:
  1. View points widget
  2. Check point total
- **Expected**:
  - Current points shown
  - Star icon visible
  - Proper formatting

#### Test 7.4: Savings Goals
- **Steps**:
  1. View savings goals section
  2. Check existing goals
  3. Progress bars visible
- **Expected**:
  - All goals listed
  - Progress accurate
  - Percentages calculated correctly

#### Test 7.5: Achievement Badges
- **Steps**:
  1. View achievements section
  2. See earned badges
- **Expected**:
  - Badges displayed
  - Names and icons visible
  - Unlock conditions clear

#### Test 7.6: Financial Tips
- **Steps**:
  1. View financial tips section
  2. Click Previous/Next
  3. Rotate through all tips
- **Expected**:
  - All 4 tips display
  - Navigation works
  - Text age-appropriate

---

### 8. AI ADVISOR

#### Test 8.1: Open Chat
- **Steps**:
  1. Navigate to AI Advisor
  2. Chat interface visible
- **Expected**:
  - Input field ready
  - Send button enabled
  - Chat history visible (if exists)

#### Test 8.2: Send Message
- **Steps**:
  1. Type: "What is budgeting?"
  2. Click Send or press Enter
- **Expected**:
  - Message appears in chat
  - User message right-aligned
  - AI response follows

#### Test 8.3: Conversation History
- **Steps**:
  1. Send multiple messages
  2. Scroll up to see previous
  3. Refresh page
- **Expected**:
  - History preserved
  - Loads on next visit
  - All messages persist

#### Test 8.4: Different Questions
- **Steps**:
  1. Ask about different topics
  2. Spending, saving, budgeting, goals
- **Expected**:
  - Context-aware responses
  - Appropriate advice level
  - No errors

---

### 9. BUDGET MANAGEMENT

#### Test 9.1: Set Budget
- **Steps**:
  1. Navigate to Budgets
  2. Add budget for "Groceries"
  3. Set limit: $300.00
  4. Set alert threshold: 80%
- **Expected**:
  - Budget created
  - Appears in budget list
  - Tracked correctly

#### Test 9.2: Budget Tracking
- **Steps**:
  1. Add expenses in category
  2. Check budget usage
  3. Add more to trigger alert
- **Expected**:
  - Percentage calculated
  - Status updates (OK → Warning → Over)
  - Color coding changes

#### Test 9.3: Budget Alerts
- **Steps**:
  1. Approach budget limit
  2. Exceed limit
- **Expected**:
  - Alert shows warning
  - Notification triggered (if enabled)
  - Clear status message

---

### 10. UI/UX TESTING

#### Test 10.1: Responsive Layout
- **Steps**:
  1. Resize window
  2. Test at different sizes
  3. 1920x1080 → 1200x800
- **Expected**:
  - Layout adjusts smoothly
  - Content readable
  - No overlapping
  - Scrollbars appear when needed

#### Test 10.2: Theme Consistency
- **Steps**:
  1. Check all pages
  2. Verify colors match
  3. Font sizes consistent
- **Expected**:
  - Unified design
  - No mismatched colors
  - Proper spacing throughout

#### Test 10.3: Button Functionality
- **Steps**:
  1. Click all buttons
  2. Verify each works
- **Expected**:
  - No exceptions
  - Correct actions triggered
  - Visual feedback (hover/press)

#### Test 10.4: Input Validation
- **Steps**:
  1. Leave fields empty
  2. Enter invalid amounts
  3. Special characters
- **Expected**:
  - Validation prevents errors
  - Error messages shown
  - User can correct

---

### 11. DATABASE TESTING

#### Test 11.1: Data Persistence
- **Steps**:
  1. Add data
  2. Close app
  3. Reopen
  4. Verify data exists
- **Expected**:
  - Data saved to database
  - Loads on next session
  - No data loss

#### Test 11.2: Database Integrity
- **Steps**:
  1. Delete parent account
  2. Check children deleted too
- **Expected**:
  - Foreign keys enforced
  - Cascading deletes work
  - No orphaned records

#### Test 11.3: Concurrent Updates
- **Steps**:
  1. Multiple rapid updates
  2. Different features
- **Expected**:
  - All saved correctly
  - No conflicts
  - Consistent state

---

### 12. SETTINGS & PREFERENCES

#### Test 12.1: Open Settings
- **Steps**:
  1. Navigate to Settings
  2. All tabs visible
- **Expected**:
  - Theme, Notification, Privacy tabs
  - About tab shows info
  - Version number correct

#### Test 12.2: Change Settings
- **Steps**:
  1. Toggle notifications
  2. Change theme
  3. Click Save
- **Expected**:
  - Settings saved
  - Changes take effect
  - Persist on reload

#### Test 12.3: Data Backup
- **Steps**:
  1. Click "Backup My Data"
  2. Choose location
- **Expected**:
  - Backup file created
  - Contains all data
  - Can be restored

---

## PERFORMANCE TESTING

### Test 13.1: Large Dataset
- **Steps**:
  1. Add 1000+ transactions
  2. Generate reports
  3. Display charts
- **Expected**:
  - No lag or freezing
  - All data loads
  - Charts render smoothly

### Test 13.2: Memory Usage
- **Steps**:
  1. Monitor system memory
  2. Use app normally
  3. Check usage doesn't grow excessively
- **Expected**:
  - Stable memory usage
  - No memory leaks
  - Reasonable baseline

---

## BUG REPORTING

When you find a bug, document:
1. **Steps to Reproduce**: Exact steps to cause issue
2. **Expected**: What should happen
3. **Actual**: What actually happened
4. **Environment**: OS, Python version, etc.
5. **Screenshot/Log**: Include if helpful

---

## TEST CHECKLIST

- [ ] Login works with correct credentials
- [ ] Demo data loads on first login
- [ ] Dashboard displays all stats correctly
- [ ] Expenses can be added/edited/deleted
- [ ] Income tracking works
- [ ] Receipt scanner uploads images
- [ ] Kids dashboard shows gamification
- [ ] Points and achievements track
- [ ] Savings goals display with progress
- [ ] AI advisor responds to messages
- [ ] Budgets alert when exceeded
- [ ] Settings save and persist
- [ ] UI responsive at different sizes
- [ ] All buttons functional
- [ ] Data persists after restart
- [ ] No console errors
- [ ] Charts/graphs render properly
- [ ] Notifications work (if enabled)
- [ ] Export/backup features work
- [ ] Performance acceptable with large datasets

---

## KNOWN LIMITATIONS (Version 1.0)

- OCR requires pytesseract (manual setup needed)
- OpenAI integration uses mock responses
- Camera capture not yet implemented
- Single-user per database (shared device)
- No cloud sync
- No mobile companion app

---

## NEXT STEPS FOR TESTING

1. Run through all test scenarios
2. Document any issues found
3. Note feature requests
4. Test with real family data
5. Gather user feedback
6. Plan improvements for v1.1

---

**Test Coverage Target: 95%**
**Last Updated: 2024**
