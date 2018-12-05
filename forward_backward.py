import numpy as np

def initialization():
    initialState = [1/18, 2/18, 3/18, 1/18, 2/18, 2/18, 4/18, 2/18, 1/18]
    transition=[]

    for i in range(9):
        transition.append([1/9 for i in range(9)])
    print("transition matirx", transition)
    # for i in range(9):
    #     emission.append([1/8, 2/8, 3/8, 2/8])
    emission = np.array([
        [1/4, 1/4, 1/4, 1/4],
        [1/8, 2/8, 3/8, 2/8],
        [1/8, 1/8, 4/8, 2/8],
        [3/8, 3/8, 1/8, 1/8],
        [2/8, 2/8, 2/8, 2/8],
        [1/8, 3/8, 1/8, 3/8],
        [2/8, 3/8, 1/8, 2/8],
        [4/8, 1/8, 1/8, 2/8],
        [5/8, 1/8, 1/8, 1/8]
        ])
    print("emission matrix", emission)
    return np.array(initialState), np.array(transition), np.array(emission)

def forward(s, initialState, transition, emission):
    """
    s: observation sequences
    """
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0 for j in range(len(s))] for i in range(9)]
    for i in range(0, len(initialState)):
        result[i][0] = initialState[i]*emission[i][dictionary[s[0]]]
        
    for j in range(1, len(s)):
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, len(initialState)):
                total = total + result[temp][j-1] * transition[temp][z]
            result[z][j] = total * emission[z][dictionary[s[j]]]
    # print("forward result "+str(result))
    return result

def backward(s, initialState, transition, emission):
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0 for j in range(len(s))] for i in range(9)]
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
    # print("backward result "+str(result))
    return result
        
if __name__ == "__main__":
    initialization()
    forward("AAGGC")
    backward("GCCCA")
    
