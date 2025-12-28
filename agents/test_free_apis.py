#!/usr/bin/env python3
"""
Test Free APIs - Quick validation for free tier LLM providers

Tests only the FREE tier APIs:
1. Groq (Llama 3.3 70B) - for Hiro 🛡️
2. Google (Gemini 1.5 Flash) - for Sakura 🌸

Perfect for development and testing without API costs!

Usage:
    export GROQ_API_KEY=gsk_...
    export GOOGLE_API_KEY=...
    
    python agents/test_free_apis.py
"""

import os
import sys
from typing import Dict, Any


def test_groq() -> Dict[str, Any]:
    """Test Groq API (Llama) for Hiro - FREE TIER."""
    print("Testing Groq API (Llama 3.3 70B) [FREE TIER]...")
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "GROQ_API_KEY not set",
            "agent": "Hiro"
        }
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "You are Hiro, an SRE expert. Say 'API test successful' and briefly introduce yourself."
            }]
        )
        
        return {
            "success": True,
            "model": "llama-3.3-70b-versatile",
            "agent": "🛡️ Hiro",
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "Hiro"
        }


def test_google() -> Dict[str, Any]:
    """Test Google API (Gemini) for Sakura - FREE TIER."""
    print("Testing Google API (Gemini 1.5 Flash) [FREE TIER]...")
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "GOOGLE_API_KEY not set",
            "agent": "Sakura"
        }
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            "You are Sakura, a documentation specialist. Say 'API test successful' and briefly introduce yourself.",
            generation_config={"max_output_tokens": 100}
        )
        
        return {
            "success": True,
            "model": "gemini-1.5-flash",
            "agent": "🌸 Sakura",
            "response": response.text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "Sakura"
        }


def main():
    """Run free tier API tests."""
    print("=" * 70)
    print("🧪 Tokyo-IA FREE Tier API Test - Groq + Google")
    print("=" * 70)
    print()
    print("💚 Testing only FREE tier providers:")
    print("   🛡️ Hiro (Groq - Llama 3.3 70B)")
    print("   🌸 Sakura (Google - Gemini 1.5 Flash)")
    print()
    
    # Check for environment variables
    api_keys = {
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY"),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY")
    }
    
    configured = sum(1 for v in api_keys.values() if v)
    print(f"📋 API Keys Configured: {configured}/2")
    for key, value in api_keys.items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}")
    print()
    
    if configured == 0:
        print("❌ No API keys configured!")
        print()
        print("To use FREE tier agents, get API keys from:")
        print()
        print("1. Groq (FREE - No credit card required)")
        print("   → https://console.groq.com")
        print("   → export GROQ_API_KEY=gsk_...")
        print()
        print("2. Google AI (FREE - No credit card required)")
        print("   → https://makersuite.google.com/app/apikey")
        print("   → export GOOGLE_API_KEY=...")
        print()
        return 1
    
    print("=" * 70)
    print("Running API Tests...")
    print("=" * 70)
    print()
    
    # Run tests
    results = []
    
    # Test 1: Groq
    result = test_groq()
    results.append(("Groq", result))
    if result["success"]:
        print(f"✅ Groq API working - Agent: {result['agent']}")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response']}")
    else:
        print(f"❌ Groq API failed - {result['error']}")
    print()
    
    # Test 2: Google
    result = test_google()
    results.append(("Google", result))
    if result["success"]:
        print(f"✅ Google API working - Agent: {result['agent']}")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response']}")
    else:
        print(f"❌ Google API failed - {result['error']}")
    print()
    
    # Summary
    print("=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    successful = sum(1 for _, r in results if r["success"])
    print(f"Successful: {successful}/2")
    print(f"Failed: {2 - successful}/2")
    print()
    
    print("Free Tier Agent Availability:")
    print("  🛡️ Hiro (SRE/DevOps): " + ("✅" if results[0][1]["success"] else "❌"))
    print("  🌸 Sakura (Documentation): " + ("✅" if results[1][1]["success"] else "❌"))
    print()
    
    # Next steps
    print("💡 What You Can Do:")
    if successful == 2:
        print("  ✅ All FREE agents working!")
        print("  → Infrastructure analysis with Hiro")
        print("  → Documentation generation with Sakura")
        print("  → Repository cleanup workflows")
        print("  → Branch analysis and recommendations")
        print()
        print("  💰 Cost: $0/month (100% FREE)")
    elif successful == 1:
        agent_name = "Hiro" if results[0][1]["success"] else "Sakura"
        print(f"  ⚠️  Only {agent_name} is working")
        print(f"  → Check API key configuration for the other agent")
    else:
        print("  ❌ No agents working")
        print("  → Double-check your API keys")
        print("  → Verify network connectivity")
    
    print()
    print("🚀 To add premium agents (optional):")
    print("  → Akira (Code Review): export ANTHROPIC_API_KEY=sk-ant-...")
    print("  → Yuki & Kenji (Testing/Architecture): export OPENAI_API_KEY=sk-...")
    print("=" * 70)
    
    if successful > 0:
        print(f"✅ {successful}/2 FREE tier API tests passed!")
        print("💚 You can use Tokyo-IA at ZERO cost with these agents!")
        return 0
    else:
        print("❌ All FREE tier API tests failed")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
