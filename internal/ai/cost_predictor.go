// Package ai provides artificial intelligence features for Tokyo-IA.
package ai

import (
	"encoding/json"
	"fmt"
	"math"
	"time"
)

// CostPrediction represents a cost prediction result
type CostPrediction struct {
	EstimatedCost     float64            `json:"estimated_cost"`
	ConfidenceMin     float64            `json:"confidence_min"`
	ConfidenceMax     float64            `json:"confidence_max"`
	ConfidenceLevel   float64            `json:"confidence_level"`
	ModelVersion      string             `json:"model_version"`
	PredictedAt       time.Time          `json:"predicted_at"`
	Recommendations   []string           `json:"recommendations"`
	BreakdownByAction map[string]float64 `json:"breakdown_by_action"`
}

// RequestMetrics contains metrics for a request
type RequestMetrics struct {
	Tokens      int                    `json:"tokens"`
	ModelName   string                 `json:"model_name"`
	RequestType string                 `json:"request_type"`
	Complexity  float64                `json:"complexity"`
	Features    map[string]interface{} `json:"features"`
}

// CostPredictor predicts costs before executing requests
type CostPredictor struct {
	ModelVersion    string              `json:"model_version"`
	HistoricalData  []HistoricalRequest `json:"historical_data"`
	ModelParameters ModelParameters     `json:"model_parameters"`
}

// HistoricalRequest represents a historical request for training
type HistoricalRequest struct {
	Metrics RequestMetrics `json:"metrics"`
	Cost    float64        `json:"cost"`
	Time    time.Time      `json:"time"`
}

// ModelParameters contains the cost prediction model parameters
type ModelParameters struct {
	TokenCostFactor    float64
	ComplexityFactor   float64
	BaselineCost       float64
	ConfidenceInterval float64
}

// NewCostPredictor creates a new cost predictor
func NewCostPredictor() *CostPredictor {
	return &CostPredictor{
		ModelVersion:   "v1.0.0",
		HistoricalData: make([]HistoricalRequest, 0),
		ModelParameters: ModelParameters{
			TokenCostFactor:    0.0001, // $0.0001 per token
			ComplexityFactor:   0.05,   // 5% increase per complexity unit
			BaselineCost:       0.001,  // $0.001 baseline
			ConfidenceInterval: 0.15,   // 15% confidence interval
		},
	}
}

// PredictCost predicts the cost of a request
func (cp *CostPredictor) PredictCost(metrics RequestMetrics) (*CostPrediction, error) {
	if metrics.Tokens <= 0 {
		return nil, fmt.Errorf("invalid token count: %d", metrics.Tokens)
	}

	// Calculate base cost
	baseCost := cp.ModelParameters.BaselineCost
	tokenCost := float64(metrics.Tokens) * cp.ModelParameters.TokenCostFactor
	complexityCost := metrics.Complexity * cp.ModelParameters.ComplexityFactor

	estimatedCost := baseCost + tokenCost + complexityCost

	// Apply model-specific multipliers
	multiplier := cp.getModelMultiplier(metrics.ModelName)
	estimatedCost *= multiplier

	// Calculate confidence intervals
	confidenceInterval := estimatedCost * cp.ModelParameters.ConfidenceInterval
	confidenceMin := estimatedCost - confidenceInterval
	confidenceMax := estimatedCost + confidenceInterval

	// Generate recommendations
	recommendations := cp.generateRecommendations(metrics, estimatedCost)

	// Create breakdown
	breakdown := map[string]float64{
		"baseline":   baseCost,
		"tokens":     tokenCost,
		"complexity": complexityCost,
		"multiplier": estimatedCost - (baseCost + tokenCost + complexityCost),
	}

	return &CostPrediction{
		EstimatedCost:     math.Round(estimatedCost*10000) / 10000,
		ConfidenceMin:     math.Round(confidenceMin*10000) / 10000,
		ConfidenceMax:     math.Round(confidenceMax*10000) / 10000,
		ConfidenceLevel:   1.0 - cp.ModelParameters.ConfidenceInterval,
		ModelVersion:      cp.ModelVersion,
		PredictedAt:       time.Now(),
		Recommendations:   recommendations,
		BreakdownByAction: breakdown,
	}, nil
}

// getModelMultiplier returns the cost multiplier for a given model
func (cp *CostPredictor) getModelMultiplier(modelName string) float64 {
	multipliers := map[string]float64{
		"gpt-4":           15.0,
		"gpt-4-turbo":     10.0,
		"gpt-3.5-turbo":   1.0,
		"claude-3-opus":   15.0,
		"claude-3-sonnet": 3.0,
		"gemini-pro":      0.5,
		"llama-3":         0.1,
	}

	if mult, ok := multipliers[modelName]; ok {
		return mult
	}
	return 1.0 // Default multiplier
}

// generateRecommendations generates optimization recommendations
func (cp *CostPredictor) generateRecommendations(metrics RequestMetrics, cost float64) []string {
	recommendations := make([]string, 0)

	// High token count
	if metrics.Tokens > 10000 {
		recommendations = append(recommendations, "Consider reducing input size to lower token costs")
	}

	// High complexity
	if metrics.Complexity > 0.8 {
		recommendations = append(recommendations, "Request complexity is high - consider breaking into smaller tasks")
	}

	// Expensive model
	if cost > 0.1 {
		recommendations = append(recommendations, "Consider using a more cost-effective model for this task")
	}

	// Model-specific recommendations
	if metrics.ModelName == "gpt-4" {
		recommendations = append(recommendations, "GPT-4 detected - consider GPT-3.5-turbo for simpler tasks")
	}

	if len(recommendations) == 0 {
		recommendations = append(recommendations, "Cost is optimized for current request")
	}

	return recommendations
}

// AddHistoricalData adds historical request data for model improvement
func (cp *CostPredictor) AddHistoricalData(metrics RequestMetrics, actualCost float64) {
	historical := HistoricalRequest{
		Metrics: metrics,
		Cost:    actualCost,
		Time:    time.Now(),
	}
	cp.HistoricalData = append(cp.HistoricalData, historical)

	// Keep only last 10K entries
	if len(cp.HistoricalData) > 10000 {
		cp.HistoricalData = cp.HistoricalData[len(cp.HistoricalData)-10000:]
	}
}

// GetModelAccuracy calculates the model's prediction accuracy
func (cp *CostPredictor) GetModelAccuracy() float64 {
	if len(cp.HistoricalData) == 0 {
		return 0.0
	}

	totalError := 0.0
	for _, historical := range cp.HistoricalData {
		prediction, err := cp.PredictCost(historical.Metrics)
		if err != nil {
			continue
		}
		error := math.Abs(prediction.EstimatedCost - historical.Cost)
		totalError += error
	}

	avgError := totalError / float64(len(cp.HistoricalData))
	accuracy := 1.0 - avgError
	if accuracy < 0 {
		accuracy = 0
	}
	return accuracy
}

// ExportModel exports the model as JSON
func (cp *CostPredictor) ExportModel() ([]byte, error) {
	return json.MarshalIndent(cp, "", "  ")
}

// ImportModel imports the model from JSON
func (cp *CostPredictor) ImportModel(data []byte) error {
	return json.Unmarshal(data, cp)
}
