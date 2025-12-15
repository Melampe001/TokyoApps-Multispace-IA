// Package security provides compliance checking functionality.
package security

import (
	"fmt"
	"strings"
	"time"
)

// ComplianceStandard represents a compliance standard
type ComplianceStandard string

const (
	SOC2  ComplianceStandard = "SOC2"
	GDPR  ComplianceStandard = "GDPR"
	HIPAA ComplianceStandard = "HIPAA"
	PCI   ComplianceStandard = "PCI-DSS"
	ISO27001 ComplianceStandard = "ISO27001"
)

// ComplianceCheck represents a compliance check result
type ComplianceCheck struct {
	Standard    ComplianceStandard `json:"standard"`
	Requirement string             `json:"requirement"`
	Status      string             `json:"status"`
	Description string             `json:"description"`
	Findings    []string           `json:"findings"`
	CheckedAt   time.Time          `json:"checked_at"`
}

// ComplianceReport represents a compliance report
type ComplianceReport struct {
	Standards       []ComplianceStandard `json:"standards"`
	Checks          []ComplianceCheck    `json:"checks"`
	OverallScore    int                  `json:"overall_score"`
	PassedChecks    int                  `json:"passed_checks"`
	FailedChecks    int                  `json:"failed_checks"`
	WarningChecks   int                  `json:"warning_checks"`
	GeneratedAt     time.Time            `json:"generated_at"`
}

// ComplianceChecker checks code for compliance with security standards
type ComplianceChecker struct {
	enabledStandards []ComplianceStandard
}

// NewComplianceChecker creates a new compliance checker
func NewComplianceChecker() *ComplianceChecker {
	return &ComplianceChecker{
		enabledStandards: []ComplianceStandard{SOC2, GDPR, HIPAA, PCI, ISO27001},
	}
}

// CheckCompliance checks code for compliance
func (cc *ComplianceChecker) CheckCompliance(code string, filePath string) *ComplianceReport {
	checks := make([]ComplianceCheck, 0)
	
	for _, standard := range cc.enabledStandards {
		standardChecks := cc.checkStandard(standard, code, filePath)
		checks = append(checks, standardChecks...)
	}
	
	// Calculate statistics
	passed := 0
	failed := 0
	warnings := 0
	
	for _, check := range checks {
		switch check.Status {
		case "PASS":
			passed++
		case "FAIL":
			failed++
		case "WARNING":
			warnings++
		}
	}
	
	// Calculate overall score
	totalChecks := len(checks)
	score := 0
	if totalChecks > 0 {
		score = (passed * 100) / totalChecks
	}
	
	return &ComplianceReport{
		Standards:     cc.enabledStandards,
		Checks:        checks,
		OverallScore:  score,
		PassedChecks:  passed,
		FailedChecks:  failed,
		WarningChecks: warnings,
		GeneratedAt:   time.Now(),
	}
}

// checkStandard checks code against a specific standard
func (cc *ComplianceChecker) checkStandard(standard ComplianceStandard, code string, filePath string) []ComplianceCheck {
	checks := make([]ComplianceCheck, 0)
	
	switch standard {
	case SOC2:
		checks = append(checks, cc.checkSOC2(code, filePath)...)
	case GDPR:
		checks = append(checks, cc.checkGDPR(code, filePath)...)
	case HIPAA:
		checks = append(checks, cc.checkHIPAA(code, filePath)...)
	case PCI:
		checks = append(checks, cc.checkPCI(code, filePath)...)
	case ISO27001:
		checks = append(checks, cc.checkISO27001(code, filePath)...)
	}
	
	return checks
}

// checkSOC2 checks for SOC2 compliance
func (cc *ComplianceChecker) checkSOC2(code string, filePath string) []ComplianceCheck {
	checks := make([]ComplianceCheck, 0)
	
	// CC6.1 - Logical and Physical Access Controls
	findings := make([]string, 0)
	if strings.Contains(code, "public") && strings.Contains(code, "api") {
		findings = append(findings, "Public API endpoint detected - ensure proper access controls")
	}
	
	status := "PASS"
	if len(findings) > 0 {
		status = "WARNING"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    SOC2,
		Requirement: "CC6.1 - Access Controls",
		Status:      status,
		Description: "Logical and physical access controls",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	// CC7.2 - System Monitoring
	findings = make([]string, 0)
	hasLogging := strings.Contains(code, "log.") || strings.Contains(code, "logger")
	if !hasLogging {
		findings = append(findings, "No logging detected - implement audit logging")
		status = "WARNING"
	} else {
		status = "PASS"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    SOC2,
		Requirement: "CC7.2 - System Monitoring",
		Status:      status,
		Description: "System monitoring and audit logging",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	return checks
}

// checkGDPR checks for GDPR compliance
func (cc *ComplianceChecker) checkGDPR(code string, filePath string) []ComplianceCheck {
	checks := make([]ComplianceCheck, 0)
	
	// Article 32 - Security of processing
	findings := make([]string, 0)
	if strings.Contains(code, "password") && !strings.Contains(code, "hash") {
		findings = append(findings, "Potential unencrypted password - ensure encryption")
	}
	
	status := "PASS"
	if len(findings) > 0 {
		status = "FAIL"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    GDPR,
		Requirement: "Article 32 - Data Security",
		Status:      status,
		Description: "Security of processing personal data",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	// Article 25 - Data protection by design
	findings = make([]string, 0)
	hasEncryption := strings.Contains(code, "encrypt") || strings.Contains(code, "cipher")
	if !hasEncryption && (strings.Contains(code, "user") || strings.Contains(code, "personal")) {
		findings = append(findings, "Personal data without encryption - implement data protection")
		status = "WARNING"
	} else {
		status = "PASS"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    GDPR,
		Requirement: "Article 25 - Data Protection by Design",
		Status:      status,
		Description: "Data protection by design and by default",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	return checks
}

// checkHIPAA checks for HIPAA compliance
func (cc *ComplianceChecker) checkHIPAA(code string, filePath string) []ComplianceCheck {
	checks := make([]ComplianceCheck, 0)
	
	// 164.312(a)(1) - Access Control
	findings := make([]string, 0)
	if strings.Contains(code, "health") || strings.Contains(code, "patient") {
		if !strings.Contains(code, "auth") && !strings.Contains(code, "permission") {
			findings = append(findings, "Health data without access control - implement authentication")
		}
	}
	
	status := "PASS"
	if len(findings) > 0 {
		status = "FAIL"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    HIPAA,
		Requirement: "164.312(a)(1) - Access Control",
		Status:      status,
		Description: "Technical safeguards for access control",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	return checks
}

// checkPCI checks for PCI-DSS compliance
func (cc *ComplianceChecker) checkPCI(code string, filePath string) []ComplianceCheck {
	checks := make([]ComplianceCheck, 0)
	
	// Requirement 3 - Protect stored cardholder data
	findings := make([]string, 0)
	if strings.Contains(code, "card") || strings.Contains(code, "credit") {
		if !strings.Contains(code, "encrypt") {
			findings = append(findings, "Card data without encryption - must encrypt cardholder data")
		}
	}
	
	status := "PASS"
	if len(findings) > 0 {
		status = "FAIL"
	}
	
	checks = append(checks, ComplianceCheck{
		Standard:    PCI,
		Requirement: "Requirement 3 - Protect Cardholder Data",
		Status:      status,
		Description: "Protect stored cardholder data",
		Findings:    findings,
		CheckedAt:   time.Now(),
	})
	
	return checks
}

// checkISO27001 checks for ISO 27001 compliance
func (cc *ComplianceChecker) checkISO27001(code string, filePath string) []ComplianceCheck {
	// A.9 - Access Control
	findings := make([]string, 0)
	if strings.Contains(code, "admin") && !strings.Contains(code, "role") {
		findings = append(findings, "Admin access without role-based control")
	}
	
	status := "PASS"
	if len(findings) > 0 {
		status = "WARNING"
	}
	
	return []ComplianceCheck{
		{
			Standard:    ISO27001,
			Requirement: "A.9 - Access Control",
			Status:      status,
			Description: "Access control requirements",
			Findings:    findings,
			CheckedAt:   time.Now(),
		},
	}
}

// GenerateReport generates a compliance report
func (cc *ComplianceChecker) GenerateReport(report *ComplianceReport) string {
	output := "Compliance Report\n"
	output += "=================\n\n"
	output += fmt.Sprintf("Overall Score: %d/100\n", report.OverallScore)
	output += fmt.Sprintf("Passed: %d, Failed: %d, Warnings: %d\n\n", 
		report.PassedChecks, report.FailedChecks, report.WarningChecks)
	
	output += "Standards Checked:\n"
	for _, std := range report.Standards {
		output += fmt.Sprintf("  - %s\n", std)
	}
	
	return output
}
