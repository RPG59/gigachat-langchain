import os
import getpass

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain import VectorDBQA
from langchain.llms.fake import FakeListLLM
from langchain.embeddings import HuggingFaceEmbeddings
from llm import CustomLLM


def run_search():
    # responses = ["Action: Python REPL\nAction Input: print(2 + 2)", "Final Answer: 4"]
    # llm = FakeListLLM(responses=responses)

    # --qdrant load --

    # docs_path = '/home/rpg59/work/infra/docs/sections'
    llm = CustomLLM(n=10)
    # documents = []
    # text_splitter = CharacterTextSplitter()

    # for fileneame in os.listdir(docs_path):
    #     filepath = os.path.join(docs_path, fileneame)

    #     if os.path.isfile(filepath):
    #         documents += text_splitter.split_documents(TextLoader(filepath).load())

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    # doc_store = Qdrant.from_documents(documents, embeddings, location="127.0.0.1", collection_name="my_documents")

    # --qdrant load end --

    query = "Привет. Упал релиз на проверке info.json, хотя https://myUrl1/info.json https://myUrl2/info.json доступны"
    # query = "What are the benefits of using server components?"
    # query = "How streaming works?"
    # found_docs = doc_store.similarity_search(query)
    # found_docs = doc_store.similarity_search_with_score(query)
    # found_docs = doc_store.max_marginal_relevance_search(query, k=2, fetch_k=10)

    # print(found_docs)

    # doc_store = Qdrant.from_texts(

    # )

    client = QdrantClient()
    doc_store = Qdrant(client, "my_documents", embeddings)

    qa = VectorDBQA.from_chain_type(llm=llm, chain_type="stuff", vectorstore=doc_store)
    res = qa.run(query)
    return res


run_search()
