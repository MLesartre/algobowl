from operator import itemgetter
def read_input(inputfile):
    edges = []
    #try:
    with open(inputfile) as edgesfile:
        header=False
        for line in edgesfile:
            values = [int(x) for x in line.split(' ')]
            if(not header):
                header=True
                connectionmap = [[] for x in range(0, int(values[0])+1)]
            else:
                connectionmap[values[0]].append((values[1], values[2]))
                connectionmap[values[1]].append((values[0], values[2]))
                edges.append((values[0],values[1],values[2]))
    #except Exception as e:
    return (connectionmap, edges)

#Solves by iterating through nodes in order of sum of weights, adding to the set they are more connected to unless needed to balance
def mapSolve(connectionmap, edges):
    weights = [edge[2] for edge in edges]
    bias_weight = sum(weights)/len(weights)
    left=set()
    right=set()
    nodes = [(i, connections) for i, connections in enumerate(connectionmap)]
    nodes=sorted(nodes[1:], key=lambda x:sum([connection[1] for connection in x[1]]))
    for node in nodes:
        decision = (len(left)-len(right))*bias_weight
        for connection in node[1]:
            if(connection[0] in left):
                decision-=connection[1]
            elif(connection[0] in right):
                decision+=connection[1]
        if(decision > 0):
            right.add(node[0])
        else:
            left.add(node[0])
    return rebalance(left, right, connectionmap)

#Helper function for mapSolve
def rebalance(left, right, connectionmap):
    if (len(left) - len(right)) % 2 != 0:
        raise ValueError("set total is not even")
    if len(left)>len(right):
        to_move = (len(left)-len(right))/2
        print(to_move)
        importance_list = sorted(left, key=lambda x: sum(
            [(connection[1] if connection[0] in left else -1*connection[1]) for connection in connectionmap[x]]))
        for node in importance_list[:to_move]:
            left.remove(node)
            right.add(node)
    elif len(right)>len(left):
        to_move = (len(right)-len(left))/2
        print(to_move)
        importance_list = sorted(right, key=lambda x: sum(
            [(connection[1] if connection[0] in right else -1 * connection[1]) for connection in connectionmap[x]]))
        for node in importance_list[:to_move]:
            right.remove(node)
            left.add(node)
    return (left, right)


def calculateCost(left, right, connectionmap):
    cost=0;
    for node in left:
        for connection in connectionmap[node]:
            if connection[0] in right:
                cost+=connection[1]
    return cost



#Solves the problem by picking random sets, then improving them
def improveSolve(connectionmap):
    #Populates two random sets with all points
    left = set()
    right = set()
    for i in range(1, int(len(connectionmap) / 2)):
        left.add(i)
    for i in range(int(len(connectionmap) / 2) + 1, len(connectionmap)):
        right.add(i)
        
    hasImprovements = true
    while hasImprovements:
        worst = 10000000
        worstnum = 0
        for i in range(1, len(connectiomap)):
            if i in left:
                total = 0
                for j in i:
                    if j in right:
                        total += j[1]
                if(total < worst):
                    worst = total
                    worstnum = i
        best = 0
        bestnum = 0
        for j in connectionmap:
            if i in right:
                total = 0
                for j in i:
                    total += 1
    
    return (left, right)

values = read_input('input.txt')
mapSolveSets = mapSolve(values[0], values[1])
print(calculateCost(mapSolveSets[0], mapSolveSets[1], values[0]))
improveSolveSets = improveSolve(values[0])
print(calculateCost(improveSolveSets[0], improveSolveSets[1], values[0]))
