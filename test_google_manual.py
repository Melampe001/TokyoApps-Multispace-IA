#!/usr/bin/env python3
"""
Quick test for Google AI API (Sakura agent - Gemini 1.5 Flash)
Run: python test_google_manual.py
"""

import os
import google.generativeai as genai

def test_google_api():
    """Test Google AI API connection with Gemini 1.5 Flash."""
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment")
        print("Set it with: export GOOGLE_API_KEY='your-key-here'")
        return False
    
    print("🌸 Testing Sakura (Google - Gemini 1.5 Flash)...")
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(
            "You are Sakura, a documentation specialist from Tokyo-IA. Introduce yourself in exactly 15 words.",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=100,
            ),
        )
        
        print("\n✅ GOOGLE AI TEST PASSED!")
        print(f"\n🌸 Sakura says: {response.text}")
        print(f"\nModel: gemini-1.5-flash")
        print(f"Cost: $0.00 (Free Tier)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GOOGLE AI TEST FAILED!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_google_api()
    exit(0 if success else 1)
