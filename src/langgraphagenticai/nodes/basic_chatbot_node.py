from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    A basic chatbot node for a conversational agent graph.
    """

    def __init__(self, model):
        self.llm = model

    def process(self,state:State) -> dict:
        """
        Process the input state and generate a response using the language model.
        """
        return {"messages": self.llm.invoke(state["messages"])}
