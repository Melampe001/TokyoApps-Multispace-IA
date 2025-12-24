# AWS Setup Guide

This guide provides comprehensive instructions for setting up AWS infrastructure for the Tokyo-IA project, including IAM configuration, credential management, and security best practices.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [IAM User Setup](#iam-user-setup)
3. [Required IAM Policies](#required-iam-policies)
4. [GitHub Actions Configuration](#github-actions-configuration)
5. [OIDC Setup (Recommended)](#oidc-setup-recommended)
6. [Testing Credentials](#testing-credentials)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)

## Prerequisites

- AWS Account with administrative access
- GitHub repository with Actions enabled
- Basic understanding of AWS IAM concepts
- AWS CLI installed (for local testing)

## IAM User Setup

### Option 1: Programmatic Access (Quick Setup)

This method uses long-lived access keys. For enhanced security, see [OIDC Setup](#oidc-setup-recommended).

#### Step 1: Create IAM User

1. Sign in to the [AWS Console](https://console.aws.amazon.com/)
2. Navigate to **IAM** → **Users** → **Add users**
3. Configure user details:
   - **User name**: `github-actions-tokyo-ia`
   - **Access type**: Select "Access key - Programmatic access"
4. Click **Next: Permissions**

#### Step 2: Attach Permissions

Choose one of these methods:

**Method A: Attach Custom Policy (Recommended)**
1. Click **Attach existing policies directly**
2. Click **Create policy**
3. Use the JSON policy template from [Required IAM Policies](#required-iam-policies)
4. Name it: `TerraformInfrastructurePolicy`
5. Return to user creation and attach the new policy

**Method B: Use AWS Managed Policies (Development Only)**
- ⚠️ Only for testing/development environments
- Attach these managed policies:
  - `AmazonS3FullAccess`
  - `AWSGlueConsoleFullAccess`
  - `AmazonAthenaFullAccess`
  - `IAMFullAccess` (or `IAMReadOnlyAccess` if not creating roles)
  - `CloudWatchLogsFullAccess`

#### Step 3: Review and Create

1. Add tags (optional but recommended):
   - `Project`: `tokyo-ia`
   - `ManagedBy`: `Terraform`
   - `Purpose`: `GitHub Actions CI/CD`
2. Review configuration
3. Click **Create user**

#### Step 4: Save Credentials

**⚠️ CRITICAL SECURITY STEP**

1. AWS displays the **Access Key ID** and **Secret Access Key** only once
2. Click **Download .csv** to save credentials securely
3. Store in a password manager (1Password, LastPass, etc.)
4. **Never** commit these credentials to version control
5. Click **Close** when done

Example credential format:
```
Access Key ID: AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

## Required IAM Policies

### Terraform Infrastructure Policy

This policy grants minimum required permissions for the Tokyo-IA Terraform infrastructure.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketManagement",
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:DeleteBucket",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:GetBucketVersioning",
        "s3:GetBucketTagging",
        "s3:PutBucketTagging",
        "s3:PutBucketVersioning",
        "s3:PutBucketPublicAccessBlock",
        "s3:GetBucketPublicAccessBlock",
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucketVersions"
      ],
      "Resource": [
        "arn:aws:s3:::tokyo-ia-*",
        "arn:aws:s3:::tokyo-ia-*/*"
      ]
    },
    {
      "Sid": "GlueManagement",
      "Effect": "Allow",
      "Action": [
        "glue:CreateDatabase",
        "glue:DeleteDatabase",
        "glue:GetDatabase",
        "glue:GetDatabases",
        "glue:UpdateDatabase",
        "glue:CreateTable",
        "glue:DeleteTable",
        "glue:GetTable",
        "glue:GetTables",
        "glue:UpdateTable",
        "glue:BatchCreatePartition",
        "glue:CreatePartition",
        "glue:UpdatePartition",
        "glue:GetPartition",
        "glue:GetPartitions",
        "glue:TagResource",
        "glue:UntagResource"
      ],
      "Resource": [
        "arn:aws:glue:*:*:catalog",
        "arn:aws:glue:*:*:database/tokyo_ia_*",
        "arn:aws:glue:*:*:table/tokyo_ia_*/*"
      ]
    },
    {
      "Sid": "AthenaManagement",
      "Effect": "Allow",
      "Action": [
        "athena:CreateWorkGroup",
        "athena:DeleteWorkGroup",
        "athena:GetWorkGroup",
        "athena:UpdateWorkGroup",
        "athena:ListWorkGroups",
        "athena:TagResource",
        "athena:UntagResource",
        "athena:StartQueryExecution",
        "athena:GetQueryExecution",
        "athena:GetQueryResults",
        "athena:StopQueryExecution"
      ],
      "Resource": [
        "arn:aws:athena:*:*:workgroup/tokyo-ia-*"
      ]
    },
    {
      "Sid": "IAMRoleManagement",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:GetRole",
        "iam:PassRole",
        "iam:ListRolePolicies",
        "iam:ListAttachedRolePolicies",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:UpdateAssumeRolePolicy",
        "iam:TagRole",
        "iam:UntagRole"
      ],
      "Resource": [
        "arn:aws:iam::*:role/tokyo-ia-*"
      ]
    },
    {
      "Sid": "IAMPolicyManagement",
      "Effect": "Allow",
      "Action": [
        "iam:CreatePolicy",
        "iam:DeletePolicy",
        "iam:GetPolicy",
        "iam:GetPolicyVersion",
        "iam:ListPolicyVersions",
        "iam:CreatePolicyVersion",
        "iam:DeletePolicyVersion",
        "iam:TagPolicy",
        "iam:UntagPolicy"
      ],
      "Resource": [
        "arn:aws:iam::*:policy/tokyo-ia-*"
      ]
    },
    {
      "Sid": "CloudWatchLogsManagement",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:DeleteLogGroup",
        "logs:DescribeLogGroups",
        "logs:ListTagsLogGroup",
        "logs:TagLogGroup",
        "logs:UntagLogGroup",
        "logs:PutRetentionPolicy",
        "logs:DeleteRetentionPolicy"
      ],
      "Resource": [
        "arn:aws:logs:*:*:log-group:/aws/tokyo-ia/*"
      ]
    }
  ]
}
```

### Copy-Paste Policy Template

Save this as `TerraformInfrastructurePolicy`:

1. Go to IAM → Policies → Create policy
2. Click **JSON** tab
3. Paste the above policy
4. Click **Next: Tags** (optional)
5. Click **Next: Review**
6. Name: `TerraformInfrastructurePolicy`
7. Description: `Permissions for Tokyo-IA Terraform infrastructure deployment`
8. Click **Create policy**

## GitHub Actions Configuration

### Adding Secrets to GitHub

1. Navigate to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret individually:

| Secret Name | Value | Required |
|-------------|-------|----------|
| `AWS_ACCESS_KEY_ID` | Your IAM user access key | ✅ Yes |
| `AWS_SECRET_ACCESS_KEY` | Your IAM user secret key | ✅ Yes |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) | ✅ Yes |
| `DB_HOST` | PostgreSQL hostname | No |
| `DB_NAME` | Database name | No |
| `DB_USER` | Database username | No |
| `DB_PASSWORD` | Database password | No |

### Validation

After adding secrets, trigger the workflow:

```bash
# Push a change to infrastructure/ directory
git commit --allow-empty -m "Test infrastructure workflow"
git push
```

Check the workflow run in the **Actions** tab. The "Validate AWS Credentials" step should show:
```
✅ AWS credentials are configured
```

## OIDC Setup (Recommended)

OpenID Connect (OIDC) provides a more secure alternative to long-lived access keys.

### Benefits

- No long-lived credentials stored in GitHub
- Automatic credential rotation
- Enhanced security through trust policies
- Auditable through CloudTrail

### Setup Steps

#### 1. Create OIDC Identity Provider in AWS

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

#### 2. Create IAM Role for GitHub Actions

Create a file `github-actions-trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:*"
        }
      }
    }
  ]
}
```

Replace:
- `YOUR_ACCOUNT_ID` with your AWS account ID
- `YOUR_ORG/YOUR_REPO` with your GitHub repository (e.g., `Melampe001/TokyoApps-Multispace-IA`)

Create the role:

```bash
aws iam create-role \
  --role-name github-actions-tokyo-ia \
  --assume-role-policy-document file://github-actions-trust-policy.json

aws iam attach-role-policy \
  --role-name github-actions-tokyo-ia \
  --policy-arn arn:aws:iam::YOUR_ACCOUNT_ID:policy/TerraformInfrastructurePolicy
```

#### 3. Update GitHub Workflow

Replace the credential configuration step in `.github/workflows/infrastructure.yml`:

```yaml
- name: Configure AWS Credentials
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::YOUR_ACCOUNT_ID:role/github-actions-tokyo-ia
    aws-region: us-east-1
```

#### 4. Update Repository Settings

Add only one secret:
- `AWS_ROLE_ARN`: `arn:aws:iam::YOUR_ACCOUNT_ID:role/github-actions-tokyo-ia`

Remove `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` if using OIDC.

## Testing Credentials

### Local Testing with AWS CLI

```bash
# Configure AWS CLI with your credentials
aws configure

# Test S3 access
aws s3 ls

# Test Athena access
aws athena list-work-groups --region us-east-1

# Test Glue access
aws glue get-databases --region us-east-1
```

### Test Terraform Locally

```bash
cd infrastructure
terraform init
terraform plan
```

If successful, you'll see a plan output without authentication errors.

## Troubleshooting

### Error: "Credentials could not be loaded"

**Cause**: Missing or incorrectly named GitHub secrets

**Solution**:
1. Verify secret names are exact (case-sensitive):
   - `AWS_ACCESS_KEY_ID` (not `aws_access_key_id`)
   - `AWS_SECRET_ACCESS_KEY` (not `aws_secret_access_key`)
2. Check for extra spaces or newlines in secret values
3. Ensure secrets are in the correct repository (not organization secrets)

### Error: "Access Denied" for S3 operations

**Cause**: IAM policy doesn't allow S3 bucket creation

**Solution**:
1. Verify IAM policy includes `s3:CreateBucket`
2. Check resource patterns match your bucket names
3. Ensure bucket names follow pattern `tokyo-ia-*`

### Error: "InvalidClientTokenId"

**Cause**: Access key is invalid or deleted

**Solution**:
1. Verify the access key is active in IAM console
2. Check if access key was accidentally deleted
3. Create a new access key and update GitHub secrets

### Error: "User is not authorized to perform: iam:CreateRole"

**Cause**: IAM user lacks permissions to create roles

**Solution**:
1. Attach IAM management permissions to the user
2. Or have an administrator pre-create the roles
3. Update Terraform to use existing roles

### Workflow Validation Step Fails

**Cause**: The validation check runs before secrets are available

**Solution**:
- This is expected behavior when secrets are not configured
- Add secrets following the [GitHub Actions Configuration](#github-actions-configuration) section
- Re-run the workflow after adding secrets

## Security Best Practices

### Credential Rotation

Set up regular credential rotation:

1. **Create a calendar reminder** for every 90 days
2. **Generate new access keys**:
   ```bash
   aws iam create-access-key --user-name github-actions-tokyo-ia
   ```
3. **Update GitHub secrets** with new credentials
4. **Delete old access keys**:
   ```bash
   aws iam delete-access-key --user-name github-actions-tokyo-ia --access-key-id OLD_KEY_ID
   ```

### Least Privilege Principle

- Grant only permissions required for Terraform operations
- Avoid using AWS managed policies in production
- Regularly audit IAM policies with AWS Access Analyzer
- Use condition keys to restrict actions (e.g., by resource tags)

### Monitoring and Auditing

Enable CloudTrail for audit logging:

```bash
aws cloudtrail create-trail \
  --name tokyo-ia-audit \
  --s3-bucket-name tokyo-ia-cloudtrail-logs

aws cloudtrail start-logging --name tokyo-ia-audit
```

Set up CloudWatch alarms for suspicious activity:
- Repeated access denied errors
- Unusual API call patterns
- Access from unexpected IP addresses

### Emergency Response

If credentials are compromised:

1. **Immediately disable the access key**:
   ```bash
   aws iam update-access-key --user-name github-actions-tokyo-ia --access-key-id COMPROMISED_KEY --status Inactive
   ```

2. **Review CloudTrail logs** for unauthorized access:
   ```bash
   aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=github-actions-tokyo-ia
   ```

3. **Rotate credentials**:
   - Create new access key
   - Update GitHub secrets
   - Delete compromised key

4. **Notify security team** if sensitive data was accessed

### Additional Resources

- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [AWS Security Blog](https://aws.amazon.com/blogs/security/)
- [Terraform AWS Provider Authentication](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#authentication-and-configuration)

## Next Steps

1. Complete the setup by following [ATHENA_SETUP.md](ATHENA_SETUP.md)
2. Deploy infrastructure with Terraform
3. Configure monitoring and alerting
4. Document any organization-specific security requirements
5. Schedule credential rotation reminders

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review GitHub Actions workflow logs
- Consult AWS documentation
- Open an issue in the repository
