"""
Tools and utilities for the Research Assistant Agent
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

class ResearchTools:
    def __init__(self):
        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Please create a .env file with your OpenAI API key:\n"
                "OPENAI_API_KEY=your_api_key_here"
            )
        
        self.search_tool = DuckDuckGoSearchRun()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Using mini for cost efficiency
            temperature=0.1,
            max_tokens=2000,
            api_key=api_key  # Explicitly pass the API key
        )
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the web using DuckDuckGo and return structured results
        """
        try:
            # Get raw search results
            raw_results = self.search_tool.run(query)
            
            # Structure the results
            search_results = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results": raw_results,
                "status": "success"
            }
            
            return search_results
            
        except Exception as e:
            return {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results": f"Search failed: {str(e)}",
                "status": "error"
            }
    
    def call_llm(self, prompt: str) -> str:
        """
        Call the LLM with a prompt and return the response
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"LLM call failed: {str(e)}"
    
    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Try to parse LLM response as JSON, return dict or error info
        """
        try:
            
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {"error": "No JSON found in response", "raw_response": response}
                
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {str(e)}", "raw_response": response}
    
    def parse_list_response(self, response: str) -> List[str]:
        """
        Try to parse LLM response as a Python list
        """
        try:
            # Find list in the response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                list_str = response[start_idx:end_idx]
                return eval(list_str)  # Note: eval is used here for simplicity, use ast.literal_eval in production
            else:
                # Fallback: split by newlines and clean up
                lines = response.strip().split('\n')
                queries = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('Search'):
                        # Remove quotes and clean up
                        line = line.strip('"\'').strip()
                        if line:
                            queries.append(line)
                return queries[:5]  # Limit to 5 queries
                
        except Exception as e:
            return [f"Parse error: {str(e)}"]
    
    def save_report(self, report: str, topic: str) -> str:
        """
        Save the research report to a file
        """
        try:
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs/reports", exist_ok=True)
            
            # Create filename from topic
            filename = f"research_report_{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            filepath = os.path.join("outputs/reports", filename)
            
            # Save the report
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            return f"Report saved to: {filepath}"
            
        except Exception as e:
            return f"Failed to save report: {str(e)}"
    
    def log_state(self, state_name: str, state_data: Dict[str, Any]):
        """
        Simple logging for debugging
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n[{timestamp}] {state_name}")
        print("-" * 50)
        
        # Print key information from state
        if "topic" in state_data:
            print(f"Topic: {state_data['topic']}")
        if "iteration_count" in state_data:
            print(f"Iteration: {state_data['iteration_count']}")
        if "next_action" in state_data:
            print(f"Next Action: {state_data['next_action']}")
        
        print("-" * 50)