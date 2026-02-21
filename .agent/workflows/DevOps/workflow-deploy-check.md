---
description: Pre-deployment checklist to ensure production readiness
---

1. **Verify environment configuration**

    Check that all required environment variables are configured for production.

    Create checklist:
    - [ ] Production environment variables documented
    - [ ] No hardcoded secrets in code
    - [ ] `.env.example` file is up-to-date
    - [ ] Environment-specific configs (dev/staging/prod) are separate

    ```bash
    # Check for environment variable usage
    git grep -n "process\.env\|os\.getenv\|ENV\["
    ```

    Verify each variable has a production value ready.

2. **Run all tests**

    Execute the full test suite to ensure no regressions.

    ```bash
    # Run tests based on your stack
    npm test # JavaScript/TypeScript
    pytest # Python
    go test ./... # Go
    cargo test # Rust
    flutter test # Flutter
    ```

    Expected: All tests pass (100% success rate).

    **If tests fail:**
    - Stop deployment
    - Debug failed tests
    - Fix issues
    - Re-run this workflow

3. **Check code quality and linting**

    Ensure code passes all linters and formatters.

    // turbo

    ```bash
    # JavaScript/TypeScript
    npm run lint
    npm run typecheck # if using TypeScript

    # Python
    flake8 .
    mypy .
    black --check .

    # Go
    golangci-lint run

    # Rust
    cargo clippy -- -D warnings
    cargo fmt -- --check
    ```

    Expected: No errors or warnings.

    Fix any issues before proceeding.

4. **Security audit**

    Run security audit to check for vulnerabilities.

    Refer to `/workflow-security-audit` for comprehensive security checks.

    Quick security scan:

    ```bash
    # Dependencies
    npm audit --production
    # or
    pip-audit
    # or
    cargo audit

    # Secrets scan (using gitleaks or similar)
    git secrets --scan-history
    ```

    **Critical**: Fix any high/critical vulnerabilities before deployment.

5. **Build production bundle**

    Create optimized production build.

    ```bash
    # Next.js
    npm run build
    npm run start # Test production build locally

    # React/Vite
    npm run build
    npm run preview

    # Flutter
    flutter build apk --release # Android
    flutter build ios --release # iOS
    flutter build web --release # Web

    # Go
    go build -ldflags="-w -s" -o app cmd/main.go

    # Python (if building Docker)
    docker build -t myapp:latest .
    ```

    Expected: Build succeeds without errors.

    **Verify build output:**
    - Check bundle size (should be optimized)
    - Test built app locally
    - Verify assets are properly included

6. **Performance check**

    Verify performance metrics meet requirements.

    For web applications:
    - Lighthouse score > 90 (Performance, Accessibility, Best Practices, SEO)
    - First Contentful Paint < 1.8s
    - Time to Interactive < 3.8s
    - Cumulative Layout Shift < 0.1

    ```bash
    # Run Lighthouse (for web apps)
    npx lighthouse https://localhost:3000 --view
    ```

    For mobile apps:
    - App size < reasonable limit (e.g., < 50MB for mobile)
    - Cold start time < 3s
    - Memory usage acceptable

7. **Database migration check**

    If database changes are included, verify migration scripts.

    - [ ] Migration scripts tested on staging
    - [ ] Rollback scripts prepared
    - [ ] Backup strategy confirmed
    - [ ] Migration is backward compatible (zero-downtime if needed)

    ```bash
    # Test migrations (in staging/local)
    # Django
    python manage.py migrate --check

    # TypeORM
    npm run typeorm migration:run

    # Alembic
    alembic upgrade head

    # Prisma
    npx prisma migrate deploy
    ```

8. **API compatibility check**

    Ensure API changes are backward compatible.

    - [ ] No breaking changes to public APIs
    - [ ] API versioning updated if needed
    - [ ] Deprecated endpoints documented
    - [ ] Client apps compatible with new API

    Review API changes:

    ```bash
    git diff main HEAD -- '**/api/**' '**/routes/**'
    ```

9. **Deployment configuration verification**

    Check deployment configuration files.

    **Docker:**
    - [ ] `Dockerfile` optimized (multi-stage build)
    - [ ] Health check endpoint configured
    - [ ] Resource limits set (CPU, memory)
    - [ ] Non-root user configured

    **Kubernetes:**
    - [ ] Deployment YAML has resource requests/limits
    - [ ] Liveness and readiness probes configured
    - [ ] ConfigMaps and Secrets properly set
    - [ ] HPA (Horizontal Pod Autoscaler) configured if needed

    **Terraform:**
    - [ ] `terraform plan` reviewed
    - [ ] State file backed up
    - [ ] Variables properly parameterized

10. **Monitoring and logging setup**

    Ensure monitoring and alerting are configured.

    - [ ] Application metrics exported (if using Prometheus/Grafana)
    - [ ] Logging configured (structured logs)
    - [ ] Error tracking enabled (Sentry, Rollbar, etc.)
    - [ ] Alerts configured for critical errors
    - [ ] Uptime monitoring enabled

    ```bash
    # Verify monitoring endpoints
    curl http://localhost:3000/health
    curl http://localhost:3000/metrics
    ```

11. **Documentation update**

    Ensure documentation is current.

    - [ ] README updated with latest setup instructions
    - [ ] CHANGELOG updated with new version
    - [ ] API documentation generated/updated
    - [ ] Deployment guide current

    ```bash
    # Update CHANGELOG
    echo "## [$(date +%Y.%m.%d)]" >> CHANGELOG.md
    echo "### Added/Changed/Fixed" >> CHANGELOG.md
    ```

12. **Create deployment tag**

    Tag the release version in git.

    ```bash
    # Create version tag
    git tag -a v1.0.0 -m "Release version 1.0.0"
    git push origin v1.0.0
    ```

13. **Backup current production**

    Before deployment, backup current production state.

    - [ ] Database backup completed
    - [ ] Configuration files backed up
    - [ ] Previous Docker images tagged
    - [ ] Rollback plan documented

14. **Final deployment checklist**

    Review final checklist before triggering deployment:

    - [ ] All tests passing ✅
    - [ ] Security audit passed ✅
    - [ ] Production build successful ✅
    - [ ] Performance metrics acceptable ✅
    - [ ] Database migrations ready ✅
    - [ ] API compatibility verified ✅
    - [ ] Monitoring configured ✅
    - [ ] Documentation updated ✅
    - [ ] Backup completed ✅
    - [ ] Rollback plan ready ✅

    **If all checks pass:** Proceed with deployment.

    **Deployment command examples:**

    ```bash
    # Vercel/Netlify
    vercel --prod
    # or
    netlify deploy --prod

    # Docker + k8s
    docker push myregistry/myapp:v1.0.0
    kubectl set image deployment/myapp myapp=myregistry/myapp:v1.0.0

    # Traditional VPS
    ssh user@server 'cd /app && git pull && npm install && pm2 restart app'
    ```

15. **Post-deployment verification**

    After deployment, verify the application works correctly.

    // turbo

    ```bash
    # Health check
    curl https://myapp.com/health

    # Basic functionality test
    curl https://myapp.com/api/status
    ```

    Monitor for:
    - Error rate (should be low)
    - Response time (should be acceptable)
    - Server resources (CPU, memory)

    **Watch for 10-15 minutes post-deployment.**

    If errors spike or performance degrades:
    - **ROLLBACK IMMEDIATELY**
    - Investigate issues
    - Fix and re-deploy

    **Next Steps:**
    - Monitor application for 24-48 hours
    - Review logs for any anomalies
    - Update runbooks based on deployment experience
    - Schedule next security audit
