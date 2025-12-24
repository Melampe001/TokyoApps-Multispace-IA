package monetization

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"time"
)

// BillingValidator validates Google Play billing purchases
type BillingValidator struct {
	publicKey   *rsa.PublicKey
	packageName string
}

// NewBillingValidator creates a new billing validator
func NewBillingValidator(base64PublicKey string, packageName string) (*BillingValidator, error) {
	if base64PublicKey == "" {
		return nil, fmt.Errorf("public key is required")
	}
	if packageName == "" {
		return nil, fmt.Errorf("package name is required")
	}

	// Decode the base64 public key
	keyBytes, err := base64.StdEncoding.DecodeString(base64PublicKey)
	if err != nil {
		return nil, fmt.Errorf("failed to decode public key: %w", err)
	}

	// Parse the public key
	pubKey, err := x509.ParsePKIXPublicKey(keyBytes)
	if err != nil {
		return nil, fmt.Errorf("failed to parse public key: %w", err)
	}

	rsaPubKey, ok := pubKey.(*rsa.PublicKey)
	if !ok {
		return nil, fmt.Errorf("public key is not RSA")
	}

	return &BillingValidator{
		publicKey:   rsaPubKey,
		packageName: packageName,
	}, nil
}

// ValidatePurchase validates a Google Play billing purchase
func (v *BillingValidator) ValidatePurchase(purchase *PurchaseData) *ValidationResult {
	result := &ValidationResult{
		Valid:     false,
		Method:    PaymentMethodGooglePlay,
		ProductID: purchase.ProductID,
		Timestamp: time.Now(),
		Details:   make(map[string]interface{}),
	}

	// Validate package name
	if purchase.PackageName != v.packageName {
		result.Error = fmt.Errorf("package name mismatch: expected %s, got %s", v.packageName, purchase.PackageName)
		return result
	}

	// Validate signature
	if err := v.verifySignature(purchase); err != nil {
		result.Error = fmt.Errorf("%w: %v", ErrInvalidSignature, err)
		return result
	}

	// Validate purchase token
	if purchase.PurchaseToken == "" {
		result.Error = ErrInvalidToken
		return result
	}

	// Validate product ID
	if purchase.ProductID == "" {
		result.Error = ErrInvalidProductID
		return result
	}

	// Validate purchase state (0 = purchased, 1 = canceled)
	if purchase.PurchaseState != 0 {
		result.Error = fmt.Errorf("purchase is not in valid state: %d", purchase.PurchaseState)
		return result
	}

	// Check if purchase is not too old (e.g., within 365 days)
	if time.Since(purchase.PurchaseTime) > 365*24*time.Hour {
		result.Error = ErrPurchaseExpired
		return result
	}

	result.Valid = true
	result.Details["order_id"] = purchase.OrderID
	result.Details["purchase_time"] = purchase.PurchaseTime
	result.Details["acknowledged"] = purchase.Acknowledged

	return result
}

// verifySignature verifies the purchase signature using RSA-SHA1
func (v *BillingValidator) verifySignature(purchase *PurchaseData) error {
	// Create the purchase data JSON (without signature)
	purchaseJSON, err := json.Marshal(map[string]interface{}{
		"orderId":       purchase.OrderID,
		"packageName":   purchase.PackageName,
		"productId":     purchase.ProductID,
		"purchaseTime":  purchase.PurchaseTime.Unix(),
		"purchaseState": purchase.PurchaseState,
		"purchaseToken": purchase.PurchaseToken,
	})
	if err != nil {
		return fmt.Errorf("failed to marshal purchase data: %w", err)
	}

	// Decode signature
	signatureBytes, err := base64.StdEncoding.DecodeString(purchase.Signature)
	if err != nil {
		return fmt.Errorf("failed to decode signature: %w", err)
	}

	// Hash the purchase data
	hashed := sha1.Sum(purchaseJSON)

	// Verify signature
	err = rsa.VerifyPKCS1v15(v.publicKey, crypto.SHA1, hashed[:], signatureBytes)
	if err != nil {
		return fmt.Errorf("signature verification failed: %w", err)
	}

	return nil
}

// ValidatePaymentMethod validates that the payment method is allowed
func ValidatePaymentMethod(method PaymentMethod) *ValidationResult {
	result := &ValidationResult{
		Valid:     false,
		Method:    method,
		Timestamp: time.Now(),
		Details:   make(map[string]interface{}),
	}

	switch method {
	case PaymentMethodGooglePlay, PaymentMethodLocal:
		result.Valid = true
		result.Details["allowed"] = true
	case PaymentMethodExternal:
		result.Error = ErrExternalPayment
		result.Details["allowed"] = false
		result.Details["reason"] = "external payment methods are not allowed"
	case PaymentMethodRemote:
		result.Error = ErrRemotePayment
		result.Details["allowed"] = false
		result.Details["reason"] = "remote payment methods are not allowed"
	default:
		result.Error = fmt.Errorf("unknown payment method: %s", method)
		result.Details["allowed"] = false
	}

	return result
}
