---
description: Comprehensive security audit workflow based on OWASP and security best practices
---

1. **Review secrets and credentials**

    Check for hardcoded secrets, API keys, passwords, or tokens in the codebase.

    ```bash
    # Search for common secret patterns
    git grep -i "api_key\|password\|secret\|token\|credentials" -- ':!*.md' ':!*.lock' ':!*.sum'
    ```

    Review results carefully. Any found secrets should be:
    - Removed from code
    - Moved to environment variables
    - Rotated if already committed

    **Critical**: Check `.env*` files are in `.gitignore`.

2. **OWASP Top 10 verification**

    Review code against OWASP Top 10 vulnerabilities based on `700-Security` rules.

    **A01 - Broken Access Control:**
    - Verify all endpoints have proper authentication
    - Check for IDOR (Insecure Direct Object Reference)
    - Ensure users can only access their own resources

    ```bash
    # Search for unprotected routes/endpoints
    git grep -n "router\.\|@app\.\|@Get\|@Post" 
    ```

    Review each route for authentication/authorization middleware.

    **A02 - Cryptographic Failures:**
    - Verify HTTPS is enforced in production
    - Check password hashing (bcrypt, argon2, never plain text)
    - Ensure sensitive data is encrypted at rest

    **A03 - Injection:**
    - SQL: All queries use parameterized statements (no string concatenation)
    - NoSQL: Validate and sanitize all inputs
    - Command: No shell command execution with user input

    ```bash
    # Check for SQL injection risks
    git grep -n "execute\|query.*+\|query.*\$\|query.*f\""
    ```

    **A04 - Insecure Design:**
    - Review authentication flow
    - Check rate limiting on sensitive endpoints
    - Verify security requirements in design

    **A05 - Security Misconfiguration:**
    - Check for debug mode disabled in production
    - Verify error messages don't leak information
    - Ensure security headers are set (CSP, HSTS, X-Frame-Options)

    **A06 - Vulnerable Components:**

    ```bash
    # Check for outdated dependencies
    npm audit
    # or
    pip-audit
    # or
    cargo audit
    ```

    Fix high/critical vulnerabilities immediately.

    **A07 - Identification & Authentication Failures:**
    - Verify strong password requirements
    - Check for account lockout after failed attempts
    - Ensure session timeout is configured
    - Verify MFA is available for sensitive operations

    **A08 - Software & Data Integrity Failures:**
    - Verify dependencies are from trusted sources
    - Check for supply chain security (lock files committed)
    - Ensure CI/CD pipeline validates artifacts

    **A09 - Security Logging & Monitoring Failures:**
    - Verify security events are logged (login failures, access denials)
    - Check logs don't contain sensitive data
    - Ensure monitoring is in place

    // turbo
    **A10 - Server-Side Request Forgery (SSRF):**
    - Verify URL validation on user inputs
    - Check for whitelist of allowed domains

    ```bash
    git grep -n "requests\.\|fetch(\|axios\.\|http\."
    ```

    Review each external request for proper validation.

3. **XSS (Cross-Site Scripting) check**

    Verify all user inputs are properly sanitized and escaped.

    Frontend:
    - React: Using `{}` instead of `dangerouslySetInnerHTML`
    - Vue: Using `{{ }}` instead of `v-html`
    - Angular: Using interpolation instead of `innerHTML`

    Backend:
    - HTML escaping all output
    - Content Security Policy (CSP) headers configured

    ```bash
    # Search for dangerous patterns
    git grep -n "dangerouslySetInnerHTML\|v-html\|innerHTML\|eval("
    ```

4. **CSRF (Cross-Site Request Forgery) protection**

    Verify CSRF tokens are implemented for state-changing operations.

    - Check CSRF middleware is enabled
    - Verify SameSite cookie attribute is set
    - Ensure anti-CSRF tokens in forms

    ```bash
    # Check for CSRF protection
    git grep -n "csrf\|SameSite"
    ```

5. **Authentication & Authorization audit**

    Review authentication implementation:
    - Password storage: bcrypt/argon2 with proper rounds
    - Session management: secure cookies, HttpOnly, SameSite
    - JWT: Proper signing, expiration, refresh token rotation
    - OAuth: Proper state parameter, PKCE for public clients

    ```bash
    # Check auth implementation
    git grep -n "bcrypt\|argon2\|jwt\|passport\|oauth"
    ```

    Verify authorization:
    - Role-Based Access Control (RBAC) if applicable
    - Attribute-Based Access Control (ABAC) for complex scenarios
    - Deny by default (whitelist approach)

6. **Input validation review**

    Check all user inputs are validated:
    - Server-side validation (never trust client)
    - Type checking (Zod, Joi, Pydantic)
    - Length limits
    - Format validation (email, URL, etc.)

    ```bash
    # Check for validation libraries
    git grep -n "zod\|joi\|validator\|pydantic\|marshmallow"
    ```

7. **Error handling audit**

    Verify error handling doesn't leak sensitive information:
    - Generic error messages to users
    - Detailed logs server-side only
    - No stack traces in production
    - Custom error pages (400, 401, 403, 404, 500)

    ```bash
    # Check for exposed errors
    git grep -n "console\.error\|printStackTrace\|traceback"
    ```

8. **Dependency security scan**

    Run automated security scanners on dependencies.

    ```bash
    # npm
    npm audit fix

    # Python
    uv pip install safety
    safety check

    # Go
    go list -json -m all | nancy sleuth

    # Rust
    cargo audit
    ```

    Review and update vulnerable packages.

9. **API security checklist**

    For REST/GraphQL APIs:
    - [ ] Rate limiting implemented (per IP and per user)
    - [ ] API keys/tokens properly validated
    - [ ] CORS configured (not `*` in production)
    - [ ] Request size limits enforced
    - [ ] Proper HTTP methods (GET for read, POST for write)
    - [ ] API versioning in place

// turbo
10. **Generate security audit report**

    Create a security audit report with findings and recommendations.

    ```bash
    # Create report directory if it doesn't exist
    mkdir -p docs/security

    # Save audit date
    echo "# Security Audit Report" > docs/security/audit-$(date +%Y-%m-%d).md
    echo "**Date:** $(date +%Y-%m-%d)" >> docs/security/audit-$(date +%Y-%m-%d).md
    ```

    Document:
    - High/Critical vulnerabilities found
    - Recommended fixes with priority
    - Compliance status (OWASP Top 10)
    - Next audit date

    **Next Steps:**
    - Fix critical vulnerabilities immediately
    - Schedule fixes for high-severity issues
    - Review and update `agent/rules/700-Security` based on findings
    - Consider penetration testing for production systems
    - Setup automated security scans in CI/CD pipeline
