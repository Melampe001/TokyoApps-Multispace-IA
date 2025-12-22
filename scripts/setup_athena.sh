#!/bin/bash
# Tokyo-IA Athena Setup Script
# Initial setup for the hybrid PostgreSQL + Athena architecture

set -e

echo "========================================"
echo "Tokyo-IA Athena Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check required tools
echo "Checking required tools..."

command -v aws >/dev/null 2>&1 || { echo -e "${RED}ERROR: AWS CLI is required but not installed.${NC}" >&2; exit 1; }
command -v terraform >/dev/null 2>&1 || { echo -e "${YELLOW}WARNING: Terraform not found. Infrastructure setup will be skipped.${NC}"; }
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}ERROR: Python 3 is required but not installed.${NC}" >&2; exit 1; }

echo -e "${GREEN}✓ Required tools found${NC}"
echo ""

# Check AWS credentials
echo "Validating AWS credentials..."
if aws sts get-caller-identity >/dev/null 2>&1; then
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    echo -e "${GREEN}✓ AWS credentials valid (Account: ${ACCOUNT_ID})${NC}"
else
    echo -e "${RED}ERROR: AWS credentials are not configured or invalid${NC}"
    echo "Please configure AWS CLI with: aws configure"
    exit 1
fi
echo ""

# Load environment variables safely
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    set -a
    source .env
    set +a
    echo -e "${GREEN}✓ Environment variables loaded${NC}"
else
    echo -e "${YELLOW}WARNING: .env file not found. Using defaults.${NC}"
    echo "Copy .env.example to .env and configure it."
fi
echo ""

# Step 1: Check/Create S3 Buckets
echo "Step 1: Checking S3 buckets..."
BUCKET_DATA_LAKE="${S3_DATA_LAKE_BUCKET:-tokyo-ia-data-lake-dev}"
BUCKET_ATHENA_RESULTS="${S3_ATHENA_RESULTS_BUCKET:-tokyo-ia-athena-results-dev}"

for BUCKET in $BUCKET_DATA_LAKE $BUCKET_ATHENA_RESULTS; do
    if aws s3 ls "s3://${BUCKET}" 2>&1 | grep -q 'NoSuchBucket'; then
        echo "Creating bucket: ${BUCKET}"
        aws s3 mb "s3://${BUCKET}" --region "${AWS_REGION:-us-east-1}"
        echo -e "${GREEN}✓ Created${NC}"
    else
        echo -e "${GREEN}✓ Bucket exists: ${BUCKET}${NC}"
    fi
done
echo ""

# Step 2: Apply Terraform (if available)
if command -v terraform >/dev/null 2>&1; then
    echo "Step 2: Applying Terraform infrastructure..."
    read -p "Do you want to apply Terraform configuration? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd infrastructure
        terraform init
        terraform plan
        read -p "Apply the plan? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            terraform apply -auto-approve
            echo -e "${GREEN}✓ Terraform applied successfully${NC}"
        fi
        cd ..
    fi
else
    echo "Step 2: Skipping Terraform (not installed)"
fi
echo ""

# Step 3: Install Python dependencies
echo "Step 3: Installing Python dependencies..."
if [ -f python/etl/requirements.txt ]; then
    pip3 install -r python/etl/requirements.txt --quiet
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}ERROR: requirements.txt not found${NC}"
fi
echo ""

# Step 4: Setup Athena tables
echo "Step 4: Setting up Athena tables and partitions..."
python3 python/etl/athena_setup.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Athena setup completed${NC}"
else
    echo -e "${RED}ERROR: Athena setup failed${NC}"
    exit 1
fi
echo ""

# Step 5: Run initial ETL (optional)
echo "Step 5: Initial ETL execution (optional)"
read -p "Do you want to run initial ETL to export data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running ETL export..."
    python3 python/etl/export_to_s3.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ ETL export completed${NC}"
    else
        echo -e "${YELLOW}WARNING: ETL export failed. Check logs for details.${NC}"
    fi
fi
echo ""

# Step 6: Verify setup
echo "Step 6: Verifying setup..."
echo "Checking data in S3..."
aws s3 ls "s3://${BUCKET_DATA_LAKE}/" --recursive | head -n 5
echo ""

# Summary
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Verify data in S3: aws s3 ls s3://${BUCKET_DATA_LAKE}/"
echo "2. Check Athena database: aws athena list-databases"
echo "3. Run sample queries in Athena console"
echo "4. Set up GitHub Actions secrets for automated ETL"
echo ""
echo "Resources created:"
echo "  - S3 Data Lake: ${BUCKET_DATA_LAKE}"
echo "  - S3 Athena Results: ${BUCKET_ATHENA_RESULTS}"
echo "  - Athena Database: ${ATHENA_DATABASE:-tokyo_ia_billing_dev}"
echo ""
echo -e "${GREEN}Setup completed successfully!${NC}"
