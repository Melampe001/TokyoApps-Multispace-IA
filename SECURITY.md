# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to the project maintainers. You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

This information will help us triage your report more quickly.

## Security Best Practices

### For Contributors

1. **Never Commit Secrets**
   - No API keys, passwords, or tokens in code
   - No keystore files or service account JSONs
   - Use `.gitignore` to exclude sensitive files
   - Use environment variables for configuration

2. **Dependencies**
   - Keep dependencies up to date
   - Review Dependabot security alerts
   - Check for known vulnerabilities before adding dependencies
   - Use `npm audit` / `gradle dependencies` to check for issues

3. **Code Review**
   - Review security implications of changes
   - Check for SQL injection, XSS, CSRF vulnerabilities
   - Validate input and sanitize output
   - Use parameterized queries

4. **Authentication & Authorization**
   - Never store passwords in plain text
   - Use secure password hashing (bcrypt, argon2)
   - Implement proper session management
   - Follow principle of least privilege

### For Android Development

1. **ProGuard/R8**
   - Enable code obfuscation for release builds
   - Protect sensitive strings and algorithms

2. **Network Security**
   - Use HTTPS only
   - Implement certificate pinning for critical APIs
   - Validate SSL certificates

3. **Data Storage**
   - Encrypt sensitive data using Android Keystore
   - Never store credentials in SharedPreferences unencrypted
   - Use EncryptedSharedPreferences for sensitive data

4. **Permissions**
   - Request only necessary permissions
   - Explain permission usage to users
   - Handle permission denials gracefully

### For Web Development

1. **XSS Prevention**
   - Sanitize user input
   - Use Content Security Policy headers
   - Escape output in templates

2. **CSRF Protection**
   - Use anti-CSRF tokens
   - Validate request origins
   - Use SameSite cookie attribute

3. **Authentication**
   - Implement secure session management
   - Use HTTP-only cookies
   - Implement rate limiting on authentication endpoints

4. **Dependencies**
   - Audit npm packages regularly
   - Use `npm audit fix` to patch vulnerabilities
   - Review package permissions and downloads

### For Server Development

1. **API Security**
   - Implement authentication and authorization
   - Use API rate limiting
   - Validate and sanitize all input
   - Return appropriate HTTP status codes

2. **Database Security**
   - Use parameterized queries
   - Implement proper access controls
   - Encrypt sensitive data at rest
   - Regular backups with encryption

3. **Environment Variables**
   - Never commit `.env` files
   - Use secrets management services
   - Rotate credentials regularly

4. **Error Handling**
   - Don't expose stack traces in production
   - Log security events
   - Implement proper error handling

## Secrets Management in CI/CD

### GitHub Actions Secrets

Store sensitive data in GitHub Actions Secrets:

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add secrets like:
   - `ANDROID_KEYSTORE_BASE64`
   - `GOOGLE_PLAY_JSON`
   - `API_KEYS`

### Using Secrets

In workflows:
```yaml
env:
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

**Never:**
- Echo secrets in logs
- Store secrets in code
- Share secrets via insecure channels

## Vulnerability Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Acknowledge receipt
3. **Day 3-7**: Investigate and verify
4. **Day 8-30**: Develop and test fix
5. **Day 31**: Release patch
6. **Day 32**: Public disclosure (if appropriate)

We ask security researchers to:
- Give us reasonable time to fix issues
- Not publicly disclose until patch is released
- Not exploit vulnerabilities

## Security Updates

We will:
- Release security patches as soon as possible
- Notify users of security updates via GitHub releases
- Credit security researchers (if they wish)
- Maintain a security advisory for each vulnerability

## Automated Security Scanning

We use:
- **Dependabot**: Automatic dependency updates
- **GitHub Code Scanning**: Static analysis
- **npm audit**: Node.js dependency scanning
- **Android Lint**: Android security checks

## Security Checklist for PRs

Before merging, ensure:

- [ ] No secrets committed
- [ ] No new high/critical security alerts
- [ ] Input validation implemented
- [ ] Output sanitization implemented
- [ ] Authentication/authorization working
- [ ] Dependencies up to date
- [ ] Security best practices followed
- [ ] Error handling doesn't leak sensitive info

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Android Security Best Practices](https://developer.android.com/topic/security/best-practices)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [React Security Best Practices](https://react.dev/learn/security)

## Contact

For security concerns, contact: [Add contact email]

For general questions, open an issue on GitHub.

---

Thank you for helping keep Tokyo-IA secure! 🔒
