#!/usr/bin/env python3

import pygame
import sys

# game loop
def gameLoop():
    """

    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(60)

# main function
def main():
    """

    """
    gameLoop()

if __name__ == "__main__":
    print("Bongani")
    main()

