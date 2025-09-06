"""
Basic example of using the Research Assistant Agents
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from agent import research_agent

def run_basic_example():
    """
    Run a basic research example
    """
    # Load environment variables
    load_dotenv()
    
    # Example research topics
    topics = [
        "Benefits of renewable energy",
        "Impact of remote work on productivity",
        "Latest developments in quantum computing"
    ]
    
    print("🚀 Running Basic Research Examples")
    print("=" * 50)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n📚 Example {i}: {topic}")
        print("-" * 40)
        
        try:
            # Conduct research
            result = research_agent.research(topic)
            
            # Print summary
            research_agent.print_summary(result)
            
            # Get and display report
            report = research_agent.get_report(result)
            print(f"\n📄 Report Preview (first 500 chars):")
            print(report[:500] + "..." if len(report) > 500 else report)
            
        except Exception as e:
            print(f"❌ Error in example {i}: {str(e)}")
        
        # Add separator between examples
        if i < len(topics):
            print("\n" + "="*50)
            input("Press Enter to continue to next example...")

if __name__ == "__main__":
    run_basic_example()
