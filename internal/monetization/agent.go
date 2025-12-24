package monetization

import (
	"fmt"
	"time"
)

// MonetizationAgent is the main agent for handling monetization validation
type MonetizationAgent struct {
	billingValidator *BillingValidator
	unlockValidator  *UnlockValidator
	restoreValidator *RestoreValidator
}

// NewMonetizationAgent creates a new monetization agent
func NewMonetizationAgent(publicKey string, packageName string, restoreWindow time.Duration) (*MonetizationAgent, error) {
	billingValidator, err := NewBillingValidator(publicKey, packageName)
	if err != nil {
		return nil, fmt.Errorf("failed to create billing validator: %w", err)
	}

	return &MonetizationAgent{
		billingValidator: billingValidator,
		unlockValidator:  NewUnlockValidator(),
		restoreValidator: NewRestoreValidator(restoreWindow),
	}, nil
}

// ValidateGooglePlayBilling validates a Google Play billing purchase
func (a *MonetizationAgent) ValidateGooglePlayBilling(purchase *PurchaseData) *ValidationResult {
	return a.billingValidator.ValidatePurchase(purchase)
}

// ValidateLocalUnlock validates a local unlock
func (a *MonetizationAgent) ValidateLocalUnlock(productID string) *ValidationResult {
	return a.unlockValidator.ValidateUnlock(productID)
}

// UnlockProduct unlocks a product locally
func (a *MonetizationAgent) UnlockProduct(productID string, expiresAt *time.Time) error {
	return a.unlockValidator.Unlock(productID, expiresAt)
}

// LockProduct locks a product
func (a *MonetizationAgent) LockProduct(productID string) error {
	return a.unlockValidator.Lock(productID)
}

// ValidateRestore validates an idempotent restore operation
func (a *MonetizationAgent) ValidateRestore(userID string, productIDs []string, method PaymentMethod) *ValidationResult {
	return a.restoreValidator.ValidateRestore(userID, productIDs, method)
}

// ValidatePaymentMethod validates a payment method
func (a *MonetizationAgent) ValidatePaymentMethod(method PaymentMethod) *ValidationResult {
	return ValidatePaymentMethod(method)
}

// GetUnlockState returns the current unlock state for a product
func (a *MonetizationAgent) GetUnlockState(productID string) UnlockState {
	return a.unlockValidator.GetUnlockState(productID)
}
