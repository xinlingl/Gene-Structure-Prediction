#import numpy as np
#initialState=[1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9)]
#transition=[]
#emission=[]
    
def initialization():
    initialState=[1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9), 1/float(9)]
    transition=[]
    emission=[]
    for index in range(0,9):
        transition.append(initialState)

    for i in range(0,9):
        emission.append([1/float(4),1/float(4),1/float(4),1/float(4)])
    return initialState, transition, emission

def forward(s, initialState, transition, emission, newdictionary):
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0]*len(s) for i in range(9)]
    for i in range(0, len(initialState)):
        result[i][0] = initialState[i]*emission[i][dictionary[s[0]]]/newdictionary[s[0]]
        #print("before "+str(initialState[i]*emission[i][dictionary[s[0]]]))
        #print("after "+str(result[i][0]))
    #np.dot(np.array(initialState[:0])*np.array(emission[:0]))
        
    for j in range(1, len(s)):
        for z in range(0, len(initialState)):
            total = 0
            for temp in range(0, 9):
                total = total + result[temp][j-1] * transition[temp][z]
            #print("before "+str(total * emission[z][dictionary[s[j]]]))
            result[z][j] = total * emission[z][dictionary[s[j]]]/newdictionary[s[j]]
            #print("after "+str(result[z][j]))
    #print("forward result "+str(result))
    return result

def backward(s, initialState, transition, emission, newdictionary):
    dictionary = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = [[0]*len(s) for i in range(9)]
    product = 1

    for i in range(0, len(s)):
        product = product * newdictionary[s[i]]

    for index in range(0, 9):
        result[index][len(s)-1] = 1/product

    j = len(s) - 2
    while j >= 0:
        product = product / newdictionary[s[j]]
        #print("product "+str(product))
        for z in range(0, 9):
            total = 0
            for temp in range(0, len(initialState)):
                total = total + result[temp][j+1] * transition[z][temp] * emission[temp][dictionary[s[j + 1]]]
            result[z][j] = total/product
        j = j - 1
    #print("backward result "+str(result))
    return result
        
if __name__ == "__main__":
    newdictionary = {'A': 0.1, 'C': 0.2, 'T': 0.3, 'G': 0.4}
    initialProbability, transition, emission = initialization()
    result = forward("AAGGC", initialProbability, transition, emission, newdictionary)
    newresult = backward("GCCCA", initialProbability, transition, emission, newdictionary)
    #print("result "+str(result))
    #print("newresult "+str(newresult))
