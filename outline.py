import os
import validators
import requests


class Outline:
    def __init__(self):
        self.outline_token = os.getenv("OUTLINE_TOKEN")
        self.outline_collection_id = os.getenv("OUTLINE_COLLECTION_ID")
        self.outline_api_url = os.getenv("OUTLINE_API_URL")

        if self.outline_token is None:
            raise ValueError("Invalid OUTLINE_TOKEN")

        if self.outline_collection_id is None:
            raise ValueError("Invalid OUTLINE_COLLECTION_ID")

        if self.outline_api_url is None or not validators.url(self.outline_api_url):
            raise ValueError("Invalid OUTLINE_API_URL")

    def get_documents(self) -> list[str]:
        headers = {
            "Authorization": f"Bearer {self.outline_token}",
        }

        documents = []
        offset = 0
        limit = 10

        while True:
            body = {
                "collectionId": self.outline_collection_id,
                "limit": limit,
                "offset": offset
            }

            res = requests.post(f"{self.outline_api_url}/documents.list", body, headers=headers).json()
            data = res['data']
            documents.extend(data)
            offset += limit

            if len(data) < limit:
                break

        return list(map(lambda document: document["text"], documents))
