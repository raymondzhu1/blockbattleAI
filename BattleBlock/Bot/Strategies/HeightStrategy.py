# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Strategies.AbstractStrategy import AbstractStrategy

class HeightStrategy(AbstractStrategy):
    def __init__(self, game):
        AbstractStrategy.__init__(self, game)
        self.game = game
        self._actions = ['left', 'right', 'turnleft', 'turnright', 'down', 'drop']


    def space(self):
        count = 0 #holes
        col = 0
        row = 0
        done = 0 #have you done the append to heightNum
        #gone = 0 #gone through rows at least once
        aggregate = 0
        heightNum = []
        ones = []
        print(self.game.me.field.field)
        while (col < self.game.me.field.width):
            free = 0 #0 is false
            done = 0
            row = 0
            # if gone == 1:
            # 	col += 1
            #gone = col
            while (row < self.game.me.field.height):
                if self.game.me.field.field[row][col] > 1:
                    free = 1 #true
                    if done == 0:
                        aggregate = aggregate + (self.game.me.field.height - row) + 1
                        heightNum.append((self.game.me.field.height - row))
                        done = 1
                    row += 1
                    if row == self.game.me.field.height:
                        col += 1
                    # if done == 0 and row == self.game.me.field.height:
                    # 	heightNum = heightNum.append(0)
                    # 	done = 1
                    #gone = 1
                elif self.game.me.field.field[row][col] > 1 and free == 1:
                    count += 1
                    row += 1
                    if row == self.game.me.field.height:
                        col += 1
                    #gone = 1
                else:
                    if self.game.me.field.field[row][col] == 1:
                        ones.append([[row], [col]])
                    row += 1
                    #gone = 1
                    #print(row)
                    if row == self.game.me.field.height:
                        col += 1
                    if done == 0 and row == self.game.me.field.height:
                        heightNum.append(0)
                        done = 1
            print(heightNum)
        return count, aggregate, heightNum, ones


    def choose(self):
        _, _, height, loc = self.space()
        count = 1
        index = 0
        least = height[0]
        greatPos = loc[0][1][0]
        moves = []
        diff = 0
        dropped = 0
        while (count < len(height)):
            if(least > height[count]):
                least = height[count]
                index = count
            count += 1
        for x, y in loc:
            if(greatPos > y[0]):
                greatPos = y[0]
        diff = index - greatPos
        while (greatPos > 0):
            # print(least)
            # print(greatPos)
            if diff >= 1:
                moves.append('right')
                greatPos = greatPos - 1
            if diff <= -1:
                moves.append('left')
                greatPos = greatPos - 1
            if diff == 0:
                moves.append('drop')
                dropped = 1
                greatPos = 0
        if dropped == 0:
            moves.append('drop')
        return moves
