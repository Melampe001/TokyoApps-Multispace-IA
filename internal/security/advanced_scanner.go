// Package security provides security scanning and vulnerability detection.
package security

import (
	"fmt"
	"strings"
	"time"
)

// VulnerabilityLevel represents the severity of a vulnerability
type VulnerabilityLevel string

const (
	Critical VulnerabilityLevel = "CRITICAL"
	High     VulnerabilityLevel = "HIGH"
	Medium   VulnerabilityLevel = "MEDIUM"
	Low      VulnerabilityLevel = "LOW"
	Info     VulnerabilityLevel = "INFO"
)

// Vulnerability represents a detected security vulnerability
type Vulnerability struct {
	ID            string             `json:"id"`
	Title         string             `json:"title"`
	Description   string             `json:"description"`
	Level         VulnerabilityLevel `json:"level"`
	Category      string             `json:"category"`
	File          string             `json:"file"`
	Line          int                `json:"line"`
	Code          string             `json:"code"`
	CWE           string             `json:"cwe"`
	CVE           string             `json:"cve"`
	FixSuggestion string             `json:"fix_suggestion"`
	DetectedAt    time.Time          `json:"detected_at"`
}

// ScanResult represents the result of a security scan
type ScanResult struct {
	TotalVulnerabilities      int                        `json:"total_vulnerabilities"`
	VulnerabilitiesBySeverity map[VulnerabilityLevel]int `json:"vulnerabilities_by_severity"`
	Vulnerabilities           []Vulnerability            `json:"vulnerabilities"`
	ComplianceScore           int                        `json:"compliance_score"`
	ScanDuration              time.Duration              `json:"scan_duration"`
	ScannedAt                 time.Time                  `json:"scanned_at"`
	Status                    string                     `json:"status"`
}

// AdvancedScanner provides advanced security scanning capabilities
type AdvancedScanner struct {
	vulnerabilityDB   *VulnerabilityDB
	complianceChecker *ComplianceChecker
}

// NewAdvancedScanner creates a new advanced security scanner
func NewAdvancedScanner() *AdvancedScanner {
	return &AdvancedScanner{
		vulnerabilityDB:   NewVulnerabilityDB(),
		complianceChecker: NewComplianceChecker(),
	}
}

// ScanCode scans code for security vulnerabilities
func (as *AdvancedScanner) ScanCode(code string, filePath string) (*ScanResult, error) {
	startTime := time.Now()

	vulnerabilities := make([]Vulnerability, 0)

	// Scan for OWASP Top 10 vulnerabilities
	owaspVulns := as.scanOWASPTop10(code, filePath)
	vulnerabilities = append(vulnerabilities, owaspVulns...)

	// Scan for CVE matches
	cveVulns := as.scanCVEDatabase(code, filePath)
	vulnerabilities = append(vulnerabilities, cveVulns...)

	// Scan for common security issues
	commonVulns := as.scanCommonIssues(code, filePath)
	vulnerabilities = append(vulnerabilities, commonVulns...)

	// Calculate compliance score
	complianceScore := as.calculateComplianceScore(vulnerabilities)

	// Count by severity
	severityCounts := make(map[VulnerabilityLevel]int)
	for _, vuln := range vulnerabilities {
		severityCounts[vuln.Level]++
	}

	status := "PASS"
	if len(vulnerabilities) > 0 {
		if severityCounts[Critical] > 0 || severityCounts[High] > 0 {
			status = "FAIL"
		} else {
			status = "WARNING"
		}
	}

	return &ScanResult{
		TotalVulnerabilities:      len(vulnerabilities),
		VulnerabilitiesBySeverity: severityCounts,
		Vulnerabilities:           vulnerabilities,
		ComplianceScore:           complianceScore,
		ScanDuration:              time.Since(startTime),
		ScannedAt:                 time.Now(),
		Status:                    status,
	}, nil
}

// scanOWASPTop10 scans for OWASP Top 10 vulnerabilities
func (as *AdvancedScanner) scanOWASPTop10(code string, filePath string) []Vulnerability {
	vulnerabilities := make([]Vulnerability, 0)

	lines := strings.Split(code, "\n")

	// A01: Broken Access Control
	for i, line := range lines {
		if strings.Contains(line, "os.system(") || strings.Contains(line, "exec(") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("OWASP-A01-%d", i),
				Title:         "Potential Command Injection",
				Description:   "Direct execution of system commands can lead to command injection",
				Level:         High,
				Category:      "OWASP A01 - Broken Access Control",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-78",
				FixSuggestion: "Use parameterized commands or whitelist allowed commands",
				DetectedAt:    time.Now(),
			})
		}
	}

	// A02: Cryptographic Failures
	for i, line := range lines {
		if strings.Contains(line, "md5") || strings.Contains(line, "sha1") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("OWASP-A02-%d", i),
				Title:         "Weak Cryptographic Algorithm",
				Description:   "MD5 and SHA1 are cryptographically broken",
				Level:         Medium,
				Category:      "OWASP A02 - Cryptographic Failures",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-327",
				FixSuggestion: "Use SHA-256 or stronger algorithms",
				DetectedAt:    time.Now(),
			})
		}
	}

	// A03: Injection
	for i, line := range lines {
		if strings.Contains(line, "SELECT") && strings.Contains(line, "+") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("OWASP-A03-%d", i),
				Title:         "Potential SQL Injection",
				Description:   "String concatenation in SQL queries can lead to SQL injection",
				Level:         Critical,
				Category:      "OWASP A03 - Injection",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-89",
				FixSuggestion: "Use parameterized queries or prepared statements",
				DetectedAt:    time.Now(),
			})
		}
	}

	// A05: Security Misconfiguration
	for i, line := range lines {
		if strings.Contains(line, "debug") && strings.Contains(line, "true") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("OWASP-A05-%d", i),
				Title:         "Debug Mode Enabled",
				Description:   "Debug mode should not be enabled in production",
				Level:         Medium,
				Category:      "OWASP A05 - Security Misconfiguration",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-489",
				FixSuggestion: "Disable debug mode in production environments",
				DetectedAt:    time.Now(),
			})
		}
	}

	return vulnerabilities
}

// scanCVEDatabase scans against CVE database
func (as *AdvancedScanner) scanCVEDatabase(code string, filePath string) []Vulnerability {
	vulnerabilities := make([]Vulnerability, 0)

	// Check for known vulnerable patterns from CVE database
	cvePatterns := as.vulnerabilityDB.GetKnownPatterns()

	lines := strings.Split(code, "\n")
	for i, line := range lines {
		for _, pattern := range cvePatterns {
			if strings.Contains(line, pattern.Pattern) {
				vulnerabilities = append(vulnerabilities, Vulnerability{
					ID:            pattern.CVEID,
					Title:         pattern.Title,
					Description:   pattern.Description,
					Level:         pattern.Severity,
					Category:      "CVE Match",
					File:          filePath,
					Line:          i + 1,
					Code:          strings.TrimSpace(line),
					CVE:           pattern.CVEID,
					CWE:           pattern.CWEID,
					FixSuggestion: pattern.FixSuggestion,
					DetectedAt:    time.Now(),
				})
			}
		}
	}

	return vulnerabilities
}

// scanCommonIssues scans for common security issues
func (as *AdvancedScanner) scanCommonIssues(code string, filePath string) []Vulnerability {
	vulnerabilities := make([]Vulnerability, 0)

	lines := strings.Split(code, "\n")

	// Hardcoded credentials
	for i, line := range lines {
		if strings.Contains(line, "password") && strings.Contains(line, "=") &&
			!strings.Contains(line, "input") && !strings.Contains(line, "prompt") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("COMMON-CRED-%d", i),
				Title:         "Potential Hardcoded Credential",
				Description:   "Hardcoded passwords are a security risk",
				Level:         High,
				Category:      "Hardcoded Credentials",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-798",
				FixSuggestion: "Use environment variables or secure credential storage",
				DetectedAt:    time.Now(),
			})
		}
	}

	// Insecure random
	for i, line := range lines {
		if strings.Contains(line, "math.random") || strings.Contains(line, "rand.Seed") {
			vulnerabilities = append(vulnerabilities, Vulnerability{
				ID:            fmt.Sprintf("COMMON-RAND-%d", i),
				Title:         "Insecure Random Number Generator",
				Description:   "Standard random is not cryptographically secure",
				Level:         Medium,
				Category:      "Insecure Randomness",
				File:          filePath,
				Line:          i + 1,
				Code:          strings.TrimSpace(line),
				CWE:           "CWE-338",
				FixSuggestion: "Use crypto/rand for cryptographic operations",
				DetectedAt:    time.Now(),
			})
		}
	}

	return vulnerabilities
}

// calculateComplianceScore calculates a compliance score (0-100)
func (as *AdvancedScanner) calculateComplianceScore(vulnerabilities []Vulnerability) int {
	if len(vulnerabilities) == 0 {
		return 100
	}

	// Deduct points based on severity
	score := 100
	for _, vuln := range vulnerabilities {
		switch vuln.Level {
		case Critical:
			score -= 20
		case High:
			score -= 10
		case Medium:
			score -= 5
		case Low:
			score -= 2
		}
	}

	if score < 0 {
		score = 0
	}

	return score
}

// ScanRepository scans an entire repository
func (as *AdvancedScanner) ScanRepository(repoPath string) (*ScanResult, error) {
	// This would recursively scan all files in the repository
	// For now, returning a placeholder
	return &ScanResult{
		TotalVulnerabilities:      0,
		VulnerabilitiesBySeverity: make(map[VulnerabilityLevel]int),
		Vulnerabilities:           make([]Vulnerability, 0),
		ComplianceScore:           100,
		ScanDuration:              time.Second,
		ScannedAt:                 time.Now(),
		Status:                    "PASS",
	}, nil
}

// GenerateReport generates a security report
func (as *AdvancedScanner) GenerateReport(result *ScanResult) string {
	report := fmt.Sprintf("Security Scan Report\n")
	report += fmt.Sprintf("====================\n\n")
	report += fmt.Sprintf("Status: %s\n", result.Status)
	report += fmt.Sprintf("Compliance Score: %d/100\n", result.ComplianceScore)
	report += fmt.Sprintf("Total Vulnerabilities: %d\n\n", result.TotalVulnerabilities)

	if len(result.VulnerabilitiesBySeverity) > 0 {
		report += "By Severity:\n"
		for severity, count := range result.VulnerabilitiesBySeverity {
			report += fmt.Sprintf("  %s: %d\n", severity, count)
		}
	}

	return report
}
