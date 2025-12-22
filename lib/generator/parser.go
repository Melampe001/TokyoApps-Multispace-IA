// Package generator provides parsing functionality for project commands.
package generator

import (
	"regexp"
	"strings"
)

// Parser handles parsing of project generation commands.
type Parser struct{}

// NewParser creates a new Parser instance.
func NewParser() *Parser {
	return &Parser{}
}

// ParseCommand extracts the project description from a command.
// Supports formats:
// - "// PROYECTO: [description]"
// - "PROYECTO: [description]"
// - Plain description
func (p *Parser) ParseCommand(input string) string {
	input = strings.TrimSpace(input)

	// Match "// PROYECTO: description" or "PROYECTO: description"
	re := regexp.MustCompile(`(?i)^(?://\s*)?PROYECTO:\s*(.+)$`)
	matches := re.FindStringSubmatch(input)

	if len(matches) > 1 {
		return strings.TrimSpace(matches[1])
	}

	// If no match, return the input as-is (assume it's just the description)
	return input
}

// ExtractKeywords extracts important keywords from a description.
func (p *Parser) ExtractKeywords(description string) []string {
	// Convert to lowercase for matching
	lower := strings.ToLower(description)

	// Split into words
	words := strings.Fields(lower)

	// Remove common stop words
	stopWords := map[string]bool{
		"the": true, "a": true, "an": true, "and": true, "or": true,
		"but": true, "in": true, "on": true, "at": true, "to": true,
		"for": true, "of": true, "with": true, "by": true, "from": true,
		"up": true, "about": true, "into": true, "through": true, "during": true,
	}

	var keywords []string
	for _, word := range words {
		// Remove punctuation
		word = strings.Trim(word, ".,;:!?()[]{}\"'")
		if word != "" && !stopWords[word] {
			keywords = append(keywords, word)
		}
	}

	return keywords
}
