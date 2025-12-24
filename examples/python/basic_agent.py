#!/usr/bin/env python3
"""
Tokyo-IA Basic Agent Example

This script demonstrates basic usage of CrewAI with Groq LLM inference.
It creates a Tokyo travel expert agent that provides recommendations.

Requirements:
- GROQ_API_KEY environment variable must be set
- Install dependencies: pip install -r requirements.txt

Usage:
    export GROQ_API_KEY=your_api_key_here
    python examples/python/basic_agent.py

Optional:
    export GROQ_MODEL=groq/llama-3.1-70b-versatile  # Default model if not specified
"""

import os
import sys
from typing import Optional


def check_api_key() -> Optional[str]:
    """Check if GROQ_API_KEY is set in environment."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY environment variable is not set!")
        print("\nPlease set your API key:")
        print("  export GROQ_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://console.groq.com")
        sys.exit(1)
    return api_key


def main():
    """Main function to run the basic agent example."""
    print("🗼 Tokyo-IA - Basic Agent Example\n")

    # Check for API key
    api_key = check_api_key()
    print("✅ API key found")

    try:
        from crewai import Agent, Task, Crew, LLM

        print("✅ Dependencies loaded successfully\n")
    except ImportError as e:
        print(f"❌ Error importing dependencies: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Initialize Groq LLM using CrewAI's LLM class
    # Note: API key is automatically read from GROQ_API_KEY environment variable
    print("🔧 Initializing Groq LLM...")
    model = os.environ.get("GROQ_MODEL", "groq/llama-3.1-70b-versatile")
    print(f"   Using model: {model}")
    try:
        llm = LLM(model=model, temperature=0.7)
        print("✅ LLM initialized\n")
    except Exception as e:
        print(f"❌ Error initializing LLM: {e}")
        sys.exit(1)

    # Create a Tokyo travel expert agent
    print("🤖 Creating Tokyo Travel Expert agent...")
    tokyo_guide = Agent(
        role="Tokyo Travel Expert",
        goal="Provide accurate and helpful information about Tokyo attractions",
        backstory="""You are an experienced travel guide who has lived in Tokyo 
        for over 10 years. You have deep knowledge about Tokyo's culture, 
        attractions, food, and transportation. You love sharing insider tips 
        and helping visitors make the most of their Tokyo experience.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    print("✅ Agent created\n")

    # Create a task for the agent
    print("📋 Creating task...")
    task = Task(
        description="""Recommend 3 must-visit places in Tokyo for first-time 
        visitors. For each place, provide:
        1. The name of the place
        2. Why it's worth visiting
        3. A practical tip for visiting
        
        Keep recommendations diverse (traditional, modern, nature/city mix).""",
        agent=tokyo_guide,
        expected_output="""A formatted list of 3 Tokyo attractions with names, 
        reasons to visit, and practical tips.""",
    )
    print("✅ Task created\n")

    # Create a crew and execute
    print("🚀 Starting crew execution...\n")
    print("=" * 70)

    crew = Crew(agents=[tokyo_guide], tasks=[task], verbose=True)

    try:
        result = crew.kickoff()

        print("=" * 70)
        print("\n✨ Result:\n")
        print(result)
        print("\n✅ Example completed successfully!")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("\nPossible causes:")
        print("  - Invalid API key")
        print("  - Rate limit exceeded")
        print("  - Network connectivity issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
