from turtle import st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from numpy.core.records import array

LEVEL_SIZE = 28
GENERATED_LEVELS = 5
START_LEVEL = 1

MAX_PIG_COUNT = 4

# blocks number and size
# Dictionary represents [RealWorld Size (width, height), actual size, block name key, material]

           # ICE            #STONE          #WOOD                       RealWorld Size 
blocks = {'1':[0.22,0.22,1,1,1], '2':[0.22,0.22,1,1,2], '3':[0.22,0.22,1,1,3],    # [1,1]
          '5':[0.43,0.22,2,2,1], '6':[0.43,0.22,2,2,2], '7':[0.43,0.22,2,2,3],    # [2,1]
          '8':[0.22,0.43,2,3,1], '9':[0.22,0.43,2,3,2], '10':[0.22,0.43,2,3,3],   # [1,2]
          '11':[0.85,0.22,4,4,1], '12':[0.85,0.22,4,4,2], '13':[0.85,0.22,4,4,3], # [4,1]
          '14':[0.22,0.85,4,5,1], '15':[0.22,0.85,4,5,2], '16':[0.22,0.85,4,5,3], # [1,4]
          '17':[1.68,0.22,8,6,1], '18':[1.68,0.22,8,6,2], '19':[1.68,0.22,8,6,3], # [8,1] 
          '20':[0.22,1.68,8,7,1], '21':[0.22,1.68,8,7,2], '22':[0.22,1.68,8,7,3], # [1,8]
          '23':[2.06,0.22,9,8,1], '24':[2.06,0.22,9,8,2], '25':[2.06,0.22,9,8,3], # [9,1]
          '26':[0.22,2.06,9,9,1], '27':[0.22,2.06,9,9,2], '28':[0.22,2.06,9,9,3]} # [1,9]



blocks_sizes = {'1': [1,1], '2': [2,1], '3': [1,2], '4': [4,1],
          '5': [1,4], '6':[8,1], '7':[1,8],
          '8': [9,1], '9':[1,9]}

blocks_strings = {"2ice": "11", "2stone": "22", "2wood": "33",
                 "4ice": "1111", "4stone": "2222", "4wood": "3333",
                 "8ice": "11111111", "8stone": "22222222", "8wood": "33333333",
                 "9ice": "111111111", "9stone": "222222222", "9wood": "333333333"}

pig_size = [0.5,0.45] 

tiny_block_size = [0.22,0.22]
tiny_block_name = "SquareTiny"

# blocks number and name
# (blocks 3, 5, 7, 9) are their respective block names rotated 90 derees clockwise
block_names = {'1':"SquareTiny", '2':"RectTiny", '3':"RectTiny", '4':"RectSmall",
               '5':"RectSmall", '6':"RectMedium", '7':"RectMedium",
               '8':"RectBig", '9':"RectBig"}

# materials number and name
materials = {'1':"ice", '2':"stone", '3':"wood"}

absolute_ground_y = -3.5
absolute_ground_x = 2.0 

data = []

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def clearSquareBracketsIfNeeded(line: str):
    return line.replace("[", "").replace("]","")

def clearLine(line: str):
    line = line.replace("\n", "")
    line = clearSquareBracketsIfNeeded(line)
    splittedLine = line.split(" ")
    splittedLine = remove_values_from_list(splittedLine, "")
    return splittedLine

def draw(twoDArray):
    # plot
    fig, ax = plt.subplots()

    ca = []
    ca.append([0,255,255,255])

    iceIncluded = False
    stoneIncluded = False
    woodIncluded = False
    pigIncluded = False

    for i in range(0, len(twoDArray)):
        for j in range(0, len(twoDArray[i])):
            if twoDArray[i][j] == 1 and iceIncluded == False :
                ca.append([1,0,228,255])
                iceIncluded = True
            elif twoDArray[i][j] == 2 and stoneIncluded == False:
                ca.append([2,144,148,151])
                stoneIncluded = True
            elif twoDArray[i][j] == 3 and woodIncluded == False:
                ca.append([3,214,137,16])
                woodIncluded = True
            elif twoDArray[i][j] == 4 and pigIncluded == False:
                ca.append([4,40,180,99])
                pigIncluded = True

    ca = np.array(ca)

    colors = ca[ca[:,0].argsort()][:,1:]/255.
    cmap = matplotlib.colors.ListedColormap(colors)

    ax.imshow(twoDArray, cmap)

    plt.show()


def readData():
    for j in range(START_LEVEL,GENERATED_LEVELS+1):
        FILE = open("generated_level_{size}x{size}_{number}.txt".format(size = LEVEL_SIZE, number = j), 'r') 
        levelArray = []
        for line in FILE:
            if line == "\n":
                data.append(np.array(levelArray))
                levelArray = []
                continue
            else:
                levelRow = clearLine(line)
                charArrayLength = len(levelRow)
                castedLevelRow = []
                for i in range(0, charArrayLength):
                    if levelRow[i] == '1':  #Ice Material
                        castedLevelRow.append(1) 
                    elif levelRow[i] == '2': #Stone Material
                        castedLevelRow.append(2)
                    elif levelRow[i] == '3': #Wood Material
                        castedLevelRow.append(3)
                    elif levelRow[i] == '4': #Pig
                        castedLevelRow.append(4)
                    else:
                        castedLevelRow.append(0)
                levelArray.append(castedLevelRow)
        if len(levelArray) != 0:
            data.append(np.array(levelArray))
        FILE.close()
    for i in range(len(data)):
        if data[i].size != LEVEL_SIZE * LEVEL_SIZE:
            print(i)

def checkFourDirection(level, i, j):
    if j-1 >= 0 and j-1 < LEVEL_SIZE:
        if level[i][j-1] != 0:
            return False
    if j+1 >= 0 and j+1 < LEVEL_SIZE:
        if level[i][j+1] != 0:
            return False   
    if i-1 >= 0 and i-1 < LEVEL_SIZE:
        if level[i-1][j] != 0:
            return False
    if i+1 >= 0 and i+1 < LEVEL_SIZE:
        if level[i+1][j] != 0:
            return False
    return True

def levelIslandCleaner(level):
    for i in range(LEVEL_SIZE-1): #Cells at the bottom should not be cleared
        for j in range(LEVEL_SIZE):
            if level[i][j] != 0:
                if checkFourDirection(level, i, j):
                    level[i][j] = 0

def generateString(character, count):
    generated = ""
    for i in range(count):
        generated += character
    return generated

def findAll(sentence, word):
    index = sentence.find(word)
    while index != -1:
        yield index
        index = sentence.find(word, index+1)

def findStructures(level):
    levelText = []

    #Looking for horizontal structures
    for i in range(LEVEL_SIZE-1, -1, -1): 
        levelSentence = ""
        for j in range(LEVEL_SIZE):
            levelSentence += str(level[i][j])
        
        ####### Horizontal RectBig #######
        hRectBigSize = blocks_sizes['8'][0]    
        
        for is9ice in findAll(levelSentence, blocks_strings["9ice"]): #Horizontal Ice RectBig 
            for j in range(is9ice, is9ice+hRectBigSize, 1):
                level[i][j] = 23
            levelSentence = levelSentence.replace(blocks_strings["9ice"], generateString('s', hRectBigSize), 1)

        for is9stone in findAll(levelSentence, blocks_strings["9stone"]): #Horizontal Stone RectBig 
            for j in range(is9stone, is9stone+hRectBigSize, 1):
                level[i][j] = 24
            levelSentence = levelSentence.replace(blocks_strings["9stone"], generateString('u', hRectBigSize), 1)

        for is9wood in findAll(levelSentence, blocks_strings["9wood"]): #Horizontal Wood RectBig 
            for j in range(is9wood, is9wood+hRectBigSize, 1):
                level[i][j] = 25
            levelSentence = levelSentence.replace(blocks_strings["9wood"], generateString('w', hRectBigSize), 1)

        
        ####### Horizontal RectMedium #######
        hRectMediumSize = blocks_sizes['6'][0]    
        
        for is8ice in findAll(levelSentence, blocks_strings["8ice"]): #Horizontal Ice RectMedium 
            for j in range(is8ice, is8ice+hRectMediumSize, 1):
                level[i][j] = 17
            levelSentence = levelSentence.replace(blocks_strings["8ice"], generateString('m', hRectMediumSize), 1)

        for is8stone in findAll(levelSentence, blocks_strings["8stone"]): #Horizontal Stone RectMedium 
            for j in range(is8stone, is8stone+hRectMediumSize, 1):
                level[i][j] = 18
            levelSentence = levelSentence.replace(blocks_strings["8stone"], generateString('o', hRectMediumSize), 1)

        for is8wood in findAll(levelSentence, blocks_strings["8wood"]): #Horizontal Wood RectMedium 
            for j in range(is8wood, is8wood+hRectMediumSize, 1):
                level[i][j] = 19
            levelSentence = levelSentence.replace(blocks_strings["8wood"], generateString('q', hRectMediumSize), 1)

        ####### Horizontal RectSmall #######
        hRectSmallSize = blocks_sizes['4'][0]    
        
        for is4ice in findAll(levelSentence, blocks_strings["4ice"]): #Horizontal Ice RectSmall 
            for j in range(is4ice, is4ice+hRectSmallSize, 1):
                level[i][j] = 11
            levelSentence = levelSentence.replace(blocks_strings["4ice"], generateString('g', hRectSmallSize), 1)

        for is4stone in findAll(levelSentence, blocks_strings["4stone"]): #Horizontal Stone RectSmall 
            for j in range(is4stone, is4stone+hRectSmallSize, 1):
                level[i][j] = 12
            levelSentence = levelSentence.replace(blocks_strings["4stone"], generateString('i', hRectSmallSize), 1)

        for is4wood in findAll(levelSentence, blocks_strings["4wood"]): #Horizontal Wood RectSmall 
            for j in range(is4wood, is4wood+hRectSmallSize, 1):
                level[i][j] = 13
            levelSentence = levelSentence.replace(blocks_strings["4wood"], generateString('k', hRectSmallSize), 1)

        ####### Horizontal RectTiny #######
        hRectTinySize = blocks_sizes['2'][0]    
        
        for is2ice in findAll(levelSentence, blocks_strings["2ice"]): #Horizontal Ice RectSmall 
            for j in range(is2ice, is2ice+hRectTinySize, 1):
                level[i][j] = 5
            levelSentence = levelSentence.replace(blocks_strings["2ice"], generateString('a', hRectTinySize), 1)

        for is2stone in findAll(levelSentence, blocks_strings["2stone"]): #Horizontal Stone RectSmall 
            for j in range(is2stone, is2stone+hRectTinySize, 1):
                level[i][j] = 6
            levelSentence = levelSentence.replace(blocks_strings["2stone"], generateString('c', hRectTinySize), 1)

        for is2wood in findAll(levelSentence, blocks_strings["2wood"]): #Horizontal Wood RectSmall 
            for j in range(is2wood, is2wood+hRectTinySize, 1):
                level[i][j] = 7
            levelSentence = levelSentence.replace(blocks_strings["2wood"], generateString('e', hRectTinySize), 1)
        
        levelText.insert(0, levelSentence)
        

    newLevelText = []
    #Looking for vertical structures
    for j in range(LEVEL_SIZE):
        levelSentence = ""
        for i in range(LEVEL_SIZE):
            levelSentence += levelText[i][j]

        ####### Vertical RectBig #######
        vRectBigSize = blocks_sizes['9'][1]    
        
        for is9ice in findAll(levelSentence, blocks_strings["9ice"]): #Vertical Ice RectBig 
            for i in range(is9ice, is9ice+vRectBigSize, 1):
                level[i][j] = 26
            levelSentence = levelSentence.replace(blocks_strings["9ice"], generateString('t', vRectBigSize), 1)

        for is9stone in findAll(levelSentence, blocks_strings["9stone"]): #Vertical Stone RectBig 
            for i in range(is9stone, is9stone+vRectBigSize, 1):
                level[i][j] = 27
            levelSentence = levelSentence.replace(blocks_strings["9stone"], generateString('v', vRectBigSize), 1)

        for is9wood in findAll(levelSentence, blocks_strings["9wood"]): #Vertical Wood RectBig 
            for i in range(is9wood, is9wood+vRectBigSize, 1):
                level[i][j] = 28
            levelSentence = levelSentence.replace(blocks_strings["9wood"], generateString('x', vRectBigSize), 1)

        
        ####### Vertical RectMedium #######
        vRectMediumSize = blocks_sizes['7'][1]    
        
        for is8ice in findAll(levelSentence, blocks_strings["8ice"]): #Vertical Ice RectMedium 
            for i in range(is8ice, is8ice+vRectMediumSize, 1):
                level[i][j] = 20
            levelSentence = levelSentence.replace(blocks_strings["8ice"], generateString('n', vRectMediumSize), 1)

        for is8stone in findAll(levelSentence, blocks_strings["8stone"]): #Vertical Stone RectMedium 
            for i in range(is8stone, is8stone+vRectMediumSize, 1):
                level[i][j] = 21
            levelSentence = levelSentence.replace(blocks_strings["8stone"], generateString('p', vRectMediumSize), 1)

        for is8wood in findAll(levelSentence, blocks_strings["8wood"]): #Vertical Wood RectMedium 
            for i in range(is8wood, is8wood+vRectMediumSize, 1):
                level[i][j] = 22
            levelSentence = levelSentence.replace(blocks_strings["8wood"], generateString('r', vRectMediumSize), 1)

        ####### Vertical RectSmall #######
        vRectSmallSize = blocks_sizes['5'][1]    
        
        for is4ice in findAll(levelSentence, blocks_strings["4ice"]): #Vertical Ice RectSmall 
            for i in range(is4ice, is4ice+vRectSmallSize, 1):
                level[i][j] = 14
            levelSentence = levelSentence.replace(blocks_strings["4ice"], generateString('h', vRectSmallSize), 1)

        for is4stone in findAll(levelSentence, blocks_strings["4stone"]): #Vertical Stone RectSmall 
            for i in range(is4stone, is4stone+vRectSmallSize, 1):
                level[i][j] = 15
            levelSentence = levelSentence.replace(blocks_strings["4stone"], generateString('j', vRectSmallSize), 1)

        for is4wood in findAll(levelSentence, blocks_strings["4wood"]): #Vertical Wood RectSmall 
            for i in range(is4wood, is4wood+vRectSmallSize, 1):
                level[i][j] = 16
            levelSentence = levelSentence.replace(blocks_strings["4wood"], generateString('l', vRectSmallSize), 1)

        ####### Vertical RectTiny #######
        vRectTinySize = blocks_sizes['3'][1]    
        
        for is2ice in findAll(levelSentence, blocks_strings["2ice"]): #Vertical Ice RectSmall 
            for i in range(is2ice, is2ice+vRectTinySize, 1):
                level[i][j] = 8
            levelSentence = levelSentence.replace(blocks_strings["2ice"], generateString('b', vRectTinySize), 1)

        for is2stone in findAll(levelSentence, blocks_strings["2stone"]): #Vertical Stone RectSmall 
            for i in range(is2stone, is2stone+vRectTinySize, 1):
                level[i][j] = 9
            levelSentence = levelSentence.replace(blocks_strings["2stone"], generateString('d', vRectTinySize), 1)

        for is2wood in findAll(levelSentence, blocks_strings["2wood"]): #Vertical Wood RectSmall 
            for i in range(is2wood, is2wood+vRectTinySize, 1):
                level[i][j] = 10
            levelSentence = levelSentence.replace(blocks_strings["2wood"], generateString('f', vRectTinySize), 1)

        newLevelText.insert(0,levelSentence)


def findPigLocations(level):
    pig_locations = []
    for i in range(LEVEL_SIZE): 
        for j in range(LEVEL_SIZE):
            if level[i][j] == 4:
                pig_locations.append([i, j])
    
    if len(pig_locations) != 0:
        return pig_locations
    else:
        #Control floor gaps between structures firstly
        emptyIndex = 0
        while emptyIndex < LEVEL_SIZE-1:
            if level[LEVEL_SIZE-1][emptyIndex] == 0 and level[LEVEL_SIZE-1][emptyIndex+1]:
                if len(pig_locations) < MAX_PIG_COUNT:
                    pig_locations.append([LEVEL_SIZE-1, emptyIndex])
                    level[LEVEL_SIZE-1][emptyIndex] = 4
                emptyIndex += 2 
            else: 
                emptyIndex += 1

        #Control pig sized gaps in structures or gaps on top of structure      
        i = LEVEL_SIZE-1
        while i > 2:
            j = 0
            while j < LEVEL_SIZE-1:
                if level[i][j] != 0 and level[i][j+1] != 0:
                    if level[i-1][j] == 0 and level[i-1][j+1] == 0 and level[i-2][j] == 0 and level[i-2][j+1] == 0 and level[i-3][j] == 0 and level[i-3][j+1] == 0:
                        if len(pig_locations) < MAX_PIG_COUNT:
                            pig_locations.append([i-11, j])
                            level[i-1][j] = 4
                        j += 2
                    else:
                        j += 1
                else:
                    j += 1
            i -= 1
        return pig_locations

def writeLevelXML(levels):
    XML_LEVEL_COUNTER = 1
    for index in range(len(levels)):
        f = open("level-{:02d}.xml".format(XML_LEVEL_COUNTER), "w")

        f.write('<?xml version="1.0" encoding="utf-16"?>\n')
        f.write('<Level width ="2">\n')
        f.write('<Camera x="0" y="2" minWidth="20" maxWidth="30">\n')
        f.write('<Birds>\n')
        f.write('<Bird type="BirdYellow"/>\n')
        f.write('<Bird type="BirdBlue"/>\n') 
        f.write('<Bird type="BirdRed"/>\n')   
        f.write('</Birds>\n')
        f.write('<Slingshot x="-8" y="-2.5">\n')
        f.write('<GameObjects>\n')
        
        level = levels[index]
        levelIslandCleaner(level)
        findStructures(level)
        pig_locations = findPigLocations(level)

        for i in range(LEVEL_SIZE-1, -1, -1):
            j = 0
            while j < LEVEL_SIZE:
                cell = level[i][j]
                if cell != 0 and cell != 4:
                    structure = blocks[str(cell)]
                    structure_size = structure[2]
                    block_name_key = structure[3]
                    material_key = structure[4]

                    if block_name_key in (3,5,7,9):
                        j += 1
                    else: 
                        rotation = 0
                        x_location = absolute_ground_x + (structure_size * tiny_block_size[0])/2 + j * tiny_block_size[0]
                        y_location = absolute_ground_y + tiny_block_size[1]/2 + (LEVEL_SIZE-1-i) * tiny_block_size[1] 
                        
                        f.write('<Block type="%s" material="%s" x="%s" y="%s" rotation="%s" />\n' % (block_names[str(block_name_key)], materials[str(material_key)], str(x_location), str(y_location), str(rotation)))
                        j += structure_size
                else:
                    j += 1

        for j in range(LEVEL_SIZE):
            i = LEVEL_SIZE - 1
            while i >= 0:
                cell = level[i][j]
                if cell != 0 and cell != 4:
                    structure = blocks[str(cell)]
                    structure_size = structure[2]
                    block_name_key = structure[3]
                    material_key = structure[4]

                    if block_name_key in (3,5,7,9):
                        rotation = 90
                        x_location = absolute_ground_x + tiny_block_size[0]/2 + j * tiny_block_size[0]
                        y_location = absolute_ground_y + (structure_size * tiny_block_size[1])/2 + (LEVEL_SIZE-1-i) * tiny_block_size[1] 
                        
                        f.write('<Block type="%s" material="%s" x="%s" y="%s" rotation="%s" />\n' % (block_names[str(block_name_key)], materials[str(material_key)], str(x_location), str(y_location), str(rotation)))
                        i -= structure_size
                    else: 
                        i -= 1
                else:
                    i -= 1

        
        for i in range(LEVEL_SIZE-1, -1, -1):
            for j in range(LEVEL_SIZE):
                if level[i][j] == 4:
                    pig_x_location = absolute_ground_x + tiny_block_size[0] + j * tiny_block_size[0]
                    pig_y_locations = absolute_ground_y + tiny_block_size[0] + (LEVEL_SIZE-1-i) * tiny_block_size[1] 
                    f.write('<Pig type="BasicSmall" material="" x="%s" y="%s" rotation="0" />\n' % (str(pig_x_location),str(pig_y_locations)))

        f.write('</GameObjects>\n')
        f.write('</Level>\n')

        f.close()

        XML_LEVEL_COUNTER = XML_LEVEL_COUNTER + 1


readData()
levels = np.array(data)


#for index in range(len(levels)):
#    level = levels[index]
#    draw(level) 

writeLevelXML(levels)


