package security

import (
	"os"
	"path/filepath"
	"testing"
)

// Test data for manifests
const cleanManifest = `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.tokyoia.app">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name">
    </application>
</manifest>`

const manifestWithForbiddenPerms = `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.tokyoia.app">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name">
    </application>
</manifest>`

const manifestWithTrackingPerms = `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.tokyoia.tracking">
    
    <uses-permission android:name="android.permission.READ_PHONE_STATE" />
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
    
    <application
        android:allowBackup="true">
    </application>
</manifest>`

func TestNewManifestAuditor(t *testing.T) {
	auditor := NewManifestAuditor()
	if auditor == nil {
		t.Fatal("NewManifestAuditor returned nil")
	}

	if len(auditor.forbiddenPerms) == 0 {
		t.Error("Expected forbidden permissions to be initialized")
	}

	// Verify some key forbidden permissions are loaded
	expectedPerms := []string{
		"android.permission.ACCESS_FINE_LOCATION",
		"android.permission.CAMERA",
		"android.permission.READ_CONTACTS",
	}

	for _, perm := range expectedPerms {
		if _, exists := auditor.forbiddenPerms[perm]; !exists {
			t.Errorf("Expected forbidden permission %s not found", perm)
		}
	}
}

func TestAuditManifestFile_CleanManifest(t *testing.T) {
	// Create temporary manifest file
	tmpDir := t.TempDir()
	manifestPath := filepath.Join(tmpDir, "AndroidManifest.xml")

	if err := os.WriteFile(manifestPath, []byte(cleanManifest), 0644); err != nil {
		t.Fatalf("Failed to create test manifest: %v", err)
	}

	auditor := NewManifestAuditor()
	result, err := auditor.AuditManifestFile(manifestPath)

	if err != nil {
		t.Fatalf("AuditManifestFile failed: %v", err)
	}

	if !result.Passed {
		t.Error("Expected clean manifest to pass audit")
	}

	if !result.IsLocalFirst {
		t.Error("Expected clean manifest to be local-first")
	}

	if len(result.ForbiddenFound) != 0 {
		t.Errorf("Expected 0 forbidden permissions, got %d", len(result.ForbiddenFound))
	}

	if result.TotalPermissions != 3 {
		t.Errorf("Expected 3 total permissions, got %d", result.TotalPermissions)
	}
}

func TestAuditManifestFile_WithForbiddenPermissions(t *testing.T) {
	tmpDir := t.TempDir()
	manifestPath := filepath.Join(tmpDir, "AndroidManifest.xml")

	if err := os.WriteFile(manifestPath, []byte(manifestWithForbiddenPerms), 0644); err != nil {
		t.Fatalf("Failed to create test manifest: %v", err)
	}

	auditor := NewManifestAuditor()
	result, err := auditor.AuditManifestFile(manifestPath)

	if err != nil {
		t.Fatalf("AuditManifestFile failed: %v", err)
	}

	if result.Passed {
		t.Error("Expected manifest with forbidden permissions to fail audit")
	}

	if result.IsLocalFirst {
		t.Error("Expected manifest with forbidden permissions not to be local-first")
	}

	if len(result.ForbiddenFound) != 4 {
		t.Errorf("Expected 4 forbidden permissions, got %d", len(result.ForbiddenFound))
	}

	// Verify specific forbidden permissions are detected
	expectedForbidden := map[string]bool{
		"android.permission.ACCESS_FINE_LOCATION": false,
		"android.permission.CAMERA":               false,
		"android.permission.READ_CONTACTS":        false,
		"android.permission.WAKE_LOCK":            false,
	}

	for _, forbidden := range result.ForbiddenFound {
		if _, exists := expectedForbidden[forbidden.Name]; exists {
			expectedForbidden[forbidden.Name] = true
		}
	}

	for perm, found := range expectedForbidden {
		if !found {
			t.Errorf("Expected forbidden permission %s not detected", perm)
		}
	}
}

func TestAuditManifestFile_TrackingPermissions(t *testing.T) {
	tmpDir := t.TempDir()
	manifestPath := filepath.Join(tmpDir, "AndroidManifest.xml")

	if err := os.WriteFile(manifestPath, []byte(manifestWithTrackingPerms), 0644); err != nil {
		t.Fatalf("Failed to create test manifest: %v", err)
	}

	auditor := NewManifestAuditor()
	result, err := auditor.AuditManifestFile(manifestPath)

	if err != nil {
		t.Fatalf("AuditManifestFile failed: %v", err)
	}

	if result.Passed {
		t.Error("Expected manifest with tracking permissions to fail audit")
	}

	// Should detect all 4 tracking permissions
	if len(result.ForbiddenFound) != 4 {
		t.Errorf("Expected 4 forbidden tracking permissions, got %d", len(result.ForbiddenFound))
	}

	// Verify they're all categorized as TRACKING
	for _, forbidden := range result.ForbiddenFound {
		if forbidden.Category != "TRACKING" {
			t.Errorf("Expected TRACKING category for %s, got %s", forbidden.Name, forbidden.Category)
		}
	}
}

func TestAuditManifestFile_NonExistentFile(t *testing.T) {
	auditor := NewManifestAuditor()
	_, err := auditor.AuditManifestFile("/nonexistent/path/AndroidManifest.xml")

	if err == nil {
		t.Error("Expected error for non-existent file")
	}
}

func TestAuditManifestFile_InvalidXML(t *testing.T) {
	tmpDir := t.TempDir()
	manifestPath := filepath.Join(tmpDir, "AndroidManifest.xml")

	invalidXML := `<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.tokyoia.app">
    <uses-permission android:name="android.permission.INTERNET"
</manifest>`

	if err := os.WriteFile(manifestPath, []byte(invalidXML), 0644); err != nil {
		t.Fatalf("Failed to create test manifest: %v", err)
	}

	auditor := NewManifestAuditor()
	_, err := auditor.AuditManifestFile(manifestPath)

	if err == nil {
		t.Error("Expected error for invalid XML")
	}
}

func TestFindManifestFiles(t *testing.T) {
	tmpDir := t.TempDir()

	// Create directory structure with multiple manifests
	dirs := []string{
		filepath.Join(tmpDir, "app", "src", "main"),
		filepath.Join(tmpDir, "lib", "src", "main"),
		filepath.Join(tmpDir, ".hidden", "src"),
	}

	for _, dir := range dirs {
		if err := os.MkdirAll(dir, 0755); err != nil {
			t.Fatalf("Failed to create directory: %v", err)
		}
	}

	// Create manifest files
	manifests := []string{
		filepath.Join(tmpDir, "app", "src", "main", "AndroidManifest.xml"),
		filepath.Join(tmpDir, "lib", "src", "main", "AndroidManifest.xml"),
		filepath.Join(tmpDir, ".hidden", "src", "AndroidManifest.xml"), // Should be skipped
	}

	for _, manifest := range manifests {
		if err := os.WriteFile(manifest, []byte(cleanManifest), 0644); err != nil {
			t.Fatalf("Failed to create manifest: %v", err)
		}
	}

	auditor := NewManifestAuditor()
	foundFiles, err := auditor.FindManifestFiles(tmpDir)

	if err != nil {
		t.Fatalf("FindManifestFiles failed: %v", err)
	}

	// Should find 2 manifests (hidden directory should be skipped)
	if len(foundFiles) != 2 {
		t.Errorf("Expected 2 manifest files, found %d", len(foundFiles))
	}
}

func TestAuditDirectory(t *testing.T) {
	tmpDir := t.TempDir()

	// Create test structure
	appDir := filepath.Join(tmpDir, "app", "src", "main")
	if err := os.MkdirAll(appDir, 0755); err != nil {
		t.Fatalf("Failed to create directory: %v", err)
	}

	// Create clean manifest
	cleanPath := filepath.Join(appDir, "AndroidManifest.xml")
	if err := os.WriteFile(cleanPath, []byte(cleanManifest), 0644); err != nil {
		t.Fatalf("Failed to create clean manifest: %v", err)
	}

	// Create directory with forbidden permissions
	badAppDir := filepath.Join(tmpDir, "badapp", "src", "main")
	if err := os.MkdirAll(badAppDir, 0755); err != nil {
		t.Fatalf("Failed to create directory: %v", err)
	}

	badPath := filepath.Join(badAppDir, "AndroidManifest.xml")
	if err := os.WriteFile(badPath, []byte(manifestWithForbiddenPerms), 0644); err != nil {
		t.Fatalf("Failed to create bad manifest: %v", err)
	}

	auditor := NewManifestAuditor()
	results, err := auditor.AuditDirectory(tmpDir)

	if err != nil {
		t.Fatalf("AuditDirectory failed: %v", err)
	}

	if len(results) != 2 {
		t.Errorf("Expected 2 results, got %d", len(results))
	}

	// Check that one passed and one failed
	passCount := 0
	failCount := 0

	for _, result := range results {
		if result.Passed {
			passCount++
		} else {
			failCount++
		}
	}

	if passCount != 1 {
		t.Errorf("Expected 1 passed result, got %d", passCount)
	}

	if failCount != 1 {
		t.Errorf("Expected 1 failed result, got %d", failCount)
	}
}

func TestAuditDirectory_NoManifests(t *testing.T) {
	tmpDir := t.TempDir()

	auditor := NewManifestAuditor()
	_, err := auditor.AuditDirectory(tmpDir)

	if err == nil {
		t.Error("Expected error when no manifests found")
	}
}

func TestHasFailures(t *testing.T) {
	tests := []struct {
		name     string
		results  []*AuditResult
		expected bool
	}{
		{
			name: "No failures",
			results: []*AuditResult{
				{Passed: true},
				{Passed: true},
			},
			expected: false,
		},
		{
			name: "One failure",
			results: []*AuditResult{
				{Passed: true},
				{Passed: false},
			},
			expected: true,
		},
		{
			name: "All failures",
			results: []*AuditResult{
				{Passed: false},
				{Passed: false},
			},
			expected: true,
		},
		{
			name:     "Empty results",
			results:  []*AuditResult{},
			expected: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := HasFailures(tt.results)
			if result != tt.expected {
				t.Errorf("HasFailures() = %v, expected %v", result, tt.expected)
			}
		})
	}
}

func TestForbiddenPermissions_Coverage(t *testing.T) {
	// Ensure all required categories are covered
	requiredCategories := map[string]bool{
		"LOCATION":            false,
		"CONTACTS":            false,
		"CAMERA":              false,
		"TRACKING":            false,
		"BACKGROUND_SERVICES": false,
	}

	for _, perm := range ForbiddenPermissions {
		if _, exists := requiredCategories[perm.Category]; exists {
			requiredCategories[perm.Category] = true
		}
	}

	for category, found := range requiredCategories {
		if !found {
			t.Errorf("Required category %s not found in ForbiddenPermissions", category)
		}
	}
}

func TestPermissionCategories(t *testing.T) {
	tests := []struct {
		permission string
		category   string
	}{
		{"android.permission.ACCESS_FINE_LOCATION", "LOCATION"},
		{"android.permission.CAMERA", "CAMERA"},
		{"android.permission.READ_CONTACTS", "CONTACTS"},
		{"android.permission.READ_PHONE_STATE", "TRACKING"},
		{"android.permission.WAKE_LOCK", "BACKGROUND_SERVICES"},
	}

	auditor := NewManifestAuditor()

	for _, tt := range tests {
		t.Run(tt.permission, func(t *testing.T) {
			perm, exists := auditor.forbiddenPerms[tt.permission]
			if !exists {
				t.Errorf("Permission %s not found in forbidden list", tt.permission)
				return
			}

			if perm.Category != tt.category {
				t.Errorf("Permission %s: expected category %s, got %s",
					tt.permission, tt.category, perm.Category)
			}
		})
	}
}
