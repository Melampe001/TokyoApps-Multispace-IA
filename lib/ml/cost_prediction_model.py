"""
Cost Prediction Model - ML-based cost predictor for Tokyo-IA

This module provides machine learning capabilities for predicting
LLM request costs based on historical data.
"""

import json
import pickle
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class PredictionFeatures:
    """Features for cost prediction"""
    tokens: int
    model_name: str
    request_type: str
    complexity: float
    hour_of_day: int
    day_of_week: int
    
    def to_vector(self) -> np.ndarray:
        """Convert features to numpy vector"""
        # Model encoding
        model_encoding = {
            'gpt-4': 0,
            'gpt-4-turbo': 1,
            'gpt-3.5-turbo': 2,
            'claude-3-opus': 3,
            'claude-3-sonnet': 4,
            'gemini-pro': 5,
            'llama-3': 6,
        }.get(self.model_name, 7)
        
        # Request type encoding
        request_encoding = {
            'completion': 0,
            'chat': 1,
            'embedding': 2,
        }.get(self.request_type, 0)
        
        return np.array([
            self.tokens,
            model_encoding,
            request_encoding,
            self.complexity,
            self.hour_of_day,
            self.day_of_week,
        ])


@dataclass
class PredictionResult:
    """Cost prediction result"""
    estimated_cost: float
    confidence_min: float
    confidence_max: float
    confidence_level: float
    feature_importance: Dict[str, float]
    model_version: str
    predicted_at: str


class CostPredictionModel:
    """Machine learning model for cost prediction"""
    
    def __init__(self):
        self.model_version = "v1.0.0"
        self.trained = False
        self.weights = None
        self.bias = 0.0
        self.scaler_mean = None
        self.scaler_std = None
        self.training_history = []
        
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, learning_rate: float = 0.01):
        """
        Train the model using gradient descent
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y: Target values (n_samples,)
            epochs: Number of training epochs
            learning_rate: Learning rate for gradient descent
        """
        n_samples, n_features = X.shape
        
        # Normalize features
        self.scaler_mean = np.mean(X, axis=0)
        self.scaler_std = np.std(X, axis=0) + 1e-8
        X_normalized = (X - self.scaler_mean) / self.scaler_std
        
        # Initialize weights
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0
        
        # Training loop
        for epoch in range(epochs):
            # Forward pass
            predictions = np.dot(X_normalized, self.weights) + self.bias
            
            # Compute loss (MSE)
            loss = np.mean((predictions - y) ** 2)
            
            # Backward pass
            d_weights = (2 / n_samples) * np.dot(X_normalized.T, (predictions - y))
            d_bias = (2 / n_samples) * np.sum(predictions - y)
            
            # Update parameters
            self.weights -= learning_rate * d_weights
            self.bias -= learning_rate * d_bias
            
            # Store training history
            if epoch % 10 == 0:
                self.training_history.append({
                    'epoch': epoch,
                    'loss': float(loss),
                    'timestamp': datetime.now().isoformat()
                })
        
        self.trained = True
        
    def predict(self, features: PredictionFeatures) -> PredictionResult:
        """
        Predict cost for given features
        
        Args:
            features: Input features
            
        Returns:
            Prediction result with confidence intervals
        """
        if not self.trained:
            # Fallback to simple heuristic if not trained
            return self._heuristic_predict(features)
        
        # Convert features to vector
        X = features.to_vector().reshape(1, -1)
        
        # Normalize
        X_normalized = (X - self.scaler_mean) / self.scaler_std
        
        # Predict
        prediction_value = np.dot(X_normalized, self.weights) + self.bias
        estimated_cost = float(prediction_value.item() if hasattr(prediction_value, 'item') else prediction_value)
        
        # Ensure positive prediction
        estimated_cost = max(0.0, estimated_cost)
        
        # Calculate confidence intervals (±15%)
        confidence_interval = estimated_cost * 0.15
        confidence_min = max(0.0, estimated_cost - confidence_interval)
        confidence_max = estimated_cost + confidence_interval
        
        # Calculate feature importance
        feature_importance = self._calculate_feature_importance(features)
        
        return PredictionResult(
            estimated_cost=round(estimated_cost, 4),
            confidence_min=round(confidence_min, 4),
            confidence_max=round(confidence_max, 4),
            confidence_level=0.85,
            feature_importance=feature_importance,
            model_version=self.model_version,
            predicted_at=datetime.now().isoformat()
        )
    
    def _heuristic_predict(self, features: PredictionFeatures) -> PredictionResult:
        """Fallback heuristic prediction when model is not trained"""
        # Base costs per model
        model_multipliers = {
            'gpt-4': 15.0,
            'gpt-4-turbo': 10.0,
            'gpt-3.5-turbo': 1.0,
            'claude-3-opus': 15.0,
            'claude-3-sonnet': 3.0,
            'gemini-pro': 0.5,
            'llama-3': 0.1,
        }
        
        base_cost = 0.001
        token_cost = features.tokens * 0.0001
        complexity_cost = features.complexity * 0.05
        multiplier = model_multipliers.get(features.model_name, 1.0)
        
        estimated_cost = (base_cost + token_cost + complexity_cost) * multiplier
        
        confidence_interval = estimated_cost * 0.15
        
        return PredictionResult(
            estimated_cost=round(estimated_cost, 4),
            confidence_min=round(max(0.0, estimated_cost - confidence_interval), 4),
            confidence_max=round(estimated_cost + confidence_interval, 4),
            confidence_level=0.85,
            feature_importance={
                'tokens': 0.5,
                'model_name': 0.3,
                'complexity': 0.2,
            },
            model_version=self.model_version,
            predicted_at=datetime.now().isoformat()
        )
    
    def _calculate_feature_importance(self, features: PredictionFeatures) -> Dict[str, float]:
        """Calculate feature importance based on weights"""
        if self.weights is None:
            return {}
        
        # Normalize weights to get importance
        abs_weights = np.abs(self.weights)
        total_weight = np.sum(abs_weights)
        
        if total_weight == 0:
            return {}
        
        normalized_weights = abs_weights / total_weight
        
        return {
            'tokens': float(normalized_weights[0]),
            'model_name': float(normalized_weights[1]),
            'request_type': float(normalized_weights[2]),
            'complexity': float(normalized_weights[3]),
            'hour_of_day': float(normalized_weights[4]),
            'day_of_week': float(normalized_weights[5]),
        }
    
    def save(self, filepath: str):
        """Save model to disk"""
        model_data = {
            'model_version': self.model_version,
            'trained': self.trained,
            'weights': self.weights.tolist() if self.weights is not None else None,
            'bias': self.bias,
            'scaler_mean': self.scaler_mean.tolist() if self.scaler_mean is not None else None,
            'scaler_std': self.scaler_std.tolist() if self.scaler_std is not None else None,
            'training_history': self.training_history,
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_data, f, indent=2)
    
    def load(self, filepath: str):
        """Load model from disk"""
        with open(filepath, 'r') as f:
            model_data = json.load(f)
        
        self.model_version = model_data['model_version']
        self.trained = model_data['trained']
        self.weights = np.array(model_data['weights']) if model_data['weights'] else None
        self.bias = model_data['bias']
        self.scaler_mean = np.array(model_data['scaler_mean']) if model_data['scaler_mean'] else None
        self.scaler_std = np.array(model_data['scaler_std']) if model_data['scaler_std'] else None
        self.training_history = model_data['training_history']
    
    def get_model_stats(self) -> Dict:
        """Get model statistics"""
        return {
            'model_version': self.model_version,
            'trained': self.trained,
            'n_features': len(self.weights) if self.weights is not None else 0,
            'training_epochs': len(self.training_history),
            'final_loss': self.training_history[-1]['loss'] if self.training_history else None,
        }


def create_sample_dataset(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create a sample dataset for training
    
    Args:
        n_samples: Number of samples to generate
        
    Returns:
        Tuple of (X, y) - features and targets
    """
    np.random.seed(42)
    
    X = []
    y = []
    
    models = ['gpt-4', 'gpt-3.5-turbo', 'gemini-pro', 'claude-3-sonnet']
    model_costs = {'gpt-4': 15.0, 'gpt-3.5-turbo': 1.0, 'gemini-pro': 0.5, 'claude-3-sonnet': 3.0}
    
    for _ in range(n_samples):
        tokens = np.random.randint(100, 10000)
        model = np.random.choice(models)
        request_type = np.random.choice(['completion', 'chat', 'embedding'])
        complexity = np.random.uniform(0.1, 1.0)
        hour = np.random.randint(0, 24)
        day = np.random.randint(0, 7)
        
        features = PredictionFeatures(
            tokens=tokens,
            model_name=model,
            request_type=request_type,
            complexity=complexity,
            hour_of_day=hour,
            day_of_week=day
        )
        
        # Calculate synthetic cost
        base_cost = 0.001
        token_cost = tokens * 0.0001
        complexity_cost = complexity * 0.05
        multiplier = model_costs[model]
        cost = (base_cost + token_cost + complexity_cost) * multiplier
        
        # Add some noise
        cost += np.random.normal(0, cost * 0.1)
        
        X.append(features.to_vector())
        y.append(cost)
    
    return np.array(X), np.array(y)


if __name__ == '__main__':
    # Example usage
    print("Tokyo-IA Cost Prediction Model")
    print("=" * 50)
    
    # Create and train model
    model = CostPredictionModel()
    print("\nGenerating sample dataset...")
    X, y = create_sample_dataset(1000)
    
    print("Training model...")
    model.train(X, y, epochs=100, learning_rate=0.01)
    
    print(f"\nModel Statistics:")
    stats = model.get_model_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Make a prediction
    print("\nMaking sample prediction...")
    features = PredictionFeatures(
        tokens=5000,
        model_name='gpt-4',
        request_type='completion',
        complexity=0.7,
        hour_of_day=14,
        day_of_week=3
    )
    
    result = model.predict(features)
    print(f"\nPrediction Results:")
    print(f"  Estimated Cost: ${result.estimated_cost}")
    print(f"  Confidence Range: ${result.confidence_min} - ${result.confidence_max}")
    print(f"  Confidence Level: {result.confidence_level * 100}%")
    print(f"\n  Feature Importance:")
    for feature, importance in result.feature_importance.items():
        print(f"    {feature}: {importance:.3f}")
