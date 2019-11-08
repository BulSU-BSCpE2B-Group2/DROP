import pygame
import random
import settings

# initialize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption("MY GAME")
pygame.display.update()