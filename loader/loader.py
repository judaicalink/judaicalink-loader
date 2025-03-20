import hugotools as h
import os
import sparqltools as s
import io
import argparse
import logging

# Directories and SPARQL endpoint
hugo_dir = "/data/web.judaicalink.org/judaicalink-site/content/datasets/"
local_dir = "/data/dumps/"
global_dir = "http://data.judaicalink.org/dumps/"
endpoint = "http://localhost:3030/judaicalink/update"

# Argument parser
parser = argparse.ArgumentParser(
    description='Load and manage named graphs for JudaicaLink datasets.'
)
parser.add_argument('--dataset', type=str, help='Dataset acronym to load a specific dataset only.')
parser.add_argument('--file', type=str, help='Specify a file to use for graph creation.')
parser.add_argument('--drop-only', action='store_true', help='Only drop the graph without reloading.')
args = parser.parse_args()

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Function to load a single dataset
def load_dataset(dataset_file):
    try:
        d = h.get_data(os.path.join(hugo_dir, dataset_file))
        if "graph" in d:
            graph = d["graph"]
            logger.info(f"Target graph: {graph}")
            if args.drop_only:
                s.unload(endpoint, graph)
                logger.info(f"Graph {graph} dropped successfully.")
                return
            if "loaded" in d and d["loaded"]:
                if "files" in d:
                    files = d["files"]
                    logger.info(f"Files in dataset: {files}")
                    s.unload(endpoint, graph)
                    for f in files:
                        try:
                            file_url = f["url"].replace(global_dir, local_dir)
                            if file_url.endswith((".ttl.gz", ".ttl", ".nt.gz", ".nt")):
                                s.load(file_url, endpoint, graph)
                                logger.info(f"File {file_url} successfully loaded into graph {graph}.")
                        except Exception as e:
                            logger.error(f"Error loading file {file_url} into graph {graph}: {e}")
                else:
                    logger.warning(f"No files found to load in dataset {dataset_file}.")
            else:
                logger.info(f"Dropping graph: {graph}")
                s.unload(endpoint, graph)
                logger.info(f"Graph {graph} dropped successfully.")
        else:
            logger.warning(f"No 'graph' key found in dataset {dataset_file}. Skipping.")
    except Exception as e:
        logger.error(f"Error processing dataset {dataset_file}: {e}")

# Main logic
if args.file:
    # Load dataset using a specific file
    dataset_file = os.path.basename(args.file)
    if os.path.exists(args.file):
        load_dataset(dataset_file)
    else:
        logger.error(f"The specified file {args.file} does not exist.")
elif args.dataset:
    # Load a specific dataset by acronym
    dataset_file = f"{args.dataset}.md"
    if os.path.exists(os.path.join(hugo_dir, dataset_file)):
        load_dataset(dataset_file)
    else:
        logger.error(f"Dataset {args.dataset} not found in {hugo_dir}.")
else:
    # Default: Load all datasets
    for file in os.listdir(hugo_dir):
        if file.endswith(".md"):
            logger.info(f"Processing dataset file: {file}")
            load_dataset(file)
