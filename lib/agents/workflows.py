"""
Workflow definitions for Tokyo-IA AI orchestration.

This module defines complete workflows using CrewAI agents and tasks.
"""

from crewai import Crew, Task
from typing import Dict, Any, List
from .crew_config import (
    create_research_agent,
    create_code_reviewer_agent,
    create_content_writer_agent,
    create_data_analyst_agent,
    get_llm
)
from .tools import ALL_TOOLS


def research_workflow(topic: str) -> Dict[str, Any]:
    """
    Research workflow: Comprehensive research on a topic.
    
    Args:
        topic: The topic to research
        
    Returns:
        Research results
    """
    # Create agent
    researcher = create_research_agent()
    
    # Define task
    research_task = Task(
        description=f"""
        Conduct comprehensive research on the topic: {topic}
        
        Your research should include:
        1. Key concepts and definitions
        2. Current state and trends
        3. Important developments
        4. Expert opinions and perspectives
        5. Reliable sources and references
        
        Present your findings in a well-structured format.
        """,
        agent=researcher,
        expected_output="A comprehensive research report with citations"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "workflow": "research",
        "topic": topic,
        "result": str(result),
        "status": "completed"
    }


def code_review_workflow(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Code review workflow: Thorough code review with recommendations.
    
    Args:
        code: The code to review
        language: Programming language
        
    Returns:
        Code review results
    """
    # Create agent
    reviewer = create_code_reviewer_agent()
    
    # Define task
    review_task = Task(
        description=f"""
        Review the following {language} code:
        
        ```{language}
        {code}
        ```
        
        Provide a comprehensive review covering:
        1. Code quality and readability
        2. Potential bugs or errors
        3. Security vulnerabilities
        4. Performance considerations
        5. Best practices and improvements
        6. Testing recommendations
        
        Rate the code on a scale of 1-10 and provide specific recommendations.
        """,
        agent=reviewer,
        expected_output="A detailed code review with ratings and recommendations"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[reviewer],
        tasks=[review_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "workflow": "code_review",
        "language": language,
        "result": str(result),
        "status": "completed"
    }


def content_creation_workflow(topic: str, content_type: str = "blog") -> Dict[str, Any]:
    """
    Content creation workflow: Research and write content.
    
    Args:
        topic: Content topic
        content_type: Type of content (blog, article, documentation, etc.)
        
    Returns:
        Created content
    """
    # Create agents
    researcher = create_research_agent()
    writer = create_content_writer_agent()
    
    # Define tasks
    research_task = Task(
        description=f"""
        Research the topic: {topic}
        
        Gather key information, facts, and insights that will be useful 
        for creating a {content_type}.
        """,
        agent=researcher,
        expected_output="Research findings and key points"
    )
    
    writing_task = Task(
        description=f"""
        Using the research provided, create a compelling {content_type} about {topic}.
        
        The content should:
        1. Have an engaging introduction
        2. Be well-structured with clear sections
        3. Include relevant examples and explanations
        4. Have a strong conclusion
        5. Be appropriate for the target audience
        
        Aim for 500-800 words.
        """,
        agent=writer,
        expected_output=f"A complete {content_type} article",
        context=[research_task]
    )
    
    # Create and run crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "workflow": "content_creation",
        "topic": topic,
        "content_type": content_type,
        "result": str(result),
        "status": "completed"
    }


def data_analysis_workflow(data_description: str, analysis_goals: List[str]) -> Dict[str, Any]:
    """
    Data analysis workflow: Analyze data and provide insights.
    
    Args:
        data_description: Description of the data
        analysis_goals: List of analysis objectives
        
    Returns:
        Analysis results
    """
    # Create agent
    analyst = create_data_analyst_agent()
    
    goals_text = "\n".join(f"{i+1}. {goal}" for i, goal in enumerate(analysis_goals))
    
    # Define task
    analysis_task = Task(
        description=f"""
        Analyze the following data:
        
        {data_description}
        
        Analysis objectives:
        {goals_text}
        
        Provide:
        1. Key findings and patterns
        2. Statistical insights
        3. Trends and anomalies
        4. Actionable recommendations
        5. Visualizations suggestions
        
        Present your analysis in a clear, structured format.
        """,
        agent=analyst,
        expected_output="Comprehensive data analysis with insights and recommendations"
    )
    
    # Create and run crew
    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        verbose=True
    )
    
    result = crew.kickoff()
    
    return {
        "workflow": "data_analysis",
        "data_description": data_description,
        "analysis_goals": analysis_goals,
        "result": str(result),
        "status": "completed"
    }


# Workflow registry for easy access
WORKFLOWS = {
    "research": research_workflow,
    "code_review": code_review_workflow,
    "content_creation": content_creation_workflow,
    "data_analysis": data_analysis_workflow
}


def run_workflow(workflow_name: str, **kwargs) -> Dict[str, Any]:
    """
    Run a workflow by name.
    
    Args:
        workflow_name: Name of the workflow
        **kwargs: Workflow-specific arguments
        
    Returns:
        Workflow results
    """
    if workflow_name not in WORKFLOWS:
        return {
            "error": f"Unknown workflow: {workflow_name}",
            "available_workflows": list(WORKFLOWS.keys())
        }
    
    try:
        workflow_func = WORKFLOWS[workflow_name]
        return workflow_func(**kwargs)
    except Exception as e:
        return {
            "workflow": workflow_name,
            "status": "failed",
            "error": str(e)
        }
