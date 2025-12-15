// Package generator provides project type analysis and detection.
package generator

import (
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)

// Analyzer detects project types and optimal stacks.
type Analyzer struct {
	manifestPath string
	patterns     map[string][]string
}

// NewAnalyzer creates a new Analyzer with the given manifest path.
func NewAnalyzer(manifestPath string) *Analyzer {
	return &Analyzer{
		manifestPath: manifestPath,
		patterns:     make(map[string][]string),
	}
}

// DetectProjectType analyzes keywords and determines the best project type.
func (a *Analyzer) DetectProjectType(keywords []string) (ProjectType, error) {
	// Load manifest to get detection patterns
	err := a.loadPatterns()
	if err != nil {
		// Fallback to simple keyword matching if manifest not available
		return a.simpleDetection(keywords), nil
	}
	
	// Score each project type based on keyword matches
	scores := make(map[ProjectType]int)
	
	for _, keyword := range keywords {
		keyword = strings.ToLower(keyword)
		
		// Check against patterns
		if a.matchesPattern(keyword, "pwa") {
			scores[ProjectTypePWA]++
		}
		if a.matchesPattern(keyword, "bot") {
			scores[ProjectTypeBot]++
		}
		if a.matchesPattern(keyword, "api") {
			scores[ProjectTypeAPI]++
		}
		if a.matchesPattern(keyword, "ecommerce") {
			scores[ProjectTypeEcommerce]++
		}
		if a.matchesPattern(keyword, "ai-agent") {
			scores[ProjectTypeAIAgent]++
		}
	}
	
	// Find the type with highest score
	var bestType ProjectType
	maxScore := 0
	
	for pType, score := range scores {
		if score > maxScore {
			maxScore = score
			bestType = pType
		}
	}
	
	// Default to API if no clear match
	if maxScore == 0 {
		return ProjectTypeAPI, nil
	}
	
	return bestType, nil
}

// loadPatterns loads detection patterns from the manifest.
func (a *Analyzer) loadPatterns() error {
	data, err := os.ReadFile(a.manifestPath)
	if err != nil {
		return err
	}
	
	var manifest struct {
		DetectionPatterns map[string]struct {
			Keywords   []string `yaml:"keywords"`
			Indicators []string `yaml:"indicators"`
		} `yaml:"detection_patterns"`
	}
	
	err = yaml.Unmarshal(data, &manifest)
	if err != nil {
		return err
	}
	
	// Build patterns map
	for pType, pattern := range manifest.DetectionPatterns {
		allPatterns := append(pattern.Keywords, pattern.Indicators...)
		a.patterns[pType] = allPatterns
	}
	
	return nil
}

// matchesPattern checks if a keyword matches any pattern for a project type.
func (a *Analyzer) matchesPattern(keyword string, projectType string) bool {
	patterns, exists := a.patterns[projectType]
	if !exists {
		return false
	}
	
	for _, pattern := range patterns {
		if strings.Contains(keyword, pattern) || strings.Contains(pattern, keyword) {
			return true
		}
	}
	
	return false
}

// simpleDetection provides basic detection without manifest.
func (a *Analyzer) simpleDetection(keywords []string) ProjectType {
	keywordStr := strings.ToLower(strings.Join(keywords, " "))
	
	if strings.Contains(keywordStr, "bot") || strings.Contains(keywordStr, "telegram") || strings.Contains(keywordStr, "discord") {
		return ProjectTypeBot
	}
	if strings.Contains(keywordStr, "ecommerce") || strings.Contains(keywordStr, "shop") || strings.Contains(keywordStr, "store") {
		return ProjectTypeEcommerce
	}
	if strings.Contains(keywordStr, "ai") || strings.Contains(keywordStr, "agent") || strings.Contains(keywordStr, "crewai") {
		return ProjectTypeAIAgent
	}
	if strings.Contains(keywordStr, "pwa") || strings.Contains(keywordStr, "progressive") {
		return ProjectTypePWA
	}
	
	// Default to API
	return ProjectTypeAPI
}

// GetOptimalStack returns the optimal technology stack for a project type.
func (a *Analyzer) GetOptimalStack(projectType ProjectType) ([]string, error) {
	// Load manifest
	data, err := os.ReadFile(a.manifestPath)
	if err != nil {
		return a.defaultStack(projectType), nil
	}
	
	var manifest struct {
		Templates map[string]struct {
			Stack []string `yaml:"stack"`
		} `yaml:"templates"`
	}
	
	err = yaml.Unmarshal(data, &manifest)
	if err != nil {
		return a.defaultStack(projectType), nil
	}
	
	template, exists := manifest.Templates[string(projectType)]
	if !exists || len(template.Stack) == 0 {
		return a.defaultStack(projectType), nil
	}
	
	return template.Stack, nil
}

// defaultStack provides default stacks when manifest is not available.
func (a *Analyzer) defaultStack(projectType ProjectType) []string {
	switch projectType {
	case ProjectTypePWA:
		return []string{"typescript", "react", "vite", "pwa"}
	case ProjectTypeBot:
		return []string{"python", "python-telegram-bot", "asyncio"}
	case ProjectTypeAPI:
		return []string{"go", "gin", "gorm", "swagger"}
	case ProjectTypeEcommerce:
		return []string{"typescript", "nextjs", "stripe", "prisma"}
	case ProjectTypeAIAgent:
		return []string{"python", "crewai", "groq", "langchain"}
	default:
		return []string{"go"}
	}
}
