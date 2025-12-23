package monetization

import (
	"fmt"
	"sync"
	"time"
)

// UnlockValidator validates local unlock states
type UnlockValidator struct {
	mu      sync.RWMutex
	unlocks map[string]*LocalUnlock
}

// NewUnlockValidator creates a new unlock validator
func NewUnlockValidator() *UnlockValidator {
	return &UnlockValidator{
		unlocks: make(map[string]*LocalUnlock),
	}
}

// Unlock marks a product as unlocked locally
func (v *UnlockValidator) Unlock(productID string, expiresAt *time.Time) error {
	if productID == "" {
		return ErrInvalidProductID
	}

	v.mu.Lock()
	defer v.mu.Unlock()

	unlock := &LocalUnlock{
		ProductID:  productID,
		UnlockedAt: time.Now(),
		State:      UnlockStateUnlocked,
		ExpiresAt:  expiresAt,
		Metadata:   make(map[string]interface{}),
	}

	v.unlocks[productID] = unlock
	return nil
}

// ValidateUnlock validates a local unlock state
func (v *UnlockValidator) ValidateUnlock(productID string) *ValidationResult {
	result := &ValidationResult{
		Valid:     false,
		Method:    PaymentMethodLocal,
		ProductID: productID,
		Timestamp: time.Now(),
		Details:   make(map[string]interface{}),
	}

	if productID == "" {
		result.Error = ErrInvalidProductID
		return result
	}

	v.mu.RLock()
	unlock, exists := v.unlocks[productID]
	v.mu.RUnlock()

	if !exists {
		result.Error = ErrUnauthorized
		result.Details["state"] = UnlockStateLocked
		return result
	}

	// Check if unlock has expired
	if unlock.ExpiresAt != nil && time.Now().After(*unlock.ExpiresAt) {
		v.mu.Lock()
		unlock.State = UnlockStateExpired
		v.mu.Unlock()

		result.Error = ErrPurchaseExpired
		result.Details["state"] = UnlockStateExpired
		result.Details["expired_at"] = *unlock.ExpiresAt
		return result
	}

	// Check current state
	if unlock.State != UnlockStateUnlocked {
		result.Error = ErrInvalidUnlockState
		result.Details["state"] = unlock.State
		return result
	}

	result.Valid = true
	result.Details["state"] = unlock.State
	result.Details["unlocked_at"] = unlock.UnlockedAt
	if unlock.ExpiresAt != nil {
		result.Details["expires_at"] = *unlock.ExpiresAt
	}

	return result
}

// GetUnlockState returns the current unlock state for a product
func (v *UnlockValidator) GetUnlockState(productID string) UnlockState {
	v.mu.RLock()
	defer v.mu.RUnlock()

	unlock, exists := v.unlocks[productID]
	if !exists {
		return UnlockStateLocked
	}

	// Check expiration
	if unlock.ExpiresAt != nil && time.Now().After(*unlock.ExpiresAt) {
		return UnlockStateExpired
	}

	return unlock.State
}

// Lock marks a product as locked
func (v *UnlockValidator) Lock(productID string) error {
	if productID == "" {
		return ErrInvalidProductID
	}

	v.mu.Lock()
	defer v.mu.Unlock()

	unlock, exists := v.unlocks[productID]
	if !exists {
		return fmt.Errorf("product not found: %s", productID)
	}

	unlock.State = UnlockStateLocked
	return nil
}

// Clear removes all unlocks (for testing purposes)
func (v *UnlockValidator) Clear() {
	v.mu.Lock()
	defer v.mu.Unlock()
	v.unlocks = make(map[string]*LocalUnlock)
}
