import sys
import pygame
import numpy as np

from Cell import Cell


class Game:
    def __init__(self):
        pygame.init()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.GREY = (192, 192, 192)

        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.block_size = 40
        self.x_size = self.WINDOW_WIDTH // self.block_size  # Get cell count along x-axis
        self.y_size = self.WINDOW_HEIGHT // self.block_size  # Get cell count along y-axis
        self.cell_sprites = pygame.sprite.Group()  # Create group for sprites to be added

        self.start = (-1, -1)  # Start and target nodes selected by user
        self.target = (-1, -1)

        pygame.display.set_caption("\"Maze\" Solving")
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.SCREEN.fill(self.BLACK)
        self.CLOCK = pygame.time.Clock()
        self.cells = np.zeros((self.x_size, self.y_size))
        self.init_sprites()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Close Game
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    x_pos, y_pos = pygame.mouse.get_pos()  # gets current mouse position
                    curr_coord = (x_pos // self.block_size, y_pos // self.block_size)
                    if event.key == pygame.K_s:  # places start node at mouse position when 's' is pressed
                        for sprites in self.cell_sprites:
                            if sprites.rect.collidepoint(x_pos, y_pos):
                                self.cells = sprites.update(self.cells, 2)
                                if self.start == (-1, -1):
                                    self.start = curr_coord
                                else:
                                    self.start = (-1, -1)
                    elif event.key == pygame.K_e:  # places start node at mouse position when 'e' is pressed
                        for sprites in self.cell_sprites:
                            if sprites.rect.collidepoint(x_pos, y_pos):
                                self.cells = sprites.update(self.cells, 3)
                                if self.target == (-1, -1):
                                    self.target = curr_coord
                                else:
                                    self.target = (-1, -1)
                    elif event.key == pygame.K_BACKSPACE:  # If backspace is pressed, resets grid
                        self.cells = np.zeros((self.x_size, self.x_size))
                        self.start, self.target = (-1, -1), (-1, -1)
                    elif event.key == pygame.K_d:  # Performs DFS to find target node
                        self.depth_first()
                    elif event.key == pygame.K_b:  # Performs BFS to find target node
                        self.breadth_first()
            self.draw_obstacles()  # Draws our "walls"
            self.update_cells()  # Updates cell images
            self.cell_sprites.draw(self.SCREEN)
            self.create_grid()  # Creates our gridlines
            self.CLOCK.tick(60)
            pygame.display.update()

    def draw_obstacles(self):
        x_pos, y_pos = pygame.mouse.get_pos()  # Get mouse position
        click = pygame.mouse.get_pressed()  # Get mouse click action
        if click[0] == True:  # While we have left-click held down, draw our walls continuously
            for sprites in self.cell_sprites:
                if sprites.rect.collidepoint(x_pos, y_pos):
                    self.cells = sprites.update(self.cells, 4)
        elif click[2] == True:  # Same as above but for right-click
            for sprites in self.cell_sprites:
                if sprites.rect.collidepoint(x_pos, y_pos):
                    self.cells = sprites.update(self.cells, 1)

    def update_cells(self):  # First makes the board all
        for sprites in self.cell_sprites:  # Turns board into empty board. Helpful for when we reset
            sprites.image.fill(self.BLACK)
        for white_cells in zip(*np.where(self.cells == 1)):
            # Wherever cells are white or = 1, find sprites and change image
            r, c = white_cells
            for sprites in self.cell_sprites:
                if sprites.rect.collidepoint(r * self.block_size, c * self.block_size):
                    sprites.image.fill(self.WHITE)
        for grey_cells in zip(*np.where(self.cells == 4)):
            # Same idea as above for wall cells
            r, c = grey_cells
            for sprites in self.cell_sprites:
                if sprites.rect.collidepoint(r * self.block_size, c * self.block_size):
                    sprites.image.fill(self.GREY)
        for sprites in self.cell_sprites:  # From class variables for start/target nodes, update their appearance
            start_r, start_c = self.start
            target_r, target_c = self.target
            if sprites.rect.collidepoint(start_r * self.block_size, start_c * self.block_size):
                sprites.image.fill(self.GREEN)
            elif sprites.rect.collidepoint(target_r * self.block_size, target_c * self.block_size):
                sprites.image.fill(self.RED)

    def init_sprites(self):
        for w, h in np.ndindex(self.cells.shape):
            self.cell_sprites.add(Cell(w, h, self.block_size))  # Add our sprites to our Sprite Group

    def create_grid(self):
        for w, h in np.ndindex(self.cells.shape):
            rect = pygame.Rect(w * self.block_size, h * self.block_size, self.block_size, self.block_size)
            pygame.draw.rect(self.SCREEN, (200, 200, 200), rect, 1)

    def get_neighbors(self, coord):
        r, c = coord
        res = []
        neighbors = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
        # Gets neighbors from N --> E --> S --> W
        for neighbor in neighbors:
            curr_r, curr_c = neighbor
            if (0 <= curr_r < self.x_size and 0 <= curr_c < self.y_size) and self.cells[curr_r, curr_c] != 4:
                # If neighbor is within cell bounds and not a wall, we add it to result
                res.append((curr_r, curr_c))
        return res

    def breadth_first(self):  # iterative BFS
        queue = [self.start]
        visited = set(self.start)
        while queue:
            for _ in range(len(queue)):
                curr = queue.pop(0)
                if curr == self.target:
                    return
                r, c = curr
                for sprites in self.cell_sprites:
                    if sprites.rect.collidepoint(r * self.block_size, c * self.block_size):
                        self.cells = sprites.update(self.cells)
                        self.create_grid()
                        pygame.display.flip()
                self.cell_sprites.draw(self.SCREEN)
                self.CLOCK.tick(60)
                neighbors = self.get_neighbors(curr)
                for neighbor in neighbors:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    queue.append(neighbor)

    def depth_first(self):  # iterative DFS
        stack = [self.start]
        visited = set(self.start)
        while stack:
            curr = stack.pop()
            r, c = curr
            if curr == self.target:
                return
            for sprites in self.cell_sprites:
                if sprites.rect.collidepoint(r * self.block_size, c * self.block_size):
                    self.cells = sprites.update(self.cells)
                    self.create_grid()
                    pygame.display.flip()
            self.cell_sprites.draw(self.SCREEN)
            self.CLOCK.tick(60)
            neighbors = self.get_neighbors(curr)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                stack.append(neighbor)


def main():
    Game()


if __name__ == "__main__":
    main()
