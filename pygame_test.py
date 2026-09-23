import pygame

block_size = 40 #Set the size of the grid block
grid_size = 18
window_width = grid_size * block_size
window_height = grid_size * block_size
white = (200, 200, 200)
black = (0, 0, 0)
screen = pygame.display.set_mode((window_width, window_height))

def draw_grid():
    for x in range(0, window_width, block_size):
        for y in range(0, window_height, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, white, rect, 1)

def main():
    pygame.init()  # starts up pygame's internals
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Boar Trial")  # window title

    clock = pygame.time.Clock()

    running = True
    while running:
        # Handle events (input) that happened since the last frame
        screen.fill(black)  # clear screen to black each frame
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # player clicked the window's close button
                running = False
            if event.type == pygame.KEYDOWN:  # a key was pressed
                if event.key == pygame.K_UP:
                    print("up arrow pressed")
                elif event.key == pygame.K_DOWN:
                    print("down arrow pressed")
                # K_LEFT, K_RIGHT similarly

        # show what we just drew
        pygame.display.flip()

        clock.tick(30)  # limit to 30 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()