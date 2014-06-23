#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""

A simple game based on 1980's BEAST.EXE

20140623 gwillem@gmail.com

"""

import curses
import unittest
import math
import logging
import time

from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import shuffle
import sys

logger = logging.getLogger(__file__)


class Config:

    TICK_TIME = 50  # ms
    MONSTER_DELAY = 20  # relative to speed of player
    MONSTER_NUM = 10
    SAND_NUM = 600

    # http://unicodeemoticons.com/cool_text_icons_and_pictures.htm
    if sys.version_info < (3, 3):
        ICONS = {
            'monster': 'X',
            'hero': 'C',
            'sand': ' ',
            'rock': '#'
        }
    else:
        ICONS = {
            'monster': 'X',
            'hero': '☺',
            'sand': ' ',
            'rock': '◼'
        }


class Board:

    layout = ((3, 10), (3, 15), (3, 17), (3, 21), (3, 23), (3, 24), (3, 25), (3, 26), (3, 27), (3, 30), (3, 31), (3, 32), (3, 33), (3, 34), (3, 35), (3, 37), (3, 38), (3, 39), (3, 40), (3, 41), (3, 44), (3, 49), (3, 52), (3, 53), (3, 54), (3, 55), (3, 58), (3, 59), (3, 60), (3, 61), (3, 62), (3, 65), (3, 66), (3, 67), (3, 68), (3, 69), (3, 70), (4, 10), (4, 15), (4, 18), (4, 20), (4, 23), (4, 28), (4, 30), (4, 37), (4, 42), (4, 44), (4, 45), (4, 49), (4, 51), (4, 56), (4, 58), (4, 63), (4, 65), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15), (5, 19), (5, 23), (5, 28), (5, 30), (5, 31), (5, 32), (5, 33), (5, 34), (5, 37), (5, 42), (5, 44), (5, 46), (5, 49), (5, 51), (5, 56), (5, 58), (5, 63), (5, 65), (5, 66), (5, 67), (5, 68), (5, 69), (6, 10), (6, 15), (6, 19), (6, 23), (6, 24), (6, 25), (6, 26), (6, 27), (6, 30), (6, 37), (6, 38), (6, 39), (6, 40), (6, 41), (6, 44), (6, 47), (6, 49), (6, 51), (6, 56), (6, 58), (6, 63), (6, 65), (7, 10), (7, 15), (7, 19), (7, 23), (7, 30), (7, 37), (7, 41), (7, 44), (7, 48), (7, 49), (7, 51), (7, 56), (7, 58), (7, 63), (7, 65), (8, 10), (8, 15), (8, 19), (8, 23), (8, 30), (8, 31), (8, 32), (8, 33), (8, 34), (8, 35), (8, 37), (8, 42), (8, 44), (8, 49), (8, 52), (8, 53), (8, 54), (8, 55), (8, 58), (8, 59), (8, 60), (8, 61), (8, 62), (8, 65), (8, 66), (8, 67), (8, 68), (8, 69), (8, 70), (11, 15), (11, 16), (11, 17), (11, 18), (11, 21), (11, 26), (11, 28), (11, 29), (11, 30), (11, 31), (11, 32), (11, 35), (11, 40), (11, 42), (11, 44), (11, 49), (11, 52), (11, 53), (11, 54), (11, 55), (11, 58), (11, 59), (11, 60), (11, 61), (11, 62), (12, 14), (12, 21), (12, 26), (12, 28), (12, 33), (12, 35), (12, 40), (12, 42), (12, 44), (12, 49), (12, 51), (12, 56), (12, 58), (12, 63), (13, 15), (13, 16), (13, 17), (13, 18), (13, 21), (13, 26), (13, 28), (13, 33), (13, 35), (13, 40), (13, 42), (13, 44), (13, 49), (13, 51), (13, 56), (13, 58), (13, 63), (14, 19), (14, 21), (14, 26), (14, 28), (14, 29), (14, 30), (14, 31), (14, 32), (14, 35), (14, 40), (14, 42), (14, 44), (14, 49), (14, 51), (14, 56), (14, 58), (14, 59), (14, 60), (14, 61), (14, 62), (15, 14), (15, 19), (15, 21), (15, 26), (15, 28), (15, 32), (15, 36), (15, 39), (15, 42), (15, 45), (15, 48), (15, 51), (15, 56), (15, 58), (15, 62), (16, 15), (16, 16), (16, 17), (16, 18), (16, 22), (16, 23), (16, 24), (16, 25), (16, 28), (16, 33), (16, 37), (16, 38), (16, 42), (16, 46), (16, 47), (16, 52), (16, 53), (16, 54), (16, 55), (16, 58), (16, 63))

    @classmethod
    def wrap(cls, loc, dimy, dimx):
        """ Convert out-of-bounds coordinates """
        y, x = loc

        if x == 0: x = dimx - 2
        if y == 0: y = dimy - 2

        if x == dimx - 1: x = 1
        if y == dimy - 1: y = 1

        return y, x

    def unwrap(self, loc, dimy, dimx):
        pass


class Colors(object):

    sand = 1
    hero = 2
    monster = 3

    @classmethod
    def setup(cls):
        curses.start_color()
        curses.use_default_colors()
        # -1 = transparent
        curses.init_pair(cls.sand, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(cls.hero, curses.COLOR_GREEN, -1)
        curses.init_pair(cls.monster, curses.COLOR_RED, -1)


class Game(object):

    def __init__(self):

        curses.initscr()
        self.dim_y = 20
        self.dim_x = 80
        # this is the viewport, the playing field runs from 1 to dim-2 (inclusive)

        self.loop_id = 0

        win = curses.newwin(self.dim_y, self.dim_x, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)

        Colors.setup()

        win.border(0)
        win.nodelay(1)
        win.addstr(0, 3, " Hyperbeast v0.1 ")

        self.win = win

        self.monsters = []
        self.sand = []
        self.rocks = []

        all_cells = [(y, x) for y in range(1, self.dim_y-1) for x in range(1, self.dim_x-1)]
        shuffle(all_cells)

        for pos in Board.layout:
            self.sand.append(pos)
            self.print_actor(pos, 'sand')
            all_cells.remove(pos)

        self.hero = all_cells.pop()
        self.print_actor(self.hero, 'hero')

        for _ in range(Config.MONSTER_NUM):
            l = all_cells.pop()
            self.monsters.append(l)
            self.print_actor(l, 'monster')

        # for _ in range(SAND_NUM):
        #     l = all_cells.pop()
        #     self.sand.append(l)
        #     self.print_actor(l, 'sand')

    def print_ch(self, loc, char, *arg, **kwarg):
        self.win.addch(loc[0], loc[1], char, *arg, **kwarg)

    def print_actor(self, loc, actor):
        self.print_ch(loc, Config.ICONS[actor], curses.color_pair(getattr(Colors, actor)) | curses.A_BOLD)

    def mainloop(self):
        # used to maintain player vs monster speed difference, as monsters only get to move on MOD x loops
        self.loop_id = 0
        while True:
            self.loop_id += 1
            self.win.refresh()
            self.win.timeout(0)
            self.move_hero()
            if not self.loop_id % Config.MONSTER_DELAY:
                self.move_monsters()
            time.sleep(Config.TICK_TIME / 1000.0)  # bah, int division default under 2.7

    def move_monsters(self):
        for i, oldpos in enumerate(self.monsters):
            cur_distance = self.dist(oldpos, self.hero)

            # only take adj that are not sand|blocks|monsters
            adj = [x for x in self.adjacents(*oldpos) if x not in self.sand and x not in self.monsters]

            # only take adj that are closer to hero
            adj = [x for x in adj if self.dist(self.hero, x) < cur_distance]

            if not adj:
                # there's nothing closer
                # self.debug("Monster not moved @ %s (cur distance: %s" %
                #            (str(monster),
                #            cur_distance))
                continue

            # sort on hero distance
            adj.sort(key=lambda x: self.dist(self.hero, x))
            newpos = adj[0]

            if newpos == self.hero:
                self.endgame("Poof, you're dead!")

            self.print_ch(oldpos, ' ')
            self.print_actor(newpos, 'monster')
            self.monsters[i] = newpos

            # self.debug("Moved monster from %s to %s (because %s < %s)" %
            #            (str(monster),
            #             str(newpos),
            #             self.dist(self.hero, newpos),
            #             cur_distance
            #            ))

    @staticmethod
    def endgame(msg):
        curses.endwin()
#        self.win.addstr(msg)
        print(msg + "\n\n")
        time.sleep(1)
        sys.exit(0)

    def adjacents(self, y, x):
        """
        Generate all direct 1-step neighbours for (x,y)
        """
        neighbours = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):

                # skip center
                if delta_y == 0 and delta_x == 0:
                    continue

                # skip out of bounds
                if y + delta_y in (0, self.dim_y - 1):
                    continue
                if x + delta_x in (0, self.dim_x - 1):
                    continue

                neighbours.append((y + delta_y, x + delta_x))

        return neighbours

    @staticmethod
    def dist(q, p):
        """ Distance """
        return math.hypot(p[0] - q[0], p[1] - q[1])

    def add_loc(self, q, p):
        """ Add two vectors / coordinates, wrap borders """

        newloc = tuple(map(sum, zip(q, p)))
        return Board.wrap(newloc, self.dim_y, self.dim_x)

    def debug(self, msg):
        logger.info("[%4d] %s" % (self.loop_id, msg))

    def find_next_non_sand_cell(self, loc, direction):
        for _ in range(100):
            loc = self.add_loc(loc, direction)
            if loc not in self.sand:
                return loc
        raise RuntimeError("Oops, couldnt find non-sand cell!")

    def move_hero(self):

        # nonblocking, as configured in __init__
        key = self.win.getch()

        if key == -1:
            return

        direction = (key == KEY_DOWN and 1) + (key == KEY_UP and -1), \
                    (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)

        newpos = self.add_loc(self.hero, direction)

        # cannot move into monsters
        if newpos in self.monsters:
            self.endgame("Poof, you're dead!")

        # cannot move into rock
        if newpos in self.rocks:
            return

        if newpos in self.sand:
            # now, iteralively, iterate into direction to find next non-sand block
            # is it empty : move sand item here
            next_non_sand_pos = self.find_next_non_sand_cell(newpos, direction)

            # did we hit a rock?
            if next_non_sand_pos in self.rocks:
                return

            # did we hit a monster?
            if next_non_sand_pos in self.monsters:
                # only squash monster, if the NEXT non-sand block is rock or sand
                behind_monster_pos = self.add_loc(next_non_sand_pos, direction)
                if behind_monster_pos not in self.rocks + self.sand:
                    return

                self.monsters.remove(next_non_sand_pos)
                if not self.monsters:
                    self.endgame("Hurray, all monsters slayed!")

            # now, move sand!
            self.sand.remove(newpos)
            self.sand.append(next_non_sand_pos)
            self.print_actor(next_non_sand_pos, 'sand')

        newpos = Board.wrap(newpos, self.dim_y, self.dim_x)

        # Did I move?
        if self.hero == newpos:
            return

        self.print_ch(self.hero, ' ')
        self.print_actor(newpos, 'hero')

        self.hero = newpos
        self.debug("Move hero to %s" % str(self.hero))
        # self.debug(1, "Pos hero: %s, %s " % self.hero)


def setlogger():
    hdlr = logging.FileHandler('beast.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger.info("Game started")


def main(stdscr):
    game = Game()
    game.mainloop()

if __name__ == '__main__':
    setlogger()
    curses.wrapper(main)


class TestClass(unittest.TestCase):

    def test_adjacents(self):
        g = Game()
        n = g.adjacents(5, 5)
        assert len(n) == 8, n
        assert (6, 6) in n, n

    def test_dist(self):
        q = (0, 0)
        p = (3, 2)
        n = Game.dist(q, p)
        assert abs(n - math.sqrt(13)) < 0.000001, n
