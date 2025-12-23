// Package main provides the orchestrator command-line interface.
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/Melampe001/Tokyo-IA/internal/orchestrator"
)

func main() {
	fmt.Println("🗼 Tokyo-IA Orchestrator Agent System")
	fmt.Println("=====================================")
	fmt.Println()
	fmt.Println("ROLE: ORCHESTRATOR_AGENT")
	fmt.Println("ORDER: architect → dependency → validator → security → optimization → monetization → build")
	fmt.Println("RULE: If any agent fails → STOP EVERYTHING")
	fmt.Println()

	// Create orchestrator with all agents
	orch := orchestrator.NewDefaultOrchestrator()

	// Execute all agents in order
	ctx := context.Background()
	results, err := orch.Execute(ctx)

	fmt.Println()
	fmt.Println("=====================================")
	fmt.Println("📊 Execution Summary")
	fmt.Println("=====================================")

	for _, result := range results {
		fmt.Println(result.String())
	}

	fmt.Println()

	if err != nil {
		fmt.Printf("❌ Orchestration FAILED: %v\n", err)
		fmt.Println("⛔ Execution stopped due to agent failure")
		os.Exit(1)
	}

	fmt.Println("✅ Orchestration completed successfully!")
	fmt.Println("🎉 All agents executed without errors")
}
