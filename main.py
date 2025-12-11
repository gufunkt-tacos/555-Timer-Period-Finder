from math import log

stdR = [100,120,150,180,220,270,330,390,470,560,620,680,1000,1200,1500,1800,2200,2700,3300,3900,4700,5600,6800,8200,10000,12000,15000,18000,22000,27000,33000,39000,47000,56000,68000,82000,100000,120000,150000,180000,220000,270000,330000,390000,470000,560000,680000,820000,1000000,2200000,2700000,3300000,3900000,4700000,5600000,10000000]
stdC = [10*10**-12,47*10**-12,100*10**-12,120*10**-12,150*10**-12,180*10**-12,220*10**-12,270*10**-12,330*10**-12,390*10**-12,560*10**-12,680*10**-12,820*10**-12,1*10**-9,2.2*10**-9,3.3*10**-9,4.7*10**-9,10*10**-9,22*10**-9,33*10**-9,47*10**-9,68*10**-9,100*10**-9,150*10**-9,220*10**-9,330*10**-9,470*10**-9,680*10**-9,1*10**-6, 2.2*10**-6,3.3*10**-6,4.7*10**-6,10*10**-6,22*10**-6,33*10**-6,47*10**-6,100*10**-6,330*10**-6,470*10**-6,1000*10**-6,2200*10**-6,4700*10**-6]


global currentLowest
currentLowest = 0
global bestR1
global bestR2
global bestC

def timePeriod(R1, R2, C):
    return (R1 + 2*R2)*C / log(2)

def printOut(R1, R2, C, time):
    print("This time is " + str(time) + "s.")
    print("R1 = " + str(R1))
    print("R2 = " + str(R2))
    print("C = " + str(C))
    print()

def iterate():
    global currentLowest
    global bestR1
    global bestR2
    global bestC
    for R1 in stdR:
        for R2 in stdR:
            for C in stdC:
                newTime = timePeriod(R1, R2, C)

                if abs(newTime - 1) < abs(currentLowest - 1):
                    currentLowest = newTime
                    bestR1 = R1
                    bestR2 = R2
                    bestC = C
                if abs(newTime - 1) < 0.0005:
                    printOut(R1, R2, C, newTime)
                


iterate()

print("Best time:")
printOut(bestR1, bestR2, bestC, currentLowest)




                



