# -*- coding: utf-8 -*-
# Python3.4*

import copy


class Field:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.field = [[0]*self.width]*self.height

    def size(self):
        return self.width, self.height

    def updateField(self, field):
        self.field = field

    def projectPieceDown(self, piece, offset):
        piecePositions = self.__offsetPiece(piece.positions(), offset)

        field = None
        for height in range(0, self.height-1):
            tmp = self.fitPiece(piecePositions, [0, height])

            if not tmp:
                break
            field = tmp

        return field

    @staticmethod
    def __offsetPiece(piecePositions, offset, turn=None):
        #in GA algorithm we use piecePositions as an array of [x, y] pos of blocks
        #Make optional parameter named
        piece = copy.deepcopy(piecePositions)
        if turn == None:
            #piece = copy.deepcopy(piecePositions)
            for pos in piece:
                pos[0] += offset[0]
                pos[1] += offset[1]
            return piece

        else:
            for pos, off in zip(piece, offset):
                print(pos[0])
                print(off[0]) #This is a numer, int cannot take index of it.
                pos[0] += off[0]
                pos[1] += off[1]
            return piece

    def __checkIfPieceFits(self, piecePositions):
        for x, y in piecePositions:
            if 0 <= x < self.width and 0 <= y < self.height:
                if self.field[y][x] > 1: #self.field is different from field in fitpiece
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, offset=None, turn=None, wantField=None):
        #use this to check for what happens to board for the moves it got
        #change so that it gives the piece, unless requested through a parameter
        #that's optional, otherwise default to None.
        #Let piecePositions be leftmost piece being operated on.
        if offset:
            piece = self.__offsetPiece(piecePositions, offset, turn)
        else:
            piece = piecePositions

        field = copy.deepcopy(self.field)
        if self.__checkIfPieceFits(piece):
            for x, y in piece:
                field[y][x] = 4
            if wantField != None:
                return field
            else:
                return piece
        else:
            return None
