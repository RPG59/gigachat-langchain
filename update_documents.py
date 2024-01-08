from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from outline import Outline

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]


def update_documents(outline: Outline, qdrant_url: str, client: QdrantClient):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    documents = outline.get_documents()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    splits = []

    for document in documents:
        splits.extend(splitter.split_text(document))

    client.delete_collection("default")
    Qdrant.from_documents(splits, embeddings, url=qdrant_url, collection_name="default")
