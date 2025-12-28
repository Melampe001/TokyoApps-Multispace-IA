#!/usr/bin/env python3
"""
Kenji (🏗️) - Architecture Visionary

A master architect who sees the grand design in every system.
Expertise in:
- System design
- Software architecture
- Design patterns
- Scalability planning

Model: OpenAI o3
Agent ID: kenji-005
"""

import os
import json
from typing import Dict, Any, Optional
from crewai import Agent, Task, Crew, LLM


class KenjiArchitect:
    """Architecture Visionary - System Design, Patterns, Scalability"""
    
    AGENT_ID = "kenji-005"
    NAME = "Kenji"
    EMOJI = "🏗️"
    
    def __init__(self, api_key: Optional[str] = None, model: str = "o3"):
        """
        Initialize Kenji the Architecture Visionary.
        
        Args:
            api_key: OpenAI API key (reads from OPENAI_API_KEY if not provided)
            model: OpenAI model to use (default: o3)
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set")
        
        self.model = model
        self.llm = LLM(
            model=f"openai/{model}",
            temperature=0.4,  # Balanced for creative yet structured thinking
            api_key=self.api_key
        )
        
        self.agent = Agent(
            role='Architecture Visionary',
            goal='Design elegant, scalable, and maintainable system architectures',
            backstory="""You are Kenji, a master architect who sees the grand 
            design in every system. With wisdom gained from building countless 
            systems, you plan with consideration for scalability, maintainability, 
            and elegance. You understand that great architecture is not about 
            complexity, but about finding the simplest solution that solves the 
            problem while anticipating future needs. You consider trade-offs, 
            evaluate alternatives, and make decisions based on context and 
            requirements. Your designs are both practical and forward-thinking.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def design_system_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design comprehensive system architecture.
        
        Args:
            requirements: System requirements and constraints
            
        Returns:
            Dict with architecture design
        """
        req_json = json.dumps(requirements, indent=2)
        
        description = f"""Design a comprehensive system architecture for:
        
        Requirements:
        {req_json}
        
        Provide:
        1. **High-level architecture**: Overall system structure
        2. **Component design**: Each major component with responsibilities
        3. **Data architecture**: Data models, storage, and flow
        4. **API design**: Interface contracts between components
        5. **Technology stack**: Recommended technologies with justification
        6. **Scalability strategy**: How system scales (vertical/horizontal)
        7. **Deployment architecture**: Infrastructure and orchestration
        8. **Security architecture**: Authentication, authorization, data protection
        9. **Monitoring and observability**: Logging, metrics, tracing
        10. **Trade-offs and alternatives**: Decisions made and why
        
        Consider:
        - Performance requirements
        - Scalability needs
        - Reliability and availability
        - Maintainability
        - Cost constraints
        - Team expertise
        - Time to market
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete architecture design with:
            - System diagram (Mermaid/PlantUML)
            - Component descriptions
            - Data architecture
            - API contracts
            - Technology recommendations
            - Scalability plan
            - Security design
            - Deployment strategy
            - Trade-off analysis
            - Implementation roadmap"""
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
            "task_type": "design_system_architecture",
            "result": str(result),
            "metadata": requirements
        }
    
    def recommend_design_patterns(self, problem_description: str, language: str = "python") -> Dict[str, Any]:
        """
        Recommend appropriate design patterns for a problem.
        
        Args:
            problem_description: Description of the design problem
            language: Programming language context
            
        Returns:
            Dict with pattern recommendations
        """
        description = f"""Recommend design patterns for this {language} problem:
        
        Problem:
        {problem_description}
        
        For each recommended pattern:
        1. **Pattern name**: Creational, Structural, or Behavioral
        2. **Why it fits**: How it solves the problem
        3. **Implementation**: Code example in {language}
        4. **Benefits**: Advantages of using this pattern
        5. **Trade-offs**: Potential drawbacks
        6. **When to use**: Appropriate scenarios
        7. **When not to use**: Anti-patterns and pitfalls
        8. **Related patterns**: Patterns that work well together
        
        Consider:
        - SOLID principles
        - Code reusability
        - Flexibility and extensibility
        - Testability
        - Complexity vs. benefit
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output=f"""Design pattern recommendations with:
            - Primary pattern recommendation
            - Alternative patterns
            - Code examples in {language}
            - Benefit/trade-off analysis
            - Usage guidelines
            - Anti-pattern warnings
            - Integration with other patterns"""
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
            "task_type": "recommend_design_patterns",
            "result": str(result),
            "metadata": {
                "language": language,
                "problem_length": len(problem_description)
            }
        }
    
    def review_architecture(self, architecture_doc: str) -> Dict[str, Any]:
        """
        Review existing architecture and provide feedback.
        
        Args:
            architecture_doc: Architecture documentation to review
            
        Returns:
            Dict with review feedback
        """
        description = f"""Review this architecture design:
        
        {architecture_doc}
        
        Evaluate:
        1. **Clarity**: Is the design clear and well-documented?
        2. **Scalability**: Can it handle growth?
        3. **Reliability**: Is it fault-tolerant?
        4. **Performance**: Will it meet performance requirements?
        5. **Security**: Are security concerns addressed?
        6. **Maintainability**: Is it easy to modify and extend?
        7. **Cost efficiency**: Is it cost-effective?
        8. **Technology choices**: Are they appropriate?
        
        Provide:
        - Strengths of the design
        - Potential issues and risks
        - Improvement recommendations
        - Alternative approaches
        - Questions to clarify requirements
        - Rating (Excellent/Good/Needs Work/Poor)
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Architecture review with:
            - Summary assessment
            - Strengths highlighted
            - Issues identified with severity
            - Specific recommendations
            - Alternative designs considered
            - Risk analysis
            - Overall rating with justification"""
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
            "task_type": "review_architecture",
            "result": str(result),
            "metadata": {
                "doc_length": len(architecture_doc)
            }
        }
    
    def plan_refactoring(self, codebase_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Plan architectural refactoring for existing codebase.
        
        Args:
            codebase_info: Information about current codebase
            
        Returns:
            Dict with refactoring plan
        """
        info_json = json.dumps(codebase_info, indent=2)
        
        description = f"""Plan architectural refactoring for this codebase:
        
        {info_json}
        
        Create a refactoring plan that addresses:
        1. **Current issues**: Technical debt and pain points
        2. **Target architecture**: Desired end state
        3. **Migration strategy**: How to get there safely
        4. **Phased approach**: Break down into manageable phases
        5. **Risk mitigation**: How to minimize disruption
        6. **Testing strategy**: Ensure nothing breaks
        7. **Rollback plan**: What if something goes wrong
        8. **Team coordination**: How to coordinate across team
        
        For each phase:
        - Goals and scope
        - Estimated effort
        - Dependencies and prerequisites
        - Success criteria
        - Rollout strategy
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Refactoring plan with:
            - Current state analysis
            - Target architecture vision
            - Phased migration plan
            - Risk assessment per phase
            - Testing strategy
            - Rollback procedures
            - Success metrics
            - Timeline estimate
            - Resource requirements"""
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
            "task_type": "plan_refactoring",
            "result": str(result),
            "metadata": codebase_info
        }
    
    def design_microservices(self, monolith_description: str) -> Dict[str, Any]:
        """
        Design microservices architecture from monolith.
        
        Args:
            monolith_description: Description of current monolithic application
            
        Returns:
            Dict with microservices design
        """
        description = f"""Design a microservices architecture from this monolith:
        
        {monolith_description}
        
        Provide:
        1. **Service boundaries**: How to decompose the monolith
        2. **Service definitions**: Each microservice with:
           - Responsibilities
           - Data ownership
           - API contracts
           - Dependencies
        3. **Communication patterns**: Sync/async, protocols
        4. **Data management**: Database per service, shared data
        5. **Service discovery**: How services find each other
        6. **API gateway**: External access pattern
        7. **Deployment strategy**: Containers, orchestration
        8. **Migration path**: Strangler pattern or big bang
        
        Consider:
        - Domain-driven design principles
        - Bounded contexts
        - Service independence
        - Data consistency (eventual vs. strong)
        - Observability across services
        - Failure handling and resilience
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Microservices architecture with:
            - Service decomposition diagram
            - Service definitions and boundaries
            - Inter-service communication
            - Data architecture per service
            - API gateway design
            - Service mesh considerations
            - Migration strategy
            - Operational concerns
            - Trade-offs vs. monolith"""
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
            "task_type": "design_microservices",
            "result": str(result),
            "metadata": {
                "description_length": len(monolith_description)
            }
        }


def main():
    """Example usage of Kenji Architect."""
    print("🏗️ Initializing Kenji - Architecture Visionary...")
    
    # Example system requirements
    requirements = {
        "name": "E-commerce Platform",
        "users": "1M+ concurrent",
        "features": ["product catalog", "shopping cart", "payments", "recommendations"],
        "constraints": ["high availability", "low latency", "GDPR compliant"],
        "scale": "global"
    }
    
    try:
        architect = KenjiArchitect()
        
        print("\n=== System Architecture Design ===")
        arch_result = architect.design_system_architecture(requirements)
        print(json.dumps(arch_result, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set OPENAI_API_KEY environment variable")


if __name__ == "__main__":
    main()
