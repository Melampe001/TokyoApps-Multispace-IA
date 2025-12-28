// Package main provides the security agent CLI for auditing Android manifests
package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/Melampe001/Tokyo-IA/internal/security"
)

func main() {
	// Define command line flags
	pathFlag := flag.String("path", ".", "Path to directory or AndroidManifest.xml file to audit")
	verboseFlag := flag.Bool("v", false, "Verbose output")
	helpFlag := flag.Bool("h", false, "Show help message")

	flag.Parse()

	if *helpFlag {
		printHelp()
		os.Exit(0)
	}

	// Print banner
	if *verboseFlag {
		printBanner()
	}

	// Create auditor
	auditor := security.NewManifestAuditor()

	// Check if path is a file or directory
	fileInfo, err := os.Stat(*pathFlag)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: Failed to access path '%s': %v\n", *pathFlag, err)
		os.Exit(1)
	}

	var results []*security.AuditResult

	if fileInfo.IsDir() {
		// Audit directory
		if *verboseFlag {
			fmt.Printf("Scanning directory: %s\n\n", *pathFlag)
		}

		results, err = auditor.AuditDirectory(*pathFlag)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: Failed to audit directory: %v\n", err)
			os.Exit(1)
		}
	} else {
		// Audit single file
		if *verboseFlag {
			fmt.Printf("Auditing file: %s\n\n", *pathFlag)
		}

		result, err := auditor.AuditManifestFile(*pathFlag)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: Failed to audit file: %v\n", err)
			os.Exit(1)
		}
		results = []*security.AuditResult{result}
	}

	// Print results
	security.PrintResults(results)

	// Exit with appropriate code
	if security.HasFailures(results) {
		os.Exit(1)
	}

	os.Exit(0)
}

func printBanner() {
	fmt.Print(`
  ╔════════════════════════════════════════════════════════╗
  ║                                                        ║
  ║       🔒 TOKYO-IA SECURITY AGENT 🔒                   ║
  ║                                                        ║
  ║       Android Manifest Permission Auditor              ║
  ║       Local-First Architecture Validator               ║
  ║                                                        ║
  ╚════════════════════════════════════════════════════════╝
`)
}

func printHelp() {
	fmt.Print(`Tokyo-IA Security Agent - Android Manifest Auditor

ROLE: SECURITY_AGENT

DESCRIPTION:
  Audits AndroidManifest.xml files for forbidden permissions that violate
  local-first architecture principles.

USAGE:
  security-agent [flags]

FLAGS:
  -path string
        Path to directory or AndroidManifest.xml file to audit (default: ".")
  -v    Verbose output
  -h    Show this help message

FORBIDDEN PERMISSIONS:
  The following permissions are strictly forbidden:

  LOCATION:
    - ACCESS_FINE_LOCATION
    - ACCESS_COARSE_LOCATION
    - ACCESS_BACKGROUND_LOCATION

  CONTACTS:
    - READ_CONTACTS
    - WRITE_CONTACTS
    - GET_ACCOUNTS

  CAMERA:
    - CAMERA

  TRACKING:
    - READ_PHONE_STATE
    - ACCESS_WIFI_STATE
    - BLUETOOTH
    - BLUETOOTH_ADMIN
    - BLUETOOTH_CONNECT
    - BLUETOOTH_SCAN

  BACKGROUND_SERVICES:
    - WAKE_LOCK
    - FOREGROUND_SERVICE
    - REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
    - SYSTEM_ALERT_WINDOW

  PRIVACY:
    - RECORD_AUDIO
    - READ_SMS / SEND_SMS / RECEIVE_SMS
    - READ_CALL_LOG / WRITE_CALL_LOG

EXIT CODES:
  0 - All audits passed (no forbidden permissions found)
  1 - One or more audits failed (forbidden permissions detected)

EXAMPLES:
  # Audit current directory
  security-agent

  # Audit specific directory
  security-agent -path ./app/src/main

  # Audit specific file with verbose output
  security-agent -path ./app/src/main/AndroidManifest.xml -v

  # Scan entire project
  security-agent -path . -v

RULE:
  Forbidden permission detected → FAIL
  Local-first verification → PASS only if no forbidden permissions

For more information, visit:
https://github.com/Melampe001/Tokyo-IA
`)
}
