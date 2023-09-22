import os

from dotenv import load_dotenv

load_dotenv()


def get_embeddings():
    embeddings_engine = os.environ.get("EMBEDDINGS")
    assert embeddings_engine is not None

    match embeddings_engine:
        case "openai":
            from langchain.embeddings.openai import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

            return embeddings

        case "huggingface":
            from langchain.embeddings import HuggingFaceEmbeddings

            if os.environ.get("CUDA_ENABLED") == "True":
                model_kwargs = {"device": "cuda"}
            elif os.environ.get("MPS_ENABLED") == "True":
                model_kwargs = {"device": "mps"}
            else:
                model_kwargs = {"device": "cpu"}
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
                cache_folder="./models",
                model_kwargs=model_kwargs,
            )

            return embeddings
        case "huggingface-hub":
            from langchain.embeddings import HuggingFaceHubEmbeddings

            embeddings = HuggingFaceHubEmbeddings(
                repo_id="sentence-transformers/multi-qa-mpnet-base-dot-v1",
                task="feature-extraction",
                huggingfacehub_api_token=os.environ.get("HUGGINGFACE_API_TOKEN"),
            )

            return embeddings
        case "huggingface-inference":
            from .inference_embeddings import HuggingFaceInferenceEmbeddings

            embeddings = HuggingFaceInferenceEmbeddings(
                model_url=os.environ.get("HUGGINGFACE_MODEL_URL"),
                huggingface_api_token=os.environ.get("HUGGINGFACE_API_TOKEN"),
            )

            return embeddings
        case _:
            raise ValueError(f"Unsupported embeddings : {embeddings_engine}")


def get_database():
    database = os.environ.get("DATABASE")
    assert database is not None

    match database:
        case "qdrant":
            from langchain.vectorstores import Qdrant
            from qdrant_client import QdrantClient
            from qdrant_client.http.models import Distance, VectorParams

            embeddings = get_embeddings()

            qdrant_client = QdrantClient(
                host=os.getenv("QDRANT_HOST", "localhost"),
                port=os.getenv("QDRANT_PORT", "6333"),
                prefer_grpc=True,
            )

            db = Qdrant(
                collection_name="arxiv",
                client=qdrant_client,
                embeddings=embeddings,
            )

            return db

        case "chroma":
            import chromadb
            from chromadb.config import Settings
            from langchain.vectorstores import Chroma

            embeddings = get_embeddings()
            client_settings = Settings(
                chroma_api_impl="rest",
                chroma_server_host=os.getenv("CHROMA_HOST", "localhost"),
                chroma_server_http_port=os.getenv("CHROMA_PORT", "8000"),
                anonymized_telemetry=False,
                chroma_db_impl="duckdb+parquet",
            )
            client = chromadb.Client(settings=client_settings)
            client.get_or_create_collection(
                name=os.getenv("CHROMA_COLLECTION", "arxiv"),
                embedding_function=embeddings,
            )
            db = Chroma(
                collection_name=os.getenv("CHROMA_COLLECTION", "arxiv"),
                embedding_function=embeddings,
                client=client,
            )

            return db

        case "pinecone":
            from langchain.vectorstores import Pinecone

            embeddings = get_embeddings()
            import pinecone

            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY", "absdef-123456-gfdsa-sss-uuu"),
                environment=os.getenv(
                    "PINECONE_ENVIRONMENT", "northamerica-northeast1-gcp"
                ),
            )
            index_name = os.getenv("PINECONE_INDEX_NAME", "arxiv")
            db = Pinecone.from_existing_index(
                embedding=embeddings,
                index_name=index_name,
                namespace=os.getenv("PINECONE_NAMESPACE", "website"),
            )

            return db

        case _:
            raise ValueError(f"Unsupported vector database: {database}")
