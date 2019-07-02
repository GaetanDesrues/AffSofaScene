import sys
import os

class Graph:
    def __init__(self, filename):
        lines = open(filename,'r').readlines()

        self.rootNodeFound = False
        self.graph = Node("rootName")

        for line in lines[Graph.findBeginFunction(lines):]:
            if "return" in line: break
            if not Graph.isCommented(line) and ("createObject" in line or "createChild" in line):
                parent = Graph.findParent(line)

                if not self.rootNodeFound:
                    self.rootNodeFound = True
                    self.graph.name = parent

                if "createObject" in line:
                    self.graph[parent].addComponent(Graph.findComponentName(line))

                if "createChild" in line:
                    self.graph[parent].addChild(Graph.findChildName(line))


    def __str__(self):
        return str(self.graph)


    def findParent(string):
        i = string.rfind(".", 0, string.find("create"))
        i2, s = i, ""
        while s!=" " and s!="=" and s!=".":
            i2 -= 1
            s = string[i2]
        return string[i2+1:i]

    def findComponentName(line):
        i1 = line.find("createObject")+13
        gui = line[i1:i1+1]
        i2 = line.find(gui, i1+1)
        return line[i1+1:i2]

    def findChildName(line):
        i1 = line.find("createChild")+12
        gui = line[i1:i1+1]
        i2 = line.find(gui, i1+1)
        return line[i1+1:i2]

    def findBeginFunction(lines):
        ic, ig = None, None
        for i,line in enumerate(lines):
            if "createGraph" in line: ig = i
            if "createScene" in line: ic = i
        if ig is None: return ic
        return ig

    def isCommented(line):
        for c in line:
            if c!=" ":
                if c=="#": return True
                else: return False


class Node:
    def __init__(self, name, i=0):
        self.name = name
        self.components = list()
        self.parent = None
        self.children = list()
        self.i = i

    def __getitem__(self, i):
        if self.name == i: return self
        for c in self.children:
            d = c[i]
            if d is not None: return d

    def __str__(self):
        s = self.name
        for c in self.components:
            s += "\n"+"     "*(self.i+1)+c
        for c in self.children:
            s += "\n"+"     "*(self.i+1)+"-> "+str(c)
        return s

    def addChild(self, name):
        c = Node(name, self.i+1)
        c.parent = self
        self.children.append(c)

    def addComponent(self, name):
        self.components.append(name)




if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Wrong command line arguments. Ex: python {} scene.py".format(sys.argv[0]))
        sys.exit()
    filename = sys.argv[1]
    if not os.path.exists(filename):
        print("File {} not found".format(filename))
        sys.exit()

    print(Graph(filename))
