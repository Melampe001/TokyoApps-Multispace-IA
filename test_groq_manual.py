#!/usr/bin/env python3
"""
Quick test for Groq API (Hiro agent - Llama 3.3 70B)
Run: python test_groq_manual.py
"""

import os
from groq import Groq

def test_groq_api():
    """Test Groq API connection with Llama 3.3 70B."""
    
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not found in environment")
        print("Set it with: export GROQ_API_KEY='your-key-here'")
        return False
    
    print("🛡️ Testing Hiro (Groq - Llama 3.3 70B)...")
    print(f"API Key: {api_key[:20]}...{api_key[-4:]}")
    
    try:
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Hiro, an SRE and DevOps expert from Tokyo-IA."
                },
                {
                    "role": "user",
                    "content": "Introduce yourself in exactly 15 words.",
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=100,
        )
        
        response = chat_completion.choices[0].message.content
        
        print("\n✅ GROQ API TEST PASSED!")
        print(f"\n🛡️ Hiro says: {response}")
        print(f"\nModel: {chat_completion.model}")
        print(f"Tokens used: {chat_completion.usage.total_tokens}")
        print(f"Cost: $0.00 (Free Tier)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GROQ API TEST FAILED!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_groq_api()
    exit(0 if success else 1)
