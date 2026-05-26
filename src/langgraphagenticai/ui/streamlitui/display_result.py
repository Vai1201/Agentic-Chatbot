from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import streamlit as st


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def _get_human_message(self):
        if isinstance(self.user_message, HumanMessage):
            return self.user_message

        if isinstance(self.user_message, str):
            return HumanMessage(content=self.user_message)

        return HumanMessage(content=str(self.user_message))

    def display_result_on_ui(self):
        human_message = self._get_human_message()

        if self.usecase == "Chatbot":

            with st.chat_message("user"):
                st.write(human_message.content)

            for event in self.graph.stream({
                "messages": [human_message]
            }):
                for value in event.values():
                    messages = value.get("messages", [])

                    if not isinstance(messages, list):
                        messages = [messages]

                    for message in messages:
                        if isinstance(message, AIMessage) and message.content:
                            with st.chat_message("assistant"):
                                st.write(message.content)

        elif self.usecase == "Chatbot with Tavily":

            initial_state = {
                "messages": [human_message]
            }

            res = self.graph.invoke(initial_state)

            for message in res["messages"]:

                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)

                elif isinstance(message, ToolMessage):
                    with st.chat_message("assistant"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")

                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif self.usecase == "AI News":
            frequency = str(self.user_message)
            with st.spinner(f"Fetching  AI news and summarizing..."):
                result = self.graph.invoke({
                            "messages": [HumanMessage(content=frequency)]
                        })
                try:
                    #Read the markdown file
                    AI_NEWS_PATH =f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, 'r') as f:
                        markdown_content = f.read()

                    #Display the markdown content in Streamlit
                    st.markdown(markdown_content,unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error fetching or displaying AI news: {str(e)}")
                except FileNotFoundError:
                    st.error("Summary file not found. Please ensure the graph executed correctly and the file was created.")