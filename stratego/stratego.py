#!/usr/bin/env python 

import sys
import pygame
from pygame import *

BOARD_OFFSET_X = 16
BOARD_OFFSET_Y = 16
TILE_SIZE = 48
PIECE_SIZE = 36
PIECE_OFFSET = (TILE_SIZE - PIECE_SIZE) / 2

pygame.init()
screen = pygame.display.set_mode((1024,500))
pygame.display.set_caption("Stratego with Love")

images = {}


def load_images():
    for piece_char in [str(x) for x in range(1,10)] + ['s', 'b', 'f']:
        print piece_char
        images['red' + piece_char] = image.load('red' + piece_char + '.png').convert()
        images['blue' + piece_char] = image.load('blue' + piece_char + '.png').convert()
    images['board'] = image.load('board.png').convert()
    images['crosshairs'] = image.load('crosshairs.png').convert()
    images['crosshairs'].set_colorkey((255,0,128), RLEACCEL)

def grid_to_screen(coords):
    x, y = coords
    return ((x*TILE_SIZE)+BOARD_OFFSET_X, (y*TILE_SIZE)+BOARD_OFFSET_Y)

def screen_to_grid(coords):
    x, y = coords
    return (((x-BOARD_OFFSET_X)/TILE_SIZE), ((y-BOARD_OFFSET_Y)/TILE_SIZE))

def align_to_grid(coords):
    x, y = coords
    return (((x-BOARD_OFFSET_X)/TILE_SIZE)*TILE_SIZE+BOARD_OFFSET_X, ((y-BOARD_OFFSET_Y)/TILE_SIZE)*TILE_SIZE+BOARD_OFFSET_Y)

load_images()

dragging_piece = None
dragging_offset = ()
board = [
[images['red1'], images['red2'], images['red3'], images['red3'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue1'], images['blue2'], images['blue3'], images['blue3']],
[images['red4'], images['red4'], images['red4'], images['red5'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue4'], images['blue4'], images['blue4'], images['blue5']],
[images['red5'], images['red5'], images['red5'], images['red6'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue5'], images['blue5'], images['blue5'], images['blue6']],
[images['red6'], images['red6'], images['red6'], images['red7'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue6'], images['blue6'], images['blue6'], images['blue7']],
[images['red7'], images['red7'], images['red7'], images['red8'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue7'], images['blue7'], images['blue7'], images['blue8']],
[images['red8'], images['red8'], images['red8'], images['red8'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue8'], images['blue8'], images['blue8'], images['blue8']],
[images['red9'], images['red9'], images['red9'], images['red9'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue9'], images['blue9'], images['blue9'], images['blue9']],
[images['red9'], images['red9'], images['red9'], images['red9'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blue9'], images['blue9'], images['blue9'], images['blue9']],
[images['reds'], images['redb'], images['redb'], images['redb'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blues'], images['blueb'], images['blueb'], images['blueb']],
[images['redb'], images['redb'], images['redb'], images['redf'], None,  None, None, None, None, None, None, None, None, None, None,  None, images['blueb'], images['blueb'], images['blueb'], images['bluef']]
]


clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = screen_to_grid(mouse_pos)
            hover_piece = board[y][x]
            board[y][x] = None
            if hover_piece != None:
                dragging_piece = hover_piece
                dragging_offset = (mouse_pos[0] - (x*TILE_SIZE+BOARD_OFFSET_X+PIECE_OFFSET), mouse_pos[1] - (y*TILE_SIZE+BOARD_OFFSET_Y+PIECE_OFFSET))
        elif event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if dragging_piece != None:
                gridx, gridy = screen_to_grid((x, y))
                board[gridy][gridx] = dragging_piece
                dragging_piece = None


    screen.blit(images['board'], (BOARD_OFFSET_X, BOARD_OFFSET_Y))

    x, y = BOARD_OFFSET_X, BOARD_OFFSET_Y
    for row in board:
        for piece in row:
            if piece != None:
                screen.blit(piece, (x+PIECE_OFFSET,y+PIECE_OFFSET))
            x+=TILE_SIZE
        x = BOARD_OFFSET_X
        y+=TILE_SIZE


    screen.blit(images['crosshairs'], align_to_grid(pygame.mouse.get_pos()))
    if dragging_piece != None:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(dragging_piece, (mouse_pos[0] - dragging_offset[0], mouse_pos[1] - dragging_offset[1]))
    pygame.display.flip()
    clock.tick(30)
