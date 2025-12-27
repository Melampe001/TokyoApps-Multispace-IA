#!/usr/bin/env python3
"""
Yuki (❄️) - Test Engineering Specialist

Like pristine snow, Yuki ensures purity in code quality through comprehensive testing.
Expertise in:
- Unit testing
- Integration testing
- End-to-end testing
- Test automation

Model: OpenAI o3
Agent ID: yuki-002
"""

import os
import json
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, LLM


class YukiTestEngineer:
    """Test Engineering Specialist - Unit/Integration/E2E Testing"""
    
    AGENT_ID = "yuki-002"
    NAME = "Yuki"
    EMOJI = "❄️"
    
    def __init__(self, api_key: Optional[str] = None, model: str = "o3"):
        """
        Initialize Yuki the Test Engineering Specialist.
        
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
            temperature=0.2,  # Lower temperature for consistent test generation
            api_key=self.api_key
        )
        
        self.agent = Agent(
            role='Test Engineering Specialist',
            goal='Ensure comprehensive test coverage and quality assurance',
            backstory="""You are Yuki, a meticulous test engineering specialist. 
            Like the pristine snow that covers everything, you ensure complete test 
            coverage across all aspects of the codebase. With an analytical mind and 
            methodical approach, no bug escapes your careful examination. You believe 
            in test-driven development and that well-tested code is the foundation of 
            reliable software. Your tests are thorough, maintainable, and serve as 
            living documentation.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def generate_unit_tests(self, code: str, language: str = "python", framework: str = "pytest") -> Dict[str, Any]:
        """
        Generate comprehensive unit tests for given code.
        
        Args:
            code: Source code to test
            language: Programming language
            framework: Testing framework to use
            
        Returns:
            Dict with generated test code
        """
        description = f"""Generate comprehensive unit tests for this {language} code using {framework}.
        
        Code to test:
        ```{language}
        {code}
        ```
        
        Create tests that cover:
        1. **Happy path**: Normal execution with valid inputs
        2. **Edge cases**: Boundary values, empty inputs, special characters
        3. **Error cases**: Invalid inputs, exception handling
        4. **State changes**: Verify side effects and state transitions
        5. **Mocking**: Mock external dependencies properly
        
        Follow {framework} best practices:
        - Clear test names that describe what's being tested
        - Arrange-Act-Assert pattern
        - One assertion concept per test
        - Proper setup and teardown
        - Good test data fixtures
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output=f"""Complete {framework} test suite with:
            - Test class/module structure
            - All test cases with clear names
            - Fixtures and mocks
            - Assertions for expected behavior
            - Comments explaining complex test scenarios
            - Test coverage goals achieved"""
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
            "task_type": "generate_unit_tests",
            "result": str(result),
            "metadata": {
                "language": language,
                "framework": framework,
                "code_length": len(code)
            }
        }
    
    def generate_integration_tests(self, components: List[str], language: str = "python") -> Dict[str, Any]:
        """
        Generate integration tests for multiple components.
        
        Args:
            components: List of component descriptions to integrate
            language: Programming language
            
        Returns:
            Dict with integration test suite
        """
        components_desc = "\n".join([f"- {comp}" for comp in components])
        
        description = f"""Create integration tests for these {language} components:
        
        {components_desc}
        
        Focus on:
        1. **Component interactions**: How components work together
        2. **Data flow**: Verify data passes correctly between components
        3. **API contracts**: Ensure interfaces are respected
        4. **Error propagation**: Test how errors flow through the system
        5. **Transaction boundaries**: Database/external system interactions
        
        Use appropriate testing patterns:
        - Test doubles for external dependencies
        - Database transactions for test isolation
        - Proper cleanup between tests
        - Realistic test scenarios
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Integration test suite with:
            - Test scenarios covering component interactions
            - Setup and teardown for test environment
            - Mock configurations for external services
            - Data fixtures for realistic testing
            - Assertions verifying integration points
            - Documentation of test scenarios"""
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
            "task_type": "generate_integration_tests",
            "result": str(result),
            "metadata": {
                "language": language,
                "component_count": len(components)
            }
        }
    
    def generate_e2e_tests(self, user_stories: List[str], tool: str = "playwright") -> Dict[str, Any]:
        """
        Generate end-to-end tests from user stories.
        
        Args:
            user_stories: List of user story descriptions
            tool: E2E testing tool (playwright, selenium, cypress)
            
        Returns:
            Dict with E2E test suite
        """
        stories_desc = "\n".join([f"{i+1}. {story}" for i, story in enumerate(user_stories)])
        
        description = f"""Create end-to-end tests using {tool} for these user stories:
        
        {stories_desc}
        
        For each user story:
        1. **Setup**: Initialize test environment and test data
        2. **Navigation**: Simulate user navigation through the application
        3. **Interactions**: Click, type, select - all user actions
        4. **Assertions**: Verify UI state, data display, user feedback
        5. **Cleanup**: Reset state for next test
        
        Best practices:
        - Use page object pattern for maintainability
        - Reliable selectors (prefer test IDs over CSS)
        - Wait strategies for dynamic content
        - Screenshot on failure
        - Descriptive test names
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output=f"""Complete {tool} E2E test suite with:
            - Page object models
            - Test cases for each user story
            - Proper wait strategies
            - Error handling and recovery
            - Test data management
            - Configuration for different environments"""
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
            "task_type": "generate_e2e_tests",
            "result": str(result),
            "metadata": {
                "tool": tool,
                "story_count": len(user_stories)
            }
        }
    
    def analyze_test_coverage(self, code: str, tests: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze test coverage and suggest improvements.
        
        Args:
            code: Source code being tested
            tests: Existing test code
            language: Programming language
            
        Returns:
            Dict with coverage analysis and recommendations
        """
        description = f"""Analyze test coverage for this {language} code.
        
        Source code:
        ```{language}
        {code}
        ```
        
        Existing tests:
        ```{language}
        {tests}
        ```
        
        Provide:
        1. **Coverage analysis**: What's tested, what's not
        2. **Missing tests**: Specific scenarios not covered
        3. **Test quality**: Are tests effective and maintainable?
        4. **Recommendations**: Prioritized list of tests to add
        5. **Test improvements**: How to enhance existing tests
        """
        
        task = Task(
            description=description,
            agent=self.agent,
            expected_output="""Coverage analysis report with:
            - Coverage percentage estimation
            - List of untested code paths
            - Missing edge cases
            - Test quality assessment
            - Prioritized recommendations
            - Sample tests for critical gaps"""
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
            "task_type": "analyze_test_coverage",
            "result": str(result),
            "metadata": {
                "language": language,
                "code_length": len(code),
                "test_length": len(tests)
            }
        }


def main():
    """Example usage of Yuki Test Engineer."""
    print("❄️ Initializing Yuki - Test Engineering Specialist...")
    
    # Example code to test
    example_code = '''
def calculate_discount(price, discount_percent):
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
'''
    
    try:
        engineer = YukiTestEngineer()
        
        print("\n=== Generating Unit Tests ===")
        test_result = engineer.generate_unit_tests(example_code, "python", "pytest")
        print(json.dumps(test_result, indent=2))
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set OPENAI_API_KEY environment variable")


if __name__ == "__main__":
    main()
