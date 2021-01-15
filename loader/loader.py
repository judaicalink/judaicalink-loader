import hugotools as h
import os
import sparqltools as s
import io

hugo_dir = "/data/judaicalink/web.judaicalink.org/hugo/judaicalink-site/content/datasets"
local_dir = "/data/judaicalink/dumps/"
global_dir = "http://data.judaicalink.org/dumps/"
endpoint = "http://localhost:8080/fuseki/judaicalink/update"


for file in os.listdir(hugo_dir):
    if file.endswith(".md"):
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
                        s.unload(endpoint, d["graph"])
                        for f in d["files"]:
                            if f["url"].endswith(".ttl.gz") or f["url"].endswith(".ttl") or \
                            f["url"].endswith(".nt.gz") or f["url"].endswith(".nt"):
                                s.load(f["url"].replace(global_dir, local_dir), endpoint, d["graph"])
                    else:
                        print("No files found to be loaded!")

                else:
                    print("Unloading graph: {}".format(d["graph"]))
                    s.unload(endpoint, d["graph"])
