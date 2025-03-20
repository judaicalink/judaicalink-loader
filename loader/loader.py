import hugotools as h
import os
import sparqltools as s
import io
import argparse
import logging
import sys

hugo_dir = "/data/web.judaicalink.org/judaicalink-site/content/datasets/"
local_dir = "/data/dumps/"
global_dir = "http://data.judaicalink.org/dumps/"
endpoint = "http://localhost:3030/judaicalink/update"

parser = argparse.ArgumentParser(
    description='Load and manage named graphs for JudaicaLink datasets.'
)
parser.add_argument('--dataset', type=str, help='Dataset acronym to load or drop a specific dataset.')
parser.add_argument('--file', type=str, help='Specify a file to use for graph creation.')
parser.add_argument('--drop-only', action='store_true', help='Drop the specified graph without reloading.')
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def graph_exists(graph):
    query = f'ASK WHERE {{ GRAPH <{graph}> {{ ?s ?p ?o }} }}'
    return s.ask(endpoint + '/query', query)

def drop_graph(graph):
    if graph_exists(graph):
        s.unload(endpoint + '/update', graph)
        logger.info(f"Graph {graph} dropped successfully.")
    else:
        logger.info(f"Graph {graph} does not exist, nothing to drop.")

def create_graph(graph):
    update = f'CREATE GRAPH <{graph}>'
    if not graph_exists(graph):
        try:
            s.update(endpoint + '/update', update)
            logger.info(f"Graph {graph} created successfully.")
        except Exception as e:
            logger.error(f"Error creating graph {graph}: {e}")
    else:
        logger.info(f"Graph {graph} already exists.")

def load_dataset(dataset_file):
    try:
        d = h.get_data(os.path.join(hugo_dir, dataset_file))
        if "graph" in d:
            graph = d["graph"]
            logger.info(f"Target graph: {graph}")
            if "loaded" in d and d["loaded"]:
                if "files" in d:
                    files = d["files"]
                    logger.info(f"Files in dataset: {files}")
                    drop_graph(graph)
                    create_graph(graph)
                    for f in files:
                        try:
                            file_url = f["url"].replace(global_dir, local_dir)
                            if file_url.endswith((".ttl.gz", ".ttl", ".nt.gz", ".nt")):
                                s.load(file_url, endpoint + '/update', graph)
                                logger.info(f"File {file_url} successfully loaded into graph {graph}.")
                        except Exception as e:
                            logger.error(f"Error loading file {file_url} into graph {graph}: {e}")
                else:
                    logger.warning(f"No files found to load in dataset {dataset_file}.")
            else:
                logger.info(f"Graph marked as not loaded. Dropping: {graph}")
                drop_graph(graph)
        else:
            logger.warning(f"No 'graph' key found in dataset {dataset_file}. Skipping.")
    except Exception as e:
        logger.error(f"Error processing dataset {dataset_file}: {e}")

# Handle --drop-only logic first
if args.drop_only:
    if not args.dataset:
        logger.error("The --drop-only option requires --dataset to be specified.")
        sys.exit(1)
    dataset_file = f"{args.dataset}.md"
    if os.path.exists(os.path.join(hugo_dir, dataset_file)):
        d = h.get_data(os.path.join(hugo_dir, dataset_file))
        if "graph" in d:
            graph = d["graph"]
            drop_graph(graph)
        else:
            logger.error(f"No 'graph' key found in {dataset_file}.")
    else:
        logger.error(f"Dataset {args.dataset} not found in {hugo_dir}.")
    sys.exit(0)

# Normal dataset loading logic
if args.file:
    dataset_file = os.path.basename(args.file)
    if os.path.exists(args.file):
        load_dataset(dataset_file)
    else:
        logger.error(f"The specified file {args.file} does not exist.")
elif args.dataset:
    dataset_file = f"{args.dataset}.md"
    if os.path.exists(os.path.join(hugo_dir, dataset_file)):
        load_dataset(dataset_file)
    else:
        logger.error(f"Dataset {args.dataset} not found in {hugo_dir}.")
else:
    for file in os.listdir(hugo_dir):
        if file.endswith(".md"):
            logger.info(f"Processing dataset file: {file}")
            load_dataset(file)
