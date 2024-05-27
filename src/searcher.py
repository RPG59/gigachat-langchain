from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_core.language_models import BaseChatModel
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


class Searcher:
    not_found_answer = "#НЕ ЗНАЮ#"
    fallback_phrases = ["Не люблю менять тему разговора", "Что-то в вашем вопросе меня смущает",
                        "Как у нейросетевой языковой модели"]

    def __init__(self, llm: BaseChatModel, client: QdrantClient, embeddings):
        self.llm = llm
        self.client = client
        self.doc_store = Qdrant(self.client, "default", embeddings)

    def parse_answer(self, answer: str) -> str | None:
        for phrase in self.fallback_phrases:
            if phrase.lower() in answer.lower():
                return None

        if answer.startswith(self.not_found_answer):
            return None

        return answer

    def search(self, query: str) -> str | None:
        system_prompt = (
            "Используя данный контекст ответь на вопрос. "
            "Отвечай только на вопросы, которые относятся к определенному контексту. "
            f"Если тебя спросят о вопросе вне контекста, ответить {self.not_found_answer}. "
            "Используй максимум три предложения и будь кратким. "
            "Контекст: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        chain = create_retrieval_chain(self.doc_store.as_retriever(), question_answer_chain)

        return self.parse_answer(chain.invoke({"input": query}).get("answer"))
