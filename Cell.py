import pygame
import numpy as np
from Board import Board

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GREY = (192, 192, 192)


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, block_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((block_size, block_size))  # Create a block_size x block_size surface for sprite
        self.image.fill(BLACK)  # Fill cell with black
        self.rect = self.image.get_rect()  # Obtain the coordinates contained in our cell
        self.rect.x = x * block_size  # Get start upper-left coord of our rectangle
        self.rect.y = y * block_size
        self.block_size = block_size

    def update(self, cells, status=0):
        x_val, y_val = self.rect.x // self.block_size, self.rect.y // self.block_size
        if status == 1:
            self.image.fill(BLACK)  # If status == 1, we revert to original fill color, BLACK
            cells[x_val][y_val] = 0
            return cells
        elif status == 2:
            if cells[x_val][y_val] == 2:
                self.image.fill(BLACK)
                cells[x_val][y_val] = 0
            else:
                self.image.fill(GREEN)
                cells[x_val][y_val] = 2
            return cells
        elif status == 3:
            if cells[x_val][y_val] == 3:
                self.image.fill(BLACK)
                cells[x_val][y_val] = 0
            else:
                self.image.fill(RED)
                cells[x_val][y_val] = 3
            return cells
        elif status == 4:
            self.image.fill(GREY)
            cells[x_val][y_val] = 4
            return cells
        else:
            # The above gives us the corresponding index for our cell in our sparse matrix
            if cells[x_val][y_val] == 0:
                self.image.fill(WHITE)
                cells[x_val][y_val] = 1
            return cells
