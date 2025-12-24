#!/bin/bash
set -euo pipefail

# ============================================================================
# Tokyo-IA Emulator/Validator
# Validates generated platform code and performs security scanning
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_BASE="$PROJECT_ROOT/output"
REPORT_FILE="$PROJECT_ROOT/simulator/output/emulator_report.txt"

echo "🔍 Tokyo-IA Emulator/Validator"
echo "==============================="
echo ""

# Initialize report
{
    echo "==============================================="
    echo "Tokyo-IA Platform Code Validation Report"
    echo "Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
    echo "==============================================="
    echo ""
} > "$REPORT_FILE"

TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNINGS=0

# Helper function to log results
log_result() {
    local status=$1
    local message=$2
    echo "$status $message" | tee -a "$REPORT_FILE"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ "$status" = "✅" ]; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    elif [ "$status" = "❌" ]; then
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    elif [ "$status" = "⚠️ " ]; then
        WARNINGS=$((WARNINGS + 1))
    fi
}

# ============================================================================
# ANDROID VALIDATION
# ============================================================================

echo "📱 Validating Android Code..." | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

ANDROID_DIR="$OUTPUT_BASE/android"

if [ -d "$ANDROID_DIR" ] && [ "$(ls -A "$ANDROID_DIR" 2>/dev/null)" ]; then
    log_result "✅" "Android code directory exists and is not empty"
    
    # Check MainActivity.kt
    if [ -f "$ANDROID_DIR/MainActivity.kt" ]; then
        log_result "✅" "MainActivity.kt exists"
        
        # Verify package declaration
        if grep -q "^package com\\.tokyoia\\.app" "$ANDROID_DIR/MainActivity.kt"; then
            log_result "✅" "MainActivity has valid package declaration"
        else
            log_result "❌" "MainActivity missing or invalid package declaration"
        fi
        
        # Verify imports
        if grep -q "import androidx\\.coordinatorlayout\\.widget\\.CoordinatorLayout" "$ANDROID_DIR/MainActivity.kt"; then
            log_result "✅" "MainActivity has required CoordinatorLayout import"
        else
            log_result "⚠️ " "MainActivity missing CoordinatorLayout import"
        fi
        
        if grep -q "import com\\.google\\.android\\.material\\.appbar\\.MaterialToolbar" "$ANDROID_DIR/MainActivity.kt"; then
            log_result "✅" "MainActivity has required MaterialToolbar import"
        else
            log_result "⚠️ " "MainActivity missing MaterialToolbar import"
        fi
        
        # Check for deprecated APIs
        if grep -q "ActionBarActivity\|PreferenceActivity" "$ANDROID_DIR/MainActivity.kt"; then
            log_result "❌" "MainActivity uses deprecated APIs"
        else
            log_result "✅" "MainActivity does not use deprecated APIs"
        fi
    else
        log_result "❌" "MainActivity.kt not found"
    fi
    
    # Check activity_main.xml
    if [ -f "$ANDROID_DIR/activity_main.xml" ]; then
        log_result "✅" "activity_main.xml exists"
        
        # Verify valid XML structure
        if xmllint --noout "$ANDROID_DIR/activity_main.xml" 2>/dev/null; then
            log_result "✅" "activity_main.xml is valid XML"
        else
            # Try basic validation if xmllint is not available
            if grep -q "<?xml version" "$ANDROID_DIR/activity_main.xml" && grep -q "</androidx.coordinatorlayout.widget.CoordinatorLayout>" "$ANDROID_DIR/activity_main.xml"; then
                log_result "✅" "activity_main.xml has valid structure"
            else
                log_result "❌" "activity_main.xml has invalid XML structure"
            fi
        fi
        
        # Check for required components
        if grep -q "CoordinatorLayout" "$ANDROID_DIR/activity_main.xml"; then
            log_result "✅" "Layout uses CoordinatorLayout"
        else
            log_result "❌" "Layout missing CoordinatorLayout"
        fi
        
        if grep -q "MaterialToolbar" "$ANDROID_DIR/activity_main.xml"; then
            log_result "✅" "Layout includes MaterialToolbar"
        else
            log_result "❌" "Layout missing MaterialToolbar"
        fi
    else
        log_result "❌" "activity_main.xml not found"
    fi
else
    log_result "⚠️ " "Android code not generated (platform may not be selected)"
fi

# ============================================================================
# iOS VALIDATION
# ============================================================================

echo "" | tee -a "$REPORT_FILE"
echo "🍎 Validating iOS Code..." | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

IOS_DIR="$OUTPUT_BASE/ios"

if [ -d "$IOS_DIR" ] && [ "$(ls -A "$IOS_DIR" 2>/dev/null)" ]; then
    log_result "✅" "iOS code directory exists and is not empty"
    
    # Check MainViewController.swift
    if [ -f "$IOS_DIR/MainViewController.swift" ]; then
        log_result "✅" "MainViewController.swift exists"
        
        # Verify UIKit import
        if grep -q "^import UIKit" "$IOS_DIR/MainViewController.swift"; then
            log_result "✅" "MainViewController imports UIKit"
        else
            log_result "❌" "MainViewController missing UIKit import"
        fi
        
        # Verify class declaration
        if grep -q "class MainViewController: UIViewController" "$IOS_DIR/MainViewController.swift"; then
            log_result "✅" "MainViewController has valid class declaration"
        else
            log_result "❌" "MainViewController has invalid class declaration"
        fi
        
        # Check for viewDidLoad
        if grep -q "override func viewDidLoad()" "$IOS_DIR/MainViewController.swift"; then
            log_result "✅" "MainViewController implements viewDidLoad"
        else
            log_result "❌" "MainViewController missing viewDidLoad implementation"
        fi
        
        # Check for Auto Layout constraints
        if grep -q "NSLayoutConstraint\|translatesAutoresizingMaskIntoConstraints" "$IOS_DIR/MainViewController.swift"; then
            log_result "✅" "MainViewController uses Auto Layout"
        else
            log_result "⚠️ " "MainViewController may not be using Auto Layout"
        fi
    else
        log_result "❌" "MainViewController.swift not found"
    fi
else
    log_result "⚠️ " "iOS code not generated (platform may not be selected)"
fi

# ============================================================================
# WEB VALIDATION
# ============================================================================

echo "" | tee -a "$REPORT_FILE"
echo "🌐 Validating Web Code..." | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

WEB_DIR="$OUTPUT_BASE/web"

if [ -d "$WEB_DIR" ] && [ "$(ls -A "$WEB_DIR" 2>/dev/null)" ]; then
    log_result "✅" "Web code directory exists and is not empty"
    
    # Check App.tsx
    if [ -f "$WEB_DIR/App.tsx" ]; then
        log_result "✅" "App.tsx exists"
        
        # Verify React import
        if grep -q "^import React from 'react'" "$WEB_DIR/App.tsx"; then
            log_result "✅" "App.tsx imports React"
        else
            log_result "❌" "App.tsx missing React import"
        fi
        
        # Verify component structure
        if grep -q "const App: React\\.FC" "$WEB_DIR/App.tsx"; then
            log_result "✅" "App.tsx has valid React component"
        else
            log_result "❌" "App.tsx has invalid component structure"
        fi
        
        # Check for semantic HTML
        if grep -q "<main\\|<header\\|<div" "$WEB_DIR/App.tsx"; then
            log_result "✅" "App.tsx uses semantic HTML"
        else
            log_result "⚠️ " "App.tsx may not use semantic HTML"
        fi
        
        # Check for accessibility attributes
        if grep -q "aria-\\|role=" "$WEB_DIR/App.tsx"; then
            log_result "✅" "App.tsx includes accessibility attributes"
        else
            log_result "⚠️ " "App.tsx missing accessibility attributes (consider adding aria-labels)"
        fi
    else
        log_result "❌" "App.tsx not found"
    fi
    
    # Check App.css
    if [ -f "$WEB_DIR/App.css" ]; then
        log_result "✅" "App.css exists"
        
        # Verify CSS structure
        if grep -q "\\.scaffold\\|\\.app-bar\\|\\.container" "$WEB_DIR/App.css"; then
            log_result "✅" "App.css has valid CSS classes"
        else
            log_result "❌" "App.css missing expected CSS classes"
        fi
    else
        log_result "❌" "App.css not found"
    fi
else
    log_result "⚠️ " "Web code not generated (platform may not be selected)"
fi

# ============================================================================
# SECURITY SCAN
# ============================================================================

echo "" | tee -a "$REPORT_FILE"
echo "🔒 Security Scan..." | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Search for hardcoded secrets
SECRET_PATTERNS=("api_key" "password" "secret" "token" "private_key" "apikey" "api-key")
SECRETS_FOUND=0

for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -ri "$pattern" "$OUTPUT_BASE" 2>/dev/null | grep -v "Auto-generated" | grep -v "comment" | head -n 1 > /dev/null; then
        log_result "⚠️ " "Potential secret pattern found: $pattern (verify if it's hardcoded)"
        SECRETS_FOUND=$((SECRETS_FOUND + 1))
    fi
done

if [ $SECRETS_FOUND -eq 0 ]; then
    log_result "✅" "No hardcoded secrets detected"
else
    log_result "⚠️ " "Found $SECRETS_FOUND potential secret patterns - manual review recommended"
fi

# Check for SQL injection vulnerabilities
if grep -ri "executeQuery\|rawQuery" "$OUTPUT_BASE" 2>/dev/null | grep -v "?" > /dev/null; then
    log_result "⚠️ " "Potential SQL injection risk - ensure parameterized queries are used"
else
    log_result "✅" "No SQL injection patterns detected"
fi

# ============================================================================
# STORE POLICY COMPLIANCE
# ============================================================================

echo "" | tee -a "$REPORT_FILE"
echo "📋 Store Policy Compliance..." | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Check for prohibited APIs
PROHIBITED_APIS=("ANDROID_ID" "getDeviceId" "getSubscriberId")
PROHIBITED_FOUND=0

for api in "${PROHIBITED_APIS[@]}"; do
    if grep -ri "$api" "$OUTPUT_BASE" 2>/dev/null > /dev/null; then
        log_result "⚠️ " "Prohibited API found: $api (may violate store policies)"
        PROHIBITED_FOUND=$((PROHIBITED_FOUND + 1))
    fi
done

if [ $PROHIBITED_FOUND -eq 0 ]; then
    log_result "✅" "No prohibited APIs detected"
fi

# ============================================================================
# SUMMARY
# ============================================================================

echo "" | tee -a "$REPORT_FILE"
echo "===============================================" | tee -a "$REPORT_FILE"
echo "VALIDATION SUMMARY" | tee -a "$REPORT_FILE"
echo "===============================================" | tee -a "$REPORT_FILE"
echo "Total Checks: $TOTAL_CHECKS" | tee -a "$REPORT_FILE"
echo "Passed: $PASSED_CHECKS" | tee -a "$REPORT_FILE"
echo "Failed: $FAILED_CHECKS" | tee -a "$REPORT_FILE"
echo "Warnings: $WARNINGS" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo "✅ Validation completed successfully!" | tee -a "$REPORT_FILE"
    EXIT_CODE=0
else
    echo "⚠️  Validation completed with $FAILED_CHECKS failed checks" | tee -a "$REPORT_FILE"
    EXIT_CODE=1
fi

echo "" | tee -a "$REPORT_FILE"
echo "📄 Full report saved to: $REPORT_FILE"

exit $EXIT_CODE
