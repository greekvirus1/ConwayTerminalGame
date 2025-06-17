import random
from blessed import Terminal

WIDTH: int = 100 #Total terminal width
HEIGHT: int = 50 #Total terminal height
OFFSET_W: int = 4 #Offset width of cell arena 4 characters from left and 4 from right
OFFSET_H: int = 4 #Offset height of cell arena 4 characters from top and 4 from bottom


def customSize2dArray(x: int ,y: int) -> list[list[int]]:
    '''
    Returns a 2D array of size x times y
    '''
    arr = [[0] * x for _ in range(y)]
    return arr


def conwayNextStep(currentStep: list[list[int]]) -> list[list[int]]:
    """
    Calculate and return next step
    """
    nextStep = currentStep.copy()
    for j in range(len(currentStep)):
        for i in range(len(currentStep[0])):
            #Count live cells in 3x3 grid around and INCLUDING current cell
            aliveCells: int = 0
            for m in range(-1, 2):
                for k in range(-1, 2):
                    if (i+k < 0) or (j+m < 0) or (i+k > len(currentStep[0]) -1) or (j+m > len(currentStep) -1):
                        continue
                    else:
                        if currentStep[j + m][i + k] == 1:
                            aliveCells += 1

            #Calculate current cell's state on the next step
            if currentStep[j][i] ==  1:
                if aliveCells == 3 or aliveCells == 4:
                    nextStep[j][i] = 1
                else:
                    nextStep[j][i] = 0
            else:
                if aliveCells == 3:
                    nextStep[j][i] = 1
                else:
                    nextStep[j][i] = 0
    return nextStep


def main() -> None:
    cellArena: list[list[int]] = customSize2dArray((WIDTH - OFFSET_W*2) //2, HEIGHT - OFFSET_W*2)

    population: int = 0 #Total live cells
    generations: int = 0 #Total steps from first generation

    paused: bool = True
    cursor: tuple[int, int] = (WIDTH //2, HEIGHT //2) #Cursor location

    term = Terminal()
    bgColor: str = term.on_black
    txtColor: str = term.gray80
    wallColor: str = term.gray30
    cursorColor: str = term.gold2
    aliveColor: str = term.on_webgreen #Live cell color
    deadColor: str = term.on_darkolivegreen #Dead cell color
    ultraColorOn: str = term.red1 #Color of ULTRA speed
    ultraColorOff: str = term.webmaroon #Color of ULTRA speed

    speedDict: dict[str, str] = {
    "2.0": "<" + wallColor + "<o>>" + ultraColorOff + " ULTRA",
    "1.0": "<<" + wallColor + "o>>" + ultraColorOff + " ULTRA",
    "0.5": "<<o" + wallColor + ">>" + ultraColorOff + " ULTRA",
    "0.4": "<<o>" + wallColor + ">" + ultraColorOff + " ULTRA",
    "0.2": "<<o>>" + ultraColorOff + " ULTRA",
    "0.1": "<<o>>" + ultraColorOn + " ULTRA",
    }
    speedList: list[str] = ["2.0", "1.0", "0.5", "0.4", "0.2", "0.1"]
    speedIndex: int = 2

    inp = None #Input

    with term.hidden_cursor(), term.cbreak():#, term.fullscreen():
        while inp not in (u"q", u"Q"):
            #Render screen
            print(term.home + term.clear + bgColor + txtColor)

            #Render above cell arena
            print(f"Gen: {generations}" + " " *((WIDTH -32)//2), end="")
            print("←↑→↓: Move" + " " *((WIDTH -37)//2), end="")
            print(f"t: Theme -> THEME") #REMEMBER TO FIX THIS
            print(f"Pop: {population}" + " " *(WIDTH -25), end= "")
            print("r: Randomize")

            #Render wall around cell arena
            print(wallColor, end="")
            print(" " *(OFFSET_W -2) + "+" + "-" *(WIDTH - OFFSET_W*2) + "+")
            for _ in range(HEIGHT - OFFSET_H*2):
                print(" " *(OFFSET_W -2) + "|" + " " *(WIDTH - OFFSET_W*2) + "|")
            print(" " *(OFFSET_W -2) + "+" + "-" *(WIDTH - OFFSET_W*2) + "+")

            #Render bellow cell arena
            print(txtColor + "n: Next step", end="")
            print(" " *(WIDTH -30) + "Enter: Place/del")
            print("+: Faster", end="")
            print(" " *((WIDTH -38)//2) + speedDict[speedList[speedIndex]] + " " *((WIDTH -38)//2), end= "")
            if paused:
                print(wallColor + "p: Pause")
                print(txtColor, end="")
            else:
                print(txtColor + "p: Pause")
            print("-: Slower" + " " *(WIDTH -27), end= "")
            print("q: Quit")

            #Render cell arena
            for y in range(OFFSET_H, HEIGHT - OFFSET_H):
                for x in range(OFFSET_W - 1, WIDTH - OFFSET_W - 1, 2):
                    print(term.move_yx(y, x), end="")
                    if cellArena[y - OFFSET_H][(x - OFFSET_W) //2] == 0:
                        print(deadColor + "  ", end="")
                    else:
                        print(aliveColor + "  ", end="")
                print()

            #Render cursor
            print(term.move_xy(cursor[0], cursor[1]) + cursorColor + "[]")

            #Wait for input
            print(bgColor, flush=True)
            inp = term.inkey(float(speedList[speedIndex]))
            





if __name__ == "__main__":
    main()