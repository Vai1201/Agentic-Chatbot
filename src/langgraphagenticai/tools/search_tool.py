from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode



def get_tools():
    """
    Get the tools to be used in the chatbot with tool use case.
    """
    tools=[TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    Create a tool node for the chatbot with tool use case.
    This method initializes a ToolNode with the provided tools and returns it for integration into the graph.
    """
    tool_node=ToolNode(tools)
    return tool_node