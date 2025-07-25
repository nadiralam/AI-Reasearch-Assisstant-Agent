"""
Node functions for the Research Assistant Agent
"""

from typing import Dict, Any
from tools import ResearchTools
from prompts import (
    QUERY_PLANNING_PROMPT,
    CONTENT_ANALYSIS_PROMPT,
    SYNTHESIS_PROMPT,
    REPORT_GENERATION_PROMPT
)

# Initialize tools
tools = ResearchTools()


def query_planner(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate focused search queries from the research topic
    """
    tools.log_state("QUERY PLANNER", state)
    
    topic = state["topic"]
    iteration = state.get("iteration_count", 0)
    
    # Create prompt
    prompt = QUERY_PLANNING_PROMPT.format(topic=topic)
    
    # If this is a follow-up iteration, consider previous findings
    if iteration > 0 and state.get("analyzed_content"):
        prompt += f"\n\nPrevious research findings to build upon:\n{state['analyzed_content'][-1]}"
    
    # Get LLM response
    response = tools.call_llm(prompt)
    
    # Parse the queries
    search_queries = tools.parse_list_response(response)
    
    # Update state
    state["search_queries"] = search_queries
    state["next_action"] = "search"
    
    print(f"Generated {len(search_queries)} search queries: {search_queries}")
    
    return state


def web_searcher(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute searches and collect results
    """
    tools.log_state("WEB SEARCHER", state)
    
    search_queries = state["search_queries"]
    search_results = []
    
    # Execute each search query
    for query in search_queries:
        print(f"Searching for: {query}")
        result = tools.search_web(query)
        search_results.append(result)
    
    # Update state
    state["search_results"] = search_results
    state["next_action"] = "analyze"
    
    print(f"Completed {len(search_results)} searches")
    
    return state


def content_analyzer(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze search results and extract key information
    """
    tools.log_state("CONTENT ANALYZER", state)
    
    search_results = state["search_results"]
    analyzed_content = state.get("analyzed_content", [])
    
    # Analyze each search result
    for result in search_results:
        if result["status"] == "success":
            query = result["query"]
            results = result["results"]
            
            # Create analysis prompt
            prompt = CONTENT_ANALYSIS_PROMPT.format(
                query=query,
                results=results
            )
            
            # Get LLM analysis
            response = tools.call_llm(prompt)
            
            # Parse JSON response
            analysis = tools.parse_json_response(response)
            analysis["query"] = query  # Add the query for reference
            
            analyzed_content.append(analysis)
            
            print(f"Analyzed content for query: {query}")
    
    # Update state
    state["analyzed_content"] = analyzed_content
    state["next_action"] = "synthesize"
    
    return state


def synthesizer(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesize information and decide next steps
    """
    tools.log_state("SYNTHESIZER", state)
    
    topic = state["topic"]
    analyzed_content = state["analyzed_content"]
    iteration = state.get("iteration_count", 0)
    
    # Create synthesis prompt
    prompt = SYNTHESIS_PROMPT.format(
        topic=topic,
        analyzed_content=analyzed_content,
        iteration=iteration
    )
    
    # Get LLM synthesis
    response = tools.call_llm(prompt)
    
    # Parse JSON response
    synthesis = tools.parse_json_response(response)
    
    # Update iteration count
    state["iteration_count"] = iteration + 1
    
    # Determine next action based on synthesis
    if (synthesis.get("research_quality") == "sufficient" or 
        synthesis.get("confidence_level", 0) > 7 or 
        iteration >= 2):  # Max 3 iterations (0, 1, 2)
        state["next_action"] = "generate_report"
        print("Research is sufficient. Moving to report generation.")
    else:
        state["next_action"] = "continue_research"
        print("Research needs more information. Continuing research.")
    
    # Store synthesis results
    state["synthesis"] = synthesis
    
    return state


def report_generator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate the final research report
    """
    tools.log_state("REPORT GENERATOR", state)
    
    topic = state["topic"]
    analyzed_content = state["analyzed_content"]
    
    # Create report generation prompt
    prompt = REPORT_GENERATION_PROMPT.format(
        topic=topic,
        analyzed_content=analyzed_content
    )
    
    # Generate report
    response = tools.call_llm(prompt)
    
    # Update state
    state["final_report"] = response
    state["next_action"] = "complete"
    
    # Save report to file
    save_result = tools.save_report(response, topic)
    print(f"Report generated! {save_result}")
    
    return state


def should_continue(state: Dict[str, Any]) -> str:
    """
    Conditional routing logic - decide whether to continue research or generate report
    """
    next_action = state.get("next_action", "")
    
    if next_action == "generate_report":
        return "finish"
    elif next_action == "continue_research":
        return "continue"
    else:
        # Default: continue if we haven't generated a report yet
        return "continue" if not state.get("final_report") else "finish"