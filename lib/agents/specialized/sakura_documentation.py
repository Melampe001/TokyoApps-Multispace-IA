#!/usr/bin/env python3
"""
Sakura (🌸) - Documentation Artist

Like cherry blossoms bringing beauty to spring, Sakura transforms complex 
technical concepts into elegant, understandable documentation.

Expertise in:
- Technical writing
- API documentation
- Architecture diagrams
- User guides

Model: Gemini 3.0 Ultra
Agent ID: sakura-004
"""

import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, LLM


class SakuraDocumentation:
    """Documentation Artist - Technical Writing, Diagrams, API Docs"""
    
    AGENT_ID = "sakura-004"
    NAME = "Sakura"
    EMOJI = "🌸"
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-3.0-ultra"):
        """
        Initialize Sakura the Documentation Artist.
        
        Args:
            api_key: Google API key (reads from GOOGLE_API_KEY if not provided)
            model: Gemini model to use (default: gemini-3.0-ultra, fallback: gemini-pro)
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set")
        
        # Fallback to available model
        self.model = "google/gemini-pro"
        self.llm = LLM(
            model=self.model,
            temperature=0.7,  # Creative but consistent
            api_key=self.api_key
        )
        
        self.agent = Agent(
            role='Documentation Artist',
            goal='Create beautiful, clear, and comprehensive documentation',
            backstory="""You are Sakura, a documentation artist who brings beauty 
            and clarity to technical writing. Like cherry blossoms that make spring 
            beautiful, you transform complex technical concepts into elegant, 
            understandable documentation. Every word is carefully chosen, every 
            diagram thoughtfully crafted. You believe documentation is not just 
            explaining how something works, but making readers excited to use it. 
            Your writing is clear, engaging, and accessible to all skill levels.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_api_documentation(self, api_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive API documentation.
        
        Args:
            api_spec: API specification (endpoints, methods, parameters)
            
        Returns:
            Dict with formatted API documentation
        """
        spec_json = json.dumps(api_spec, indent=2)
        
        description = f"""Create beautiful, comprehensive API documentation:
        
        API Specification:
        {spec_json}
        
        Include:
        1. **Overview**: What the API does and who should use it
        2. **Authentication**: How to authenticate requests
        3. **Endpoints**: Each endpoint with:
           - HTTP method and path
           - Description and use cases
           - Request parameters (path, query, body)
           - Request examples (curl, JavaScript, Python)
           - Response format and status codes
           - Response examples (success and error)
           - Rate limiting information
        4. **Error handling**: Common errors and solutions
        5. **SDKs and libraries**: If available
        6. **Quick start guide**: Get developers started quickly
        7. **Code examples**: Realistic usage scenarios
        
        Use markdown format with:
        - Clear headings and sections
        - Code blocks with syntax highlighting
        - Tables for parameters
        - Emoji for visual appeal
        - Best practices and tips
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete API documentation in markdown with:
            - Well-structured sections
            - Clear explanations for all endpoints
            - Multiple code examples per endpoint
            - Error handling guide
            - Quick start tutorial
            - Best practices section
            - Troubleshooting guide"""
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
            "task_type": "generate_api_documentation",
            "result": str(result),
            "metadata": {
                "endpoint_count": len(api_spec.get("endpoints", []))
            }
        }
    
    def create_user_guide(self, product_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create user-friendly guide for a product or feature.
        
        Args:
            product_info: Product information (features, use cases, target audience)
            
        Returns:
            Dict with user guide
        """
        info_json = json.dumps(product_info, indent=2)
        
        description = f"""Create an engaging user guide for this product:
        
        {info_json}
        
        Structure:
        1. **Introduction**: What is it and why use it?
        2. **Getting started**: Quick setup guide
        3. **Core features**: Main functionality with examples
        4. **Common tasks**: Step-by-step tutorials
        5. **Advanced usage**: Power user features
        6. **Tips and tricks**: Best practices
        7. **Troubleshooting**: Common issues and solutions
        8. **FAQ**: Frequently asked questions
        
        Writing style:
        - Clear and conversational
        - Use analogies and examples
        - Include screenshots placeholders
        - Progressive disclosure (simple to complex)
        - Encourage and motivate users
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""User guide with:
            - Engaging introduction
            - Step-by-step tutorials
            - Visual placeholders for screenshots
            - Real-world examples
            - Tips boxes and warnings
            - Comprehensive FAQ
            - Easy navigation structure"""
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
            "task_type": "create_user_guide",
            "result": str(result),
            "metadata": {
                "product_name": product_info.get("name", "unknown")
            }
        }
    
    def document_architecture(self, system_description: str, components: List[str]) -> Dict[str, Any]:
        """
        Create architecture documentation with diagrams.
        
        Args:
            system_description: High-level system description
            components: List of system components
            
        Returns:
            Dict with architecture documentation
        """
        components_list = "\n".join([f"- {comp}" for comp in components])
        
        description = f"""Create comprehensive architecture documentation:
        
        System: {system_description}
        
        Components:
        {components_list}
        
        Document:
        1. **Architecture overview**: High-level design and principles
        2. **System context**: How system fits in larger ecosystem
        3. **Component descriptions**: Each component's responsibility
        4. **Data flow**: How data moves through the system
        5. **Integration points**: External systems and APIs
        6. **Deployment architecture**: How it's deployed
        7. **Security architecture**: Security measures
        8. **Scalability considerations**: How system scales
        
        Include diagram descriptions in:
        - Mermaid syntax for flowcharts
        - PlantUML for sequence diagrams
        - C4 model for architecture views
        
        Explain:
        - Why decisions were made (ADRs style)
        - Trade-offs and alternatives considered
        - Future evolution path
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Architecture documentation with:
            - System overview and context
            - Component descriptions
            - Mermaid/PlantUML diagram definitions
            - Data flow explanations
            - Integration documentation
            - Security overview
            - Scalability design
            - ADRs for key decisions"""
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
            "task_type": "document_architecture",
            "result": str(result),
            "metadata": {
                "component_count": len(components)
            }
        }
    
    def create_readme(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an awesome README.md for a project.
        
        Args:
            project_info: Project information
            
        Returns:
            Dict with README content
        """
        info_json = json.dumps(project_info, indent=2)
        
        description = f"""Create an awesome README.md for this project:
        
        {info_json}
        
        Include:
        1. **Project title and badges**: Status, version, license
        2. **Description**: What it does, why it exists
        3. **Features**: Key features with emojis
        4. **Demo**: Screenshots/GIFs/video links
        5. **Installation**: Quick start steps
        6. **Usage**: Basic examples
        7. **Documentation**: Links to detailed docs
        8. **Contributing**: How to contribute
        9. **License**: License information
        10. **Credits**: Acknowledgments
        
        Make it:
        - Visually appealing with emojis and badges
        - Easy to scan (headers, lists, code blocks)
        - Informative but concise
        - Encouraging for contributors
        - Professional yet friendly
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Complete README.md with:
            - Compelling title and badges
            - Clear project description
            - Installation instructions
            - Usage examples
            - Contribution guidelines
            - Proper markdown formatting
            - Visual appeal with emojis
            - All standard sections"""
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
            "task_type": "create_readme",
            "result": str(result),
            "metadata": {
                "project_name": project_info.get("name", "unknown")
            }
        }


def main():
    """Example usage of Sakura Documentation Artist."""
    print(f"🌸 Initializing Sakura - Documentation Artist...")
    
    # Example API spec
    api_spec = {
        "name": "Tokyo-IA Registry API",
        "base_url": "https://api.tokyo-ia.com",
        "authentication": "API Key",
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/agents",
                "description": "List all agents"
            },
            {
                "method": "POST",
                "path": "/api/tasks",
                "description": "Create a new task"
            }
        ]
    }
    
    try:
        documenter = SakuraDocumentation()
        
        print("\n=== API Documentation ===")
        doc_result = documenter.generate_api_documentation(api_spec)
        print(json.dumps(doc_result, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set GOOGLE_API_KEY environment variable")


if __name__ == "__main__":
    main()
