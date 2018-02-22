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
                try:
                    connectionmap[values[0]].append((values[1], values[2]))
                    connectionmap[values[1]].append((values[0], values[2]))
                except IndexError:
                    print(values)
                    print(len(connectionmap))
                    raise SystemExit
                edges.append((values[0],values[1],values[2]))
    #except Exception as e:
    return connectionmap
read_input('input.txt')


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
