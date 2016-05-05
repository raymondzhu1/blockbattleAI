from Bot.Strategies.AbstractStrategy import AbstractStrategy
import numpy as np

class RLStrategy(AbstractStrategy):
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
        aggregate = 0
        bumpiness = 0
        whenCalc = []
        completeLiners = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Each index represents a row.
        while (col < len(actualField[0])):
            free = 0
            done = 0
            row = 0
            while (row < len(actualField)): #Change this to go from top to bottom instead of bottom to top.
                if actualField[row][col] > 1:
                    free = 1
                    if actualField[row][col] != 3:
                        completeLiners[row] += 1
                    if done == 0:
                        aggregate = aggregate + (len(actualField) - row) #Change to just row + 1
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


    def completeLines(self, arr):
        #Returns number of complete lines in an array from function space.
        #Except for 1 liners, they aren't worth any points so we avoid
        #clearing them to try to grab more clears.
        count = 0
        for x in arr:
            if x == self.game.me.field.width:
                count += 1
        if count == 0:
            return 0
        elif count == 1:
            return -0.3
        else:
            return count


    def bumpiness(self, arr):
        #Returns bumpiness of field given an array of heights for each column in the field.
        bump = 0
        count = 0
        while count < (len(arr) - 1):
            bump += abs(arr[count] - arr[count+1])
            count += 1
        return bump


    def top(self, arr):
        #Simple function that just checks if any of the rows are in the
        #0th row, if it is we REALLY don't want that field clone.
        #If x == 0 return 100 and the weight will be -1 or lower to make
        #sure any choice with x == 0 is not chosen if possible.
        theMax = 0
        for x, y in arr:
            if x == 0:
                theMax = 100
        return theMax


    def reward(self, field, newPos):
        #Fitness function, which is just our heuristic of our reinforcement learning.
        #Planned to reward bot per round for their piece placement on board, based
        #off of some features.
        fieldCopy = copy.deepcopy(field)
        a = -0.581203
        b = 0.66066
        c = -0.41
        d = -0.2
        g = -1
        count, aggregate, heightArr, comp = self.space(fieldCopy)
        clear = self.completeLines(comp)
        bump = self.bumpiness(heightArr)
        tops = self.top(newPos)
        return a*aggregate + b*clear + c*count + d*bump + g*tops


    def choose(self):
        moves = []
        lastRoundFit = self.reward(self.game.me.field.field)
        moves.append('drop')
        return moves