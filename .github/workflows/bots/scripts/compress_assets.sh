#!/bin/bash
# Asset Compression and Optimization Script
# Compresses PNG images, converts large JPGs to WebP, removes EXIF data

set -e

CHANGED_FILES=""
TOTAL_SAVED=0

echo "🎨 Frontend Asset Optimizer"
echo "============================"

# Function to optimize PNG files
optimize_png() {
    local file="$1"
    local original_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    
    if command -v pngquant &> /dev/null; then
        echo "  Compressing PNG: $file"
        pngquant --force --output "$file" --quality=65-80 "$file" 2>/dev/null || true
        local new_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        local saved=$((original_size - new_size))
        TOTAL_SAVED=$((TOTAL_SAVED + saved))
        echo "    Saved: $(numfmt --to=iec-i --suffix=B $saved 2>/dev/null || echo $saved bytes)"
        CHANGED_FILES="${CHANGED_FILES} $file"
    else
        echo "  ⚠️  pngquant not installed, skipping PNG optimization"
    fi
}

# Function to convert large JPG to WebP
convert_to_webp() {
    local file="$1"
    local original_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    local webp_file="${file%.*}.webp"
    
    if command -v cwebp &> /dev/null; then
        echo "  Converting to WebP: $file"
        cwebp -q 80 "$file" -o "$webp_file" 2>/dev/null || true
        if [ -f "$webp_file" ]; then
            local new_size=$(stat -f%z "$webp_file" 2>/dev/null || stat -c%s "$webp_file" 2>/dev/null)
            local saved=$((original_size - new_size))
            TOTAL_SAVED=$((TOTAL_SAVED + saved))
            echo "    Saved: $(numfmt --to=iec-i --suffix=B $saved 2>/dev/null || echo $saved bytes)"
            CHANGED_FILES="${CHANGED_FILES} $webp_file"
        fi
    else
        echo "  ⚠️  cwebp not installed, skipping WebP conversion"
    fi
}

# Function to remove EXIF data
remove_exif() {
    local file="$1"
    
    if command -v exiftool &> /dev/null; then
        echo "  Removing EXIF: $file"
        exiftool -all= -overwrite_original "$file" 2>/dev/null || true
        CHANGED_FILES="${CHANGED_FILES} $file"
    elif command -v mogrify &> /dev/null; then
        echo "  Removing EXIF (ImageMagick): $file"
        mogrify -strip "$file" 2>/dev/null || true
        CHANGED_FILES="${CHANGED_FILES} $file"
    else
        echo "  ⚠️  No EXIF removal tool found"
    fi
}

# Find and process image files
echo ""
echo "Searching for images to optimize..."

# Process PNG files
while IFS= read -r -d '' png_file; do
    file_size=$(stat -f%z "$png_file" 2>/dev/null || stat -c%s "$png_file" 2>/dev/null)
    # Only process PNGs > 10KB
    if [ "$file_size" -gt 10240 ]; then
        optimize_png "$png_file"
    fi
done < <(find . -type f -name "*.png" ! -path "*/node_modules/*" ! -path "*/.git/*" -print0 2>/dev/null)

# Process JPG files
while IFS= read -r -d '' jpg_file; do
    file_size=$(stat -f%z "$jpg_file" 2>/dev/null || stat -c%s "$jpg_file" 2>/dev/null)
    # Convert large JPGs (> 500KB) to WebP
    if [ "$file_size" -gt 512000 ]; then
        convert_to_webp "$jpg_file"
    fi
    # Remove EXIF from all JPGs
    remove_exif "$jpg_file"
done < <(find . -type f \( -name "*.jpg" -o -name "*.jpeg" \) ! -path "*/node_modules/*" ! -path "*/.git/*" -print0 2>/dev/null)

echo ""
echo "============================"
echo "✅ Optimization Complete"
echo "Total saved: $(numfmt --to=iec-i --suffix=B $TOTAL_SAVED 2>/dev/null || echo $TOTAL_SAVED bytes)"

if [ -n "$CHANGED_FILES" ]; then
    echo ""
    echo "Changed files:"
    echo "$CHANGED_FILES" | tr ' ' '\n' | grep -v '^$'
    echo ""
    echo "Files ready to commit"
else
    echo "No files were optimized"
fi

exit 0
