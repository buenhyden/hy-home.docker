# Example: Product Requirements Document (PRD)

This is a concrete example of a PRD following the `templates/product/prd-template.md` structure.

---

## Product Requirements Document

## 1. Product Overview

The User Authentication System provides secure, passwordless authentication for our SaaS platform. Users will authenticate via magic links sent to their email, eliminating password management overhead and improving security posture.

## 0. Pre-Review Checklist (Business & Product)

> This PRD is the single source of truth for the business/product checklist.
> Complete the PRD sections referenced below and capture alignment notes before approval.

| Item                  | Check Question                                                         | Required | Alignment Notes (Agreement) | PRD Section |
| --------------------- | ---------------------------------------------------------------------- | -------- | --------------------------- | ----------- |
| Vision & Goal         | Is the problem + business goal defined in one paragraph?               | Must     | Validated by John (PO)      | Section 1   |
| Success Metrics       | Are the key success/failure metrics defined with quantitative targets? | Must     | Target 95% defined          | Section 3   |
| Target Users          | Are specific primary personas and their pain points defined?           | Must     | SMB Owners & IT Admins      | Section 2   |
| Use Case (GWT)        | Are acceptance criteria written in Given-When-Then format?             | Must     | All stories match GWT       | Section 4   |
| Scope (In)            | Is the feature list included in this release clearly defined?          | Must     | 2 core features listed      | Section 4   |
| Not in Scope          | Is what we will NOT build in this release explicitly listed?           | Must     | Passwords/MFA explicitly out| Section 5   |
| Timeline & Milestones | Are PoC / MVP / Beta / v1.0 milestones dated?                          | Must     | Deferred to JIRA            | N/A         |
| Risks & Compliance    | Are major risks, privacy, or regulatory constraints documented?        | Must     | GDPR compliance noted       | N/A         |

## 2. Target Audience

- **Primary:** Small business owners (10-50 employees) who need simple, secure access to business tools.
- **Secondary:** Enterprise IT administrators who require audit trails and SSO integration.

## 3. Success Metrics (Quantifiable)

- **[REQ-AUTH-MET-01]** Reduce account recovery tickets by 80% (from 200/month to < 40/month) within 90 days.
- **[REQ-AUTH-MET-02]** Achieve > 95% successful login rate on first magic link attempt.
- **[REQ-AUTH-MET-03]** Decrease average login time from 45 seconds (password) to < 20 seconds (magic link).

## 4. User Stories & Features

### [REQ-AUTH-001] Feature 1: Magic Link Authentication

- **As a** user, **I want to** log in via a magic link sent to my email **so that** I don't have to remember a password.

**Acceptance Criteria (GWT Format):**

- **Given** a registered user enters their email on the login page
- **When** they click "Send Magic Link"
- **Then** an email containing a valid magic link is sent within 30 seconds

**Negative path:**

- **Given** an unregistered email is entered
- **When** the user clicks "Send Magic Link"
- **Then** no email is sent, and a generic success message is shown (security: no account enumeration)

### [REQ-AUTH-002] Feature 2: Magic Link Expiration

- **As a** security-conscious user, **I want** my magic link to expire after 15 minutes **so that** unauthorized access is prevented.

**Acceptance Criteria (GWT Format):**

- **Given** a magic link was generated 15+ minutes ago
- **When** the user clicks the link
- **Then** the link is rejected and a new login is required

## 5. Out of Scope

- Password-based authentication (deprecated for this platform)
- Multi-factor authentication (MFA) - planned for Phase 2
- Social login (Google, GitHub) - planned for Phase 3

## 6. Dependencies

- Email delivery service (SendGrid or AWS SES)
- PostgreSQL database (per ADR-001)
- Redis for magic link token caching
