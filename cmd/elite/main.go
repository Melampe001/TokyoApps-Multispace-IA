// Package main provides the CLI for the Elite Framework.
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"github.com/Melampe001/Tokyo-IA/lib/generator"
)

const (
	version = "1.0.0"
)

func main() {
	// Define flags
	generateCmd := flag.NewFlagSet("generate", flag.ExitOnError)
	outputDir := generateCmd.String("output", "./output", "Output directory for generated projects")
	
	// Parse flags
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}
	
	// Check for global flags
	for _, arg := range os.Args[1:] {
		if arg == "--version" || arg == "-v" {
			fmt.Printf("Tokyo-IA Elite Framework v%s\n", version)
			os.Exit(0)
		}
		if arg == "--help" || arg == "-h" {
			printUsage()
			os.Exit(0)
		}
	}
	
	command := os.Args[1]
	
	switch command {
	case "generate":
		if len(os.Args) < 3 {
			fmt.Println("Error: project description required")
			fmt.Println("\nUsage: elite generate \"project description\"")
			os.Exit(1)
		}
		
		generateCmd.Parse(os.Args[2:])
		
		// Get project description
		var description string
		if generateCmd.NArg() > 0 {
			description = generateCmd.Arg(0)
		} else {
			fmt.Println("Error: project description required")
			os.Exit(1)
		}
		
		err := generateProject(description, *outputDir)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
	
	case "version":
		fmt.Printf("Tokyo-IA Elite Framework v%s\n", version)
	
	case "help":
		printUsage()
	
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func generateProject(description, outputDir string) error {
	fmt.Println("🚀 Tokyo-IA Elite Framework")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("📝 Description: %s\n", description)
	fmt.Println()
	
	// Get manifest path
	manifestPath := findManifestPath()
	
	// Create generator
	gen := generator.NewGenerator(manifestPath)
	
	// Generate project
	fmt.Println("🔍 Analyzing project requirements...")
	config, err := gen.Generate(description, outputDir)
	if err != nil {
		return err
	}
	
	fmt.Println()
	fmt.Println("✅ Project generated successfully!")
	fmt.Println("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
	fmt.Printf("📦 Project Name: %s\n", config.Name)
	fmt.Printf("🏷️  Type: %s\n", config.Type)
	fmt.Printf("🛠️  Stack: %v\n", config.Stack)
	fmt.Printf("📂 Location: %s\n", config.OutputDir)
	fmt.Println()
	fmt.Println("Next steps:")
	fmt.Printf("  cd %s\n", config.OutputDir)
	fmt.Println("  cat README.md")
	fmt.Println()
	
	return nil
}

func findManifestPath() string {
	// Try several possible locations
	locations := []string{
		"templates/manifest.yaml",
		"../templates/manifest.yaml",
		"../../templates/manifest.yaml",
	}
	
	for _, loc := range locations {
		if _, err := os.Stat(loc); err == nil {
			return loc
		}
	}
	
	// Try from GOPATH or module cache
	gopath := os.Getenv("GOPATH")
	if gopath != "" {
		manifestPath := filepath.Join(gopath, "src/github.com/Melampe001/Tokyo-IA/templates/manifest.yaml")
		if _, err := os.Stat(manifestPath); err == nil {
			return manifestPath
		}
	}
	
	// Default fallback
	return "templates/manifest.yaml"
}

func printUsage() {
	fmt.Println("Tokyo-IA Elite Framework - Automated Project Generator")
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Println("  elite generate \"project description\" [flags]")
	fmt.Println("  elite version")
	fmt.Println("  elite help")
	fmt.Println()
	fmt.Println("Commands:")
	fmt.Println("  generate    Generate a new project from description")
	fmt.Println("  version     Print version information")
	fmt.Println("  help        Show this help message")
	fmt.Println()
	fmt.Println("Flags for 'generate':")
	fmt.Println("  --output    Output directory (default: ./output)")
	fmt.Println()
	fmt.Println("Examples:")
	fmt.Println("  elite generate \"REST API for task management\"")
	fmt.Println("  elite generate \"Telegram bot for weather updates\"")
	fmt.Println("  elite generate \"E-commerce platform with Stripe\" --output ./projects")
	fmt.Println("  elite generate \"// PROYECTO: AI agent with CrewAI\"")
	fmt.Println()
}
