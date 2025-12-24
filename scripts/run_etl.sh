#!/bin/bash
# Ejecutar ETL manualmente

set -e

# Default to yesterday's date if not provided
DATE=${1:-$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)}
MODE=${2:-incremental}

echo "🔄 Running ETL for date: $DATE (mode: $MODE)"

# Check if Python dependencies are installed
if [ ! -d "python/etl/__pycache__" ] && [ ! -d "venv" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r python/etl/requirements.txt
fi

# Load environment variables if .env exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Run ETL
cd python/etl
python export_to_s3.py --date $DATE --mode $MODE

echo ""
echo "✅ ETL completed successfully!"
echo ""
echo "To validate the export, run:"
echo "  python scripts/validate_data.py"
