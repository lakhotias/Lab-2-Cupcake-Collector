import pygame
import asyncio
import sys
import math

pygame.init()

# =========================================================
# CUPCAKE SKY QUEST
# One-file Pygame platformer
# No image or sound files needed
# =========================================================

WIDTH, HEIGHT = 900, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupcake Sky Quest")

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

SKY = (190, 228, 255)

CLOUD = (252, 252, 255)

HILL_1 = (178, 224, 188)

HILL_2 = (157, 211, 177)

GRASS = (112, 201, 126)

DIRT = (177, 123, 82)

PINK = (255, 164, 198)

DARK_PINK = (190, 92, 132)

PURPLE = (135, 98, 190)

LIGHT_PURPLE = (207, 183, 240)

YELLOW = (255, 223, 93)

CREAM = (255, 246, 224)

BROWN = (112, 77, 62)

DARK = (57, 48, 72)

WHITE = (255, 255, 255)

RED = (238, 93, 112)

GREEN = (79, 156, 94)


# =========================================================
# FONTS
# =========================================================

font = pygame.font.SysFont(
    "arial",
    24,
    bold=True
)

small_font = pygame.font.SysFont(
    "arial",
    18
)

big_font = pygame.font.SysFont(
    "arial",
    48,
    bold=True
)


# =========================================================
# PLAYER
# =========================================================

player = pygame.Rect(
    55,
    495,
    38,
    50
)

player_x = float(player.x)

player_y = float(player.y)

PLAYER_SPEED = 6

GRAVITY = 0.75

JUMP_POWER = -14.5

player_vel_x = 0

player_vel_y = 0

grounded = False


# =========================================================
# PLATFORMS
# =========================================================

platforms = [

    # Ground
    pygame.Rect(
        0,
        550,
        900,
        50
    ),

    pygame.Rect(
        105,
        445,
        185,
        22
    ),

    pygame.Rect(
        335,
        365,
        185,
        22
    ),

    pygame.Rect(
        600,
        295,
        180,
        22
    ),

    pygame.Rect(
        420,
        220,
        170,
        22
    ),

    pygame.Rect(
        165,
        150,
        180,
        22
    ),

    pygame.Rect(
        650,
        95,
        165,
        22
    )

]


# =========================================================
# MOVING PLATFORM
# =========================================================

moving_platform = pygame.Rect(
    545,
    465,
    135,
    20
)

moving_speed = 2

MOVING_MIN_X = 500

MOVING_MAX_X = 755


# =========================================================
# CUPCAKES
# =========================================================

def make_cupcakes():

    return [

        pygame.Rect(
            165,
            407,
            26,
            32
        ),

        pygame.Rect(
            420,
            327,
            26,
            32
        ),

        pygame.Rect(
            675,
            257,
            26,
            32
        ),

        pygame.Rect(
            490,
            182,
            26,
            32
        ),

        pygame.Rect(
            235,
            112,
            26,
            32
        ),

        pygame.Rect(
            720,
            57,
            26,
            32
        ),

        pygame.Rect(
            825,
            512,
            26,
            32
        ),

        pygame.Rect(
            590,
            425,
            26,
            32
        )

    ]


cupcakes = make_cupcakes()

TOTAL_CUPCAKES = len(cupcakes)

score = 0


# =========================================================
# ENEMY
# =========================================================

enemy = pygame.Rect(
    760,
    505,
    42,
    42
)

enemy_x = float(enemy.x)

ENEMY_SPEED = 1.15


# =========================================================
# GOAL STAR
# =========================================================

goal = pygame.Rect(
    795,
    39,
    46,
    46
)


# =========================================================
# GAME VARIABLES
# =========================================================

lives = 3

won = False

game_over = False

invincible_timer = 0


# =========================================================
# RESET PLAYER
# =========================================================

def reset_player():

    global player_x

    global player_y

    global player_vel_x

    global player_vel_y


    player.x = 55

    player.y = 495


    player_x = float(player.x)

    player_y = float(player.y)


    player_vel_x = 0

    player_vel_y = 0


# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global cupcakes

    global score

    global lives

    global won

    global game_over

    global invincible_timer

    global enemy_x


    cupcakes = make_cupcakes()


    score = 0

    lives = 3

    won = False

    game_over = False

    invincible_timer = 0


    enemy.x = 760

    enemy.y = 505

    enemy_x = float(enemy.x)


    reset_player()


# =========================================================
# DRAW CLOUD
# =========================================================

def draw_cloud(x, y):

    pygame.draw.circle(
        screen,
        CLOUD,
        (x, y),
        24
    )


    pygame.draw.circle(
        screen,
        CLOUD,
        (x + 28, y - 12),
        31
    )


    pygame.draw.circle(
        screen,
        CLOUD,
        (x + 58, y),
        23
    )


    pygame.draw.rect(
        screen,
        CLOUD,
        (
            x,
            y,
            58,
            24
        )
    )


# =========================================================
# DRAW BACKGROUND
# =========================================================

def draw_background():

    screen.fill(
        SKY
    )


    # Clouds

    draw_cloud(
        75,
        90
    )


    draw_cloud(
        355,
        105
    )


    draw_cloud(
        700,
        70
    )


    # Hills

    pygame.draw.circle(
        screen,
        HILL_1,
        (110, 615),
        190
    )


    pygame.draw.circle(
        screen,
        HILL_2,
        (420, 620),
        215
    )


    pygame.draw.circle(
        screen,
        HILL_1,
        (760, 615),
        220
    )


    # Cute flowers

    for x in range(
        40,
        880,
        90
    ):

        pygame.draw.line(
            screen,
            GREEN,
            (x, 548),
            (x, 531),
            3
        )


        pygame.draw.circle(
            screen,
            PINK,
            (x - 5, 529),
            5
        )


        pygame.draw.circle(
            screen,
            YELLOW,
            (x + 5, 529),
            5
        )


        pygame.draw.circle(
            screen,
            WHITE,
            (x, 523),
            5
        )


# =========================================================
# DRAW PLATFORM
# =========================================================

def draw_platform(rect):

    pygame.draw.rect(
        screen,
        DIRT,
        rect,
        border_radius=7
    )


    pygame.draw.rect(
        screen,
        GRASS,
        (
            rect.x,
            rect.y,
            rect.width,
            min(8, rect.height)
        ),
        border_radius=7
    )


# =========================================================
# DRAW PLAYER
# =========================================================

def draw_player(rect):

    center_x = rect.centerx

    top = rect.top


    # Ears

    pygame.draw.polygon(
        screen,
        PINK,
        [
            (
                center_x - 16,
                top + 13
            ),

            (
                center_x - 12,
                top - 2
            ),

            (
                center_x - 3,
                top + 12
            )
        ]
    )


    pygame.draw.polygon(
        screen,
        PINK,
        [
            (
                center_x + 16,
                top + 13
            ),

            (
                center_x + 12,
                top - 2
            ),

            (
                center_x + 3,
                top + 12
            )
        ]
    )


    # Body

    pygame.draw.ellipse(
        screen,
        PINK,
        (
            rect.x - 2,
            rect.y + 8,
            rect.width + 4,
            42
        )
    )


    # Head

    pygame.draw.circle(
        screen,
        PINK,
        (
            center_x,
            top + 20
        ),
        20
    )


    # Crown

    pygame.draw.polygon(
        screen,
        YELLOW,
        [
            (
                center_x - 11,
                top + 1
            ),

            (
                center_x - 7,
                top - 8
            ),

            (
                center_x - 1,
                top
            ),

            (
                center_x + 5,
                top - 8
            ),

            (
                center_x + 11,
                top + 2
            )
        ]
    )


    # Eyes

    pygame.draw.circle(
        screen,
        DARK,
        (
            center_x - 7,
            top + 19
        ),
        2
    )


    pygame.draw.circle(
        screen,
        DARK,
        (
            center_x + 7,
            top + 19
        ),
        2
    )


    # Cheeks

    pygame.draw.circle(
        screen,
        DARK_PINK,
        (
            center_x - 13,
            top + 25
        ),
        3
    )


    pygame.draw.circle(
        screen,
        DARK_PINK,
        (
            center_x + 13,
            top + 25
        ),
        3
    )


    # Smile

    pygame.draw.arc(
        screen,
        BROWN,
        (
            center_x - 7,
            top + 21,
            14,
            10
        ),
        0,
        math.pi,
        2
    )


# =========================================================
# DRAW CUPCAKE
# =========================================================

def draw_cupcake(rect):

    center_x = rect.centerx


    # Wrapper

    pygame.draw.polygon(
        screen,
        (125, 205, 235),
        [

            (
                rect.left + 3,
                rect.top + 13
            ),

            (
                rect.right - 3,
                rect.top + 13
            ),

            (
                rect.right - 6,
                rect.bottom
            ),

            (
                rect.left + 6,
                rect.bottom
            )

        ]
    )


    # Frosting

    pygame.draw.circle(
        screen,
        PINK,
        (
            center_x,
            rect.top + 11
        ),
        11
    )


    pygame.draw.circle(
        screen,
        PINK,
        (
            center_x - 7,
            rect.top + 14
        ),
        7
    )


    pygame.draw.circle(
        screen,
        PINK,
        (
            center_x + 7,
            rect.top + 14
        ),
        7
    )


    # Cherry

    pygame.draw.circle(
        screen,
        RED,
        (
            center_x,
            rect.top + 2
        ),
        4
    )


    pygame.draw.line(
        screen,
        GREEN,
        (
            center_x,
            rect.top - 2
        ),
        (
            center_x + 3,
            rect.top - 7
        ),
        2
    )


# =========================================================
# DRAW ENEMY
# =========================================================

def draw_enemy(rect):

    # Purple blob

    pygame.draw.ellipse(
        screen,
        PURPLE,
        rect
    )


    # Ears / horns

    pygame.draw.polygon(
        screen,
        PURPLE,
        [

            (
                rect.left + 6,
                rect.top + 10
            ),

            (
                rect.left + 10,
                rect.top - 4
            ),

            (
                rect.left + 18,
                rect.top + 8
            )

        ]
    )


    pygame.draw.polygon(
        screen,
        PURPLE,
        [

            (
                rect.right - 6,
                rect.top + 10
            ),

            (
                rect.right - 10,
                rect.top - 4
            ),

            (
                rect.right - 18,
                rect.top + 8
            )

        ]
    )


    # Eyes

    pygame.draw.circle(
        screen,
        DARK,
        (
            rect.centerx - 8,
            rect.top + 18
        ),
        3
    )


    pygame.draw.circle(
        screen,
        DARK,
        (
            rect.centerx + 8,
            rect.top + 18
        ),
        3
    )


    # Angry eyebrows

    pygame.draw.line(
        screen,
        DARK,
        (
            rect.centerx - 13,
            rect.top + 12
        ),
        (
            rect.centerx - 4,
            rect.top + 15
        ),
        2
    )


    pygame.draw.line(
        screen,
        DARK,
        (
            rect.centerx + 13,
            rect.top + 12
        ),
        (
            rect.centerx + 4,
            rect.top + 15
        ),
        2
    )


# =========================================================
# STAR POINTS
# =========================================================

def star_points(
    center_x,
    center_y,
    outer_radius,
    inner_radius
):

    points = []


    for i in range(10):

        angle = (
            -math.pi / 2
            +
            i * math.pi / 5
        )


        if i % 2 == 0:

            radius = outer_radius

        else:

            radius = inner_radius


        x = int(
            center_x
            +
            math.cos(angle) * radius
        )


        y = int(
            center_y
            +
            math.sin(angle) * radius
        )


        points.append(
            (x, y)
        )


    return points


# =========================================================
# DRAW STAR
# =========================================================

def draw_goal(
    rect,
    awake
):

    if awake:

        pygame.draw.circle(
            screen,
            CREAM,
            rect.center,
            31
        )


        pygame.draw.circle(
            screen,
            YELLOW,
            rect.center,
            28,
            3
        )


        color = YELLOW


    else:

        color = (
            205,
            205,
            215
        )


    pygame.draw.polygon(
        screen,
        color,
        star_points(
            rect.centerx,
            rect.centery,
            22,
            10
        )
    )


    # Star face

    pygame.draw.circle(
        screen,
        DARK,
        (
            rect.centerx - 6,
            rect.centery - 2
        ),
        2
    )


    pygame.draw.circle(
        screen,
        DARK,
        (
            rect.centerx + 6,
            rect.centery - 2
        ),
        2
    )


# =========================================================
# DRAW UI
# =========================================================

def draw_ui():

    score_text = font.render(

        "Cupcakes: "
        +
        str(score)
        +
        "/"
        +
        str(TOTAL_CUPCAKES),

        True,

        DARK

    )


    lives_text = font.render(

        "Lives: "
        +
        str(lives),

        True,

        DARK

    )


    screen.blit(
        score_text,
        (18, 15)
    )


    screen.blit(
        lives_text,
        (18, 46)
    )


    controls = small_font.render(

        "Move: arrows or A/D   Jump: up, W, or SPACE",

        True,

        DARK

    )


    screen.blit(

        controls,

        (
            WIDTH
            -
            controls.get_width()
            -
            15,

            17
        )

    )


    if score < TOTAL_CUPCAKES:

        message = small_font.render(

            "Collect every cupcake to wake the star!",

            True,

            PURPLE

        )


    else:

        message = small_font.render(

            "The star is awake! Reach it to win!",

            True,

            PURPLE

        )


    screen.blit(

        message,

        (
            WIDTH
            -
            message.get_width()
            -
            15,

            45
        )

    )


# =========================================================
# END SCREEN
# =========================================================

def draw_end_screen(
    title_text,
    subtitle_text
):

    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )


    overlay.fill(
        (
            255,
            239,
            248,
            225
        )
    )


    screen.blit(
        overlay,
        (0, 0)
    )


    title = big_font.render(
        title_text,
        True,
        PURPLE
    )


    subtitle = font.render(
        subtitle_text,
        True,
        DARK
    )


    restart = small_font.render(
        "Press R to play again",
        True,
        DARK
    )


    screen.blit(

        title,

        (
            WIDTH // 2
            -
            title.get_width() // 2,

            210
        )

    )


    screen.blit(

        subtitle,

        (
            WIDTH // 2
            -
            subtitle.get_width() // 2,

            275
        )

    )


    screen.blit(

        restart,

        (
            WIDTH // 2
            -
            restart.get_width() // 2,

            330
        )

    )


# =========================================================
# MAIN GAME
# =========================================================

async def main():

    global player_x

    global player_y

    global player_vel_x

    global player_vel_y

    global grounded

    global moving_speed

    global score

    global lives

    global won

    global game_over

    global invincible_timer

    global enemy_x


    running = True


    while running:


        # =================================================
        # EVENTS
        # =================================================

        for event in pygame.event.get():


            if event.type == pygame.QUIT:

                running = False


            if event.type == pygame.KEYDOWN:


                if (

                    event.key == pygame.K_r

                    and

                    (
                        won
                        or
                        game_over
                    )

                ):

                    reset_game()


        # =================================================
        # GAMEPLAY
        # =================================================

        if not won and not game_over:


            # =============================================
            # KEYBOARD INPUT
            # =============================================

            keys = pygame.key.get_pressed()


            player_vel_x = 0


            if (

                keys[pygame.K_LEFT]

                or

                keys[pygame.K_a]

            ):

                player_vel_x = -PLAYER_SPEED


            if (

                keys[pygame.K_RIGHT]

                or

                keys[pygame.K_d]

            ):

                player_vel_x = PLAYER_SPEED


            # Jump

            if (

                (
                    keys[pygame.K_UP]

                    or

                    keys[pygame.K_w]

                    or

                    keys[pygame.K_SPACE]
                )

                and

                grounded

            ):

                player_vel_y = JUMP_POWER

                grounded = False


            # =============================================
            # GRAVITY
            # =============================================

            player_vel_y += GRAVITY


            # =============================================
            # HORIZONTAL MOVEMENT
            # =============================================

            player_x += player_vel_x


            player.x = round(
                player_x
            )


            # Keep inside screen

            if player.left < 0:

                player.left = 0

                player_x = float(
                    player.x
                )


            if player.right > WIDTH:

                player.right = WIDTH

                player_x = float(
                    player.x
                )


            # =============================================
            # MOVING PLATFORM
            # =============================================

            moving_platform.x += moving_speed


            if (

                moving_platform.left
                <=
                MOVING_MIN_X

            ):

                moving_platform.left = (
                    MOVING_MIN_X
                )


                moving_speed *= -1


            elif (

                moving_platform.right
                >=
                MOVING_MAX_X

            ):

                moving_platform.right = (
                    MOVING_MAX_X
                )


                moving_speed *= -1


            # =============================================
            # VERTICAL MOVEMENT
            # =============================================

            old_bottom = player.bottom

            old_top = player.top


            player_y += player_vel_y


            player.y = round(
                player_y
            )


            grounded = False


            all_platforms = (
                platforms
                +
                [moving_platform]
            )


            # =============================================
            # PLATFORM COLLISION
            # =============================================

            for platform in all_platforms:


                if player.colliderect(
                    platform
                ):


                    # Landing on platform

                    if (

                        player_vel_y > 0

                        and

                        old_bottom
                        <=
                        platform.top + 10

                    ):

                        player.bottom = (
                            platform.top
                        )


                        player_y = float(
                            player.y
                        )


                        player_vel_y = 0


                        grounded = True


                        # Ride moving platform

                        if (

                            platform
                            ==
                            moving_platform

                        ):

                            player_x += moving_speed


                            player.x = round(
                                player_x
                            )


                    # Hit bottom of platform

                    elif (

                        player_vel_y < 0

                        and

                        old_top
                        >=
                        platform.bottom - 10

                    ):

                        player.top = (
                            platform.bottom
                        )


                        player_y = float(
                            player.y
                        )


                        player_vel_y = 0


            # =============================================
            # FLOOR SAFETY
            # =============================================

            if player.bottom > 550:

                player.bottom = 550


                player_y = float(
                    player.y
                )


                player_vel_y = 0


                grounded = True


            # =============================================
            # COLLECT CUPCAKES
            # =============================================

            for cupcake in cupcakes[:]:


                if player.colliderect(
                    cupcake
                ):


                    cupcakes.remove(
                        cupcake
                    )


                    score += 1


            # =============================================
            # ENEMY CHASE
            # =============================================

            if enemy.centerx < player.centerx:

                enemy_x += ENEMY_SPEED


            elif enemy.centerx > player.centerx:

                enemy_x -= ENEMY_SPEED


            enemy.x = round(
                enemy_x
            )


            enemy.y = 505


            # =============================================
            # DAMAGE TIMER
            # =============================================

            if invincible_timer > 0:

                invincible_timer -= 1


            # =============================================
            # PLAYER HITS ENEMY
            # =============================================

            if (

                player.colliderect(enemy)

                and

                invincible_timer == 0

            ):


                lives -= 1


                invincible_timer = 90


                reset_player()


                if lives <= 0:

                    game_over = True


            # =============================================
            # WIN CONDITION
            # =============================================

            if (

                score
                ==
                TOTAL_CUPCAKES

                and

                player.colliderect(goal)

            ):

                won = True


        # =================================================
        # DRAW EVERYTHING
        # =================================================

        draw_background()


        # Platforms

        for platform in platforms:

            draw_platform(
                platform
            )


        # Moving platform

        pygame.draw.rect(

            screen,

            PURPLE,

            moving_platform,

            border_radius=7

        )


        pygame.draw.rect(

            screen,

            LIGHT_PURPLE,

            (
                moving_platform.x,
                moving_platform.y,
                moving_platform.width,
                7
            ),

            border_radius=7

        )


        # Cupcakes

        for cupcake in cupcakes:

            draw_cupcake(
                cupcake
            )


        # Enemy

        draw_enemy(
            enemy
        )


        # Goal star

        draw_goal(

            goal,

            score
            ==
            TOTAL_CUPCAKES

        )


        # Player flashes after being hit

        if (

            invincible_timer == 0

            or

            (
                invincible_timer // 7
            )
            %
            2
            ==
            0

        ):

            draw_player(
                player
            )


        # UI

        draw_ui()


        # =================================================
        # WIN SCREEN
        # =================================================

        if won:

            draw_end_screen(

                "YOU DID IT!",

                "The Cupcake Star is sparkling again!"

            )


        # =================================================
        # GAME OVER SCREEN
        # =================================================

        elif game_over:

            draw_end_screen(

                "SO CLOSE!",

                "The cupcake thief got you this time."

            )


        # =================================================
        # UPDATE SCREEN
        # =================================================

        pygame.display.flip()


        clock.tick(
            60
        )


        # Needed for browser / Pygbag version

        await asyncio.sleep(0)


    pygame.quit()


    sys.exit()


# =========================================================
# START GAME
# =========================================================

asyncio.run(
    main()
)
