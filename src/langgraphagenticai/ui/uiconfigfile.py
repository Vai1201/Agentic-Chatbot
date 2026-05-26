from configparser import ConfigParser

class Config:
    def __init__(self, config_file='uiconfigfile.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self):
        return self.config['DEFAULT'].get('PAGE_TITLE', '🤖 LangGraph: Stateful Agentic AI for News, Chatbot, and Blog Generator')

    def get_llm_options(self):
        options = self.config['DEFAULT'].get('LLM_OPTIONS', 'Groq')
        return [option.strip() for option in options.split(',')]

    def get_usecase_options(self):
        options = self.config['DEFAULT'].get('USECASE_OPTIONS', 'Chatbot, Chatbot with Tavily, AI News, Blog Generator')
        return [option.strip() for option in options.split(',')]

    def get_groq_model_options(self):
        options = self.config['DEFAULT'].get('GROQ_MODEL_OPTIONS', 'llama-3.3-70b-versatile, llama-3.1-8b-instant, qwen/qwen3-32b')
        return [option.strip() for option in options.split(',')]