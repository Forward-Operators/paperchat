"""Wrapper around HuggingFace Hub embedding models."""
from typing import Any, Dict, List, Optional

from langchain.embeddings.base import Embeddings
from langchain.utils import get_from_dict_or_env
from pydantic import BaseModel, Extra, root_validator


class HuggingFaceInferenceEmbeddings(BaseModel, Embeddings):
    client: Any  #: :meta private:
    """Model url to use for embedding."""
    model_url: str = "model-url"
    """Task to call the model with."""
    model_kwargs: Optional[dict] = None
    """Key word arguments to pass to the model."""

    huggingface_api_token: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        huggingface_api_token = get_from_dict_or_env(
            values, "huggingface_api_token", "HUGGINGFACE_API_TOKEN"
        )
        try:
            from huggingface_hub import InferenceClient

            client = InferenceClient(
                token=huggingface_api_token, model=values["model_url"]
            )
            values["client"] = client
        except ImportError:
            raise ValueError(
                "Could not import huggingface_hub python package. "
                "Please install it with `pip install huggingface_hub`."
            )
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call out to HuggingFaceHub's Inference Endpoint for embedding search docs.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        # replace newlines, which can negatively affect performance.
        texts = [text.replace("\n", " ") for text in texts]
        _model_kwargs = self.model_kwargs or {}
        _res = self.client.post(json={"inputs": texts})
        responses = _res.json()["embeddings"]
        return responses

    def embed_query(self, text: str) -> List[float]:
        """Call out to HuggingFace's Inference Endpoint for embedding query text.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        response = self.embed_documents([text])[0]
        return response
