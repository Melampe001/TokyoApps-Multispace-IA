package ai

import (
	"testing"
	"time"
)

func TestNewCostPredictor(t *testing.T) {
	cp := NewCostPredictor()
	if cp == nil {
		t.Fatal("NewCostPredictor returned nil")
	}
	if cp.ModelVersion != "v1.0.0" {
		t.Errorf("Expected model version v1.0.0, got %s", cp.ModelVersion)
	}
}

func TestPredictCost(t *testing.T) {
	cp := NewCostPredictor()

	tests := []struct {
		name    string
		metrics RequestMetrics
		wantErr bool
		minCost float64
		maxCost float64
	}{
		{
			name: "basic gpt-3.5-turbo request",
			metrics: RequestMetrics{
				Tokens:      1000,
				ModelName:   "gpt-3.5-turbo",
				RequestType: "completion",
				Complexity:  0.5,
			},
			wantErr: false,
			minCost: 0.1,
			maxCost: 0.2,
		},
		{
			name: "expensive gpt-4 request",
			metrics: RequestMetrics{
				Tokens:      5000,
				ModelName:   "gpt-4",
				RequestType: "completion",
				Complexity:  0.8,
			},
			wantErr: false,
			minCost: 7.0,
			maxCost: 10.0,
		},
		{
			name: "invalid token count",
			metrics: RequestMetrics{
				Tokens:      0,
				ModelName:   "gpt-3.5-turbo",
				RequestType: "completion",
				Complexity:  0.5,
			},
			wantErr: true,
		},
		{
			name: "cheap gemini request",
			metrics: RequestMetrics{
				Tokens:      2000,
				ModelName:   "gemini-pro",
				RequestType: "completion",
				Complexity:  0.3,
			},
			wantErr: false,
			minCost: 0.05,
			maxCost: 0.15,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			prediction, err := cp.PredictCost(tt.metrics)
			if (err != nil) != tt.wantErr {
				t.Errorf("PredictCost() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if prediction == nil {
					t.Error("Expected prediction, got nil")
					return
				}
				if prediction.EstimatedCost < tt.minCost || prediction.EstimatedCost > tt.maxCost {
					t.Errorf("EstimatedCost = %v, want between %v and %v",
						prediction.EstimatedCost, tt.minCost, tt.maxCost)
				}
				if prediction.ConfidenceLevel <= 0 || prediction.ConfidenceLevel >= 1 {
					t.Errorf("ConfidenceLevel = %v, want between 0 and 1", prediction.ConfidenceLevel)
				}
				if len(prediction.Recommendations) == 0 {
					t.Error("Expected recommendations, got none")
				}
				if len(prediction.BreakdownByAction) == 0 {
					t.Error("Expected breakdown, got none")
				}
			}
		})
	}
}

func TestGenerateRecommendations(t *testing.T) {
	cp := NewCostPredictor()

	tests := []struct {
		name         string
		metrics      RequestMetrics
		cost         float64
		wantContains string
	}{
		{
			name: "high token count",
			metrics: RequestMetrics{
				Tokens:     15000,
				ModelName:  "gpt-3.5-turbo",
				Complexity: 0.5,
			},
			cost:         0.1,
			wantContains: "reducing input size",
		},
		{
			name: "high complexity",
			metrics: RequestMetrics{
				Tokens:     5000,
				ModelName:  "gpt-3.5-turbo",
				Complexity: 0.9,
			},
			cost:         0.1,
			wantContains: "complexity is high",
		},
		{
			name: "expensive cost",
			metrics: RequestMetrics{
				Tokens:     5000,
				ModelName:  "gpt-4",
				Complexity: 0.5,
			},
			cost:         0.5,
			wantContains: "cost-effective model",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			recommendations := cp.generateRecommendations(tt.metrics, tt.cost)
			found := false
			for _, rec := range recommendations {
				if contains(rec, tt.wantContains) {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("Expected recommendation containing %q, got %v",
					tt.wantContains, recommendations)
			}
		})
	}
}

func TestAddHistoricalData(t *testing.T) {
	cp := NewCostPredictor()

	metrics := RequestMetrics{
		Tokens:      1000,
		ModelName:   "gpt-3.5-turbo",
		RequestType: "completion",
		Complexity:  0.5,
	}

	cp.AddHistoricalData(metrics, 0.15)

	if len(cp.HistoricalData) != 1 {
		t.Errorf("Expected 1 historical data entry, got %d", len(cp.HistoricalData))
	}

	// Test that it keeps only 10K entries
	for i := 0; i < 11000; i++ {
		cp.AddHistoricalData(metrics, 0.15)
	}

	if len(cp.HistoricalData) > 10000 {
		t.Errorf("Expected max 10000 historical entries, got %d", len(cp.HistoricalData))
	}
}

func TestGetModelAccuracy(t *testing.T) {
	cp := NewCostPredictor()

	// No data should return 0
	accuracy := cp.GetModelAccuracy()
	if accuracy != 0.0 {
		t.Errorf("Expected 0 accuracy with no data, got %v", accuracy)
	}

	// Add some historical data
	metrics := RequestMetrics{
		Tokens:      1000,
		ModelName:   "gpt-3.5-turbo",
		RequestType: "completion",
		Complexity:  0.5,
	}

	prediction, _ := cp.PredictCost(metrics)
	cp.AddHistoricalData(metrics, prediction.EstimatedCost)

	accuracy = cp.GetModelAccuracy()
	if accuracy <= 0 {
		t.Errorf("Expected positive accuracy, got %v", accuracy)
	}
}

func TestGetModelMultiplier(t *testing.T) {
	cp := NewCostPredictor()

	tests := []struct {
		model      string
		multiplier float64
	}{
		{"gpt-4", 15.0},
		{"gpt-3.5-turbo", 1.0},
		{"gemini-pro", 0.5},
		{"unknown-model", 1.0},
	}

	for _, tt := range tests {
		t.Run(tt.model, func(t *testing.T) {
			mult := cp.getModelMultiplier(tt.model)
			if mult != tt.multiplier {
				t.Errorf("Expected multiplier %v for %s, got %v",
					tt.multiplier, tt.model, mult)
			}
		})
	}
}

func TestExportImportModel(t *testing.T) {
	cp := NewCostPredictor()

	metrics := RequestMetrics{
		Tokens:      1000,
		ModelName:   "gpt-3.5-turbo",
		RequestType: "completion",
		Complexity:  0.5,
	}
	cp.AddHistoricalData(metrics, 0.15)

	// Export
	data, err := cp.ExportModel()
	if err != nil {
		t.Fatalf("ExportModel failed: %v", err)
	}

	// Import into new predictor
	cp2 := NewCostPredictor()
	err = cp2.ImportModel(data)
	if err != nil {
		t.Fatalf("ImportModel failed: %v", err)
	}

	if len(cp2.HistoricalData) != len(cp.HistoricalData) {
		t.Errorf("Expected %d historical entries after import, got %d",
			len(cp.HistoricalData), len(cp2.HistoricalData))
	}
}

func TestCostPredictionFields(t *testing.T) {
	cp := NewCostPredictor()

	metrics := RequestMetrics{
		Tokens:      1000,
		ModelName:   "gpt-3.5-turbo",
		RequestType: "completion",
		Complexity:  0.5,
	}

	prediction, err := cp.PredictCost(metrics)
	if err != nil {
		t.Fatalf("PredictCost failed: %v", err)
	}

	// Check all fields are populated
	if prediction.EstimatedCost <= 0 {
		t.Error("EstimatedCost should be positive")
	}
	if prediction.ConfidenceMin >= prediction.EstimatedCost {
		t.Error("ConfidenceMin should be less than EstimatedCost")
	}
	if prediction.ConfidenceMax <= prediction.EstimatedCost {
		t.Error("ConfidenceMax should be greater than EstimatedCost")
	}
	if prediction.ModelVersion == "" {
		t.Error("ModelVersion should not be empty")
	}
	if prediction.PredictedAt.After(time.Now()) {
		t.Error("PredictedAt should not be in the future")
	}
	if len(prediction.Recommendations) == 0 {
		t.Error("Recommendations should not be empty")
	}
	if len(prediction.BreakdownByAction) == 0 {
		t.Error("BreakdownByAction should not be empty")
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
