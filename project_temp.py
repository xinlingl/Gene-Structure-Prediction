#initialState=[1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9)]
initialState = [0.6, 0.4]
#transition=[]
#emission=[]
"""def initialization():
    for index in range(0,9):
        transition.append(initialState)
    print("transition "+str(transition))

    for i in range(0,9):
        emission.append([1/float(4),1/float(4),1/float(4),1/float(4)])
    print("emission "+str(emission))"""

transition = [[0.7, 0.3], [0.4, 0.6]]
emission = [[0.5, 0, 0],[0.1, 0, 0]]

def forward(s):
    #dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    dictionary = {'A': 0, 'G': 1, 'C': 2}
    dictionary2 = {'N': 0, 'E': 1, 'I': 2, 'p': 3, 'P': 4, 'Z': 5, 'z': 6, 's': 7, 'S': 8}
    #result = [[0]*len(s) for i in range(9)]
    result = [[0]*len(s) for i in range(2)]
    #print("result "+str(result))
    for i in range(0, len(initialState)):
        print("i "+str(i))
        result[i][0] = initialState[i]*emission[i][dictionary[s[0]]]
        print("initialState[i] "+str(initialState[i]))
        print("emission[i][dictionary[s[0]]] "+str(emission[i][dictionary[s[0]]]))
        print("result[i][0] "+str(result[i][0]))
    print("result here "+str(result))
        
    for j in range(1, len(s)):
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, len(initialState)):
                total = total + result[temp][j-1] * transition[temp][z]
                print("result[z][j-1] "+str(result[z][j-1]))
                print("transition[temp][z] "+str(transition[temp][z]))
                print("total "+str(total))
            result[z][j] = total * emission[z][dictionary[s[j]]]
    print("result "+str(result))

def backward(s):
    dictionary = {'A': 0, 'G': 1, 'C': 2}
    result = [[0]*len(s) for i in range(9)]
    for index in range(0, len(initialState)):
        result[index][len(s)-1]=1

    j = len(s) - 2
    while j>=0:
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, len(initialState)):
                print("temp "+str(temp))
                print("j "+str(j))
                print("")
                total = total + result[temp][j+1] * transition[z][temp] * transition[temp][dictionary[s[j]]]
        j = j - 1
    print("total "+str(total))
        
if __name__ == "__main__":
    #initialization()
    #forward("AAGGC")
    backward("AAGGC")
