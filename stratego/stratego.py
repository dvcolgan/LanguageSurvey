#!/usr/bin/env python 

import sys
import pygame
from pygame import *

BOARD_OFFSET_X = 32
BOARD_OFFSET_Y = 32
TILE_SIZE = 48

pygame.init()
screen = pygame.display.set_mode((1024,500))
pygame.display.set_caption("Stratego with Love")

images = {}

pieces = {
'R11':images['red'],
'R21':images['red'],
'R31':images['red'],
'R32':images['red'],
'R41':images['red'],
'R42':images['red'],
'R43':images['red'],
'R11':images['red'],
'R11':images['red'],
'R11':images['red'],


}

def init_sprites():

def load_images():
    for piece_char in [str(x) for x in range(1,10)] + ['s', 'b', 'f']:
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
    return ((x/TILE_SIZE), y/TILE_SIZE)

def align_to_grid(coords):
    x, y = coords
    return (((x-BOARD_OFFSET_X)/TILE_SIZE)*TILE_SIZE+BOARD_OFFSET_X, ((y-BOARD_OFFSET_Y)/TILE_SIZE)*TILE_SIZE+BOARD_OFFSET_Y)

load_images()

clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        
    screen.blit(images['board'], (BOARD_OFFSET_X, BOARD_OFFSET_Y))
    screen.blit(images['crosshairs'], align_to_grid(pygame.mouse.get_pos()))
    pygame.display.flip()
    clock.tick(30)
