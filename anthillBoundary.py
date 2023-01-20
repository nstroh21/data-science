import math
import numpy as np
import matplotlib.pyplot as plt

# write a general parameterized boundary as f(x) + f(y) = C
# program asks for f(y), f(x) and C as well as theta bounds (come back to this later)

def toCartesian():
    pass

def toPolar(x,y):
    r = math.sqrt(x^2 + y^2)
    theta = math.arctan(y/x)
    return r, theta

def takeStep(x,y):
    U = np.random.uniform(0,1)
    if U < .25:
        x += 1
    elif (U >= .25) & (U < .5):
        x -= 1 
    elif (U >= .5) & (U < .75):
        y += 1
    else:
        y -= 1
    return (x,y)

# pass a boundary to simulate
def simulate(fx, fy, C):
    u,v,food, steps = 0,0,False, 0
    while (food == False):
        x,y = takeStep(u,v)
        steps += 1
        food = testBound(x,y,fx,fy,C)
        u,v = x,y
    return (steps, x, y)

def testBound(x,y,fx, fy, C):
    #print(fx(x) + fy(y))
    if (fx(x) + fy(y) > C): return True  # "outside"
    else: return False # "inside"

def main():
    fy = lambda y: ((y-2.5)/40)**2
    fx = lambda x: ((x-2.5)/30)**2
    results, stopx, stopy = [], [], []
    for i in range(100):
        steps, x, y = simulate(fx, fy, 1)
        results.append(steps)
        stopx.append(x)
        stopy.append(y)
    boundx = list(np.linspace(-29,31, 1000))
    boundy = list(np.zeros(1000))
    for i in range(1000):
        if i%2 == 0:
            boundy[i] = math.sqrt(abs(1 - fx(boundx[i]))*1600) + 2.5
        else: boundy[i] = -1*(math.sqrt(abs(1 - fx(boundx[i]))*1600) + 2.5)
    print(boundx)     
    fig,ax = plt.subplots()
    #plt.scatter(stopx, stopy)
    plt.plot(boundx, boundy)
    ax.axis('equal')
    plt.show()

    fig2 = plt.hist(boundx, bins = 10)
    plt.show()

    #fy = lambda y: eval(input())
    #fx = lambda x: eval(input())

main()