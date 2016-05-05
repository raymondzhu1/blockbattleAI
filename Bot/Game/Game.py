# -*- coding: utf-8 -*-
# Python3.4*

from Bot.Game.Player import Player


class Game:
    def __init__(self):
        self.timebank = 0
        self.timePerMove = 0

        self.enemy = Player()
        self.me = Player()

        self.piece = None
        self.pieceType = None
        self.piecePosition = None
        self.nextPiece = None
        #self.down = False
        self.round = 0
