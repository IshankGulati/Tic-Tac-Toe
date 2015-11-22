# -*- coding: utf-8 -*-
"""Tic Tac Toe"""

# Author: Ishank Gulati <gulati.ishank@gmail.com>

from __future__ import print_function, division
import pygame as pg
import os

NO_VAL = 0
X_VAL = 1
O_VAL = 2
TIE_VAL = -1

buttons =\
    {'reset': (20, 300),
     'ai': (720, 600),
     'player': (20, 600)}

config =\
    {'fullscreen': False,
     'visibmouse': True,
     'width': 800,
     'height': 800,
     'back_color': (255, 255, 255),
     'font_ratio': 10,
     'font_color': (0, 0, 255),
     'fps': 60,
     'mess_font_ratio': 20,
     'button_font_ratio': 35,
     'button_color': (255, 0, 0),
     'button_font_color': (255, 255, 255),
     'button_height': 40,
     'button_width': 70,
     'player_width': 150,
     'player_height': 150,
     'title': "Tic Tac Toe  (Play with Numpad, press Esc to exit)"}


class GameState:
    PLAYING, EXIT = range(2)


class AiMove:
    def __init__(self, score=0):
        self.row = None
        self.col = None
        self.score = score


class PygView(object):

    CURSORKEYS = slice(257, 266)
    QUIT_KEYS = pg.K_ESCAPE, pg.K_q
    MOVES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    EVENTS = 'reset', 'start_pl', 'start_ai'

    def __init__(self, controller, config, buttons):
        self.width = config.width
        self.height = config.height
        self.back_color = config.back_color
        self.fps = config.fps
        self.font_color = config.font_color
        self.button_font_color = config.button_font_color
        self.controller = controller
        self.buttons = buttons
        self.button_color = config.button_color
        self.button_height = config.button_height
        self.button_width = config.button_width
        self.player_height = config.player_height
        self.player_width = config.player_width

        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.init()
        flags = pg.DOUBLEBUF | [0, pg.FULLSCREEN][config.fullscreen]
        self.screen = pg.display.set_mode((self.width, self.height), flags)
        pg.display.set_caption(config.title)
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(config.visibmouse)
        self.font_button = pg.font.Font(None, self.height // config.button_font_ratio)
        self.font = pg.font.Font(None, self.height // config.font_ratio)
        self.font_mess = pg.font.Font(None, self.height // config.mess_font_ratio)

    def frame_duration(self):
        return 0.001 * self.clock.get_time()

    def run(self):
        self._setup()
        running = True
        while running:
            self.clock.tick_busy_loop(self.fps)
            running = self.controller.dispatch(self.get_events())
            self.flip()
        else:
            self.quit()

    def _setup(self):
        self.screen.fill(self.back_color)
        self.background = pg.image.load(os.path.join("data", "base.gif"))
        self.background = self.background.convert_alpha()
        self.x = pg.image.load(os.path.join("data", "x.png"))
        self.x = pg.transform.scale(self.x, (self.player_width, self.player_height))
        self.x = self.x.convert_alpha()
        self.o = pg.image.load(os.path.join("data", "o.png"))
        self.o = pg.transform.scale(self.o, (self.player_width, self.player_height))
        self.o = self.o.convert_alpha()
        self.screen.blit(self.background, (100, 100))
        self.background_rect = self.background.get_rect(center = (self.width // 2, self.height // 2))
        self.draw_text("Tic Tac Toe", self.font, 243, 20)
        self.draw_button("Reset", self.buttons.reset[0], self.buttons.reset[1])
        self.draw_button("You Start", self.buttons.player[0], self.buttons.player[1])
        self.draw_button("Bot Start", self.buttons.ai[0], self.buttons.ai[1])
        self.flip()

    def get_click(self, key):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if key[0] + self.button_width > mouse[0] > key[0] and key[1] + self.button_height > mouse[1] > key[1]:
            if click[0] == 1:
                return True
        return False

    def get_events(self):
        click_event = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 'quit', None, click_event
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()[PygView.CURSORKEYS]
                move_events = [e for e, k in zip(PygView.MOVES, keys) if k]
                if event.key in PygView.QUIT_KEYS:
                    return 'quit', move_events, click_event
                else:
                    return 'other_key', move_events, click_event
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.get_click(self.buttons.reset):
                    click_event = 'reset'
                if self.get_click(self.buttons.player):
                    click_event = 'start_pl'
                if self.get_click(self.buttons.ai):
                    click_event = 'start_ai'

                return None, None, click_event
        else:
            return None, None, None

    def draw_text(self, text, font, x, y):
        # w, h = self.font.size(text)
        surface = font.render(text, True, self.font_color)
        self.screen.blit(surface, (x, y))

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.button_font_color)
        return textSurface, textSurface.get_rect()

    def draw_button(self, text, x, y):
        pg.draw.rect(self.screen, self.button_color, (x, y, self.button_width, self.button_height))
        textSurf, textRect = self.text_objects(text, self.font_button)
        textRect.center = ((x + (self.button_width // 2)), (y + (self.button_height // 2)))
        self.screen.blit(textSurf, textRect)

    def draw_player(self, i, j):
        self.screen.blit(self.x, (125+200*i, 125+200*j))
        self.flip()

    def draw_ai(self, i, j):
        self.screen.blit(self.o, (125+200*i, 125+200*j))
        self.flip()

    def reset(self):
        self.screen.fill(self.back_color, (100, 700, 600, 100))
        self.screen.blit(self.background, (100, 100))
        self.flip()

    def clear(self):
        self.screen.fill(self.back_color, rect=self.background_rect)
        self.flip()

    def flip(self):
        pg.display.flip()

    def quit(self):
        pg.quit()


class Controller(object):
    def __init__(self, config, buttons):
        self.view = PygView(self, config, buttons)
        self._gameState = GameState.PLAYING
        self._game = Game(config)
        # self._game.reset()

    def run(self):
        self.view.run()

    def dispatch(self, all_events):
        event, move_events, click_event = all_events
        if event == 'quit':
            return False

        events = move_events, click_event

        if self._gameState == GameState.PLAYING:
            self._gameState = self._game.process(self.view, events)
            return True

        if self._gameState == GameState.EXIT:
            if click_event == 'reset':
                self._gameState = GameState.PLAYING
                self._game.reset(self.view)

        return True


class AI(object):
    def __init__(self):
        self._aiPlayer = O_VAL
        self._humanPlayer = X_VAL

    def performMove(self, view, board):
        bestMove = self.MiniMax(board, self._aiPlayer)
        board.setVal(bestMove.row, bestMove.col, self._aiPlayer)
        view.draw_ai(bestMove.col, bestMove.row)

    def MiniMax(self, board, player, depth=0):
        status = board.checkVictory()
        if status == self._aiPlayer:
            return AiMove(10-depth)
        elif status == self._humanPlayer:
            return AiMove(-10)
        elif status == TIE_VAL:
            return AiMove(0)

        moves = []

        for row in xrange(board._size):
            for col in xrange(board._size):
                if board.getVal(row, col) == NO_VAL:
                    move = AiMove()
                    move.row = row
                    move.col = col
                    board.setVal(row, col, player)
                    if player == self._aiPlayer:
                        move.score = self.MiniMax(board, self._humanPlayer, depth+1).score
                    else:
                        move.score = self.MiniMax(board, self._aiPlayer, depth+1).score
                    moves.append(move)
                    board.setVal(row, col, NO_VAL)

        if player == self._aiPlayer:
            bestScore = -10000
            for idx, move in enumerate(moves):
                if move.score > bestScore:
                    bestScore = move.score
                    bestMove = idx
        if player == self._humanPlayer:
            bestScore = 10000
            for idx, move in enumerate(moves):
                if move.score < bestScore:
                    bestScore = move.score
                    bestMove = idx
        return moves[bestMove]


class Game(object):
    MAP = [(2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 1),
           (0, 2)]

    def __init__(self, config):
        self.config = config
        self._currentPlayer = X_VAL
        self._aiPlayer = O_VAL
        self._humanPlayer = X_VAL
        self._board = Board()
        self._ai = AI()

    def playerMove(self, view, event):
        loc = Game.MAP[event-1]
        if self._board.getVal(loc[0], loc[1]) == NO_VAL:
            self._board.setVal(loc[0], loc[1], self._currentPlayer)
            view.draw_player(loc[1], loc[0])
            self.changePlayer()

    def aiMove(self, view):
        self._ai.performMove(view, self._board)
        self.changePlayer()

    def reset(self, view):
        self._currentPlayer = X_VAL
        self._board.clear()
        view.reset()

    def process(self, view, events):
        move_events, click_event = events

        if click_event == 'start_pl':
            self._currentPlayer = self._humanPlayer
        elif click_event == 'start_ai':
            self._currentPlayer = self._aiPlayer

        if self._currentPlayer == self._aiPlayer:
            self.aiMove(view)
        else:
            if move_events != None:
                for event in move_events:
                    self.playerMove(view, event)

        status = self._board.checkVictory()
        if status != NO_VAL:
            self.endGame(view, status == TIE_VAL)
            return GameState.EXIT

        return GameState.PLAYING

    def endGame(self, view, wasTie):
        if wasTie:
            view.draw_text("Tie Game", view.font_mess, 338, 720)
            view.draw_text("Press Reset button to play or Esc to Quit", view.font_mess, 125, 770)
        else:
            if self._currentPlayer == self._aiPlayer:
                view.draw_text("You win", view.font_mess, 338, 720)
                view.draw_text("Press Reset button to play or Esc to Quit", view.font_mess, 125, 770)
            else:
                view.draw_text("AI wins", view.font_mess, 338, 720)
                view.draw_text("Press Reset button to play or Esc to Quit", view.font_mess, 125, 770)
        view.flip()

    def changePlayer(self):
        if self._currentPlayer == self._aiPlayer:
            self._currentPlayer = self._humanPlayer
        else:
            self._currentPlayer = self._aiPlayer


class Board(object):
    def __init__(self):
        self._size = 3
        self._board = [[NO_VAL for i in xrange(self._size)]
                       for i in xrange(self._size)]

    def clear(self):
        for i in xrange(self._size):
            for j in xrange(self._size):
                self._board[i][j] = NO_VAL

    def setVal(self, x, y, val):
        self._board[x][y] = val

    def getVal(self, x, y):
        return self._board[x][y]

    def checkVictory(self):
        # check rows
        victory = False
        for row in xrange(self._size):
            player = self.getVal(0, row)
            if player != NO_VAL:
                victory = True
                for col in xrange(1, self._size):
                    if self.getVal(col, row) != player:
                        victory = False
                        break
                if victory is True:
                    return player

        # checking columns
        for col in xrange(self._size):
            player = self.getVal(col, 0)
            if player != NO_VAL:
                victory = True
                for row in xrange(1, self._size):
                    if self.getVal(col, row) != player:
                        victory = False
                        break
                if victory is True:
                    return player

        # left diagonal
        player = self.getVal(0, 0)
        if player != NO_VAL:
            victory = True
            for diag in xrange(1, self._size):
                if self.getVal(diag, diag) != player:
                    victory = False
            if victory is True:
                return player

        # right diagonal
        player = self.getVal(0, self._size-1)
        if player != NO_VAL:
            victory = True
            for diag in xrange(1, self._size):
                if self.getVal(diag, self._size - diag - 1) != player:
                    victory = False
            if victory is True:
                return player

        # no victory
        for row in xrange(self._size):
            for col in xrange(self._size):
                if self.getVal(row, col) is NO_VAL:
                    return NO_VAL

        return TIE_VAL


class Config(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Buttons(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def main():
    Controller(Config(**config), Buttons(**buttons)).run()

if __name__ == "__main__":
    main()
