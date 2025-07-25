"""
Research Assistant Agent using LangGraph
"""

from typing import Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from nodes import (
    query_planner,
    web_searcher,
    content_analyzer,
    synthesizer,
    report_generator,
    should_continue
)


class ResearchState(TypedDict):
    """State schema for the research agent"""
    topic: str
    search_queries: List[str]
    search_results: List[Dict[str, Any]]
    analyzed_content: List[Dict[str, Any]]
    synthesis: Dict[str, Any]
    final_report: str
    iteration_count: int
    next_action: str


class ResearchAssistantAgent:
    """
    Main Research Assistant Agent class
    """
    
    def __init__(self):
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
    
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow
        """
        # Create the state graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes (functions)
        workflow.add_node("plan_queries", query_planner)
        workflow.add_node("search", web_searcher)
        workflow.add_node("analyze", content_analyzer)
        workflow.add_node("synthesize", synthesizer)
        workflow.add_node("generate_report", report_generator)

        # Set entry point
        workflow.set_entry_point("plan_queries")

        # Add seqeutial edges
        workflow.add_edge("plan_queries", "search")
        workflow.add_edge("search", "analyze")
        workflow.add_edge("analyze", "synthesize")

        # Add conditional routing from synthasizer
        workflow.add_conditional_edges(
            "synthesize", should_continue,
            {
                "continue": "plan_queries",
                "finish": "generate_report"
            }
        )

        # End after report geneation
        workflow.add_edge("generate_report", END)

        return workflow

    def research(self, topic: str) -> Dict[str, Any]:
        """
        Conduct research on a given topic
        
        Args:
            topic (str): The research topic
            
        Returns:
            Dict[str, Any]: Final state with research results
        """
        print(f"\n🔍 Starting research on: {topic}")
        print("=" * 60)
        
        # Initialize state
        initial_state = {
            "topic": topic,
            "search_queries": [],
            "search_results": [],
            "analyzed_content": [],
            "synthesis": {},
            "final_report": "",
            "iteration_count": 0,
            "next_action": ""
        }

        # Run the workflow
        try:
            png_data = self.app.get_graph().draw_mermaid_png()
            final_state = self.app.invoke(initial_state)
            
            # Save to file
            with open("workflow.png", "wb") as f:
                f.write(png_data)
            
            print("\n✅ Research completed successfully!")
            print("=" * 60)
            
            return final_state
            
        except Exception as e:
            print(f"\n❌ Research failed: {str(e)}")
            return {"error": str(e)}


    def get_report(self, research_result: Dict[str, Any]) -> str:
        """
        Extract the final report from research results
        
        Args:
            research_result (Dict[str, Any]): Result from research() method
            
        Returns:
            str: The final research report
        """
        if "error" in research_result:
            return f"Research failed: {research_result['error']}"
        
        return research_result.get("final_report", "No report generated")

    def print_summary(self, research_result: Dict[str, Any]):
        """
        Print a summary of the research process
        
        Args:
            research_result (Dict[str, Any]): Result from research() method
        """
        if "error" in research_result:
            print(f"❌ Research failed: {research_result['error']}")
            return
        
        print("\n📊 RESEARCH SUMMARY")
        print("=" * 40)
        print(f"Topic: {research_result.get('topic', 'Unknown')}")
        print(f"Iterations: {research_result.get('iteration_count', 0)}")
        print(f"Queries executed: {len(research_result.get('search_queries', []))}")
        print(f"Sources analyzed: {len(research_result.get('analyzed_content', []))}")
        print(f"Report generated: {'✅' if research_result.get('final_report') else '❌'}")
        
        # Show queries used
        if research_result.get('search_queries'):
            print(f"\nSearch queries used:")
            for i, query in enumerate(research_result['search_queries'], 1):
                print(f"  {i}. {query}")


# Create a global instance
research_agent = ResearchAssistantAgent()
    