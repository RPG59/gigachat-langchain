from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_core.language_models import BaseChatModel
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


class Searcher:
    def __init__(self, llm: BaseChatModel, client: QdrantClient, embeddings):
        self.llm = llm
        self.client = client
        self.doc_store = Qdrant(self.client, "default", embeddings)

    def search(self, query: str):
        system_prompt = (
            "Используя данный контекст ответь на вопрос. "
            "Если не можешь дать ответ на вопрос, скажи #НЕ ЗНАЮ#. "
            "Используйте максимум три предложения и будьте краткими. "
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
        return chain.invoke({"input": query})
