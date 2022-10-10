RUNNING_SCORE = 0
FRAMES_AND_SHOTS = []
CURRENT_FRAME = 0
CURRENT_SHOT = 0
CURRENT_BONUS = 0
BONUS_SHOT_COUNT = 0
BONUS_ARR = []
KEEP_ALIVE = True

def getBonusCount():
    return BONUS_SHOT_COUNT
def setBonus(bonusCount):
    global BONUS_SHOT_COUNT
    BONUS_SHOT_COUNT += bonusCount
    return BONUS_SHOT_COUNT
def getBonusShots():
    return BONUS_ARR

def calculateBonus(bonusShot):
    global BONUS_ARR
    if getBonusCount() == 0:
        BONUS_ARR.clear()
    else: 
        BONUS_ARR.append(bonusShot)
        setBonus(-1)
    if len(BONUS_ARR) > getBonusCount() + 1:
        BONUS_ARR.clear()
    print("Current Bonuses: " + str(BONUS_ARR))


def gameOver():
    global KEEP_ALIVE
    KEEP_ALIVE = False
    exit()

def verifyInput(userInput):
    if userInput.isdigit() and int(userInput) < 10:
        return int(userInput)
    elif userInput == '/':
        return userInput
    elif userInput == 'x' or userInput == 'X':
        return 'X'
    elif userInput == 'r' or userInput == 'R':
        reset()
    elif userInput == 'q' or userInput == 'Q':
        gameOver()
    else:
        print("Invalid Input! Enter a digit 0-9, /, x, or X")
        return None
    
def calculateScore(newScore, scoreType='default'):
    global RUNNING_SCORE
    if isinstance(newScore, int):
        for bonus in getBonusShots():
            newScore += bonus
        RUNNING_SCORE += newScore
    elif newScore == 'X':
        newScore = 10
        for bonus in getBonusShots():
            newScore += bonus
        RUNNING_SCORE += newScore
    return RUNNING_SCORE

def printFrames():
    print(FRAMES_AND_SHOTS)

def addFrame(scoreVal):
    global CURRENT_FRAME, CURRENT_SHOT, FRAMES_AND_SHOTS
    FRAMES_AND_SHOTS.insert(CURRENT_FRAME, [scoreVal, 0])
    CURRENT_SHOT += 1
    printFrames()
    print("CURRENT SCORE: " + str(calculateScore(scoreVal)))

def addShot(scoreVal):
    global CURRENT_FRAME, CURRENT_SHOT, FRAMES_AND_SHOTS
    FRAMES_AND_SHOTS[CURRENT_FRAME][CURRENT_SHOT] = scoreVal
    CURRENT_FRAME += 1
    CURRENT_SHOT -= 1
    printFrames()
    print("CURRENT SCORE: " + str(calculateScore(scoreVal)))

def addStrike():
    global CURRENT_FRAME, CURRENT_SHOT, FRAMES_AND_SHOTS
    FRAMES_AND_SHOTS.insert(CURRENT_FRAME, ['X', 0])
    CURRENT_FRAME += 1
    setBonus(2)
    printFrames()
    print("CURRENT SCORE: " + str(calculateScore(10)))

def addSpare():
    global CURRENT_FRAME, CURRENT_SHOT, FRAMES_AND_SHOTS
    if CURRENT_SHOT == 0:
        print('cannot score a spare on the current shot, did you mean to enter a strike(X)?')
        return
    lastShot = FRAMES_AND_SHOTS[CURRENT_FRAME][CURRENT_SHOT -1]
    FRAMES_AND_SHOTS[CURRENT_FRAME][CURRENT_SHOT] = '/'
    CURRENT_SHOT -= 1
    CURRENT_FRAME += 1
    setBonus(1)
    printFrames()
    print("CURRENT SCORE: " + str(calculateScore(10 - lastShot)))

def enterShot():
    global CURRENT_FRAME, FRAMES_AND_SHOTS, CURRENT_SHOT, KEEP_ALIVE
    print("Frame " + str(CURRENT_FRAME + 1) + ", Shot " + str(CURRENT_SHOT + 1))
    shot = verifyInput(input("Enter Shot: "))
    #calculateBonus(shot)
    if CURRENT_FRAME == 11:
        KEEP_ALIVE = False
        return
    elif shot is None:
        return
    elif CURRENT_SHOT == 0 and isinstance(shot, int):
        calculateBonus(shot)
        addFrame(shot)
        return
    elif CURRENT_SHOT == 0 and shot == 'X':
        calculateBonus(10)
        addStrike()
        return
    elif CURRENT_SHOT != 0 and shot == '/':
        calculateBonus(10)
        addSpare()
        return
    elif CURRENT_SHOT > 0 and shot == 'X':
        print('cannot score strike on the current shot, did you mean to enter a spare(/)?')
        return
    else: 
        calculateBonus(shot)
        addShot(shot)
        return

def reset():
    global RUNNING_SCORE, FRAMES_AND_SHOTS, CURRENT_FRAME, CURRENT_SHOT, CURRENT_BONUS, BONUS_SHOT_COUNT, BONUS_ARR, KEEP_ALIVE
    RUNNING_SCORE = 0
    FRAMES_AND_SHOTS = []
    CURRENT_FRAME = 0
    CURRENT_SHOT = 0
    CURRENT_BONUS = 0
    BONUS_SHOT_COUNT = 0
    BONUS_ARR = []
    keepPlaying = input("Enter 'r' to start a new game. Enter 'q' to quit application.")
    if keepPlaying == 'r':
        KEEP_ALIVE = True
        loop()
    elif keepPlaying == 'q':
        gameOver()
    else:
        reset()

def loop():
    while KEEP_ALIVE:
        enterShot()
loop()
reset()