# arxivchat

## Dependencies
- python >=3.10
- poetry
- chromadb
- langchain
- arxiv

## Setup
python >= 3.10, `poetry shell`, `poetry install` and all dependencies should be resolved.
there will be also Dockerfile - for cli and API versions respectively

## Ingesting
`python app/utils/loaders/pdf_loader.py`

It will ask you about the topic you'd like to get arxiv publication for. Default result is 15 recent publications on given topic.

## Query
`python cli.py`

Ask the question about the topic you've fed the chromadb before. Return information about sources as well, run continously.

## ToDO
- deployment
