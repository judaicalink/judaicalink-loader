import gzip
import os

from SPARQLWrapper import SPARQLWrapper, JSON
import time
import requests
import environ


def create_dataset(url, dataset):
    # requests get the datasets
    res = requests.get(url+'/$/datasets', data={"user": os.environ.get("FUSEKI_USER"), "password": os.environ.get("FUSEKI_PASSWORD")})
    print(res.status_code)
    if res.status_code != 200:
        return False
    # check if the dataset exists in datasets, ds.name
    print(res.text)
    print(res.json())
    if dataset in res.json():
        return False
    # create the dataset
    else:
        requests.post("http://fuseki:3030/$/datasets", data={"dbName": dataset, "dbType": "tdb2"})
        return True


def create(endpoint, graph):
    sparql = SPARQLWrapper(endpoint)
    drop(sparql, graph)
    query = "CREATE GRAPH <%s>" % (graph)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.method = 'POST'
    return sparql.query()


def insert(sparql, prefixes, graph, data):
    query = "%s INSERT { GRAPH <%s> { %s } } WHERE {}" % (prefixes, graph, data)
    sparql.setRequestMethod("postdirectly")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.method = 'POST'
    return sparql.query()


def drop(sparql, graph):
    query = "DROP SILENT GRAPH <%s>" % (graph)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.method = 'POST'
    print("Dropping graph {}".format(graph))
    return sparql.query()


def log(message):
    f = open("log.txt", mode="a", encoding="utf8")
    f.write(str(message))


class Reader:
    linecount = 0
    _file = None
    prefixes = ""

    def __init__(self, file):
        self._file = file

    def readline(self):
        self.linecount += 1
        line = self._file.readline()
        if line.startswith("@prefix"):
            self.prefixes = "".join((self.prefixes, line.replace("@prefix", "PREFIX").strip()[:-1].strip(), "\n"))
            return "\n"
        return line

    def skiplines(self, number):
        for i in range(number):
            l = self.readline()
            if not l:
                break

    def skipafter(self, linenumber):
        assert linenumber > self.linecount
        while (linenumber > self.linecount):
            self.readline()

    def readlines(self, number):
        lines = []
        for i in range(number):
            l = self.readline()
            if l:
                lines.append(l)
            else:
                break
        if len(lines) > 0:
            return "".join(lines)
        else:
            return None

    def read_until_blank(self, number=1):
        lines = []
        done = 0
        while True:
            l = self.readline()
            if l:
                lines.append(l)
            else:
                break
            if l == "\n":
                done += 1
                if done == number:
                    break
        if len(lines) > 0:
            return ("".join(lines), done)
        else:
            return (None, done)

    def read_until_fullstop(self, number=1):
        lines = []
        done = 0
        while True:
            l = self.readline()
            if l:
                lines.append(l)
            else:
                break
            if l.strip().endswith("."):
                done += 1
                if done == number:
                    break
        if len(lines) > 0:
            return ("".join(lines), done)
        else:
            return (None, done)


def unload(endpoint, graph):
    sparql = SPARQLWrapper(endpoint)
    drop(sparql, graph)


def load(file, endpoint, graph):
    sparql = SPARQLWrapper(endpoint)
    openfunc = open
    if file.endswith(".gz"):
        openfunc = gzip.open
    with openfunc(file, "rt", encoding="utf8") as f:
        r = Reader(f)
        resources = 0
        start = time.time()
        while True:
            cycle = time.time()
            last = r.linecount
            data, chunks = r.read_until_fullstop(10000)
            resources += chunks
            if not data:
                break
            try:
                insert(sparql, r.prefixes, graph, data)
            except Exception as e:
                print("ERROR. More info in log.txt.")
                log("Error occured at line %d:" % r.linecount)
                log(e)
                log("Data: " + data)
            print("%d: %d lines (%d) -- Time: %.2f seconds (%.2f lines/s), total: %.2f seconds (%.2f lines/s)" %
                  (resources,
                   r.linecount - last,
                   r.linecount,
                   (time.time() - cycle) / 1000,
                   (r.linecount - last) / ((time.time() - cycle) / 1000),
                   (time.time() - start) / 1000,
                   (r.linecount) / ((time.time() - start) / 1000)))

        print("Finished!")
