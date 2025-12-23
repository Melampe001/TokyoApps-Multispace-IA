package monetization

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"sync"
	"time"
)

// RestoreValidator validates idempotent restore operations
type RestoreValidator struct {
	mu         sync.RWMutex
	operations map[string]*RestoreOperation
	window     time.Duration // Time window for idempotency check
}

// NewRestoreValidator creates a new restore validator
func NewRestoreValidator(window time.Duration) *RestoreValidator {
	if window <= 0 {
		window = 24 * time.Hour // Default to 24 hours
	}

	return &RestoreValidator{
		operations: make(map[string]*RestoreOperation),
		window:     window,
	}
}

// ValidateRestore validates a restore operation for idempotency
func (v *RestoreValidator) ValidateRestore(userID string, productIDs []string, method PaymentMethod) *ValidationResult {
	result := &ValidationResult{
		Valid:     false,
		Method:    method,
		Timestamp: time.Now(),
		Details:   make(map[string]interface{}),
	}

	// Validate input
	if userID == "" {
		result.Error = fmt.Errorf("user ID is required")
		return result
	}

	if len(productIDs) == 0 {
		result.Error = fmt.Errorf("at least one product ID is required")
		return result
	}

	// Validate payment method
	methodResult := ValidatePaymentMethod(method)
	if !methodResult.Valid {
		result.Error = methodResult.Error
		result.Details["payment_method_validation"] = methodResult.Details
		return result
	}

	// Generate operation ID based on user and products
	operationID := v.generateOperationID(userID, productIDs)

	// Check for duplicate operation within the window
	v.mu.RLock()
	existingOp, exists := v.operations[operationID]
	v.mu.RUnlock()

	if exists {
		// Check if the operation is within the idempotency window
		timeSinceOp := time.Since(existingOp.Timestamp)
		if timeSinceOp < v.window {
			result.Error = ErrDuplicateRestore
			result.Details["is_duplicate"] = true
			result.Details["original_timestamp"] = existingOp.Timestamp
			result.Details["time_since_original"] = timeSinceOp.String()
			result.Details["idempotency_window"] = v.window.String()
			return result
		}

		// Operation is outside the window, allow it and update
		v.mu.Lock()
		delete(v.operations, operationID)
		v.mu.Unlock()
	}

	// Create new restore operation
	operation := &RestoreOperation{
		OperationID:  operationID,
		UserID:       userID,
		ProductIDs:   productIDs,
		Timestamp:    time.Now(),
		Method:       method,
		IsIdempotent: true,
	}

	// Store the operation
	v.mu.Lock()
	v.operations[operationID] = operation
	v.mu.Unlock()

	result.Valid = true
	result.Details["operation_id"] = operationID
	result.Details["is_duplicate"] = false
	result.Details["is_idempotent"] = true
	result.Details["product_count"] = len(productIDs)
	result.Details["idempotency_window"] = v.window.String()

	// Clean up old operations (beyond window)
	go v.cleanup()

	return result
}

// generateOperationID generates a unique operation ID based on user and products
func (v *RestoreValidator) generateOperationID(userID string, productIDs []string) string {
	// Sort product IDs for consistency
	sortedIDs := make([]string, len(productIDs))
	copy(sortedIDs, productIDs)
	// Simple sort (for production, use sort.Strings)
	for i := 0; i < len(sortedIDs)-1; i++ {
		for j := i + 1; j < len(sortedIDs); j++ {
			if sortedIDs[i] > sortedIDs[j] {
				sortedIDs[i], sortedIDs[j] = sortedIDs[j], sortedIDs[i]
			}
		}
	}

	// Create hash
	h := sha256.New()
	h.Write([]byte(userID))
	for _, pid := range sortedIDs {
		h.Write([]byte(pid))
	}
	return hex.EncodeToString(h.Sum(nil))
}

// cleanup removes operations outside the idempotency window
func (v *RestoreValidator) cleanup() {
	v.mu.Lock()
	defer v.mu.Unlock()

	now := time.Now()
	for id, op := range v.operations {
		if now.Sub(op.Timestamp) > v.window {
			delete(v.operations, id)
		}
	}
}

// GetOperation retrieves a restore operation by ID
func (v *RestoreValidator) GetOperation(operationID string) (*RestoreOperation, bool) {
	v.mu.RLock()
	defer v.mu.RUnlock()

	op, exists := v.operations[operationID]
	return op, exists
}

// Clear removes all operations (for testing purposes)
func (v *RestoreValidator) Clear() {
	v.mu.Lock()
	defer v.mu.Unlock()
	v.operations = make(map[string]*RestoreOperation)
}

// GetOperationCount returns the number of stored operations
func (v *RestoreValidator) GetOperationCount() int {
	v.mu.RLock()
	defer v.mu.RUnlock()
	return len(v.operations)
}
