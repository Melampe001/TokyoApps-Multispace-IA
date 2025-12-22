#!/usr/bin/env python3
"""
Akira (侍) - Code Review Master

A disciplined samurai of code quality with expertise in:
- Security vulnerabilities detection
- Performance optimization analysis
- Architecture review
- Code quality assessment

Model: Claude Opus 4.1
Agent ID: akira-001
"""

import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, LLM


class AkiraCodeReviewer:
    """Code Review Master Agent - Security, Performance, Architecture"""
    
    AGENT_ID = "akira-001"
    NAME = "Akira"
    EMOJI = "侍"
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-opus-4.1"):
        """
        Initialize Akira the Code Review Master.
        
        Args:
            api_key: Anthropic API key (reads from ANTHROPIC_API_KEY if not provided)
            model: Claude model to use (default: claude-opus-4.1)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")
        
        self.model = model
        self.llm = LLM(
            model=f"anthropic/{model}",
            temperature=0.3,  # Lower temperature for more consistent reviews
            api_key=self.api_key
        )
        
        self.agent = Agent(
            role='Code Review Master',
            goal='Ensure code quality, security, and performance excellence',
            backstory="""You are Akira, a disciplined samurai of code quality. 
            With decades of experience in software craftsmanship, you have a keen 
            eye for security vulnerabilities, performance bottlenecks, and 
            architectural flaws. Every line of code is reviewed with the precision 
            of a master swordsman. You believe that code should not only work, but 
            be secure, efficient, and maintainable. Your reviews are thorough, 
            constructive, and always aimed at helping developers grow.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def review_code(self, code: str, language: str = "python", context: str = "") -> Dict[str, Any]:
        """
        Perform comprehensive code review.
        
        Args:
            code: Source code to review
            language: Programming language
            context: Additional context about the code
            
        Returns:
            Dict with review findings including security, performance, and quality issues
        """
        description = f"""Review the following {language} code for:
        
        1. **Security Issues**: Look for vulnerabilities, injection risks, authentication flaws
        2. **Performance Problems**: Identify inefficiencies, memory leaks, algorithmic issues
        3. **Code Quality**: Check readability, maintainability, best practices
        4. **Architecture**: Assess design patterns, structure, scalability
        
        Context: {context if context else 'No additional context provided'}
        
        Code to review:
        ```{language}
        {code}
        ```
        
        Provide a detailed review with specific recommendations for each issue found.
        Rate severity as: CRITICAL, HIGH, MEDIUM, LOW.
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""A structured code review with:
            - Summary of findings
            - Security issues (if any) with severity ratings
            - Performance concerns with optimization suggestions
            - Code quality improvements
            - Architectural recommendations
            - Overall assessment and rating"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "code_review",
            "result": str(result),
            "metadata": {
                "language": language,
                "code_length": len(code),
                "has_context": bool(context)
            }
        }
    
    def security_audit(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Focused security audit of code.
        
        Args:
            code: Source code to audit
            language: Programming language
            
        Returns:
            Dict with security findings
        """
        description = f"""Perform a security audit on this {language} code.
        
        Focus specifically on:
        - SQL Injection vulnerabilities
        - XSS (Cross-Site Scripting) risks
        - Authentication and authorization flaws
        - Insecure data handling
        - Cryptographic weaknesses
        - Dependency vulnerabilities
        - Input validation issues
        
        Code:
        ```{language}
        {code}
        ```
        
        For each security issue found:
        1. Identify the vulnerability type
        2. Explain the potential impact
        3. Provide secure code examples
        4. Rate severity (CRITICAL/HIGH/MEDIUM/LOW)
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""A security audit report with:
            - List of vulnerabilities found
            - Severity ratings
            - Exploitation scenarios
            - Remediation steps
            - Secure coding recommendations"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "security_audit",
            "result": str(result),
            "metadata": {
                "language": language,
                "code_length": len(code)
            }
        }
    
    def performance_analysis(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code for performance issues.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Dict with performance analysis
        """
        description = f"""Analyze this {language} code for performance issues.
        
        Look for:
        - Algorithm efficiency (Big O complexity)
        - Memory usage patterns
        - Unnecessary computations
        - Database query optimization
        - Network call efficiency
        - Caching opportunities
        - Concurrency issues
        
        Code:
        ```{language}
        {code}
        ```
        
        Provide specific optimization recommendations with code examples.
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Performance analysis with:
            - Identified bottlenecks
            - Complexity analysis
            - Memory usage concerns
            - Optimization recommendations with code examples
            - Expected performance improvements"""
        )
        
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "agent_id": self.AGENT_ID,
            "agent_name": self.NAME,
            "task_type": "performance_analysis",
            "result": str(result),
            "metadata": {
                "language": language,
                "code_length": len(code)
            }
        }


def main():
    """Example usage of Akira Code Reviewer."""
    print(f"侍 Initializing Akira - Code Review Master...")
    
    # Example code to review
    example_code = '''
def process_user_input(user_id, data):
    # Get user from database
    query = f"SELECT * FROM users WHERE id = {user_id}"
    user = db.execute(query)
    
    # Process data
    result = []
    for item in data:
        result.append(item * 2)
    
    return result
'''
    
    try:
        reviewer = AkiraCodeReviewer()
        
        print("\n=== Security Audit ===")
        security_result = reviewer.security_audit(example_code, "python")
        print(json.dumps(security_result, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")


if __name__ == "__main__":
    main()
