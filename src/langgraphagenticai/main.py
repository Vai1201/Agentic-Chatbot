import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, "src"))

def load_langgraph_agentic_app():

    """
    Loads and runs the LangGraph Agentic AI application using Streamlit. It initializes the UI, captures user selections for LLM and use cases, 
    and manages API key input for GROQ models. The function sets up the page configuration and handles user interactions to ensure a seamless 
    experience while using the application.
    """

    #Load UI
    ui=LoadStreamlitUI()
    user_inputs=ui.load_streamlitui()

    if not user_inputs:
        st.error("Failed to load user inputs. Please check the UI configuration.")
        return

    #Text input for user message
    if st.session_state.get("IsFetchButtonClicked",False):
        user_message = st.session_state.time_frame
    else:
        user_message = st.chat_input("Enter your message here...")

    if user_message:
        try:
            #Configure the LLMs
            obj_llm_config=GroqLLM(user_controls_input=user_inputs)
            model=obj_llm_config.get_llm_models()

            if not model:
                st.error("Failed to initialize the language model. Please check your API key and model selection.")
                return


            # Initialize and set up the graph based on the use case
            usecase=user_inputs.get("selected_usecase")

            if not usecase:
                st.error("No use case selected. Please select a use case to proceed.")
                return

            # Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error setting up the graph: {str(e)}")
                return

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return