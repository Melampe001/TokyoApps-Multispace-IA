package monetization

import (
	"testing"
	"time"
)

func TestValidatePaymentMethod(t *testing.T) {
	tests := []struct {
		name      string
		method    PaymentMethod
		wantValid bool
		wantError error
	}{
		{
			name:      "Google Play allowed",
			method:    PaymentMethodGooglePlay,
			wantValid: true,
			wantError: nil,
		},
		{
			name:      "Local payment allowed",
			method:    PaymentMethodLocal,
			wantValid: true,
			wantError: nil,
		},
		{
			name:      "External payment rejected",
			method:    PaymentMethodExternal,
			wantValid: false,
			wantError: ErrExternalPayment,
		},
		{
			name:      "Remote payment rejected",
			method:    PaymentMethodRemote,
			wantValid: false,
			wantError: ErrRemotePayment,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ValidatePaymentMethod(tt.method)

			if result.Valid != tt.wantValid {
				t.Errorf("expected valid=%v, got %v", tt.wantValid, result.Valid)
			}

			if tt.wantError != nil && result.Error != tt.wantError {
				t.Errorf("expected error %v, got %v", tt.wantError, result.Error)
			}

			if result.Method != tt.method {
				t.Errorf("expected method %s, got %s", tt.method, result.Method)
			}

			// Check that details are populated
			if result.Details == nil {
				t.Error("expected details to be populated")
			}
		})
	}
}

func TestUnlockValidator(t *testing.T) {
	validator := NewUnlockValidator()

	t.Run("unlock and validate", func(t *testing.T) {
		productID := "premium_feature"
		err := validator.Unlock(productID, nil)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		result := validator.ValidateUnlock(productID)
		if !result.Valid {
			t.Errorf("expected valid unlock, got error: %v", result.Error)
		}

		if result.Method != PaymentMethodLocal {
			t.Errorf("expected method %s, got %s", PaymentMethodLocal, result.Method)
		}
	})

	t.Run("validate locked product", func(t *testing.T) {
		result := validator.ValidateUnlock("non_existent")
		if result.Valid {
			t.Error("expected validation to fail for non-existent product")
		}

		if result.Error != ErrUnauthorized {
			t.Errorf("expected error %v, got %v", ErrUnauthorized, result.Error)
		}
	})

	t.Run("unlock with expiration", func(t *testing.T) {
		productID := "expired_feature"
		expiresAt := time.Now().Add(-1 * time.Hour) // Expired 1 hour ago
		err := validator.Unlock(productID, &expiresAt)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		result := validator.ValidateUnlock(productID)
		if result.Valid {
			t.Error("expected validation to fail for expired unlock")
		}

		if result.Error != ErrPurchaseExpired {
			t.Errorf("expected error %v, got %v", ErrPurchaseExpired, result.Error)
		}

		state := validator.GetUnlockState(productID)
		if state != UnlockStateExpired {
			t.Errorf("expected state %s, got %s", UnlockStateExpired, state)
		}
	})

	t.Run("lock product", func(t *testing.T) {
		productID := "lockable_feature"
		err := validator.Unlock(productID, nil)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		err = validator.Lock(productID)
		if err != nil {
			t.Fatalf("unexpected error: %v", err)
		}

		result := validator.ValidateUnlock(productID)
		if result.Valid {
			t.Error("expected validation to fail for locked product")
		}
	})

	t.Run("invalid product ID", func(t *testing.T) {
		err := validator.Unlock("", nil)
		if err != ErrInvalidProductID {
			t.Errorf("expected error %v, got %v", ErrInvalidProductID, err)
		}
	})
}

func TestRestoreValidator(t *testing.T) {
	window := 5 * time.Second
	validator := NewRestoreValidator(window)

	t.Run("first restore succeeds", func(t *testing.T) {
		userID := "user123"
		productIDs := []string{"product1", "product2"}

		result := validator.ValidateRestore(userID, productIDs, PaymentMethodGooglePlay)
		if !result.Valid {
			t.Errorf("expected valid restore, got error: %v", result.Error)
		}

		if result.Details["is_duplicate"] != false {
			t.Error("expected is_duplicate to be false")
		}

		if result.Details["is_idempotent"] != true {
			t.Error("expected is_idempotent to be true")
		}
	})

	t.Run("duplicate restore within window fails", func(t *testing.T) {
		userID := "user456"
		productIDs := []string{"product3", "product4"}

		// First restore
		result1 := validator.ValidateRestore(userID, productIDs, PaymentMethodLocal)
		if !result1.Valid {
			t.Fatalf("first restore failed: %v", result1.Error)
		}

		// Immediate duplicate should fail
		result2 := validator.ValidateRestore(userID, productIDs, PaymentMethodLocal)
		if result2.Valid {
			t.Error("expected duplicate restore to fail")
		}

		if result2.Error != ErrDuplicateRestore {
			t.Errorf("expected error %v, got %v", ErrDuplicateRestore, result2.Error)
		}

		if result2.Details["is_duplicate"] != true {
			t.Error("expected is_duplicate to be true")
		}
	})

	t.Run("restore after window succeeds", func(t *testing.T) {
		userID := "user789"
		productIDs := []string{"product5"}

		// First restore
		result1 := validator.ValidateRestore(userID, productIDs, PaymentMethodGooglePlay)
		if !result1.Valid {
			t.Fatalf("first restore failed: %v", result1.Error)
		}

		// Wait for window to pass
		time.Sleep(window + 100*time.Millisecond)

		// Second restore should succeed
		result2 := validator.ValidateRestore(userID, productIDs, PaymentMethodGooglePlay)
		if !result2.Valid {
			t.Errorf("expected restore after window to succeed, got error: %v", result2.Error)
		}
	})

	t.Run("restore with external payment fails", func(t *testing.T) {
		userID := "user_ext"
		productIDs := []string{"product6"}

		result := validator.ValidateRestore(userID, productIDs, PaymentMethodExternal)
		if result.Valid {
			t.Error("expected restore with external payment to fail")
		}

		if result.Error != ErrExternalPayment {
			t.Errorf("expected error %v, got %v", ErrExternalPayment, result.Error)
		}
	})

	t.Run("restore with remote payment fails", func(t *testing.T) {
		userID := "user_remote"
		productIDs := []string{"product7"}

		result := validator.ValidateRestore(userID, productIDs, PaymentMethodRemote)
		if result.Valid {
			t.Error("expected restore with remote payment to fail")
		}

		if result.Error != ErrRemotePayment {
			t.Errorf("expected error %v, got %v", ErrRemotePayment, result.Error)
		}
	})

	t.Run("invalid input validation", func(t *testing.T) {
		// Empty user ID
		result1 := validator.ValidateRestore("", []string{"product"}, PaymentMethodLocal)
		if result1.Valid {
			t.Error("expected validation to fail for empty user ID")
		}

		// Empty product IDs
		result2 := validator.ValidateRestore("user", []string{}, PaymentMethodLocal)
		if result2.Valid {
			t.Error("expected validation to fail for empty product IDs")
		}
	})

	t.Run("operation ID consistency", func(t *testing.T) {
		userID := "consistent_user"
		productIDs := []string{"b", "a", "c"} // Unsorted

		result1 := validator.ValidateRestore(userID, productIDs, PaymentMethodGooglePlay)
		if !result1.Valid {
			t.Fatalf("first restore failed: %v", result1.Error)
		}

		opID1 := result1.Details["operation_id"].(string)

		// Clear and try again with different order
		validator.Clear()
		productIDs2 := []string{"a", "c", "b"} // Different order, same products

		result2 := validator.ValidateRestore(userID, productIDs2, PaymentMethodGooglePlay)
		if !result2.Valid {
			t.Fatalf("second restore failed: %v", result2.Error)
		}

		opID2 := result2.Details["operation_id"].(string)

		if opID1 != opID2 {
			t.Error("expected same operation ID for same user and products regardless of order")
		}
	})
}

func TestGetOperationCount(t *testing.T) {
	validator := NewRestoreValidator(1 * time.Hour)

	if count := validator.GetOperationCount(); count != 0 {
		t.Errorf("expected 0 operations, got %d", count)
	}

	validator.ValidateRestore("user1", []string{"p1"}, PaymentMethodLocal)
	if count := validator.GetOperationCount(); count != 1 {
		t.Errorf("expected 1 operation, got %d", count)
	}

	validator.ValidateRestore("user2", []string{"p2"}, PaymentMethodGooglePlay)
	if count := validator.GetOperationCount(); count != 2 {
		t.Errorf("expected 2 operations, got %d", count)
	}
}
