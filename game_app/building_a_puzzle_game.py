import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEAL_SPEED = 8
BOX_SIZE = 40
GAP_SIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs an even number' \
                                              'of boxes for pairs matches. '
X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)

Gray = (100, 100, 100)
Navy_Blue = (60, 60, 100)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Orange = (255, 128, 0)
Purple = (255, 0, 255)
Cyan = (0, 255, 255)

BG_COLOR = Navy_Blue
LIGHT_BG_COLOR = Gray
BOX_COLOR = White
HIGH_LIGHT_COLOR = Blue

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (Red, Green, Blue, Yellow, Orange, Purple, Cyan)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, 'Board is ' \
                                                                            'too big for the number' \
                                                                            'of shapes / colors defined.'


def main():
    global FPS_CLOCKS, DISPLAY_SURF
    pygame.init()
    FPS_CLOCKS = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode(WINDOW_WIDTH, WINDOW_HEIGHT)

    mouse_x = 0
    mouse_y = 0
    pygame.display.set_caption("Kelechi Divine's pc game! ")

    main_Board = getRandomizedBoard()
    revealed_Boxes = generateRevealedBoxesData(False)

    first_selection = None

    DISPLAY_SURF.fill(BG_COLOR)
    start_game_animation(main_Board)

    while True:
        mouse_Click = False

        DISPLAY_SURF.fill(BG_COLOR)
        draw_Board = (main_Board, revealed_Boxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == mouse_motion:
                mouse_x, mouse_y = event.pos

            elif event.type == mouse_button_up:
                mouse_x, mouse_y = event.pos
                mouse_Click = True

        boxx, boxy = get_box_at_pixel(mouse_x, mouse_y)

        if boxx is not None and boxy is not None:
            if not revealed_Boxes[boxx][boxy]:
                draw_high_light_box(boxx, boxy)
            if not revealed_Boxes[boxx][boxy] and mouse_Click:
                revealed_Boxes_animation(main_Board, [boxx, boxy])
                revealed_Boxes[boxx][boxy] = True

                if first_selection is None:
                    first_selection = (boxx, boxy)
                else:
                    icon_shape, icon_color, = get_shape_and_color(main_Board, first_selection[0]
                                                                  , first_selection[1])
                    icon2_shape, icon2_color = get_shape_and_color(main_Board, boxy
                                                                   , boxy)

                    if icon_color is not icon2_shape or icon_color is not icon2_color:
                        pygame.time.wait(1000)
                        cover_boxes_animation(main_Board, [(first_selection[0],
                                                            first_selection[1]), (boxx, boxy)])
                        revealed_Boxes[first_selection[0]][first_selection[1]] = False
                        revealed_Boxes[boxx][boxy] = False
                    elif has_won(revealed_Boxes):
                        game_won_animation(main_Board)
                        pygame.time.wait(2000)

                        main_Board = get_randomized_board()
                        revealed_Boxes = generate_revealed_boxes_data(False)

                        draw_Board(main_Board, revealed_Boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        start_game_animation(main_Board)
                    first_selection = None

        pygame.display.update()
        FPS_CLOCKS.tick(FPS)


def generate_Revealed_Boxes_Data(val):
    revealed_boxes = []

    for i in range(BOARD_WIDTH):
        revealed_boxes.append([val] * BOARD_WIDTH)
    return revealed_boxes


def get_randomized_board():
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))

    random.shuffle(icons)
    num_icon_used = int(BOARD_WIDTH * BOARD_WIDTH / 2)

    icons = icons[: num_icon_used] * 2
    random.shuffle(icons)

    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range (BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def split_into_groups_of(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i:i + group_size])
    return result


def left_top_coords_of_box(boxx, boxy):
    left = boxx * (BOX_SIZE + GAP_SIZE) + X_MARGIN
    top = boxy * (BOX_SIZE + GAP_SIZE) + Y_MARGIN
    return left, top


def get_box_at_pixel(x, y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_react = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_react.collidepoint(x, y):
                return boxx, boxy
    return None, None


def draw_icon(shape, color, boxx, boxy):
    quater = int(BOX_SIZE * 0.25)
    half = int(BOX_SIZE * 0.25)

    left, top =  left_top_coords_of_box(boxx, boxy)

    if shape  == DONUT:
        pygame.draw.circle(Display_surf, color, (left + half, top + half), half - 5)
        pygame.draw.circle(Display_surf, color, (left + half, top + half), quater - 5)
    elif shape == SQUARE:
        pygame.draw.rect(Display_surf, color, (left + quater, top + quater, BOX_SIZE
                                               - half,BOX_SIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(Display_surf, color, ((left + half,  top), (left + BOX_SIZE - 1
                                                                        , top + half), (left
                                                                                       + half, top +
                                                                                        BOX_SIZE - 1),
                                                  (left, top + half)))
