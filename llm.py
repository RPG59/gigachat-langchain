import os
import requests
from base64 import b64encode
from typing import Any, List, Mapping, Optional
from dataclasses import dataclass

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain import OpenAI


class GigaChatApi:
    auth_token: str = None
    model_name: str = None
    instance = None

    def __init__(self):
        self.llm_username = os.getenv("LLM_USERNAME")
        self.llm_password = os.getenv("LLM_PASSWORD")
        self.llm_api_url = os.getenv("LLM_API_URL")

        if self.llm_api_url is None:
            raise ValueError("Invalid LLM_API_URL")

        if self.llm_username is None:
            raise ValueError("Invalid LLM_USERNAME")

        if self.llm_password is None:
            raise ValueError("Invalid LLM_PASSWORD")

        self.update_auth_token()
        self.update_model_name()

    @staticmethod
    def get_instance():
        if GigaChatApi.instance is None:
            GigaChatApi.instance = GigaChatApi()

        return GigaChatApi.instance

    def update_model_name(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        res = requests.get(f"{self.llm_api_url}/models", headers=headers).json()
        self.model_name = res["data"][0]["id"]

    def make_request(self, prompt: str) -> str:
        # TODO: try / catch token expired
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
        }
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model_name,
        }

        res = requests.post(
            f"{self.llm_api_url}/chat/completions", data, headers=headers
        ).json()
        return res.choices[0].message.content

    def update_auth_token(self):
        print(self.llm_api_url)

        response = requests.post(f"{self.llm_api_url}/token", auth=(self.llm_username, self.llm_password))

        # if response.status_code != 200:
        #     foobar123

        res = response.json()

        print(res)
        self.auth_token = res["tok"]


class CustomLLM(LLM):
    n: int

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        foo = GigaChatApi.get_instance()
        res = foo.make_request(prompt)

        return res

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": 10}
