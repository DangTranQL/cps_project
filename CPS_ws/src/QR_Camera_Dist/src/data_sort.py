l = ['Priority 1', 'priority 2']

def sorting(code, distance):
    f = open('data.txt', 'w')
    index = []
    code.reverse()
    for line in l:
        i = code.index(line)
        i = len(code) - i - 1
        index.append(i)
    code.reverse()
    for i in index:
        f.write(code[i] + ' ' + str(distance[i]))
        f.write('\n')
    f.close()
    del code, distance