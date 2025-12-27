// Package monetization provides monetization and billing validation for Tokyo-IA.
package monetization

import (
	"errors"
	"time"
)

// Common errors
var (
	ErrInvalidSignature   = errors.New("invalid purchase signature")
	ErrInvalidToken       = errors.New("invalid purchase token")
	ErrExternalPayment    = errors.New("external payment methods are not allowed")
	ErrRemotePayment      = errors.New("remote payment methods are not allowed")
	ErrInvalidUnlockState = errors.New("invalid unlock state")
	ErrDuplicateRestore   = errors.New("duplicate restore operation")
	ErrInvalidProductID   = errors.New("invalid product ID")
	ErrPurchaseExpired    = errors.New("purchase has expired")
	ErrUnauthorized       = errors.New("unauthorized access")
)

// PaymentMethod represents the type of payment method
type PaymentMethod string

const (
	// PaymentMethodGooglePlay represents Google Play billing
	PaymentMethodGooglePlay PaymentMethod = "google_play"
	// PaymentMethodLocal represents local unlock
	PaymentMethodLocal PaymentMethod = "local"
	// PaymentMethodExternal represents external payment (not allowed)
	PaymentMethodExternal PaymentMethod = "external"
	// PaymentMethodRemote represents remote payment (not allowed)
	PaymentMethodRemote PaymentMethod = "remote"
)

// UnlockState represents the current unlock state
type UnlockState string

const (
	// UnlockStateLocked indicates the feature is locked
	UnlockStateLocked UnlockState = "locked"
	// UnlockStateUnlocked indicates the feature is unlocked
	UnlockStateUnlocked UnlockState = "unlocked"
	// UnlockStateExpired indicates the unlock has expired
	UnlockStateExpired UnlockState = "expired"
)

// PurchaseData represents Google Play billing purchase data
type PurchaseData struct {
	OrderID          string    `json:"orderId"`
	PackageName      string    `json:"packageName"`
	ProductID        string    `json:"productId"`
	PurchaseTime     time.Time `json:"purchaseTime"`
	PurchaseState    int       `json:"purchaseState"`
	PurchaseToken    string    `json:"purchaseToken"`
	Signature        string    `json:"signature"`
	DeveloperPayload string    `json:"developerPayload,omitempty"`
	Acknowledged     bool      `json:"acknowledged"`
}

// LocalUnlock represents a local unlock state
type LocalUnlock struct {
	ProductID  string                 `json:"product_id"`
	UnlockedAt time.Time              `json:"unlocked_at"`
	State      UnlockState            `json:"state"`
	ExpiresAt  *time.Time             `json:"expires_at,omitempty"`
	Metadata   map[string]interface{} `json:"metadata,omitempty"`
}

// RestoreOperation represents a purchase restore operation
type RestoreOperation struct {
	OperationID  string        `json:"operation_id"`
	UserID       string        `json:"user_id"`
	ProductIDs   []string      `json:"product_ids"`
	Timestamp    time.Time     `json:"timestamp"`
	Method       PaymentMethod `json:"method"`
	IsIdempotent bool          `json:"is_idempotent"`
}

// ValidationResult represents the result of a validation operation
type ValidationResult struct {
	Valid     bool                   `json:"valid"`
	Method    PaymentMethod          `json:"method"`
	ProductID string                 `json:"product_id,omitempty"`
	Error     error                  `json:"error,omitempty"`
	Details   map[string]interface{} `json:"details,omitempty"`
	Timestamp time.Time              `json:"timestamp"`
}
