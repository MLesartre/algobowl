#reads data from a file, returning a list of connections for each node and a list of edges
def read_input(inputfile):
    edges = []
    with open(inputfile) as edgesfile:
        header=False
        for line in edgesfile:
            values = [int(x) for x in line.split()]
            if(not header):
                header=True
                connectionmap = [[] for x in range(0, int(values[0])+1)]
            else:
                connectionmap[values[0]].append((values[1], values[2]))
                connectionmap[values[1]].append((values[0], values[2]))
                edges.append((values[0],values[1],values[2]))
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

#Helper function for mapSolve - if halves are not balanced, moves nodes to balance them
def rebalance(left, right, connectionmap):
    if (len(left) - len(right)) % 2 != 0:
        raise ValueError("set total is not even")
    if len(left)>len(right):
        to_move = int((len(left)-len(right))/2)
        importance_list = sorted(left, key=lambda x: sum(
            [(connection[1] if connection[0] in left else -1*connection[1]) for connection in connectionmap[x]]))
        for node in importance_list[:to_move]:
            left.remove(node)
            right.add(node)
    elif len(right)>len(left):
        to_move = int((len(right)-len(left))/2)
        importance_list = sorted(right, key=lambda x: sum(
            [(connection[1] if connection[0] in right else -1 * connection[1]) for connection in connectionmap[x]]))
        for node in importance_list[:to_move]:
            right.remove(node)
            left.add(node)
    return (left, right)

#simply splits the nodes in half - used to test if an algorithm is significantly better
def splitSolve(numNodes):
    left=set()
    right=set()
    for i in range(1, numNodes):
        if i%2==0:
            left.add(i)
        else:
            right.add(i)
    return (left,right)

#finds the cost of a solution
def calculateCost(left, right, connectionmap):
    cost=0;
    for node in left:
        if node in right:
            raise ValueError("left and right sets overlap")
        for connection in connectionmap[node]:
            if connection[0] in right:
                cost+=connection[1]
    return cost

def improveSolution(left, right, connectionmap):
    swaps=0
    for lnode in left:
        lcost = sum(connection[1] if connection[0] in right else -1*connection[1] for connection in connectionmap[lnode])
        best_improvement=0
        to_swap = None
        for rnode in right:
            rcost = sum(connection[1] if connection[0] in left else -1*connection[1] for connection in connectionmap[rnode])
            if lcost+rcost>best_improvement:
                best_improvement=lcost+rcost
                to_swap = rnode
        if to_swap:
            swaps+=1
            left.remove(lnode)
            right.add(lnode)

            right.remove(to_swap)
            left.add(to_swap)
    return (left, right)

#combines algorithms to reach a better solution
def comboSolve(connectionMap, edges):
    threshold = 0
    mapSolveSets = mapSolve(connectionMap, edges)
    splitSolveSets = splitSolve(len(connectionMap))
    to_improve = mapSolveSets if calculateCost(mapSolveSets[0], mapSolveSets[1], connectionMap)<calculateCost(splitSolveSets[0], splitSolveSets[1], connectionMap) else splitSolveSets
    to_improve_cost = calculateCost(to_improve[0], to_improve[1], connectionMap)
    improved = improveSolution(to_improve[0], to_improve[1], connectionMap)
    improved_cost = calculateCost(improved[0], improved[1], connectionMap)
    improvement = to_improve_cost-improved_cost
    while improvement> threshold:
        print(f'improved solution by {improvement}')
        to_improve=improved
        to_improve_cost=improved_cost
        improved = improveSolution(to_improve[0], to_improve[1], connectionMap)
        improved_cost = calculateCost(improved[0], improved[1], connectionMap)
        improvement = to_improve_cost - improved_cost
    print(f'improved solution by {improvement}')
    return improved if improvement>=0 else to_improve

def verifyOutput(infile, outfile):
    try:
        connectionMap = read_input(infile)[0]
        with open(outfile) as output:
            lines = output.readlines()
        claimed = int(lines[0])
        left = set([int(x) for x in lines[1].split()])
        right = set([int(x) for x in lines[2].split()])
        actual = calculateCost(left, right, connectionMap)
        if claimed == actual:
            print(f"Successfully verified {outfile} based on {infile}")
        else:
            print(f"Verification failed on {outfile} based on {infile}\n\tClaimed: {claimed}\n\tActual: {actual}")
    except:
        print(f'An error occured while verifying {outfile} based on {infile}')

#Core funciton of improveSolve, except now it takes a pair of sets as the input.
def improveSolver(left, right, connectionmap):
    hasImprovements = True
    prevRNum = 0
    prevLNum = 0
    while hasImprovements:
        #Calculates the change that would occur if one node on the left/right would be swapped
        leftDelta = -1000000
        leftNum = 0
        for i in range(1, len(connectionmap)):
            if i in left:
                total = 0
                for j in connectionmap[i]:
                    if j[0] in right:
                        total += j[1]
                    else:
                        total -= j[1]
                if(total > leftDelta):
                    leftDelta = total
                    leftNum = i
        #Repeats the calculation on the right side, finding the best change
        rightDelta = -1000000
        rightNum = 0
        for i in range(1, len(connectionmap)):
            if i in right:
                total = 0
                for j in connectionmap[i]:
                    if j[0] in left:
                        total += j[1]
                    else:
                        total -= j[1]
                if(total > rightDelta):
                    rightDelta = total
                    rightNum = i
        #Checks to make sure that the change would actually decrease the cost and that both numbers exist
        if(leftDelta + rightDelta > 0 and rightNum != 0 and leftNum != 0 and leftNum != prevRNum and rightNum != prevLNum):
            prevLNum = leftNum
            prevRNum = rightNum
            left.remove(leftNum)
            right.remove(rightNum)
            left.add(rightNum)
            right.add(leftNum)
        else:
            #If the best change wouldn't decrease cost, stop improving
            hasImprovements = False
    
    return (left, right)

def generate_output():
    splitSolveCosts=[]
    comboSolveCosts=[]
    improveSolveCosts = []

    for i in range(1, 29):
        print(f'Solving group {i}')
        try:
            values = read_input(f'input_group{i}.txt')

            splitSolveSets = splitSolve(len(values[0]))
            splitSolveCosts.append(calculateCost(splitSolveSets[0], splitSolveSets[1], values[0]))

            comboSolveSets = comboSolve(values[0], values[1])
            comboSolveCost = calculateCost(comboSolveSets[0], comboSolveSets[1], values[0])
            comboSolveCosts.append(comboSolveCost)

            improveSolveSets = improveSolve(values[0])
            improveSolveCosts.append(calculateCost(improveSolveSets[0], improveSolveSets[1], values[0]))

            with open(f'output\\group{i}.txt', 'w') as output:
                output.write(f'{comboSolveCost}\n')
                leftstring = ''
                for node in comboSolveSets[0]:
                    leftstring += str(node) + ' '
                output.write(f'{leftstring[:-1]}\n')
                rightstring = ''
                for node in comboSolveSets[1]:
                    rightstring += str(node) + ' '
                output.write(f'{rightstring[:-1]}')
        except:
            print(f"Could not read group {i} input")



    print(f"total splitSolve Costs: {sum(splitSolveCosts)}")
    print(f"total comboSolve Costs: {sum(comboSolveCosts)}")
    print(f"total improveSolve costs: {sum(improveSolveCosts)}")
    improveSolveSets = improveSolve(values[0])
    print(calculateCost(improveSolveSets[0], improveSolveSets[1], values[0]))

def verifyAll():
    for i in range(1, 29):
        verifyOutput(f'input_group{i}.txt',f'output\\group{i}.txt')

verifyAll()
