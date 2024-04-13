from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate


class ReviewManager:
    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def review(self, code: str, language: str) -> str:
        prompt = PromptTemplate.from_template(
            "I'm working on a {language} project and I need you to review my code and suggest improvements. {code}")

        return self.llm.invoke(prompt.format(language=language, code=code)).content
