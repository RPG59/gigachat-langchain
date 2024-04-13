from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import GigaChat

class Searcher:
    def __init__(self):
        self.llm = GigaChat(verify_ssl_certs=False)

    def search(self, code: str):
        prompt = PromptTemplate.from_template(
            "I'm working on a {language} project and I need you to review my code and suggest improvements. {code}")
        return self.llm.invoke(prompt.format(language='typescript', code=code))
