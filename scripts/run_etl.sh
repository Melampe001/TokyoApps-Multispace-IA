#!/bin/bash
# Run ETL manually for testing or backfills

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "========================================"
echo "Tokyo-IA ETL Manual Execution"
echo "========================================"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Parse command line arguments
START_DATE=""
END_DATE=""
TABLE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --start-date)
            START_DATE="$2"
            shift 2
            ;;
        --end-date)
            END_DATE="$2"
            shift 2
            ;;
        --table)
            TABLE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --start-date DATE   Start date (YYYY-MM-DD)"
            echo "  --end-date DATE     End date (YYYY-MM-DD)"
            echo "  --table NAME        Specific table to export (optional)"
            echo "  --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0"
            echo "  $0 --start-date 2024-12-01 --end-date 2024-12-22"
            echo "  $0 --table workflows --start-date 2024-12-22"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build command
CMD="python3 python/etl/export_to_s3.py"

if [ -n "$TABLE" ]; then
    CMD="$CMD --table $TABLE"
    echo "Table filter: $TABLE"
fi

if [ -n "$START_DATE" ]; then
    CMD="$CMD --start-date $START_DATE"
    echo "Start date: $START_DATE"
fi

if [ -n "$END_DATE" ]; then
    CMD="$CMD --end-date $END_DATE"
    echo "End date: $END_DATE"
fi

echo ""
echo "Running ETL..."
echo "Command: $CMD"
echo ""

# Execute ETL
$CMD

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ ETL completed successfully${NC}"
    
    # Update partitions
    echo ""
    echo "Updating Athena partitions..."
    python3 python/etl/athena_setup.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Partitions updated${NC}"
    else
        echo -e "${YELLOW}WARNING: Failed to update partitions${NC}"
    fi
    
    # Show summary
    echo ""
    echo "========================================"
    echo "ETL Summary"
    echo "========================================"
    BUCKET="${S3_DATA_LAKE_BUCKET:-tokyo-ia-data-lake-dev}"
    echo "Data exported to: s3://$BUCKET/"
    echo ""
    echo "Recent files:"
    aws s3 ls "s3://$BUCKET/" --recursive --human-readable | tail -n 10
    
else
    echo ""
    echo -e "${RED}✗ ETL failed with exit code $EXIT_CODE${NC}"
    exit $EXIT_CODE
fi
