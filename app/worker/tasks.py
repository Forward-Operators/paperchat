import tools.loaders.arxiv_loader as arxiv_loader

from .celery import worker


@worker.task(ignore_result=False, bind=True)
def ingest_task(self, query):
    return arxiv_loader.load_data(query)
