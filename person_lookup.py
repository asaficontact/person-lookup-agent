"""
PersonLookup Agent - A specialized agent for researching and compiling information about individuals.
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime

from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool
from jinja2 import Environment, FileSystemLoader


class PersonLookupAgent:
    """
    An AI agent that searches for information about individuals and creates comprehensive reports.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the PersonLookup agent.
        
        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY in environment.
        """
        # Load environment variables
        load_dotenv()
        
        # Set up API key
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        # Set the API key for the agents SDK
        os.environ['OPENAI_API_KEY'] = self.api_key
        
        # Load and render the prompt template
        self.prompt = self._load_prompt_template()
        
        # Initialize the web search tool
        self.web_search_tool = WebSearchTool()
        
        # Create the agent
        self.agent = Agent(
            name="PersonLookup",
            instructions=self.prompt,
            tools=[self.web_search_tool],
            model="gpt-4o-mini"  # Using a reliable model
        )
    
    def _load_prompt_template(self) -> str:
        """
        Load and render the Jinja2 prompt template.
        
        Returns:
            Rendered prompt string
        """
        try:
            # Set up Jinja2 environment
            env = Environment(loader=FileSystemLoader('prompts'))
            template = env.get_template('person_lookup_prompt.jinja2')
            
            # Render the template (you can pass variables here if needed)
            return template.render(
                current_date=datetime.now().strftime("%Y-%m-%d")
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt template: {e}")
    
    def lookup_person(self, query: str) -> Dict[str, Any]:
        """
        Look up information about a person based on the query.
        
        Args:
            query: Natural language query about the person to look up
            
        Returns:
            Dictionary containing the report and metadata
        """
        try:
            # Run the agent synchronously without messing with event loops
            result = Runner.run_sync(self.agent, query)
            
            # Extract the final report
            if result and hasattr(result, 'final_output'):
                return {
                    "success": True,
                    "report": result.final_output,
                    "timestamp": datetime.now().isoformat(),
                    "query": query
                }
            else:
                return {
                    "success": False,
                    "error": "No output generated",
                    "timestamp": datetime.now().isoformat(),
                    "query": query
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "query": query
            }
    
    def lookup_person_stream(self, query: str):
        """
        Look up information about a person with streaming response.
        
        Args:
            query: Natural language query about the person to look up
            
        Returns:
            Generator yielding chunks of the response
        """
        try:
            # Note: The SDK might support streaming differently
            # For now, we'll return the full result
            result = self.lookup_person(query)
            if result["success"]:
                yield result["report"]
            else:
                yield f"Error: {result['error']}"
                
        except Exception as e:
            yield f"Error: {str(e)}"


# Convenience function for simple usage
def lookup_person(query: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to look up a person without instantiating the class.
    
    Args:
        query: Natural language query about the person
        api_key: Optional OpenAI API key
        
    Returns:
        Dictionary containing the report and metadata
    """
    agent = PersonLookupAgent(api_key=api_key)
    return agent.lookup_person(query)


# Example usage
if __name__ == "__main__":
    def main():
        # Example queries
        queries = [
            "Tell me about Andrew Lippman",
            "Find information about Ada Lovelace, the mathematician",
            "Who is Satya Nadella and what are his recent achievements?"
        ]
        
        # Initialize the agent
        try:
            agent = PersonLookupAgent()
            print("✓ Agent initialized successfully\n")
            
            # Test with the first query
            print(f"Looking up: {queries[0]}")
            print("-" * 50)
            
            result = agent.lookup_person(queries[0])
            
            if result["success"]:
                print(result["report"])
                print(f"\n{'=' * 50}")
                print(f"Report generated at: {result['timestamp']}")
            else:
                print(f"Error: {result['error']}")
                
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("\nPlease make sure to:")
            print("1. Create a .env file in the project directory")
            print("2. Add your OpenAI API key: OPENAI_API_KEY=your_key_here")
            
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    # Run the example
    main()