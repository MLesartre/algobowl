def read_input(inputfile):
    edges = []
    connectionmap = []
    try:
        with open(inputfile) as edgesfile:
            header=False
            for line in edgesfile:
                values = line.split(' ')
                if(not header):
                    header=True
                    connectionmap = [[] for x in range(0, int(values[0])-1)]
                else:
                    connectionmap[values[0]].append((values[1], values[2]))
                    connectionmap[values[1]].append((values[0], values[2]))
                    edges.append((values[0],values[1],values[2]))
    except Exception as e:
        print()
    return edges
print(read_input('input.txt'))