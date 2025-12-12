# Tokyo-IA Secrets Management

This document explains how to properly manage secrets and credentials in the Tokyo-IA project.

## Critical Security Rules

**NEVER commit these items to the repository:**
- Keystore files (`.jks`, `.keystore`)
- Service account JSON files
- API keys or tokens
- Private keys (`.pem`, `.key`)
- `.env` files with production credentials
- Passwords or passphrases

## What To Do If You Accidentally Commit a Secret

If you accidentally commit a secret to the repository:

1. **Rotate the credential immediately**
   - For Google Play: Create a new service account and revoke the old one
   - For signing keys: Generate a new keystore
   - For API keys: Regenerate the key in the service console

2. **Remove from Git history**
   ```bash
   # Using git-filter-repo (recommended)
   git filter-repo --path path/to/secret/file --invert-paths
   
   # Or using BFG Repo-Cleaner
   bfg --delete-files secret-file.json
   ```

3. **Force push the cleaned history** (coordinate with team)
   ```bash
   git push origin --force --all
   git push origin --force --tags
   ```

4. **Notify all collaborators**
   - Tell them to re-clone the repository
   - Update any local credentials
   - Ensure CI/CD secrets are updated

## Proper Secret Storage

### For Local Development

1. **Create `.env` file** (already in `.gitignore`)
   ```bash
   cd /path/to/tokyo-ia
   cp .env.example .env
   # Edit .env with your local credentials
   ```

2. **Android keystore**
   - Store outside the repository or in a secure location
   - Use environment variables to reference it:
     ```bash
     export KEYSTORE_FILE=~/secure/tokyo-ia-release.jks
     export KEYSTORE_PASSWORD=your_password
     ```

3. **API keys for MCP server**
   ```bash
   # server-mcp/.env
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_api_key
   PIN_SIN_BLOQUEOS=your_secure_pin
   ```

### For CI/CD (GitHub Actions)

Store secrets in GitHub repository settings:

1. Go to: `Settings` → `Secrets and variables` → `Actions`

2. Add these secrets:

   **Android Signing:**
   - `ANDROID_KEYSTORE_BASE64`: Base64-encoded keystore
     ```bash
     # Encode keystore
     base64 -i release.keystore > keystore.b64
     # Copy contents and add to GitHub secrets
     ```
   - `KEYSTORE_PASSWORD`: Keystore password
   - `KEY_ALIAS`: Key alias
   - `KEY_PASSWORD`: Key password

   **Google Play:**
   - `GOOGLE_PLAY_JSON`: Service account JSON content
     ```bash
     # Copy the entire JSON file content
     cat service-account.json
     # Paste into GitHub secret
     ```

   **API Keys (if needed for builds):**
   - `GEMINI_API_KEY`: Gemini API key
   - `OPENAI_API_KEY`: OpenAI API key

3. Reference in workflows:
   ```yaml
   - name: Build
     env:
       KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
       API_KEY: ${{ secrets.API_KEY }}
     run: ./gradlew assembleRelease
   ```

## Creating Secure Credentials

### Android Keystore

```bash
# Generate a new keystore
keytool -genkey -v \
  -keystore tokyo-ia-release.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias tokyo-ia-key

# Backup the keystore securely!
# If you lose this, you cannot update your app on Play Store
```

**Store the keystore:**
- Keep a backup in a secure location (password manager, encrypted drive)
- Never commit to Git
- Document the keystore details securely:
  - File name
  - Password
  - Key alias
  - Key password
  - Creation date
  - Expiration date

### Google Play Service Account

1. Go to Google Play Console
2. Navigate to: `Setup` → `API access`
3. Create a new service account
4. Download the JSON key file
5. Grant necessary permissions (e.g., "Release to production")
6. **Never commit the JSON file**
7. Store in GitHub secrets as `GOOGLE_PLAY_JSON`

### API Keys

For external services (Gemini, OpenAI, etc.):

1. Create API keys in the respective service consoles
2. Store in `.env` for local development
3. Add to GitHub secrets for CI/CD
4. Rotate keys periodically (every 90 days recommended)

## Environment Variables Reference

### Android App
```bash
KEYSTORE_FILE=/path/to/keystore.jks
KEYSTORE_PASSWORD=your_password
KEY_ALIAS=your_alias
KEY_PASSWORD=your_key_password
```

### MCP Server
```bash
PORT=3001
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
PIN_SIN_BLOQUEOS=your_secure_pin
NODE_ENV=production
```

### Web App
```bash
VITE_API_URL=http://localhost:3001
VITE_MCP_ENDPOINT=/mcp
```

## Security Best Practices

1. **Use different credentials for dev/staging/production**
2. **Rotate secrets regularly**
3. **Use least-privilege principle** (minimal permissions needed)
4. **Monitor secret usage** (check for unauthorized access)
5. **Use secret scanning tools** (GitHub Secret Scanning, TruffleHog)
6. **Document who has access** to which secrets
7. **Revoke old secrets** when no longer needed

## Verifying No Secrets in Repository

```bash
# Check for common secret patterns
git grep -i "password"
git grep -i "api_key"
git grep -i "secret"
git grep -i "private_key"

# Use TruffleHog
trufflehog git file://. --only-verified

# Check git history for removed secrets
git log --all --full-history -- "**/*.jks"
git log --all --full-history -- "**/*service-account*.json"
```

## Emergency Contacts

If a secret is compromised:

1. **Immediately revoke/rotate the credential**
2. **Notify the team lead**
3. **Check access logs** for unauthorized usage
4. **Update all systems** using the compromised secret
5. **Document the incident** for future reference

## Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Android Signing Documentation](https://developer.android.com/studio/publish/app-signing)
- [OWASP Secrets Management](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password)
