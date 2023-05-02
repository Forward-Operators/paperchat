# arxivchat

## Dependencies
- python >=3.10
- poetry
- chromadb
- langchain
- arxiv

## Setup
Follow these steps to quickly set up and run the arXiv plugin:

Install Python 3.10, if not already installed.

Clone the repository: git clone https://github.com/fwdops/arxivchat.git

Navigate to the cloned repository directory: cd /path/to/arxivchat

Install poetry: `pip install poetry`

Create a new virtual environment with Python 3.10: `poetry env use python3.10`

Activate the virtual environment: `poetry shell`

Install app dependencies: `poetry install`

Create a bearer token

Set the required environment variables:

```bash
export DATASTORE=<your_datastore>
export BEARER_TOKEN=<your_bearer_token>
export OPENAI_API_KEY=<your_openai_api_key>

# Add the environment variables for your chosen vector DB.
# Some of these are optional; read the provider's setup docs in /docs/providers for more information.

# Pinecone
export PINECONE_API_KEY=<your_pinecone_api_key>
export PINECONE_ENVIRONMENT=<your_pinecone_environment>
export PINECONE_INDEX=<your_pinecone_index>


# Qdrant
export QDRANT_URL=<your_qdrant_url>
export QDRANT_PORT=<your_qdrant_port>
export QDRANT_GRPC_PORT=<your_qdrant_grpc_port>
export QDRANT_API_KEY=<your_qdrant_api_key>
export QDRANT_COLLECTION=<your_qdrant_collection>

# Chroma
export CHROMA_HOST=<your_chroma_host>
export CHROMA_PORT=<your_chroma_port>

```

Run the API locally: poetry run start

Access the API documentation at http://0.0.0.0:8000/docs and test the API endpoints (make sure to add your bearer token).

## Ingesting
arXiv has a dataset of almost 2 million publications. it is against arXiv's ToS to fetch too much data from their website (as it creates load)
Fortunately, good people from [kaggle](https://kaggle.com) together with Cornell University create a publicly available dataset that you can use.
The dataset is freely available via Google Cloud Storage buckets and updated weekly.

Now the main issues is - how to get only a subset of that entire dataset if we don't want to ingest over 5 terabytes of pdf files?
Datase is divided into directories per-mont, per-year, so if you'd like to get all publications from September of 2021, you could just run:
`gsutil cp -r gs://arxiv-dataset/arxiv/pdf/2109/ ./local_directory`

If you'd like to get an entire dataset:
`gsutil cp -r gs://arxiv-dataset/arxiv/pdf/  ./a_local_directory/`

But if you want to get only a subset (for a given category and dates) take a look into `download.py` file.


## Query
`python cli.py`

Ask the question about the topic you've fed the chromadb before. Return information about sources as well, run continously.

## ToDO
- [ ] Automount gs arxiv bucket on deployment.
- [ ] Option to use Azure OpenAI.

## Issues & contribution
If you have any problems please use GitHub issues to report them.
If you'd like to contribute to this project, please create a pull request.