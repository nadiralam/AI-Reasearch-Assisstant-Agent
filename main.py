"""
Main entry point for the Research Assistant Agent
"""

import os
from dotenv import load_dotenv
from agent import research_agent

def main():
    """
    Main function to run the research assistant
    """

    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    print("Research Assistant Agent")
    print("=" * 50)
    print("Enter a research topic, or 'quit' to exit")
    
    while True:
        # Get user input
        topic = input("\nResearch topic: ").strip()
        
        # Check for exit command
        if topic.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        # Validate input
        if not topic:
            print("Please enter a valid research topic")
            continue
        
        # Conduct research
        try:
            result = research_agent.research(topic)
            
            # Print summary
            research_agent.print_summary(result)
            
            # Show report
            report = research_agent.get_report(result)
            print(f"\nFINAL REPORT")
            print("=" * 50)
            print(report)
            
        except KeyboardInterrupt:
            print("\nResearch interrupted by user")
            break
            
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
        # Ask if user wants to continue
        continue_research = input("\nDo another research? (y/n): ").strip().lower()
        if continue_research not in ['y', 'yes']:
            break
    
    print("\nthanks for using Research Assistant Agent!")


def quick_research(topic: str):
    """
    Quick research function for programmatic use
    
    Args:
        topic (str): Research topic
        
    Returns:
        str: Research report
    """
    # Load environment variables
    load_dotenv()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OPENAI_API_KEY not found"
    
    # Conduct research
    result = research_agent.research(topic)
    return research_agent.get_report(result)


# Example usage
if __name__ == "__main__":
    # Run interactive mode
    main()
