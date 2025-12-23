// Package security provides security auditing tools for Tokyo-IA
package security

import (
	"encoding/xml"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// ForbiddenPermission represents a permission that should not be present
type ForbiddenPermission struct {
	Name        string
	Category    string
	Description string
}

// AuditResult represents the result of a security audit
type AuditResult struct {
	FilePath         string
	TotalPermissions int
	ForbiddenFound   []ForbiddenPermission
	AllPermissions   []string
	IsLocalFirst     bool
	Passed           bool
}

// Manifest represents an Android manifest structure
type Manifest struct {
	XMLName     xml.Name             `xml:"manifest"`
	Package     string               `xml:"package,attr"`
	Permissions []ManifestPermission `xml:"uses-permission"`
}

// ManifestPermission represents a permission entry in AndroidManifest.xml
type ManifestPermission struct {
	Name string `xml:"name,attr"`
}

// ForbiddenPermissions defines all permissions that violate local-first architecture
var ForbiddenPermissions = []ForbiddenPermission{
	// Location permissions
	{Name: "android.permission.ACCESS_FINE_LOCATION", Category: "LOCATION", Description: "Fine location access"},
	{Name: "android.permission.ACCESS_COARSE_LOCATION", Category: "LOCATION", Description: "Coarse location access"},
	{Name: "android.permission.ACCESS_BACKGROUND_LOCATION", Category: "LOCATION", Description: "Background location access"},

	// Contacts permissions
	{Name: "android.permission.READ_CONTACTS", Category: "CONTACTS", Description: "Read contacts"},
	{Name: "android.permission.WRITE_CONTACTS", Category: "CONTACTS", Description: "Write contacts"},
	{Name: "android.permission.GET_ACCOUNTS", Category: "CONTACTS", Description: "Get accounts"},

	// Camera permissions
	{Name: "android.permission.CAMERA", Category: "CAMERA", Description: "Camera access"},

	// Tracking permissions
	{Name: "android.permission.READ_PHONE_STATE", Category: "TRACKING", Description: "Read phone state (tracking)"},
	{Name: "android.permission.ACCESS_WIFI_STATE", Category: "TRACKING", Description: "Access WiFi state (tracking)"},
	{Name: "android.permission.BLUETOOTH", Category: "TRACKING", Description: "Bluetooth (tracking)"},
	{Name: "android.permission.BLUETOOTH_ADMIN", Category: "TRACKING", Description: "Bluetooth admin (tracking)"},
	{Name: "android.permission.BLUETOOTH_CONNECT", Category: "TRACKING", Description: "Bluetooth connect (tracking)"},
	{Name: "android.permission.BLUETOOTH_SCAN", Category: "TRACKING", Description: "Bluetooth scan (tracking)"},

	// Background service permissions
	{Name: "android.permission.WAKE_LOCK", Category: "BACKGROUND_SERVICES", Description: "Wake lock for background services"},
	{Name: "android.permission.FOREGROUND_SERVICE", Category: "BACKGROUND_SERVICES", Description: "Foreground service"},
	{Name: "android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS", Category: "BACKGROUND_SERVICES", Description: "Ignore battery optimizations"},
	{Name: "android.permission.SYSTEM_ALERT_WINDOW", Category: "BACKGROUND_SERVICES", Description: "System alert window"},

	// Additional privacy-invasive permissions
	{Name: "android.permission.RECORD_AUDIO", Category: "PRIVACY", Description: "Record audio"},
	{Name: "android.permission.READ_SMS", Category: "PRIVACY", Description: "Read SMS"},
	{Name: "android.permission.SEND_SMS", Category: "PRIVACY", Description: "Send SMS"},
	{Name: "android.permission.RECEIVE_SMS", Category: "PRIVACY", Description: "Receive SMS"},
	{Name: "android.permission.READ_CALL_LOG", Category: "PRIVACY", Description: "Read call log"},
	{Name: "android.permission.WRITE_CALL_LOG", Category: "PRIVACY", Description: "Write call log"},
}

// ManifestAuditor performs security audits on AndroidManifest.xml files
type ManifestAuditor struct {
	forbiddenPerms map[string]ForbiddenPermission
}

// NewManifestAuditor creates a new manifest auditor
func NewManifestAuditor() *ManifestAuditor {
	auditor := &ManifestAuditor{
		forbiddenPerms: make(map[string]ForbiddenPermission),
	}

	// Build permission map for fast lookup
	for _, perm := range ForbiddenPermissions {
		auditor.forbiddenPerms[perm.Name] = perm
	}

	return auditor
}

// AuditManifestFile audits a single AndroidManifest.xml file
func (a *ManifestAuditor) AuditManifestFile(filePath string) (*AuditResult, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read manifest file: %w", err)
	}

	var manifest Manifest
	if err := xml.Unmarshal(data, &manifest); err != nil {
		return nil, fmt.Errorf("failed to parse manifest XML: %w", err)
	}

	result := &AuditResult{
		FilePath:         filePath,
		TotalPermissions: len(manifest.Permissions),
		ForbiddenFound:   []ForbiddenPermission{},
		AllPermissions:   []string{},
		IsLocalFirst:     true,
		Passed:           true,
	}

	// Check each permission
	for _, perm := range manifest.Permissions {
		result.AllPermissions = append(result.AllPermissions, perm.Name)

		// Check if permission is forbidden
		if forbiddenPerm, isForbidden := a.forbiddenPerms[perm.Name]; isForbidden {
			result.ForbiddenFound = append(result.ForbiddenFound, forbiddenPerm)
			result.IsLocalFirst = false
			result.Passed = false
		}
	}

	return result, nil
}

// FindManifestFiles searches for AndroidManifest.xml files in a directory tree
func (a *ManifestAuditor) FindManifestFiles(rootPath string) ([]string, error) {
	var manifestFiles []string

	err := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip hidden directories and git directories
		if info.IsDir() {
			if strings.HasPrefix(info.Name(), ".") {
				return filepath.SkipDir
			}
			return nil
		}

		// Check if file is AndroidManifest.xml
		if info.Name() == "AndroidManifest.xml" {
			manifestFiles = append(manifestFiles, path)
		}

		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("failed to walk directory: %w", err)
	}

	return manifestFiles, nil
}

// AuditDirectory scans a directory for AndroidManifest.xml files and audits them
func (a *ManifestAuditor) AuditDirectory(rootPath string) ([]*AuditResult, error) {
	manifestFiles, err := a.FindManifestFiles(rootPath)
	if err != nil {
		return nil, err
	}

	if len(manifestFiles) == 0 {
		return nil, fmt.Errorf("no AndroidManifest.xml files found in %s", rootPath)
	}

	var results []*AuditResult
	for _, file := range manifestFiles {
		result, err := a.AuditManifestFile(file)
		if err != nil {
			return nil, fmt.Errorf("failed to audit %s: %w", file, err)
		}
		results = append(results, result)
	}

	return results, nil
}

// PrintResults prints audit results in a formatted way
func PrintResults(results []*AuditResult) {
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println("🔒 ANDROID MANIFEST SECURITY AUDIT")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Println()

	totalPassed := 0
	totalFailed := 0

	for _, result := range results {
		if result.Passed {
			fmt.Printf("✅ PASS: %s\n", result.FilePath)
			totalPassed++
		} else {
			fmt.Printf("❌ FAIL: %s\n", result.FilePath)
			totalFailed++
		}

		fmt.Printf("   Total Permissions: %d\n", result.TotalPermissions)
		fmt.Printf("   Local-First: %v\n", result.IsLocalFirst)

		if len(result.ForbiddenFound) > 0 {
			fmt.Printf("   ⚠️  Forbidden Permissions Detected: %d\n", len(result.ForbiddenFound))
			for _, forbidden := range result.ForbiddenFound {
				fmt.Printf("      • [%s] %s - %s\n",
					forbidden.Category,
					strings.TrimPrefix(forbidden.Name, "android.permission."),
					forbidden.Description)
			}
		}

		if len(result.AllPermissions) > 0 {
			fmt.Printf("   All Permissions:\n")
			for _, perm := range result.AllPermissions {
				fmt.Printf("      • %s\n", perm)
			}
		}

		fmt.Println()
	}

	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("Summary: %d passed, %d failed\n", totalPassed, totalFailed)
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

	if totalFailed > 0 {
		fmt.Println("❌ AUDIT FAILED: Forbidden permissions detected")
		fmt.Println("   Local-first architecture violated")
	} else {
		fmt.Println("✅ AUDIT PASSED: No forbidden permissions detected")
		fmt.Println("   Local-first architecture verified")
	}
}

// HasFailures returns true if any audit result has failures
func HasFailures(results []*AuditResult) bool {
	for _, result := range results {
		if !result.Passed {
			return true
		}
	}
	return false
}
