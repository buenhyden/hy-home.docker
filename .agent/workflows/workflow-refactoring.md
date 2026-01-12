---
description: Code refactoring workflow for improving code quality and maintainability
---

1. **Identify code smells**

    Analyze codebase for common anti-patterns and improvement opportunities.

    **Run automated analysis:**

    // turbo

    ```bash
    # JavaScript/TypeScript - Code complexity
    npx escomplex src/**/*.ts --format markdown > reports/complexity.md

    # Python - Code smells
    uv pip install pylint radon
    pylint src --reports=y > reports/pylint-report.txt
    radon cc src -a -nb > reports/complexity.txt

    # Check for duplicated code
    npx jscpd src
    ```

    **Common code smells to look for:**

    - Functions > 20 lines
    - Classes > 200 lines
    - Cyclomatic complexity > 10
    - Duplicated code blocks
    - Deep nesting (> 3 levels)
    - Long parameter lists (> 4 parameters)
    - God classes/functions

2. **Prioritize refactoring targets**

    Create refactoring backlog based on impact and risk.

    **Priority matrix:**

    - **High Priority**: High complexity + frequently changed
    - **Medium Priority**: High complexity OR frequently changed  
    - **Low Priority**: Low complexity + rarely changed

    ```bash
    # Find most frequently changed files
    git log --format=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20
    ```

3. **Write characterization tests**

    Before refactoring, ensure existing behavior is tested.

    **Create tests for current behavior:**

    ```python
    # tests/characterization/test_legacy_payment.py
    def test_process_payment_current_behavior():
        """
        Characterization test: Documents current behavior before refactoring.
        DO NOT change without reviewing impact.
        """
        result = process_payment(amount=100, currency='USD')
        
        # Document exact current behavior (even if seems wrong)
        assert result['status'] == 'success'
        assert result['fee'] == 2.5  # Current calculation
    ```

4. **Run all tests as baseline**

    Ensure all existing tests pass before refactoring.

    // turbo

    ```bash
    # JavaScript/TypeScript
    npm test -- --coverage

    # Python
    pytest --cov=src

    # Record baseline
    npm test > test-baseline.txt
    ```

    Expected: 100% tests passing. If not, fix tests first.

5. **Apply refactoring patterns**

    Use established refactoring techniques.

    **Extract Method:**

    ```typescript
    // Before: Long function
    function processOrder(order) {
      // Validate order (10 lines)
      if (!order.items) throw new Error('No items');
      if (order.items.length === 0) throw new Error('Empty');
      for (const item of order.items) {
        if (!item.price || item.price <= 0) throw new Error('Invalid price');
      }
      
      // Calculate total (15 lines)
      let subtotal = 0;
      for (const item of order.items) {
        subtotal += item.price * item.quantity;
      }
      const tax = subtotal * 0.1;
      const total = subtotal + tax;
      
      // Apply discount (10 lines)
      // ...
    }

    // After: Extracted methods
    function processOrder(order) {
      validateOrder(order);
      const total = calculateOrderTotal(order);
      applyDiscounts(order, total);
      return total;
    }

    function validateOrder(order) {
      if (!order.items?.length) throw new Error('No items');
      order.items.forEach(validateItem);
    }

    function calculateOrderTotal(order) {
      const subtotal = order.items.reduce((sum, item) => 
        sum + item.price * item.quantity, 0);
      return subtotal * 1.1; // Including 10% tax
    }
    ```

    **Extract Class:**

    ```python
    # Before: God class
    class UserManager:
        def create_user(self): ...
        def send_welcome_email(self): ...
        def validate_email(self): ...
        def hash_password(self): ...
        def check_password_strength(self): ...
        def log_user_activity(self): ...
        # 20+ methods

    # After: Separated concerns
    class UserService:
        def create_user(self): ...
        
    class EmailService:
        def send_welcome_email(self): ...
        def validate_email(self): ...
        
    class PasswordService:
        def hash_password(self): ...
        def check_password_strength(self): ...
        
    class ActivityLogger:
        def log_user_activity(self): ...
    ```

6. **Run tests after each change**

    Verify behavior hasn't changed after each refactoring step.

    // turbo

    ```bash
    # Run tests frequently
    npm test

    # Or use watch mode
    npm run test:watch
    ```

    **Refactoring rule**: Tests must pass after EVERY change.

7. **Improve naming**

    Rename variables/functions/classes to better reflect intent.

    **Before:**

    ```javascript
    function calc(a, b, c) {
      const x = a * b;
      const y = x * c;
      return y;
    }
    ```

    **After:**

    ```javascript
    function calculateTotalPriceWithTax(
      unitPrice: number,
      quantity: number,
      taxRate: number
    ): number {
      const subtotal = unitPrice * quantity;
      const totalWithTax = subtotal * (1 + taxRate);
      return totalWithTax;
    }
    ```

8. **Reduce complexity**

    Break down complex functions.

    **Target**: Cyclomatic complexity < 10

    **Techniques:**

    - Extract methods
    - Replace conditionals with polymorphism
    - Use guard clauses (early returns)
    - Replace nested loops with helper functions

    ```typescript
    // Before: High complexity (12)
    function renderUserStatus(user) {
      if (user) {
        if (user.isActive) {
          if (user.subscription) {
            if (user.subscription.isPaid) {
              return 'Premium Active';
            } else {
              return 'Free Active';
            }
          } else {
            return 'No Subscription';
          }
        } else {
          return 'Inactive';
        }
      } else {
        return 'No User';
      }
    }

    // After: Lower complexity (4)
    function renderUserStatus(user) {
      if (!user) return 'No User';
      if (!user.isActive) return 'Inactive';
      if (!user.subscription) return 'No Subscription';
      
      return user.subscription.isPaid ? 'Premium Active' : 'Free Active';
    }
    ```

9. **Eliminate duplication**

    Apply DRY (Don't Repeat Yourself) principle.

    ```typescript
    // Before: Duplicated logic
    function sendEmailToUser(user) {
      const transport = nodemailer.createTransport({...});
      const mailOptions = {to: user.email, from: 'noreply@example.com'};
      transport.sendMail(mailOptions);
    }

    function sendEmailToAdmin(admin) {
      const transport = nodemailer.createTransport({...});
      const mailOptions = {to: admin.email, from: 'noreply@example.com'};
      transport.sendMail(mailOptions);
    }

    // After: Extracted common logic
    function sendEmail(recipient: string, content: EmailContent) {
      const transport = nodemailer.createTransport({...});
      const mailOptions = {
        to: recipient,
        from: 'noreply@example.com',
        ...content
      };
      return transport.sendMail(mailOptions);
    }
    ```

10. **Run full test suite**

    Execute comprehensive test suite after refactoring.

    // turbo

    ```bash
    npm test -- --coverage
    ```

    Compare with baseline from step 4.
    Expected: Same or better coverage, all tests passing.

11. **Check code quality metrics**

    Verify improvements in code quality.

    // turbo

    ```bash
    # JavaScript - Check complexity improved
    npx escomplex src/**/*.ts

    # Python - Check metrics
    radon cc src -a -nb
    radon mi src -nb  # Maintainability index

    # Compare with initial reports
    diff reports/complexity-before.txt reports/complexity-after.txt
    ```

    **Target improvements:**

    - Average complexity reduced
    - Maintainability index increased
    - Code duplication decreased

12. **Update documentation**

    Document refactored code with clear comments/docstrings.

    ```typescript
    /**
     * Calculates the total price including tax.
     * 
     * @param unitPrice - Price per unit in dollars
     * @param quantity - Number of units
     * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
     * @returns Total price including tax
     * 
     * @example
     * calculateTotalPriceWithTax(100, 2, 0.1) // Returns 220
     */
    function calculateTotalPriceWithTax(
      unitPrice: number,
      quantity: number,
      taxRate: number
    ): number {
      const subtotal = unitPrice * quantity;
      return subtotal * (1 + taxRate);
    }
    ```

13. **Commit refactoring**

    Create clear commit message.

    ```bash
    git add .
    git commit -m "refactor: simplify order processing logic

    - Extracted validation into separate functions
    - Reduced cyclomatic complexity from 15 to 6
    - Improved naming for better readability
    - All tests still passing"
    ```

14. **Code review**

    Request peer review for refactored code.

    **Review checklist:**

    - [ ] Behavior unchanged (all tests pass)
    - [ ] Code more readable
    - [ ] Complexity reduced
    - [ ] No new bugs introduced
    - [ ] Documentation updated

    **Next Steps:**

    - Review `agent/rules/097-core-implement-task-specific.md` for refactoring patterns
    - Consider performance profiling if refactoring affects hot paths
    - Schedule regular refactoring sessions
