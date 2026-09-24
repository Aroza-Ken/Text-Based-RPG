import pygame
import sprite_frames

char_move = {"boar1": "right", "boar2": "right", "boar3": "right", "boar4": "right", "boar5": "right", 
             "willow": "left", "john": "left", "reid": "left", "ingot": "left", "illydia": "left", "fursttryl": "left"}
char_pos = {"boar1": {"x": 1, "y": 1}, "boar2": {"x": 10, "y": 0}, "boar3": {"x": 9, "y": 6}, 
            "boar4": {"x": 5, "y": 11}, "boar5": {"x": 1, "y": 16}, "willow": {"x": 16, "y": 11}, 
            "john": {"x": 16, "y": 1}, "reid": {"x": 16, "y": 5}, "ingot": {"x": 16, "y": 3}, 
            "illydia": {"x": 16, "y": 9}, "fursttryl": {"x": 16, "y": 7}}

cur_animation = 0
animation_timer = 0
animation_delay = 200

block_size = 40 #Set the size of the grid block
grid_size = 18

window_width = grid_size * block_size
window_height = grid_size * block_size

white = (200, 200, 200)
black = (0, 0, 0)

screen = pygame.display.set_mode((window_width, window_height))

def get_frame(char, sprite_sheet):
    # Find the direction the boar is facing
    direction = char_move[char]

    # Find which animation frame we're on
    frame_number = cur_animation

    # Get the Rect for that particular frame
    rect = None
    if ("boar" in char):
        rect = sprite_frames.boar_frames[direction][frame_number]
    else:
        rect = sprite_frames.character_frames[direction][frame_number]

    # Cut that section out of the sprite sheet
    frame = sprite_sheet.subsurface(rect)
    return frame

def draw_char(char, sprite_sheet):
    # convert grid coordinates to pixel coordinates
    pixel_x = char_pos[char]["x"] * block_size
    pixel_y = char_pos[char]["y"] * block_size

    # get the correct-facing sprite
    frame = get_frame(char, sprite_sheet)

    # center the sprites in the blocks
    offset_x = (block_size - frame.get_width()) // 2
    offset_y = (block_size - frame.get_height()) // 2

    screen.blit(frame, (pixel_x + offset_x, pixel_y + offset_y))

def check_bounds(coordinates):
    if (coordinates < 0):
        return 0
    elif (coordinates > 17):
        return 17
    return coordinates


def move(char, key):
    cur_x = char_pos[char]["x"]
    cur_y = char_pos[char]["y"]

    temp_x = cur_x
    temp_y = cur_y

    if (key == pygame.K_UP):
        char_move[char] = "up"
        print("up arrow pressed")
        temp_y = cur_y - 1
    elif (key == pygame.K_DOWN):
        char_move[char] = "down"
        print("down arrow pressed")
        temp_y = cur_y + 1
    elif (key == pygame.K_LEFT):
        char_move[char] = "left"
        print("left arrow pressed")
        temp_x = cur_x - 1
    elif (key == pygame.K_RIGHT):
        char_move[char] = "right"
        print("right arrow pressed")
        temp_x = cur_x + 1

    new_x = check_bounds(temp_x)
    new_y = check_bounds(temp_y)
    char_pos[char]["x"] = new_x
    char_pos[char]["y"] = new_y

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
    global animation_timer
    global cur_animation
    
    running = True
    while running:
        dt = clock.tick(30)
        animation_timer += dt

        if (animation_timer >= animation_delay):
            animation_timer = 0

            if (cur_animation < 2):
                cur_animation += 1
            else:
                cur_animation = 0

        screen.fill(black)  # clear screen to black each frame
        draw_grid()

        for char in char_move:
            sprite_sheet = None
            if ("boar" in char):
                sprite_sheet = pygame.image.load("assets/sprites/boar_sprite_sheet.png").convert_alpha()
            else:
                path = f"assets/sprites/{char}_sprite_sheet.png"
                sprite_sheet = pygame.image.load(path).convert_alpha()
            draw_char(char, sprite_sheet)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):  # player clicked the window's close button
                running = False
            if (event.type == pygame.KEYDOWN):  # a key was pressed
                move("fursttryl", event.key)

        # show what we just drew
        pygame.display.flip()

        clock.tick(30)  # limit to 30 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()