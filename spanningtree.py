# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:49:34 2020

@author: jan-m
"""

file = open('graph.txt', 'rt').read()
lines = file.split('\n')

nodes = dict()

class Node(object):
    def __init__(self, weight, name):
        self.name = name
        self.weight = weight
        self.rootID = name
        self.rootCost = 0
        self.neighbours = dict()
        self.nextHop = ''

    def __str__(self):
        return "Name: "+str(self.name)+", Weight: "+str(self.weight)+", RootID: "+ str(self.rootID)+", RootCost: "+str(self.rootCost)+", Neighbors: "+str(self.neighbours)+", NextHop: "+str(self.nextHop)

    def addEdge(self, other, weight):
        self.neighbours.update({other.name : weight})
        other.neighbours.update({self.name : weight})

    def getNeighbours(self):
        return self.neighbours

    def getRootID(self):
        return str(self.rootID)

    def getNextHop(self):
        return str(self.nextHop)

    def getWeight(self):
        return self.weight

    def bestRoot(self, other, edgeCost, nodes):
        if self.rootID == other.rootID:
            if self.rootCost+edgeCost < other.rootCost:
                other.rootCost = self.rootCost+edgeCost
                other.nextHop = self.name
        selfRootWeight = nodes.get(self.rootID).getWeight()
        otherRootWeight = nodes.get(other.rootID).getWeight()

        if selfRootWeight < otherRootWeight :
            other.rootID = self.rootID
            other.rootCost = self.rootCost+edgeCost
            other.nextHop = self.name

def saveGraph(allNodes, nodes):
    finalRoot = nodes.get(allNodes[0]).getRootID()
    outputStream = "Spanning-Tree {\n\n    Root: "+finalRoot+";\n"
    for node in allNodes:
        if node is not finalRoot:
            currentNextHop = nodes.get(node).getNextHop()
            outputStream += "    "+node+" - "+currentNextHop+";\n"
    outputStream += "}"
    return outputStream

# Graph Datei einlesen
for line in lines:
    line = line.strip()

    if '=' in line:
        name, weight = line.split('=')
        name = name.strip()
        weight = int(weight.replace(';', '').strip())
        newNode = Node(weight, name)
        nodes.update({name : newNode})

    if ':' in line and '-' in line:
        node, weight = line.split(':')
        node1, node2 = node.split('-')
        node1Name = node1.strip()
        node2Name = node2.strip()
        weight = int(weight.replace(';', '').strip())
        node1 = nodes.get(node1Name)
        node2 = nodes.get(node2Name)
        node1.addEdge(node2, weight)

# Root bestimmen
for i in range(0, 20):
    allNodes = list(nodes.keys())
    for node in allNodes:
       currentNode  = nodes.get(node)
       neighbours = currentNode.getNeighbours()

       for neighbour in neighbours:
           currentNeighbour = nodes.get(neighbour[0])
           currentEdgeCost = neighbours[neighbour]
           currentNode.bestRoot(currentNeighbour, currentEdgeCost, nodes)

allNodes = list(nodes.keys())
result = open("result.txt", "w")
result.write(saveGraph(allNodes, nodes))
result.close()
