from qdrant_client import QdrantClient
from langchain.chains import VectorDBQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.chat_models import GigaChat


class Searcher:
    def __init__(self, client: QdrantClient):
        self.llm = GigaChat(verify_ssl_certs=False)
        self.client = client

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        self.doc_store = Qdrant(self.client, "default", embeddings)

    def search(self, query: str):
        qa = VectorDBQA.from_chain_type(llm=self.llm, chain_type="stuff", vectorstore=self.doc_store)

        return qa.run(query)
