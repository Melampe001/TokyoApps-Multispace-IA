"""
CrewAI Configuration for Tokyo-IA Multi-Agent System

This module defines the agent configurations for the Tokyo-IA AI orchestration system.
"""

from crewai import Agent, LLM
import os


def get_llm(model_name: str = "gpt-4") -> LLM:
    """Get LLM instance based on model name."""
    # Support multiple providers
    if model_name.startswith("gpt"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        return LLM(model=f"openai/{model_name}", api_key=api_key)
    elif model_name.startswith("claude"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        return LLM(model=f"anthropic/{model_name}", api_key=api_key)
    elif model_name.startswith("gemini"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        return LLM(model=f"google/{model_name}", api_key=api_key)
    else:
        # Default to GPT-4
        return LLM(model="openai/gpt-4")


def create_research_agent(llm: LLM = None) -> Agent:
    """Create a research specialist agent."""
    if llm is None:
        llm = get_llm("gpt-4")
    
    return Agent(
        role="Research Specialist",
        goal="Conduct thorough research and gather comprehensive information on any topic",
        backstory="""You are an expert researcher with years of experience in data gathering, 
        analysis, and synthesis. You excel at finding relevant information from various sources 
        and presenting it in a clear, organized manner.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def create_code_reviewer_agent(llm: LLM = None) -> Agent:
    """Create a code review agent."""
    if llm is None:
        llm = get_llm("claude-3-opus-20240229")
    
    return Agent(
        role="Senior Code Reviewer",
        goal="Review code for quality, best practices, security, and potential improvements",
        backstory="""You are a senior software engineer with extensive experience in code review. 
        You have a keen eye for bugs, security vulnerabilities, and opportunities for optimization. 
        Your reviews are thorough, constructive, and help teams write better code.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def create_content_writer_agent(llm: LLM = None) -> Agent:
    """Create a content writing agent."""
    if llm is None:
        llm = get_llm("gpt-4")
    
    return Agent(
        role="Content Writer",
        goal="Create engaging, well-structured content for various purposes",
        backstory="""You are a professional content writer with expertise in creating compelling 
        narratives, technical documentation, blog posts, and marketing copy. Your writing is clear, 
        engaging, and tailored to the target audience.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def create_data_analyst_agent(llm: LLM = None) -> Agent:
    """Create a data analysis agent."""
    if llm is None:
        llm = get_llm("gemini-pro")
    
    return Agent(
        role="Data Analyst",
        goal="Analyze data, identify patterns, and provide actionable insights",
        backstory="""You are a skilled data analyst with expertise in statistical analysis, 
        data visualization, and business intelligence. You can quickly identify trends, 
        anomalies, and opportunities hidden in data.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def create_translator_agent(llm: LLM = None) -> Agent:
    """Create a translation agent."""
    if llm is None:
        llm = get_llm("gpt-4")
    
    return Agent(
        role="Professional Translator",
        goal="Provide accurate, culturally-appropriate translations between languages",
        backstory="""You are a professional translator fluent in multiple languages. 
        You understand not just the words, but the cultural context and nuances that 
        make translations feel natural and authentic.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )


def create_problem_solver_agent(llm: LLM = None) -> Agent:
    """Create a general problem-solving agent."""
    if llm is None:
        llm = get_llm("gpt-4")
    
    return Agent(
        role="Problem Solver",
        goal="Analyze problems and provide creative, effective solutions",
        backstory="""You are a strategic thinker with a talent for breaking down complex 
        problems into manageable parts and finding innovative solutions. You approach 
        challenges systematically and think outside the box.""",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )
