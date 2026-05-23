from src.langgraphagenticai.state.state import State


class ChatbotWithToolNode:
    """
    A chatbot node that integrates tool usage for a conversational agent graph.
    This node is designed to handle interactions that may require external tools or APIs, allowing for a richer conversational experience.
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Process the input state and generate a response using the language model and integrated tools.
        The method first checks if the input requires tool usage based on the defined condition. If so, it processes the tool node; otherwise, it generates a response using the language model.
        """
        user_input = state["messages"][-1].content if state["messages"] else "" # Assuming the latest message is the user input
        #llm_response = self.llm.invoke([{"role": "user", "content": user_input}])
        llm_response = self.llm.invoke(state["messages"])

        # Simulate tool-specific logic
        tools_response = f"Tool integration for input: '{user_input}'"

        return {
            #"messages": [llm_response, tools_response]
            "messages": [llm_response]
        }

    def create_chatbot(self, tools):
        """
        Create a chatbot node with tool integration.
        This method initializes the chatbot node with the provided tools and returns it for integration into the graph.
        """
        # Logic to integrate tools can be added here
        llm_with_tools = self.llm.bind_tools(tools)  # Hypothetical method to bind tools to the LLM

        def chatbot_node(state: State):
            """
            Chatbot node function that processes the state and generates a response using the LLM with tool integration.
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node

