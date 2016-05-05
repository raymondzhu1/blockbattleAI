# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.AbstractStrategy import AbstractStrategy
from random import choice, random, uniform
import copy

class GeneticStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self.game = game
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']


    def space(self, field=None):
        #Returns number of holes, aggregate height, height of each column, and the number of clears and which row it was.
        actualField = self.game.me.field.field
        if field != None:
            actualField = field
        count = 0
        col = 0
        row = 0
        done = 0
        #clocked = 0
        aggregate = 0
        bumpiness = 0
        whenCalc = []
        completeLiners = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Each index represents a row.
        while (col < len(actualField[0])):
            free = 0
            done = 0
            row = 0
            while (row < len(actualField)):
                if actualField[row][col] > 1:
                    free = 1
                    if actualField[row][col] != 3:
                        completeLiners[row] += 1
                    if done == 0:
                        aggregate = aggregate + (len(actualField) - row)
                        whenCalc.append(len(actualField) - row)
                        done = 1
                    row += 1
                    if row == len(actualField):
                        col += 1
                elif actualField[row][col] == 0 and free == 1:
                    count += 1
                    row += 1
                    if row == len(actualField):
                        col += 1
                else:
                    row += 1
                    if done == 0 and row == len(actualField):
                        whenCalc.append(0)
                        done = 1
                    if row == len(actualField):
                        col += 1
        return count, aggregate, whenCalc, completeLiners


    def checkFit(self, piecePositions, field=None):
        #Checks if the piece will fit, given the positions of the blocks in the piece.
        actualField = self.game.me.field.field
        if field != None:
            actualField = field
        for x, y in piecePositions:
            if 0 <= x < len(actualField) and 0 <= y < len(actualField[0]):
                if actualField[x][y] > 1 and actualField[x][y] != 4:
                    return False
            else:
                return False
        return True


    def updateTurn(self, left, rest, turn, field=None):
        #The piece.positions() will give you the offsets for left most piece.
        #Return a field that is updated with the new rotation.
        #left for left most piece, turn = offset of the turn for left most block.
        #rest is all the coordinates for the piece on the field.
        theField = copy.deepcopy(self.game.me.field.field)
        pos = []
        counter = 0
        if field != None:
            theField = copy.deepcopy(field)
        for x, y in rest:
            theField[x][y] = 0
        for x, y in turn:
            if (left[0]+x) >= len(theField) or (left[1]+y) >= len(theField[0]):
                return field, False, None
            # theField[left[0]+x][left[1]+y] = 1
            pos.append([left[0]+x, left[1]+y])
            if self.checkFit(pos, theField) == True:
                counter += 1
                theField[left[0]+x][left[1]+y] = 1
        if counter == 4:
            return theField, True, pos
        return field, False, rest


    def updateHorizontal(self, piecePositions, offset, field=None):
        #Moves horizontally.
        #Will not work well with current choose function because
        #in close games will collide with another block, causing it to drop.
        #Edit the choose function to be smarter in its move selection.
        actualField = copy.deepcopy(self.game.me.field.field)
        pos = []
        counter = 0
        if field != None:
            actualField = copy.deepcopy(field)
        for x, y in piecePositions:
            actualField[x][y] = 0
        for x, y in piecePositions:
            if (offset[0]+x) >= len(actualField) or (y+offset[1]) >= len(actualField[0]):
                return field, False, None
            # actualField[x+offset[0]][y+offset[1]] = 1
            pos.append([x+offset[0], y+offset[1]])
            if self.checkFit(pos, actualField) == True:
                counter += 1
                actualField[x+offset[0]][y+offset[1]] = 1
        # if self.checkFit(pos, actualField) == True:
        #     return actualField, True, pos
        if counter == 4:
            return actualField, True, pos
        return field, False, piecePositions


    def leftMost(self, field=None):
        #Calculate left most block in piece being operated on in [row, col] format.
        #Returns left most block separately from all [row, col] in piece (this includes the left most).
        theField = self.game.me.field.field
        if field != None:
            theField = field
        count = 0
        left = 0
        row = 0
        col = 0
        leftCoord = []
        allCoord = []
        while row < len(theField) and count < 4:
            col = 0
            while col < len(theField[0]) and count < 4:
                if theField[row][col] == 1:
                    allCoord.append([row, col])
                    if count == 0:
                        left = col
                        count += 1
                        leftCoord = [row, col]
                    else:
                        if left > col:
                            left = col
                            leftCoord = [row, col]
                        count += 1
                col += 1
                if col == len(theField[0]):
                    row += 1
        return leftCoord, allCoord


    def parseChoice(self, choices, field=None):
        #Old function, no longer used.
        #Used to parse choices of words to offsets.
        #This was used in original GA implementation.
        moves = []
        pieceCopy = self.game.piece
        fieldCopy = self.game.me.field.field
        if field != None:
            fieldCopy = copy.deepcopy(field)
        for commands in choices:
            if commands == 'left':
                moves.append([0, -1])
            if commands == 'right':
                moves.append([0, 1])
            if commands == 'turnleft':
                #left, allCoord = leftMost(fieldCopy)
                pieceCopy.turnLeft(1)
                #newField = updateTurn(fieldCopy, left, allCoord, pieceCopy.positions())
                #rot = pieceCopy.positions()
                # for x in range(4):
                #     moves.append(rot[x])
                moves.append(pieceCopy.positions()) #for turns only use position
                #of block left most, do not give all the block positions.
            if commands == 'turnright':
                #left, allCoord = leftMost(fieldCopy)
                pieceCopy.turnRight(1)
                #newField = updateTurn(fieldCopy, left, allCoord, pieceCopy.positions())

                #rot = pieceCopy.positions()
                # for x in range(4):
                #     moves.append(rot[x])
                moves.append(pieceCopy.positions())
        #print(moves)
        return moves


    def completeLines(self, arr):
        #Returns number of complete lines in an array from function space.
        #Except for 1 liners, they aren't worth any points so we avoid
        #clearing them to try to grab more clears.
        count = 0
        for x in arr:
            if x == self.game.me.field.width:
                count += 1
        #if count == 0 or count == 1:
        if count == 0:
            return 0
        elif count == 1:
            return -0.2
        else:
            return count


    def bumpiness(self, arr):
        #Returns bumpiness of field given an array of heights for each column in the field.
        bump = 0
        count = 0
        badCols = 0
        while count < (len(arr) - 1):
            bump += abs(arr[count] - arr[count+1])
            if bump >= 3:
                badCols += 1
            count += 1
        return bump, badCols


    def justHeight(self, field=None):
        #Instead of going through function space for the height array
        #use this function, less run time.
        newField = self.game.me.field.field
        if field != None:
            newField = field
        row = 0
        col = 0
        heightArr = []
        while col < len(newField[0]):
            row = 0
            while row < len(newField):
                if newField[row][col] > 1:
                    heightArr.append(len(newField) - row)
                    row = len(newField)
                    col += 1
                elif row == (len(newField) - 1):
                    heightArr.append(0)
                    col += 1
                row += 1
        return heightArr



    def walls(self, arr, field=None):
        #Feature to calculate in our fitness function.
        #Checks the number of blocks that is 1 block away.
        #Positive feature, helps reduce holes more for the future.
        #Picks moves better when holes are equal for two or more positions.
        wall = 0
        actualField = self.game.me.field.field
        if field != None:
            actualField = field
        for x, y in arr:
            if x != (len(actualField) - 1) and x != 0:
                if actualField[x+1][y] > 1 and actualField[x+1][y] != 4:
                    wall += 1
                if actualField[x-1][y] > 1 and actualField[x-1][y] != 4:
                    wall += 1
            if y != 0 and y != (len(actualField[0]) - 1):
                if actualField[x][y+1] > 1 and actualField[x][y+1] != 4:
                    wall += 1
                if actualField[x][y-1] > 1 and actualField[x][y-1] != 4:
                    wall += 1
            elif x != 0:
                if actualField[x-1][y] > 1 and actualField[x-1][y] != 4:
                    wall += 1
                if y == 0:
                    if actualField[x][y+1] > 1 and actualField[x][y+1] != 4:
                        wall += 1
                if y == (len(actualField[0]) - 1):
                    if actualField[x][y-1] > 1 and actualField[x][y-1] != 4:
                        wall += 1
        return wall


    def projectDown(self, piecePosition, arr, field=None):
        #Let arr be the array of heights you calculate.
        theField = copy.deepcopy(self.game.me.field.field)
        pos = []
        newArr = []
        anArr = []
        #iBrokePython3 = 0
        maxRow = 0
        maxHeight = 0
        count = 0
        over = 0
        if field != None:
            theField = copy.deepcopy(field)
        #print(theField)
        tmpField = [[0]*self.game.me.field.width]*self.game.me.field.height
        for x, y in piecePosition:
            newArr.append([x+1, y])
            if self.checkFit(newArr, field) == False:
                over = 2
            theField[x][y] = 0
            theField[x+1][y] = 4
        while over == 0:
            tmpField = copy.deepcopy(theField)
            pos = copy.deepcopy(newArr)
            count = 0
            for x, y in newArr:
                #print(newArr)
                anArr = copy.deepcopy(newArr)
                anArr[count][0] = x+1
                if x + 1 == len(theField) or x >= len(theField):
                    over = 1
                else:
                    #print(anArr)
                    if self.checkFit(anArr, field) == True:
                        newArr[count][0] = x + 1
                        count += 1
                        #print(newArr)
                        theField[x][y] = 0
                        theField[x+1][y] = 4
                        #print(theField)
                    else:
                        over = 1
        if over == 1:
            for x, y in pos:
                tmpField[x][y] = 4
            return tmpField, pos, True
        else:
            return field, piecePosition, True
        # for x, y in piecePosition:
        #     newArr.append([0, arr[y]])
        #     if maxHeight < arr[y]:
        #         maxHeight = arr[y]
        #     if maxRow < x:
        #         maxRow = x
        # for x, y in zip(piecePosition, newArr): #was for x, y in piecePosition
        #     #if (arr[0]+x) >= len(theField) or (y+arr[1]) >= len(theField[0]):
        #     #print(x[0]+((len(theField)-y[1])-1))
        #     # print(field)
        #     # print(((len(theField)-y[1])-1))
        #     # print(x[0])
        #     # print(((len(theField)-y[1])-1)-x[0])
        #     if (((len(theField)-maxHeight)-1)) >= len(theField) or (x[1]+y[0]) >= len(theField[0]):
        #         return field, pos, False
        #     theField[x[0]][x[1]] = 0
        #     if x[0] == maxRow:
        #         theField[((len(theField)-maxHeight)-1)][x[1]+y[0]] = 4
        #         #theField[((len(theField)-y[1])-1)-x[0]][x[1]+y[0]] = 4
        #         pos.append([((len(theField)-maxHeight)-1), x[1]+y[0]])
        #     else:
        #         # print((len(theField)-y[1]))
        #         # print((maxRow - x[0]))
        #         # print(((len(theField)-y[1])-1-(maxRow - x[0])))
        #         # print(x[1]+y[0])
        #         theField[((len(theField)-maxHeight)-1-(maxRow - x[0]))][x[1]+y[0]] = 4
        #         #theField[((len(theField)-y[1])-1)-x[0]][x[1]+y[0]] = 4
        #         pos.append([((len(theField)-maxHeight)-1-(maxRow - x[0])), x[1]+y[0]])
        #     #theField[x][y] = 0
        #     #theField[x+arr[0]][y+arr[1]] = 4
        #     #pos.append([x+arr[0], y+arr[1]])
        #return theField, pos, True


    def top(self, arr):
        #Simple function that just checks if any of the rows are in the
        #0th row, if it is we REALLY don't want that field clone.
        #If x == 0 return 200 and the weight will be -10 to make
        #sure any choice with x == 0 is not chosen if possible.
        theMax = 0
        for x, y in arr:
            if x == 0:
                theMax = 200
        return theMax


    def maximum(self, arr):
        theMax = 0
        for x in arr:
            if theMax < x:
                theMax = x
        return theMax


    def perfectClear(self, field, comp):
    # Check if comp, array of row clear from space function, cleared any lines.
    # Then check if all those clears cleared the board by checking if 
    # any of the rows, beside the rows cleared, have int values greater than 1.
    # Not used in current version. 
    # Not tested yet, use with your own risk.
        count = 0
        clearCount = 0
        row = 0
        col = 0
        cleared = []
        over = 0
        for x in comp:
            if x == self.game.me.field.width:
                cleared.append(clearCount)
            clearCount += 1
        if len(cleared) >= 1:
            while row < len(field) and over != 1:
                col = 0
                while col < len(field[0]) and over != 1:
                    if field[row][col] > 1 and row != cleared[count]:
                        over = 1
                    if row == cleared[count] and len(cleared) > 1:
                        count += 1
                    col += 1
                    if col == len(field[0]):
                        row += 1
        if over == 1:
            return 0
        else:
            return 1


        #e = -0.14
        #pos = []
        #def fitness(self, choices):
        # moves = self.parseChoice(choices)
        # fieldCopy = copy.deepcopy(self.game.me.field.field)
        # pieceCopy = copy.deepcopy(self.game.piece)
        # #count = 0
        # for x in range(len(moves)):
        #     #print(fieldCopy.size())
        #     #pieceCopy = fieldCopy.__offsetPiece(pieceCopy, moves[x])
        #     if choices[x] != 'turnleft' and choices[x] != 'turnright':
        #         #pieceCopy = fieldCopy.fitPiece(pieceCopy.positions(), moves[x])
        #         if x < len(moves)-1:
        #             if choices[x] == 'right' and choices[x+1] != 'left':
        #                 _, allCoord = self.leftMost(fieldCopy)
        #                 fieldCopy, bol, pos = self.updateHorizontal(allCoord, moves[x], fieldCopy)
        #                 if bol == False:
        #                     return -100
        #             elif choices[x] == 'left' and choices[x+1] != 'right':
        #                 _, allCoord = self.leftMost(fieldCopy)
        #                 fieldCopy, bol, pos = self.updateHorizontal(allCoord, moves[x], fieldCopy)
        #                 if bol == False:
        #                     return -100
        #         else:
        #             _, allCoord = self.leftMost(fieldCopy)
        #             fieldCopy, bol, pos = self.updateHorizontal(allCoord, moves[x], fieldCopy)
        #             if bol == False:
        #                 return -100
        #     else:
        #         # turn = True
        #         # pieceCopy = fieldCopy.fitPiece(pieceCopy.positions(), moves[x], turn)
        #         if x < len(moves)-1:
        #             if choices[x] == 'turnright' and choices[x+1] != 'turnleft':
        #                 left, allCoord = self.leftMost(fieldCopy)
        #                 fieldCopy, bol, pos = self.updateTurn(left, allCoord, moves[x], fieldCopy)
        #                 if bol == False:
        #                     return -100

        #             elif choices[x] == 'turnleft' and choices[x+1] != 'turnright':
        #                 left, allCoord = self.leftMost(fieldCopy)
        #                 fieldCopy, bol, pos = self.updateTurn(left, allCoord, moves[x], fieldCopy)
        #                 if bol == False:
        #                     return -100
        #         else:
        #             left, allCoord = self.leftMost(fieldCopy)
        #             fieldCopy, bol, pos = self.updateTurn(left, allCoord, moves[x], fieldCopy)
        #             if bol == False:
        #                 return -100
        # heightArr = self.justHeight(fieldCopy)
        # newField, newPos, yes = self.projectDown(pos, heightArr, fieldCopy)
        # if yes == False:
        #     return -100


    def badCol(self, arr, field):
        count = 0
        blackCount = 0
        row = 19
        col = 0
        over = 0
        while row >= 0 and over != 1:
            col = 0
            while col < len(field[0]) and over != 1:
                if field[row][col] != 3:
                    over = 1
                if field[row][col] == 3:
                    row -= 1
                    col = 0
                    blackCount += 1
                else:
                    col += 1
                    if col == len(field[0]):
                        row -= 1
        for x in arr:
            if x == blackCount:
                count += 1
        return count


    def fitness(self, field, newPos):
        #Fitness function, which is just our heuristic of our graph search.
        #Originally was going to use GA, so didn't change the name of this function.
        fieldCopy = copy.deepcopy(field)
        #a = -0.510066
        #a = -0.44166
        a = -0.58066
        #a = -0.38066
        #b = 0.760666
        b = 0.760666
        c = -0.41
        #c = -0.35663
        d = -0.2
        #d = -0.18566
        #e = -0.15
        e = -0.4
        f = 0.1
        #f = 0.2
        g = -10
        h = -0.5
        #h = -0.3
        #z = 10
        wall = self.walls(newPos, fieldCopy)
        count, aggregate, heightArr, comp = self.space(fieldCopy)
        clear = self.completeLines(comp)
        bump, bigDiff = self.bumpiness(heightArr)
        tops = self.top(newPos)
        big = self.maximum(heightArr)
        noIBlockSpace = self.badCol(heightArr, fieldCopy)
        #perfect = self.perfectClear(fieldCopy, comp)
        return a*aggregate + b*clear + c*count + d*bump + g*tops + e*big + f*wall + h*noIBlockSpace


    def mutaterate(self, bestParent):
        #Not quite working yet.
        #Function not used in current version.
        #Used to calculate the mutation rate of the best parent in
        #a population.
            return ((15.2 + self.fitness(bestParent))/400)


    def mutate(self, sequence, rate):
        #Actually do the mutation given the rate from the above function.
        #Old function, not used in the current version.
        moves = []
        for element in sequence:
            if random() <= rate:
                moves.append(element)
            else:
                moves.append(choice(['left', 'right', 'turnleft', 'turnright']))
        return moves
        #return [(move if random() <= rate else choice(['left', 'right', 'turnleft', 'turnright']) for move in sequence)]


    def mate(self, a, b):
        #Does the mating between two parents to have two offsprings.
        #Do choice, split location, on smallest parent so that smallest
        #parent is split up properly.
        #Old function, not used in the current version.
        place = 0
        if choice(range(10)) < 7:
            if len(a) < len(b):
                place = choice(range(len(a)))
            else:
                place = choice(range(len(b)))
        else:
            return a, b
        a1 = a[:place]
        a1.extend(b[place:])
        b1 = b[:place]
        b1.extend(a[place:])
        return a1, b1


    def get_lucky(self, items):
        #Not used in the current version.
        #Part of the GA implementation.
        weight_total = sum((item[1] for item in items))
        n = uniform(0, weight_total)
        for item, weight in items:
            if n < weight:
                return item
            n = n - weight
        return item


    def maxFitness(self, arr):
        #Not used in the current version.
        #Part of the GA implementation.
        theMax = 0
        bestParent = []
        for x, y in arr:
            if theMax < y:
                bestParent = x
                theMax = y
        return bestParent, theMax


    def prepPiece(self, pieceType, allPos, field=None):
        #Simulate a drop in the piece so analysis can be done.
        #Also adds blocks to the field copy so that we can analyze
        #all the blocks that are actually in the field according
        #to the engine.
        #Note: I block does not need to be taken account for
        #individually because all blocks are present initially.
        #Just need to move it down so turns can be done properly.
        actualField = copy.deepcopy(self.game.me.field.field)
        if field != None:
            actualField = copy.deepcopy(field)
        for x, y in allPos:
            actualField[x][y] = 0
            actualField[x+1][y] = 1
        lefty = allPos[0][1]
        for x, y in allPos:
            if lefty > y:
                lefty = y
        if pieceType == "J":
            actualField[0][lefty] = 1
        if pieceType == "L":
            actualField[0][lefty+2] = 1
        if pieceType == "O":
            actualField[0][lefty] = 1
            actualField[0][lefty+1] = 1
        if pieceType == "S":
            actualField[0][lefty+1] = 1
            actualField[0][lefty+2] = 1
        if pieceType == "T":
            actualField[0][lefty+1] = 1
        if pieceType == "Z":
            actualField[0][lefty-1] = 1
            actualField[0][lefty] = 1
        return actualField


    def has1(self, arr, field):
        for x, y in arr:
            if field[x][y] == 1:
                return True
        return False


    def choose(self):
        #Fix stuff like removing the non-turn moves from best array
        #So doesn't overlap into bestMoves array. #I think fixed now with if block.
        #and slicing array by :count, to get first count elements, which
        #causes all the turns to appear first. #Fixed
        #2nd bug: Only calculate what was initially on field given by engine.
        #Need to calculate the position of blocks not shown on field in order
        #to calculate the moves correctly. #Fixed
        #Offset the piece here by moving down 1 row by self.game.pieceLetter
        #and their respective positions. #Done
        #Chooses the moves to be done given current information of the
        #field, pieces, etc..
        best = []
        bestMoves = []
        bestScore = -1000
        lefty = 0
        count = 0
        fit = 0
        leftyCount = 0
        newField = self.game.me.field.field
        tmpField = []
        tmpPos = []
        turnField = []
        pieceCopy = copy.deepcopy(self.game.piece)
        while count < 4:
            _, allPos = self.leftMost(self.game.me.field.field)
            if count == 0:
                #print(newField)
                newField = self.prepPiece(self.game.pieceType, allPos)
                turnField = copy.deepcopy(newField)
            left, allPos = self.leftMost(turnField) #Used to be newField
            pieceCopy.turnRight(1)
            newField, bol, newPos = self.updateTurn(left, allPos, pieceCopy.positions(), turnField)
            turnField = copy.deepcopy(newField)
            #newField, bol, newPos = self.updateTurn(left, allPos, pieceCopy.positions(), newField)
            if count > 0:
                best = best[:count]
            if bol != False:
                best.append('turnright')
            # if bol == False:
            #     count += 1
            # else:
            lefty = newPos[0][1]
            for x, y in newPos:
                if lefty > y:
                    lefty = y
            yOffset = lefty
            newField, bol, newPos = self.updateHorizontal(newPos, [0, -yOffset], newField)
            while leftyCount < abs(yOffset):
                best.append('left')
                leftyCount += 1
            leftyCount = 0
                # if bol == False:
                #     count += 1
                #else:
            while bol != False:
                heightArr = self.justHeight(newField)
                tmpField, tmpPos, bol = self.projectDown(newPos, heightArr, newField)
                        # if bol == False:
                        #     fit = 0
                            #count += 1
                        #else:
                # if bol == False:
                #     fit = 0
                fit = self.fitness(tmpField, tmpPos)
                if self.has1(tmpPos, tmpField) == True:
                    fit = -1000
                if bestScore < fit:
                            # print(newField)
                    #print(tmpField)
                    bestScore = fit
                    bestMoves = copy.deepcopy(best)
                newField, bol, newPos = self.updateHorizontal(newPos, [0, 1], newField) #Bug: if block in way to right, while loop will immmediately stop, even if more free blocks after that block.
                best.append('right')
            count += 1
        bestMoves.append('drop')
        return bestMoves

        # # GA choose function below, still very random and no idea when
        # # to stop iterating. Very slow as well.
        # moves = ['left', 'right', 'turnleft', 'turnright']
        # populationSize = 10
        # iteration = 0
        # maxSize = 10
        # bestParent = [choice(moves) for _ in (range(choice(range(maxSize))+1))]
        # perfection = 15.2
        # #while self.fitness(bestParent) != perfection:
        # while iteration < 20 and self.fitness(bestParent) != perfection:
        #     rate = self.mutaterate(bestParent)
        #     iteration += 1
        #     if iteration == 1:
        #         population = [self.mutate(bestParent, rate) for _ in range(populationSize)] + [bestParent]
        #     data = []
        #     for individual in population:
        #         fitness_val = self.fitness(individual)
        #         pair = (individual, fitness_val)
        #         data.append(pair)
        #     population = []
        #     for _ in range(int(populationSize/2)):
        #         parent1 = self.get_lucky(data)
        #         parent2 = self.get_lucky(data)
        #         child1, child2 = self.mate(parent1, parent2)
        #         population.append(self.mutate(child1, rate))
        #         population.append(self.mutate(child2, rate))
        #     bestParent = max(population, key=self.fitness)
        # bestParent.append('drop')
        # return bestParent