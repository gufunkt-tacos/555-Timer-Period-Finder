
"""
Circuit Layout
    Vin
     │
     │
    ┌─┐
    │ │ R1
    └─┘
     │
     │───────────── 7
     │
    ┌─┐                     to 555 timer
    │ │ R2
    └─┘
     │          ─── 6
     │─────────│
     │   C      ─── 2
  ───────
  ───────
     │
     │
    GND

"""
from math import log
from decimal import Decimal, getcontext

getcontext().prec = 100             # this sets to number of decimal digits used

global targetTime
targetTime = Decimal("1")           # adjust this to set target time

useE24 = False                      # set to True to use all possible combinations from the E24 series or set to False to use the custom lists below (stdR, stdC)
showTolerance = True                # set to True if you want to print out all possible solutions within a given range
tolerance = Decimal("0.0005")



# these are the values I had on hand
# feel free to use the E24 toggle to use all possible combinations

stdR = [
    Decimal("100"), Decimal("120"), Decimal("150"), Decimal("180"), Decimal("220"),
    Decimal("270"), Decimal("330"), Decimal("390"), Decimal("470"), Decimal("560"),
    Decimal("620"), Decimal("680"), Decimal("1000"), Decimal("1200"), Decimal("1500"),
    Decimal("1800"), Decimal("2200"), Decimal("2700"), Decimal("3300"), Decimal("3900"),
    Decimal("4700"), Decimal("5600"), Decimal("6800"), Decimal("8200"), Decimal("10000"),
    Decimal("12000"), Decimal("15000"), Decimal("18000"), Decimal("22000"), Decimal("27000"),
    Decimal("33000"), Decimal("39000"), Decimal("47000"), Decimal("56000"), Decimal("68000"),
    Decimal("82000"), Decimal("100000"), Decimal("120000"), Decimal("150000"), Decimal("180000"),
    Decimal("220000"), Decimal("270000"), Decimal("330000"), Decimal("390000"), Decimal("470000"),
    Decimal("560000"), Decimal("680000"), Decimal("820000"), Decimal("1000000"),
    Decimal("2200000"), Decimal("2700000"), Decimal("3300000"), Decimal("3900000"),
    Decimal("4700000"), Decimal("5600000"), Decimal("10000000")
]


stdC = [
    Decimal("10e-12"), Decimal("47e-12"), Decimal("100e-12"), Decimal("120e-12"),
    Decimal("150e-12"), Decimal("180e-12"), Decimal("220e-12"), Decimal("270e-12"),
    Decimal("330e-12"), Decimal("390e-12"), Decimal("560e-12"), Decimal("680e-12"),
    Decimal("820e-12"), Decimal("1e-9"), Decimal("2.2e-9"), Decimal("3.3e-9"),
    Decimal("4.7e-9"), Decimal("10e-9"), Decimal("22e-9"), Decimal("33e-9"),
    Decimal("47e-9"), Decimal("68e-9"), Decimal("100e-9"), Decimal("150e-9"),
    Decimal("220e-9"), Decimal("330e-9"), Decimal("470e-9"), Decimal("680e-9"),
    Decimal("1e-6"), Decimal("2.2e-6"), Decimal("3.3e-6"), Decimal("4.7e-6"),
    Decimal("10e-6"), Decimal("22e-6"), Decimal("33e-6"), Decimal("47e-6"),
    Decimal("100e-6"), Decimal("330e-6"), Decimal("470e-6"), Decimal("1000e-6"),
    Decimal("2200e-6"), Decimal("4700e-6")
]

E24 = [
    Decimal("10"), Decimal("11"), Decimal("12"), Decimal("13"),
    Decimal("15"), Decimal("16"), Decimal("18"), Decimal("20"),
    Decimal("22"), Decimal("24"), Decimal("27"), Decimal("30"),
    Decimal("33"), Decimal("36"), Decimal("39"), Decimal("43"),
    Decimal("47"), Decimal("51"), Decimal("56"), Decimal("62"),
    Decimal("68"), Decimal("75"), Decimal("82"), Decimal("91")
]



global currentLowest
currentLowest = Decimal("Infinity")
global bestR1
global bestR2
global bestC

Ln2 = Decimal("2").ln()
TEN = Decimal("10")

def timePeriod(R1, R2, C):
    return (R1 + 2*R2) * C * Ln2

def printOut(R1, R2, C, time):
    print(f"Time Period = {time} s")
    print(f"R1 = {R1} Ω")
    print(f"R2 = {R2} Ω")
    print(f"C = {C:.2E} F")
    # print("C = " + str(float('%.*g' % (2, C))) + " F") # stops you being able to see floating point error
    print()

def iterateCustom():
    global currentLowest
    global bestR1
    global bestR2
    global bestC
    for R1 in stdR:
        for R2 in stdR:
            for C in stdC:
                newTime = timePeriod(R1, R2, C)

                if abs(newTime - targetTime) < abs(currentLowest - targetTime):
                    currentLowest = newTime
                    bestR1 = R1
                    bestR2 = R2
                    bestC = C
                
                if showTolerance:
                    if abs(newTime - targetTime) <= tolerance:
                        printOut(R1, R2, C, newTime)
                

def iterateE24(ir1, ir2, ic):
    global currentLowest
    global bestR1
    global bestR2
    global bestC
    for r1 in E24:
        for r2 in E24:
            for c in E24:
                R1 = r1 * (TEN ** ir1)
                R2 = r2 * (TEN ** ir2)
                C = c * (TEN ** ic)

                newTime = timePeriod(R1, R2, C)

                if abs(newTime - targetTime) < abs(currentLowest - targetTime):
                    currentLowest = newTime
                    bestR1 = R1
                    bestR2 = R2
                    bestC = C

                if showTolerance:
                    if abs(newTime - targetTime) <= tolerance:
                        printOut(R1, R2, C, newTime)
                



if useE24 == False:
    iterateCustom()
else:
    for ir1 in range(0, 9):                     # iteration for very R1
        for ir2 in range(0, 9):                 # iteration for very R2
            for ic in range(-10, 1):            # iteration for very C
                iterateE24(ir1, ir2, ic)

print("Best:")
printOut(bestR1, bestR2, bestC, currentLowest)




                



