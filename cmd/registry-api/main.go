// Package main provides the REST API server for the Tokyo-IA agent registry.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/Melampe001/Tokyo-IA/internal/registry"
	"github.com/google/uuid"
)

// Server wraps the registry and HTTP server.
type Server struct {
	registry *registry.Registry
	mux      *http.ServeMux
}

// NewServer creates a new API server.
func NewServer(reg *registry.Registry) *Server {
	s := &Server{
		registry: reg,
		mux:      http.NewServeMux(),
	}
	s.setupRoutes()
	return s
}

func (s *Server) setupRoutes() {
	// Agent endpoints
	s.mux.HandleFunc("/api/agents", s.handleAgents)
	s.mux.HandleFunc("/api/agents/", s.handleAgentDetails)

	// Task endpoints
	s.mux.HandleFunc("/api/tasks", s.handleTasks)
	s.mux.HandleFunc("/api/tasks/", s.handleTaskDetails)

	// Workflow endpoints
	s.mux.HandleFunc("/api/workflows", s.handleWorkflows)
	s.mux.HandleFunc("/api/workflows/", s.handleWorkflowDetails)

	// Metrics endpoint
	s.mux.HandleFunc("/api/metrics", s.handleMetrics)

	// Health check
	s.mux.HandleFunc("/health", s.handleHealth)
}

// Enable CORS and logging middleware
func (s *Server) middlewareChain(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// CORS
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		// Logging
		start := time.Now()
		log.Printf("[%s] %s %s", r.Method, r.URL.Path, r.RemoteAddr)

		next.ServeHTTP(w, r)

		log.Printf("[%s] %s completed in %v", r.Method, r.URL.Path, time.Since(start))
	})
}

// Handler functions

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	respondJSON(w, http.StatusOK, map[string]string{
		"status":  "healthy",
		"service": "tokyo-ia-registry-api",
		"version": "1.0.0",
	})
}

func (s *Server) handleAgents(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	ctx := context.Background()
	agents, err := s.registry.GetAllAgents(ctx)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to get agents: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, agents)
}

func (s *Server) handleAgentDetails(w http.ResponseWriter, r *http.Request) {
	// Extract agent ID from path
	path := r.URL.Path
	agentID := path[len("/api/agents/"):]

	// Handle /api/agents/{id}/stats
	if len(agentID) > 6 && agentID[len(agentID)-6:] == "/stats" {
		agentID = agentID[:len(agentID)-6]
		s.handleAgentStats(w, r, agentID)
		return
	}

	// Handle /api/agents/{id}/tasks
	if len(agentID) > 6 && agentID[len(agentID)-6:] == "/tasks" {
		agentID = agentID[:len(agentID)-6]
		s.handleAgentTasks(w, r, agentID)
		return
	}

	// Get single agent
	ctx := context.Background()
	agent, err := s.registry.GetAgentByID(ctx, agentID)
	if err != nil {
		respondError(w, http.StatusNotFound, fmt.Sprintf("Agent not found: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, agent)
}

func (s *Server) handleAgentStats(w http.ResponseWriter, r *http.Request, agentID string) {
	if r.Method != http.MethodGet {
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	ctx := context.Background()
	stats, err := s.registry.GetAgentStats(ctx, agentID)
	if err != nil {
		respondError(w, http.StatusNotFound, fmt.Sprintf("Stats not found: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, stats)
}

func (s *Server) handleAgentTasks(w http.ResponseWriter, r *http.Request, agentID string) {
	if r.Method != http.MethodGet {
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	limit := 50
	if limitStr := r.URL.Query().Get("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	ctx := context.Background()
	tasks, err := s.registry.GetTasksByAgent(ctx, agentID, limit)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to get tasks: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, tasks)
}

func (s *Server) handleTasks(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		s.createTask(w, r)
	default:
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
	}
}

func (s *Server) createTask(w http.ResponseWriter, r *http.Request) {
	var req registry.CreateTaskRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, fmt.Sprintf("Invalid request: %v", err))
		return
	}

	ctx := context.Background()
	task, err := s.registry.CreateTask(ctx, req)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to create task: %v", err))
		return
	}

	respondJSON(w, http.StatusCreated, task)
}

func (s *Server) handleTaskDetails(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path
	taskIDStr := path[len("/api/tasks/"):]

	taskID, err := uuid.Parse(taskIDStr)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid task ID")
		return
	}

	switch r.Method {
	case http.MethodPut:
		s.updateTaskStatus(w, r, taskID)
	default:
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
	}
}

func (s *Server) updateTaskStatus(w http.ResponseWriter, r *http.Request, taskID uuid.UUID) {
	var req registry.UpdateTaskStatusRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, fmt.Sprintf("Invalid request: %v", err))
		return
	}

	ctx := context.Background()
	if err := s.registry.UpdateTaskStatus(ctx, taskID, req); err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to update task: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, map[string]string{"message": "Task updated successfully"})
}

func (s *Server) handleWorkflows(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		s.getWorkflows(w, r)
	case http.MethodPost:
		s.createWorkflow(w, r)
	default:
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
	}
}

func (s *Server) getWorkflows(w http.ResponseWriter, r *http.Request) {
	limit := 50
	if limitStr := r.URL.Query().Get("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	ctx := context.Background()
	workflows, err := s.registry.GetAllWorkflows(ctx, limit)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to get workflows: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, workflows)
}

func (s *Server) createWorkflow(w http.ResponseWriter, r *http.Request) {
	var req registry.CreateWorkflowRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, fmt.Sprintf("Invalid request: %v", err))
		return
	}

	ctx := context.Background()
	workflow, err := s.registry.CreateWorkflow(ctx, req)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to create workflow: %v", err))
		return
	}

	respondJSON(w, http.StatusCreated, workflow)
}

func (s *Server) handleWorkflowDetails(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path
	workflowIDStr := path[len("/api/workflows/"):]

	// Handle /api/workflows/{id}/tasks
	if len(workflowIDStr) > 6 && workflowIDStr[len(workflowIDStr)-6:] == "/tasks" {
		workflowIDStr = workflowIDStr[:len(workflowIDStr)-6]
		workflowID, err := uuid.Parse(workflowIDStr)
		if err != nil {
			respondError(w, http.StatusBadRequest, "Invalid workflow ID")
			return
		}
		s.handleWorkflowTasks(w, r, workflowID)
		return
	}

	workflowID, err := uuid.Parse(workflowIDStr)
	if err != nil {
		respondError(w, http.StatusBadRequest, "Invalid workflow ID")
		return
	}

	ctx := context.Background()
	workflow, err := s.registry.GetWorkflowByID(ctx, workflowID)
	if err != nil {
		respondError(w, http.StatusNotFound, fmt.Sprintf("Workflow not found: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, workflow)
}

func (s *Server) handleWorkflowTasks(w http.ResponseWriter, r *http.Request, workflowID uuid.UUID) {
	if r.Method != http.MethodGet {
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	ctx := context.Background()
	tasks, err := s.registry.GetTasksByWorkflow(ctx, workflowID)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to get tasks: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, tasks)
}

func (s *Server) handleMetrics(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		respondError(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}

	agentID := r.URL.Query().Get("agent_id")
	metricType := r.URL.Query().Get("metric_type")

	if agentID == "" || metricType == "" {
		respondError(w, http.StatusBadRequest, "agent_id and metric_type are required")
		return
	}

	limit := 100
	if limitStr := r.URL.Query().Get("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 {
			limit = l
		}
	}

	ctx := context.Background()
	metrics, err := s.registry.GetMetrics(ctx, agentID, metricType, limit)
	if err != nil {
		respondError(w, http.StatusInternalServerError, fmt.Sprintf("Failed to get metrics: %v", err))
		return
	}

	respondJSON(w, http.StatusOK, metrics)
}

// Helper functions

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

func respondError(w http.ResponseWriter, status int, message string) {
	respondJSON(w, status, map[string]string{"error": message})
}

func main() {
	// Get database URL from environment
	dbURL := os.Getenv("DATABASE_URL")
	if dbURL == "" {
		log.Fatal("DATABASE_URL environment variable is required")
	}

	// Create registry
	reg, err := registry.NewRegistry(dbURL)
	if err != nil {
		log.Fatalf("Failed to create registry: %v", err)
	}
	defer reg.Close()

	log.Println("✅ Connected to database successfully")

	// Create server
	server := NewServer(reg)

	// Get port from environment or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Wrap with middleware
	handler := server.middlewareChain(server.mux)

	// Start server
	addr := fmt.Sprintf(":%s", port)
	log.Printf("🚀 Tokyo-IA Registry API server starting on %s", addr)
	log.Printf("📚 API Documentation:")
	log.Printf("  GET    /health                      - Health check")
	log.Printf("  GET    /api/agents                  - List all agents")
	log.Printf("  GET    /api/agents/{id}             - Get agent details")
	log.Printf("  GET    /api/agents/{id}/stats       - Get agent statistics")
	log.Printf("  GET    /api/agents/{id}/tasks       - Get agent tasks")
	log.Printf("  POST   /api/tasks                   - Create new task")
	log.Printf("  PUT    /api/tasks/{id}              - Update task status")
	log.Printf("  GET    /api/workflows               - List workflows")
	log.Printf("  POST   /api/workflows               - Create workflow")
	log.Printf("  GET    /api/workflows/{id}          - Get workflow details")
	log.Printf("  GET    /api/workflows/{id}/tasks    - Get workflow tasks")
	log.Printf("  GET    /api/metrics                 - Get metrics (requires agent_id & metric_type)")

	if err := http.ListenAndServe(addr, handler); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
