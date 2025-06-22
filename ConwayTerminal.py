import random
from blessed import Terminal

#(WIDTH - 2*OFFSET_W) % 2 = 0, AND , (HEIGHT - 2*OFFSET_H) % 2 = 0, should be true for everything to work correctly
WIDTH: int = 100 #Total terminal width
HEIGHT: int = 52 #Total terminal height
OFFSET_W: int = 4 #Offset width of cell arena 4 characters from left and 4 from right
OFFSET_H: int = 4 #Offset height of cell arena 4 characters from top and 4 from bottom


def customSize2dArray(i: int ,j: int) -> list[list[int]]:
    '''
    Returns a 2D array of size i times j
    '''
    arr = [[0] * i for _ in range(j)]
    return arr


def conwayRandom(i: int ,j: int) -> list[list[int]]:
    '''
    Returns a 2D array of size i times j, filled randomly with 0s and 1s
    '''
    arrFinal = []
    for m in range(j):
        arrInternal = []
        for k in range(i):
            arrInternal.append(random.randint(0, 1))
        arrFinal.append(arrInternal)

    return arrFinal



def conwayNextStep(currentStep: list[list[int]]) -> list[list[int]]:
    """
    Calculate and return next step
    """
    nextStep = customSize2dArray(len(currentStep[0]), len(currentStep))
    for j in range(len(currentStep)):
        for i in range(len(currentStep[j])):
            aliveCells = 0
            for m in range(-1, 2):
                for k in range(-1, 2):
                    if (j + m >= 0) and (i + k >= 0):
                        try:
                            if currentStep[j + m][i +k] == 1:
                                aliveCells += 1
                        except IndexError:
                            continue
            if currentStep[j][i] == 0:
                if aliveCells == 3:
                    nextStep[j][i] = 1
                else:
                    nextStep[j][i] = 0
            else:
                if (aliveCells == 3) or (aliveCells == 4):
                    nextStep[j][i] = 1
                else:
                    nextStep[j][i] = 0
    return nextStep


def main() -> None:
    cellArena: list[list[int]] = customSize2dArray((WIDTH - OFFSET_W*2) //2, HEIGHT - OFFSET_W*2)

    population: int = 0 #Total live cells
    generations: int = 0 #Total steps from first generation

    paused: bool = True
    cursor: list[int] = [(WIDTH //2) - 1, HEIGHT //2] #Cursor location

    term = Terminal()

    themeIndex: int = 0 #[Black, Light, Crazy]
    themeName: list[str] = ["Black", "Light", "Crazy"]
    bgColor: list[str] = [term.on_black, term.on_snow4, term.on_green]
    txtColor: list[str] = [term.gray80, term.snow, term.maroon1]
    wallColor: list[str] = [term.gray30, term.gray80, term.aqua]
    cursorColor: list[str] = [term.gold2, term.fuchsia, term.red]
    aliveColor: list[str] = [term.on_webgreen, term.on_yellow2, term.on_tan4] #Live cell color
    deadColor: list[str] = [term.on_darkolivegreen, term.on_yellow3, term.on_khaki1] #Dead cell color
    ultraColorOn: list[str] = [term.red1, term.red1, term.blue] #Color of ULTRA speed
    ultraColorOff: list[str] = [term.webmaroon, term.webmaroon, term.crimson] #Color of ULTRA speed

    speedDict: dict[str, str] = {
    "2.0": "<" + wallColor[themeIndex] + "<o>>" + ultraColorOff[themeIndex] + " ULTRA",
    "1.0": "<<" + wallColor[themeIndex] + "o>>" + ultraColorOff[themeIndex] + " ULTRA",
    "0.5": "<<o" + wallColor[themeIndex] + ">>" + ultraColorOff[themeIndex] + " ULTRA",
    "0.4": "<<o>" + wallColor[themeIndex] + ">" + ultraColorOff[themeIndex] + " ULTRA",
    "0.2": "<<o>>" + ultraColorOff[themeIndex] + " ULTRA",
    "0.1": "<<o>>" + ultraColorOn[themeIndex] + " ULTRA",
    }
    speedList: list[str] = ["2.0", "1.0", "0.5", "0.4", "0.2", "0.1"]
    speedIndex: int = 2

    inp = None #Input

    with term.hidden_cursor(), term.cbreak():#, term.fullscreen():
        while inp not in (u"q", u"Q"):
            #Render screen
            print(term.home + term.clear + bgColor[themeIndex] + txtColor[themeIndex])

            #Render above cell arena
            print(f"Gen: {generations}" + " " *((WIDTH - 32 - len(str(generations))) //2), end="")
            print("←↑→↓: Move" + " " *((WIDTH - 32 - len(str(generations))) //2), end="")
            print(f"t: Theme ->{themeName[themeIndex]}")
            print(f"Pop: {population}" + " " *((WIDTH - 30 - len(str(population))) //2), end= "")
            print("c: Clear" + " " *((WIDTH - 30 - len(str(population))) //2), end= "")
            print("r: Randomize")

            #Render wall around cell arena
            print(wallColor[themeIndex], end="")
            print(" " *(OFFSET_W -2) + "+" + "-" *(WIDTH - OFFSET_W*2) + "+")
            for _ in range(HEIGHT - OFFSET_H*2):
                print(" " *(OFFSET_W -2) + "|" + " " *(WIDTH - OFFSET_W*2) + "|")
            print(" " *(OFFSET_W -2) + "+" + "-" *(WIDTH - OFFSET_W*2) + "+")

            #Render bellow cell arena
            print(txtColor[themeIndex] + "n: Next step", end="")
            print(" " *(WIDTH -30) + "Enter: Place/del")
            print("+: Faster", end="")
            print(" " *((WIDTH -38)//2) + speedDict[speedList[speedIndex]] + " " *((WIDTH -38)//2), end= "")
            if paused:
                print(wallColor[themeIndex] + "p: Pause")
                print(txtColor[themeIndex], end="")
            else:
                print(txtColor[themeIndex] + "p: Pause")
            print("-: Slower" + " " *(WIDTH -27), end= "")
            print("q: Quit")

            #Render cell arena
            for y in range(OFFSET_H, HEIGHT - OFFSET_H):
                for x in range(OFFSET_W - 1, WIDTH - OFFSET_W - 1, 2):
                    print(term.move_yx(y, x), end="")
                    if cellArena[y - OFFSET_H][(x - OFFSET_W) //2] == 0:
                        print(deadColor[themeIndex] + "  ", end="")
                    else:
                        print(aliveColor[themeIndex] + "  ", end="")
                print()

            #Render cursor
            print(term.move_xy(cursor[0], cursor[1]) + cursorColor[themeIndex] + "[]")

            #Wait for input
            print(bgColor[themeIndex] + txtColor[themeIndex], flush=True)
            inp = term.inkey(float(speedList[speedIndex]))


            #Handling inputs

            #Movement keys
            if inp.name == "KEY_LEFT":
                if cursor[0] > OFFSET_W - 1:
                    cursor[0] -= 2 
            elif inp.name == "KEY_RIGHT":
                if cursor[0] < WIDTH - OFFSET_W - 3:
                    cursor[0] += 2
            elif inp.name == "KEY_UP":
                if cursor[1] > OFFSET_H:
                    cursor[1] -= 1
            elif inp.name == "KEY_DOWN":
                if cursor[1] < HEIGHT - OFFSET_H - 1:
                    cursor[1] += 1

            #Pause key
            elif inp in (u"p", u"P"):
                paused = not paused

            #Clear key
            elif inp in (u"c", u"C"):
                cellArena = customSize2dArray((WIDTH - OFFSET_W*2) //2, HEIGHT - OFFSET_W*2)

            #Speed keys
            elif inp == u"+":
                if speedIndex < 5:
                    speedIndex += 1
            elif inp == u"-":
                if speedIndex > 0:
                    speedIndex -= 1

            #Place/delete cell key
            elif inp.name == "KEY_ENTER":
                if cellArena[cursor[1] - OFFSET_H][(cursor[0] - OFFSET_W) //2] == 0:
                    cellArena[cursor[1] - OFFSET_H][(cursor[0] - OFFSET_W) //2] = 1
                else:
                    cellArena[cursor[1] - OFFSET_H][(cursor[0] - OFFSET_W) //2] = 0

            #Next step key
            elif inp in (u"n", u"N"):
                #Next step key always pauses
                if not paused:
                    paused = not paused
                cellArena = conwayNextStep(cellArena)

            #Randomize key
            elif inp in (u"r", u"R"):
                if not paused:
                    paused = not paused
                cellArena = conwayRandom((WIDTH - OFFSET_W*2) //2, HEIGHT - OFFSET_W*2)

            #Theme key
            elif inp in (u"t", u"T"):
                themeIndex = (themeIndex + 1) % 3


            #If not paused, get next step
            if not paused:
                cellArena = conwayNextStep(cellArena)


if __name__ == "__main__":
    main()
