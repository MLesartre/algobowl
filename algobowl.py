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