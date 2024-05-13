import logging

from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from outline import Outline
from langchain_text_splitters import RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

logger = logging.getLogger("Updater")


def update_documents(outline: Outline, qdrant_url: str, client: QdrantClient, embeddings):
    logger.info("Start updating documents")

    documents = outline.get_documents()
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    chunk_size = 800
    chunk_overlap = 200
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    splits = []

    for document in documents:
        splits.extend(text_splitter.split_documents(splitter.split_text(document)))

    client.delete_collection("default")
    Qdrant.from_documents(splits, embeddings, url=qdrant_url, collection_name="default")
