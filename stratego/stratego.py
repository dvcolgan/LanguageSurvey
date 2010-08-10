#!/usr/bin/env python 

import sys
import pygame
from pygame import *
import socket
import sys
import cPickle

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

dragging_piece = '.'
dragging_offset = ()
dragging_start = ()
board = [
['red1', 'red2', 'red3', 'red3', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue1', 'blue2', 'blue3', 'blue3'],
['red4', 'red4', 'red4', 'red5', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue4', 'blue4', 'blue4', 'blue5'],
['red5', 'red5', 'red5', 'red6', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue5', 'blue5', 'blue5', 'blue6'],
['red6', 'red6', 'red6', 'red7', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue6', 'blue6', 'blue6', 'blue7'],
['red7', 'red7', 'red7', 'red8', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue7', 'blue7', 'blue7', 'blue8'],
['red8', 'red8', 'red8', 'red8', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue8', 'blue8', 'blue8', 'blue8'],
['red9', 'red9', 'red9', 'red9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue9', 'blue9', 'blue9', 'blue9'],
['red9', 'red9', 'red9', 'red9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blue9', 'blue9', 'blue9', 'blue9'],
['reds', 'redb', 'redb', 'redb', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blues', 'blueb', 'blueb', 'blueb'],
['redb', 'redb', 'redb', 'redf', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'blueb', 'blueb', 'blueb', 'bluef']
]


clock = pygame.time.Clock()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9999))
board = cPickle.loads(sock.recv(10000))
sock.setblocking(0)

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sock.close()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sock.close()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = screen_to_grid(mouse_pos)
            hover_piece = board[y][x]
            board[y][x] = '.'
            if hover_piece != '.':
                dragging_piece = hover_piece
                dragging_offset = (mouse_pos[0] - (x*TILE_SIZE+BOARD_OFFSET_X+PIECE_OFFSET), mouse_pos[1] - (y*TILE_SIZE+BOARD_OFFSET_Y+PIECE_OFFSET))
                dragging_start = (x, y)
        elif event.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if dragging_piece != '.':
                gridx, gridy = screen_to_grid((x, y))
                board[gridy][gridx] = dragging_piece
                dragging_piece = '.'
                sock.send('move:'+cPickle.dumps((dragging_start,(gridx, gridy))))

    try:
        board = cPickle.loads(sock.recv(100000))
        print 'got new board state'
    except Exception, e:
        pass


    screen.blit(images['board'], (BOARD_OFFSET_X, BOARD_OFFSET_Y))

    x, y = BOARD_OFFSET_X, BOARD_OFFSET_Y
    for row in board:
        for piece in row:
            if piece != '.':
                screen.blit(images[piece], (x+PIECE_OFFSET,y+PIECE_OFFSET))
            x+=TILE_SIZE
        x = BOARD_OFFSET_X
        y+=TILE_SIZE


    screen.blit(images['crosshairs'], align_to_grid(pygame.mouse.get_pos()))
    if dragging_piece != '.':
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(images[dragging_piece], (mouse_pos[0] - dragging_offset[0], mouse_pos[1] - dragging_offset[1]))
    pygame.display.flip()
    clock.tick(30)
