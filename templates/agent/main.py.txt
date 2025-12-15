"""
AI Agent Main Entry Point
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

# Load environment variables
load_dotenv()

def main():
    """Initialize and run the AI agent"""
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Define tools
    tools = [
        Tool(
            name="WebSearch",
            func=lambda x: "Search results for: " + x,
            description="Search the web for information"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),
            description="Calculate mathematical expressions"
        )
    ]
    
    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Run agent
    print("AI Agent initialized!")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("You: ")
        
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        try:
            result = agent.run(query)
            print(f"\nAgent: {result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()
