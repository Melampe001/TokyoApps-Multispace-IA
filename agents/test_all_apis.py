#!/usr/bin/env python3
"""
Test All APIs - Validate all 4 LLM provider configurations

Tests connectivity and authentication for:
1. Anthropic (Claude) - for Akira
2. OpenAI (GPT) - for Yuki and Kenji
3. Groq (Llama) - for Hiro [FREE TIER]
4. Google (Gemini) - for Sakura [FREE TIER]

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    export OPENAI_API_KEY=sk-...
    export GROQ_API_KEY=gsk_...
    export GOOGLE_API_KEY=...
    
    python agents/test_all_apis.py
"""

import os
import sys
from typing import Dict, Any


def test_anthropic() -> Dict[str, Any]:
    """Test Anthropic API (Claude) for Akira."""
    print("Testing Anthropic API (Claude 3.5 Sonnet)...")
    
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "ANTHROPIC_API_KEY not set",
            "agent": "Akira"
        }
    
    try:
        from anthropic import Anthropic
        
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API test successful' if you can read this."}]
        )
        
        return {
            "success": True,
            "model": "claude-3-5-sonnet-20241022",
            "agent": "侍 Akira",
            "response": response.content[0].text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "Akira"
        }


def test_openai() -> Dict[str, Any]:
    """Test OpenAI API (GPT) for Yuki and Kenji."""
    print("Testing OpenAI API (GPT-4o / GPT-4o mini)...")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY not set",
            "agents": "Yuki & Kenji"
        }
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        # Test with gpt-4o-mini (cheaper for testing)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API test successful' if you can read this."}]
        )
        
        return {
            "success": True,
            "model": "gpt-4o-mini",
            "agents": "❄️ Yuki & 🏗️ Kenji",
            "response": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agents": "Yuki & Kenji"
        }


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
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'API test successful' if you can read this."}]
        )
        
        return {
            "success": True,
            "model": "llama-3.3-70b-versatile",
            "agent": "🛡️ Hiro",
            "tier": "FREE",
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
            "Say 'API test successful' if you can read this.",
            generation_config={"max_output_tokens": 50}
        )
        
        return {
            "success": True,
            "model": "gemini-1.5-flash",
            "agent": "🌸 Sakura",
            "tier": "FREE",
            "response": response.text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent": "Sakura"
        }


def main():
    """Run all API tests."""
    print("=" * 70)
    print("🧪 Tokyo-IA API Test Suite - All Providers")
    print("=" * 70)
    print()
    
    # Check for environment variables
    api_keys = {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY"),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "GROQ_API_KEY": os.environ.get("GROQ_API_KEY"),
        "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY")
    }
    
    configured = sum(1 for v in api_keys.values() if v)
    print(f"📋 API Keys Configured: {configured}/4")
    for key, value in api_keys.items():
        status = "✅" if value else "❌"
        print(f"   {status} {key}")
    print()
    
    if configured == 0:
        print("❌ No API keys configured!")
        print("Please set at least one API key:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        print("  export OPENAI_API_KEY=sk-...")
        print("  export GROQ_API_KEY=gsk_...")
        print("  export GOOGLE_API_KEY=...")
        return 1
    
    print("=" * 70)
    print("Running API Tests...")
    print("=" * 70)
    print()
    
    # Run tests
    results = []
    
    # Test 1: Anthropic
    result = test_anthropic()
    results.append(("Anthropic", result))
    if result["success"]:
        print(f"✅ Anthropic API working - Agent: {result['agent']}")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response'][:50]}...")
    else:
        print(f"❌ Anthropic API failed - {result['error']}")
    print()
    
    # Test 2: OpenAI
    result = test_openai()
    results.append(("OpenAI", result))
    if result["success"]:
        print(f"✅ OpenAI API working - Agents: {result['agents']}")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response'][:50]}...")
    else:
        print(f"❌ OpenAI API failed - {result['error']}")
    print()
    
    # Test 3: Groq (FREE)
    result = test_groq()
    results.append(("Groq", result))
    if result["success"]:
        print(f"✅ Groq API working - Agent: {result['agent']} [{result['tier']}]")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response'][:50]}...")
    else:
        print(f"❌ Groq API failed - {result['error']}")
    print()
    
    # Test 4: Google (FREE)
    result = test_google()
    results.append(("Google", result))
    if result["success"]:
        print(f"✅ Google API working - Agent: {result['agent']} [{result['tier']}]")
        print(f"   Model: {result['model']}")
        print(f"   Response: {result['response'][:50]}...")
    else:
        print(f"❌ Google API failed - {result['error']}")
    print()
    
    # Summary
    print("=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    successful = sum(1 for _, r in results if r["success"])
    print(f"Successful: {successful}/4")
    print(f"Failed: {4 - successful}/4")
    print()
    
    print("Agent Availability:")
    print("  侍 Akira (Code Review): " + ("✅" if results[0][1]["success"] else "❌"))
    print("  ❄️ Yuki (Testing): " + ("✅" if results[1][1]["success"] else "❌"))
    print("  🏗️ Kenji (Architecture): " + ("✅" if results[1][1]["success"] else "❌"))
    print("  🛡️ Hiro (SRE/DevOps): " + ("✅ [FREE]" if results[2][1]["success"] else "❌"))
    print("  🌸 Sakura (Documentation): " + ("✅ [FREE]" if results[3][1]["success"] else "❌"))
    print()
    
    # Cost information
    print("💰 Cost Information:")
    free_agents = sum(1 for _, r in results[2:] if r["success"])
    paid_agents = sum(1 for _, r in results[:2] if r["success"])
    
    print(f"  Free Tier Agents Active: {free_agents}/2 (Hiro, Sakura)")
    print(f"  Paid Agents Active: {paid_agents}/3 (Akira, Yuki, Kenji)")
    
    if free_agents == 2 and paid_agents == 0:
        print("  💚 Running 100% FREE - No API costs!")
    elif free_agents > 0:
        print(f"  💰 Hybrid mode - {free_agents} free + {paid_agents} paid agents")
    else:
        print("  💰 Premium mode - Using paid APIs only")
    
    print("=" * 70)
    
    if successful == 4:
        print("✅ All API tests passed!")
        return 0
    elif successful > 0:
        print(f"⚠️  {successful}/4 API tests passed")
        print("   You can still use Tokyo-IA with available agents")
        return 0
    else:
        print("❌ All API tests failed")
        print("   Please check your API keys and try again")
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
