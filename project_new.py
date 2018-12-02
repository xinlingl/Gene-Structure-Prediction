initialState=[1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9)]
transition=[]
emission=[]
def initialization():
    for index in range(0,9):
        transition.append(initialState)

    for i in range(0,9):
        emission.append([1/float(4),1/float(4),1/float(4),1/float(4)])

def forward(s):
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0]*len(s) for i in range(9)]
    for i in range(0, len(initialState)):
        result[i][0] = initialState[i]*emission[i][dictionary[s[0]]]
        
    for j in range(1, len(s)):
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, len(initialState)):
                total = total + result[temp][j-1] * transition[temp][z]
            result[z][j] = total * emission[z][dictionary[s[j]]]
    print("forward result "+str(result))

def backward(s):
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0]*len(s) for i in range(9)]
    for index in range(0, len(initialState)):
        result[index][len(s)-1] = 1

    j = len(s) - 2
    while j >= 0:
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, len(initialState)):
                total = total + result[temp][j+1] * transition[z][temp] * emission[temp][dictionary[s[j + 1]]]
            result[z][j] = total
        j = j - 1
    print("backward result "+str(result))
        
if __name__ == "__main__":
    initialization()
    forward("AAGGC")
    backward("GCCCA")
    
