"""
    Public Interface to be used by the ppl who want to use the Databases
"""

import base64
import json
import os

import requests

dev_url = "http://localhost:4001/graphql"
prod_url = "http://api.chemkg.cloud:4001/graphql"
headers = {"Content-Type": "application/json"}
default_graph = "chemkg"


class ChemKG:
    def dev():
        return ChemKG(dev_url, default_graph)

    def __init__(self, url=prod_url, graph=default_graph):
        self._url = url
        self.graph = graph

    def __str__(self):
        return f"ChemKG({self.url}, {self.graph})"

    def _run(self, payload):
        request = requests.post(self._url, json=payload, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception(
                f"Query failed to run by returning code of {request.status_code}. {payload} ::{request.text}"
            )

    def _run_query(self, query):
        return self._run({"query": query})

    def _prepareFile(self, path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read())

    #
    def uploadFile(self, filePath, DOI):
        with open(filePath, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode("utf-8")
            root, ext = os.path.splitext(filePath)
            fn = f'uploadFile(file:"{encoded_string}", ext: "{ext}", doi: "{DOI}", graph: "{self.graph}")'
            self._run_query("mutation {" + fn + "}")

    #
    def uploadTurtle(self, filePath):
        with open(filePath) as f:
            encoded_string = base64.b64encode(f.read().encode("utf-8")).decode("utf-8")
            fn = f'uploadTurtle(file:"{encoded_string}", graph: "{self.graph}")'
            self._run_query("mutation {" + fn + "}")

    #
    def getGraphs(self):
        return self._run_query("mutation { getGraphs }")

    def getGraph(self):
        return self._run_query(
            'mutation { getGraph(urn: "' + self.graph + '") { virt neo4j } }'
        )

    def deleteGraph(self):
        return self._run_query('mutation { deleteGraph(urn: "' + self.graph + '") }')

    # only supported by Neo4j atm
    def fullGraph(self):
        return self._run_query("{ fullGraph }")

    def runCypher(self, query):
        return self._run_query('mutation { runCypher(query: "' + query + '") }')

    def runSparql(self, query):
        return self._run_query('mutation { runSparql(query: "' + query + '") }')


def connect(options):

    return 0
