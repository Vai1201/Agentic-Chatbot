from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os

class AINewsNode:
    def __init__(self, llm):
        """
        Initializes the AINewsNode with the provided API key for Tavily and Groq.
        """

        self.travily = TavilyClient()
        self.llm = llm

        #this is used to capture various steps in this file so that later can be use for steps shown

        self.state = {}

    
    def fetch_news(self, state:dict) -> dict:
        """
        Fetch AI news based on the user's selected time frame (daily, weekly, monthly) using the Tavily API.

        Args:
            state (dict): A dictionary containing the current state of the conversation, including the user's selected time frame.

        Returns:
            dict: A dictionary containing the fetched news articles and any relevant information to be used in the conversation.
        """

        # Assuming the time frame is provided in the first message
        message = state["messages"][0]

        if hasattr(message, "content"):
            frequency = message.content.lower()
        else:
            frequency = str(message).lower()

        self.state['frequency'] = frequency
        time_range_map = {
            'daily': 'd',
            'weekly': 'w',
            'monthly': 'm',
            'yearly': 'y'
        }

        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 366}

        response = self.travily.search(
            query="Top Artificial Intelligence News India and Globally",
            topic="news",
            time_range=time_range_map.get(frequency),
            include_answer="advanced",
            max_results=20,
            days=days_map.get(frequency, 1)

            #Uncomment and add domains if needed
            #include_domains = ["techcrunch.com","thenextweb.com","wired.com","theverge.com","ai.googleblog.com","openai.com/blog"]
        )


        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state


    def summarize_news(self, state:dict) -> dict:
        """
        Summarize the fetched news articles using the LLM.

        Args:
            state (dict): A dictionary containing the current state of the conversation, including the fetched news articles.

        Returns:
            dict: A dictionary containing the summarized news information to be used in the conversation.
        """

        news_items = self.state['news_data']

        prompt = ChatPromptTemplate.from_messages([
            ("system", """ Summarize AI news articles into markdown format. For each item include:
            - Date in YYYY-MM-DD format in IST Timezone
            - Concise summary of the news (2-3 sentences)
            - Sort news based on date, with the most recent news first
            - Source url as link
            Use Format:
            ### [Date]
            - [Summary](URL)"""),
            ("user","Articles:\n{articles}")
        ])

        article_str = "\n\n".join([
            f"Content: {item.get('content','')}\nURL: {item.get('url','')}\nDate: {item.get('published_date','')}" 
            for item in news_items
        ])

        formatted_prompt = prompt.format_messages(articles=article_str)
        response = self.llm.invoke(formatted_prompt)

        state["summary"] = response.content
        self.state["summary"] = state["summary"]
        return state


    def save_results(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']

        # Create folder if it doesn't exist
        os.makedirs("./AINews", exist_ok=True)

        filename = f"./AINews/{frequency}_summary.md"

        with open(filename, 'w', encoding="utf-8") as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state['filename'] = filename

        return self.state
        