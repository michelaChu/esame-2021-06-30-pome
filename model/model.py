import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()

    def getBestPath(self, v0):
        self._bestPath = []
        self._bestCost = 0

        self._ricorsione([v0])
        return self._bestPath

    def _ricorsione(self, parziale):
        if self.calcolaCosto(parziale) > self._bestCost:
            self._bestCost = self.calcolaCosto(parziale)
            self._bestPath = copy.deepcopy(parziale)
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    def calcolaCosto(self, parziale):
        costo = 0
        for i in range(len(parziale)-1):
            costo += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return costo

    def buildGraph(self):
        self._nodes = DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)

        connessioni = DAO.getAllEdges()
        for c in connessioni:
            if self._graph.has_edge(c[0], c[1]):
                print("Arco già presente")
            else:
                self._graph.add_edge(c[0], c[1])

        # for v in self._nodes:
        #     for u in self._nodes:
        #         if self._graph.has_edge(v,u):
        #             self._graph[u][v]["weight"] = DAO.getWeight(u, v)[0]

        pesi = DAO.getAllWeights()
        for c in pesi:
            if self._graph.has_edge(c[0], c[1]) or self._graph.has_edge(c[1], c[0]):
                self._graph[c[0]][c[1]]["weight"] = c[2]


    def statistiche(self, loc):
        list = []
        for n in self._graph.neighbors(loc):
            list.append((n, self._graph[loc][n]["weight"]))
        return list

    def getAllNodes(self):
        return self._graph.nodes

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


