import time
from datetime import datetime
from feedparser import parse


def fetch_ids(start_date, end_date):
    ids = []
    url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+submittedDate:[{start_date}+TO+{end_date}]&start=0&max_results=1000&sortBy=submittedDate&sortOrder=descending"
    response = parse(url)
    total_items = int(response.feed.opensearch_totalresults)

    for start in range(0, total_items, 1000):
        time.sleep(3)  # Respect arXiv API rate limits
        url = f"http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+submittedDate:[{start_date}+TO+{end_date}]&start={start}&max_results=1000&sortBy=submittedDate&sortOrder=descending"
        response = parse(url)

        for entry in response.entries:
            ids.append(entry.id.split("/")[-1])

    return ids


def construct_gs_paths(ids):
    gs_paths = []
    for arxiv_id in ids:
        month_year = arxiv_id[:4]
        gs_path = f"gs://arxiv-dataset/arxiv/arxiv/pdf/{month_year}/{arxiv_id}.pdf"
        gs_paths.append(gs_path)
    return gs_paths


# Define the date range
start_date = datetime(2021, 10, 1)
end_date = datetime(2023, 4, 10)

# Get the IDs for the cs.AI papers between October 2021 and April 2023
arxiv_ids = fetch_ids(
    start_date.strftime("%Y%m%d%H%M%S"), end_date.strftime("%Y%m%d%H%M%S")
)

# Construct Google Storage paths
gs_paths = construct_gs_paths(arxiv_ids)

# Save the Google Storage paths to a file
with open("gs_paths.txt", "w") as f:
    for path in gs_paths:
        f.write(path + "\n")

print(f"Google Storage paths saved to 'gs_paths.txt'.")
