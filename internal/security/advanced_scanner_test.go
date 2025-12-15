package security

import (
	"testing"
)

func TestNewAdvancedScanner(t *testing.T) {
	scanner := NewAdvancedScanner()
	if scanner == nil {
		t.Fatal("NewAdvancedScanner returned nil")
	}
	if scanner.vulnerabilityDB == nil {
		t.Error("VulnerabilityDB not initialized")
	}
	if scanner.complianceChecker == nil {
		t.Error("ComplianceChecker not initialized")
	}
}

func TestScanCode(t *testing.T) {
	scanner := NewAdvancedScanner()

	tests := []struct {
		name         string
		code         string
		wantVulns    bool
		wantSeverity VulnerabilityLevel
		wantStatus   string
	}{
		{
			name:       "clean code",
			code:       "func hello() { return \"hello\" }",
			wantVulns:  false,
			wantStatus: "PASS",
		},
		{
			name:         "SQL injection",
			code:         "query := \"SELECT * FROM users WHERE id = \" + userId",
			wantVulns:    true,
			wantSeverity: Critical,
			wantStatus:   "FAIL",
		},
		{
			name:         "command injection",
			code:         "os.system(userInput)",
			wantVulns:    true,
			wantSeverity: High,
			wantStatus:   "FAIL",
		},
		{
			name:         "weak crypto",
			code:         "hash := md5.Sum(data)",
			wantVulns:    true,
			wantSeverity: Medium,
			wantStatus:   "WARNING",
		},
		{
			name:         "debug mode",
			code:         "debug = true",
			wantVulns:    true,
			wantSeverity: Medium,
			wantStatus:   "WARNING",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := scanner.ScanCode(tt.code, "test.go")
			if err != nil {
				t.Fatalf("ScanCode failed: %v", err)
			}

			if result == nil {
				t.Fatal("Expected result, got nil")
			}

			hasVulns := result.TotalVulnerabilities > 0
			if hasVulns != tt.wantVulns {
				t.Errorf("Expected vulnerabilities=%v, got %d vulnerabilities",
					tt.wantVulns, result.TotalVulnerabilities)
			}

			if tt.wantVulns && len(result.Vulnerabilities) > 0 {
				found := false
				for _, vuln := range result.Vulnerabilities {
					if vuln.Level == tt.wantSeverity {
						found = true
						break
					}
				}
				if !found {
					t.Errorf("Expected severity %v, not found in results", tt.wantSeverity)
				}
			}

			if result.Status != tt.wantStatus {
				t.Errorf("Expected status %s, got %s", tt.wantStatus, result.Status)
			}
		})
	}
}

func TestScanOWASPTop10(t *testing.T) {
	scanner := NewAdvancedScanner()

	tests := []struct {
		name     string
		code     string
		category string
	}{
		{
			name:     "A01 - Command Injection",
			code:     "exec(user_input)",
			category: "OWASP A01",
		},
		{
			name:     "A02 - Weak Crypto",
			code:     "sha1(password)",
			category: "OWASP A02",
		},
		{
			name:     "A03 - SQL Injection",
			code:     "SELECT * FROM users WHERE name = \" + input",
			category: "OWASP A03",
		},
		{
			name:     "A05 - Security Misconfiguration",
			code:     "app.config.debug = true",
			category: "OWASP A05",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			vulns := scanner.scanOWASPTop10(tt.code, "test.go")
			if len(vulns) == 0 {
				t.Error("Expected OWASP vulnerability, found none")
			}

			found := false
			for _, vuln := range vulns {
				if contains(vuln.Category, tt.category) {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("Expected category containing %q, not found", tt.category)
			}
		})
	}
}

func TestScanCommonIssues(t *testing.T) {
	scanner := NewAdvancedScanner()

	tests := []struct {
		name    string
		code    string
		wantCWE string
	}{
		{
			name:    "hardcoded password",
			code:    "password = \"secret123\"",
			wantCWE: "CWE-798",
		},
		{
			name:    "insecure random",
			code:    "num = math.random()",
			wantCWE: "CWE-338",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			vulns := scanner.scanCommonIssues(tt.code, "test.go")
			if len(vulns) == 0 {
				t.Error("Expected vulnerability, found none")
			}

			found := false
			for _, vuln := range vulns {
				if vuln.CWE == tt.wantCWE {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("Expected CWE %q, not found", tt.wantCWE)
			}
		})
	}
}

func TestCalculateComplianceScore(t *testing.T) {
	scanner := NewAdvancedScanner()

	tests := []struct {
		name  string
		vulns []Vulnerability
		want  int
	}{
		{
			name:  "no vulnerabilities",
			vulns: []Vulnerability{},
			want:  100,
		},
		{
			name: "one critical",
			vulns: []Vulnerability{
				{Level: Critical},
			},
			want: 80,
		},
		{
			name: "multiple severities",
			vulns: []Vulnerability{
				{Level: Critical},
				{Level: High},
				{Level: Medium},
			},
			want: 65,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			score := scanner.calculateComplianceScore(tt.vulns)
			if score != tt.want {
				t.Errorf("calculateComplianceScore() = %d, want %d", score, tt.want)
			}
		})
	}
}

func TestGenerateReport(t *testing.T) {
	scanner := NewAdvancedScanner()

	result := &ScanResult{
		TotalVulnerabilities: 5,
		VulnerabilitiesBySeverity: map[VulnerabilityLevel]int{
			Critical: 1,
			High:     2,
			Medium:   2,
		},
		ComplianceScore: 75,
		Status:          "FAIL",
	}

	report := scanner.GenerateReport(result)
	if report == "" {
		t.Error("Expected non-empty report")
	}

	if !contains(report, "Security Scan Report") {
		t.Error("Report missing title")
	}
	if !contains(report, "FAIL") {
		t.Error("Report missing status")
	}
	if !contains(report, "75") {
		t.Error("Report missing compliance score")
	}
}

func TestVulnerabilityFields(t *testing.T) {
	scanner := NewAdvancedScanner()

	code := "SELECT * FROM users WHERE id = \" + userId"
	result, err := scanner.ScanCode(code, "test.go")
	if err != nil {
		t.Fatalf("ScanCode failed: %v", err)
	}

	if len(result.Vulnerabilities) == 0 {
		t.Fatal("Expected vulnerabilities, got none")
	}

	vuln := result.Vulnerabilities[0]

	if vuln.ID == "" {
		t.Error("Vulnerability ID is empty")
	}
	if vuln.Title == "" {
		t.Error("Vulnerability Title is empty")
	}
	if vuln.Description == "" {
		t.Error("Vulnerability Description is empty")
	}
	if vuln.Category == "" {
		t.Error("Vulnerability Category is empty")
	}
	if vuln.FixSuggestion == "" {
		t.Error("Vulnerability FixSuggestion is empty")
	}
}

// Helper function
func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > len(substr) &&
		(s[:len(substr)] == substr || s[len(s)-len(substr):] == substr ||
			findSubstring(s, substr)))
}

func findSubstring(s, substr string) bool {
	for i := 0; i <= len(s)-len(substr); i++ {
		if s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}
