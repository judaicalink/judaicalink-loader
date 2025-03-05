import hugotools as h
import os
import sparqltools as s
import io

hugo_dir = "/data/judaicalink/web.judaicalink.org/hugo/judaicalink-site/content/datasets/"
local_dir = "/data/judaicalink/dumps/"
global_dir = "http://data.judaicalink.org/dumps/"
url = "http://fuseki:3030"
endpoint = url + "/judaicalink/update"

# create the datasets
s.create_dataset(url, "judaicalink")

# iterate over the files in the hugo directory
for file in os.listdir(hugo_dir):
    if file.endswith(".md"):
        print(f"Parsing: {file}")
        d = h.get_data("{}{}{}".format(hugo_dir, os.sep, file))
        print("Dataset found: {}".format(file))
        if "graph" in d:
            print("Target named graph:")
            print(d["graph"])
            if "loaded" in d:
                if d["loaded"]:
                    if "files" in d:
                        print("Files in dataset:")
                        print(d["files"])
                        s.create(endpoint, d["graph"])
                        s.unload(endpoint, d["graph"])
                        for f in d["files"]:
                            try:
                                if f["url"].endswith(".ttl.gz") or f["url"].endswith(".ttl") or \
                                f["url"].endswith(".nt.gz") or f["url"].endswith(".nt"):
                                    s.load(f["url"].replace(global_dir, local_dir), endpoint, d["graph"])
                            except Exception as e:
                                print(f"Error loading file: {f['url']}, Error: {e}")
                    else:
                        print("No files found to be loaded!")

                else:
                    print("Unloading graph: {}".format(d["graph"]))
                    s.unload(endpoint, d["graph"])
