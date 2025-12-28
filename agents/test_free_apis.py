#!/usr/bin/env python3
"""
Test free tier APIs (Groq + Google) for Tokyo-IA
Quick validation without requiring paid API keys
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    """Test Groq API (Hiro - Llama 3.3 70B)"""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ GROQ_API_KEY not set")
            print("   Get your free key: https://console.groq.com/")
            return False
        
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
        
        print(f"✅ GROQ API (Hiro - Llama 3.3 70B)")
        print(f"   Response: {response}")
        print(f"   Model: {chat_completion.model}")
        print(f"   Tokens: {chat_completion.usage.total_tokens}")
        print(f"   Cost: $0.00 (Free Tier)\n")
        
        return True
        
    except ImportError:
        print("❌ GROQ: 'groq' package not installed")
        print("   Run: pip install groq\n")
        return False
    except Exception as e:
        print(f"❌ GROQ API Error: {str(e)}\n")
        return False

def test_google():
    """Test Google AI API (Sakura - Gemini 1.5 Flash)"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not set")
            print("   Get your free key: https://makersuite.google.com/app/apikey")
            return False
        
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            "You are Sakura, a documentation specialist from Tokyo-IA. Introduce yourself in exactly 15 words.",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=100,
            ),
        )
        
        print(f"✅ GOOGLE AI (Sakura - Gemini 1.5 Flash)")
        print(f"   Response: {response.text}")
        print(f"   Model: gemini-1.5-flash")
        print(f"   Cost: $0.00 (Free Tier)\n")
        
        return True
        
    except ImportError:
        print("❌ GOOGLE: 'google-generativeai' package not installed")
        print("   Run: pip install google-generativeai\n")
        return False
    except Exception as e:
        print(f"❌ GOOGLE AI API Error: {str(e)}\n")
        return False

def test_crewai():
    """Test CrewAI installation"""
    try:
        from crewai import Agent, Task, Crew
        print("✅ CREWAI: Installed and ready")
        print(f"   CrewAI framework available\n")
        return True
    except ImportError:
        print("❌ CREWAI: Not installed")
        print("   Run: pip install crewai crewai-tools\n")
        return False

def main():
    print("🚀 Tokyo-IA Free Tier API Test")
    print("=" * 60)
    print()
    
    # Test CrewAI
    crewai_ok = test_crewai()
    
    # Test APIs
    groq_ok = test_groq()
    google_ok = test_google()
    
    print("=" * 60)
    
    if groq_ok and google_ok and crewai_ok:
        print("🎉 All systems ready! Free Tier: 2/2 APIs working!")
        print("💰 Total cost: $0.00")
        print("\n📋 Next steps:")
        print("   1. Run cleanup workflow:")
        print("      python agents/tokyo_crew.py cleanup")
        print()
        print("   2. Analyze a PR:")
        print("      python agents/tokyo_crew.py analyze-pr 126")
        print()
        print("   3. Generate documentation:")
        print("      python agents/tokyo_crew.py generate-docs")
        return 0
    else:
        print("⚠️  Setup incomplete. Please fix the errors above.")
        print("\n📋 Quick fix:")
        print("   1. Install dependencies: pip install groq google-generativeai crewai crewai-tools python-dotenv")
        print("   2. Add API keys to .env file")
        print("   3. Run this test again")
        return 1

if __name__ == "__main__":
    exit(main())
