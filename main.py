
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

getcontext().prec = 5000            # this sets to number of decimal digits used

global targetTime
targetTime = Decimal("1")           # adjust this to set target time

useE24 = True                       # set to True to use all possible combinations from the E24 series or set to False to use the custom lists below (stdR, stdC)
showTolerance = True                # set to True if you want to print out all possible solutions within a given range
tolerance = Decimal("0.000001")



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

Ln2 = Decimal("0.6931471805599453094172321214581765680755001343602552541206800094933936219696947156058633269964186875420014810205706857336855202357581305570326707516350759619307275708283714351903070386238916734711233501153644979552391204751726815749320651555247341395258829504530070953263666426541042391578149520437404303855008019441706416715186447128399681717845469570262716310645461502572074024816377733896385506952606683411372738737229289564935470257626520988596932019650585547647033067936544325476327449512504060694381471046899465062201677204245245296126879465461931651746813926725041038025462596568691441928716082938031727143677826548775664850856740776484514644399404614226031930967354025744460703080960850474866385231381816767514386674766478908814371419854942315199735488037516586127535291661000710535582498794147295092931138971559982056543928717000721808576102523688921324497138932037843935308877482597017155910708823683627589842589185353024363421436706118923678919237231467232172053401649256872747782344535347648114941864238677677440606956265737960086707625719918473402265146283790488306203306114463007371948900274364396500258093651944304119115060809487930678651588709006052034684297361938412896525565396860221941229242075743217574890977067526871158170511370091589426654785959648906530584602586683829400228330053820740056770530467870018416240441883323279838634900156312188956065055315127219939833203075140842609147900126516824344389357247278820548627155274187724300248979454019618723398086083166481149093066751933931289043164137068139777649817697486890388778999129650361927071088926410523092478391737350122984242049956893599220660220465494151061391878857442455775102068370308666194808964121868077902081815885800016881159730561866761991873952007667192145922367206025395954365416553112951759899400560003665135675690512459268257439464831683326249018038242408242314523061409638057007025513877026817851630690255137032340538021450190153740295099422629957796474271381573638017298739407042421799722669629799393127069357472404933865308797587216996451294464918837711567016785988049818388967841349")
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




                



