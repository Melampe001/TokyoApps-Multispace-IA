#!/bin/bash
# Setup inicial de Athena infrastructure

set -e

echo "🚀 Setting up Athena infrastructure..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Please create one from .env.example"
    exit 1
fi

# Load environment variables
set -a
source .env
set +a

echo "📦 Installing Python dependencies..."
cd python/etl
pip install -r requirements.txt
cd ../..

echo "🏗️  Deploying infrastructure with Terraform..."
cd infrastructure

# Initialize Terraform if not already done
if [ ! -d ".terraform" ]; then
    terraform init
fi

# Plan and apply
terraform plan -out=tfplan
terraform apply tfplan

echo "✅ Infrastructure deployed!"

# Get outputs
echo ""
echo "📊 Infrastructure Details:"
terraform output

echo ""
echo "🔧 Setting up Athena tables..."
cd ..
python python/etl/athena_setup.py

echo ""
echo "✅ Athena setup complete!"
echo ""
echo "Next steps:"
echo "1. Update your .env file with the infrastructure outputs"
echo "2. Run 'scripts/run_etl.sh' to test the ETL pipeline"
echo "3. Configure GitHub Actions secrets for automated runs"
