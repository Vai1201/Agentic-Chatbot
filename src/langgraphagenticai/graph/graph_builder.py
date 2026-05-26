from langgraph.graph import StateGraph, START, END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import ToolNode, tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, mode,l):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Build a chatbot graph using Langgraph.
        This method initiliazes a chatbot node using the BasicChatbotNode class and integrates it into the graph.
        The chatbot node is set as both the entry and exit point of the graph, allowing for a simple conversational flow.
        """
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        
        #Nodes
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """
        Build a chatbot with tools graph using Langgraph.
        This method initializes a chatbot node with tool integration and constructs a more complex graph to handle interactions that may require external tools or APIs.
        The graph is designed to manage the flow of information between the user, the chatbot, and any integrated tools, allowing for a richer conversational experience.
        """
        #Define the tool and tool node
        tools =  get_tools()
        tool_node = create_tool_node(tools)

        #Define the LLM
        llm=self.llm    

        #Define the chatbot node
        obj_chatbot_with_node =ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        #Add Nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        #Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def ai_news_builder_graph(self):
        """
        Build an AI news graph using Langgraph.
        This method initializes a chatbot node designed for fetching and presenting AI news, and constructs a graph that allows users to interact with the chatbot to receive news updates based on their selected time frame (daily, weekly, monthly).
        The graph manages the flow of information between the user and the chatbot, ensuring that the user receives relevant news updates in a conversational manner.
        """
        ai_news_node = AINewsNode(self.llm)

        #Adding the nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_results", ai_news_node.save_results)

        #Add Edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_results")
        self.graph_builder.add_edge("save_results", END)

    def setup_graph(self, usecase:str):
        """
        Set up the graph based on the selected use case.
        This method checks the selected use case and calls the corresponding graph building method to construct the graph accordingly.
        If an unsupported use case is selected, it raises a ValueError to inform the user.
        """
        if usecase=="Chatbot":
            self.basic_chatbot_build_graph()

        elif usecase=="Chatbot with Tavily":
            self.chatbot_with_tools_build_graph()

        elif usecase=="AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()
