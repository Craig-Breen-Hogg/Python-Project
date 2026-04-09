
import turtle
import random
import math

# --------------- Config ---------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_MOVE_STEP = 20
BULLET_SPEED = 18
ALIEN_INIT_DX = 4        # Initial horizontal speed of alien swarm
ALIEN_STEP_DOWN = 24     # How much aliens move down when hitting a wall
ALIEN_ROWS = 4
ALIEN_COLS = 10
ALIEN_SPACING_X = 50
ALIEN_SPACING_Y = 40
ALIEN_START_Y = 180
ALIEN_PADDING = 40       # Left/right padding before wall bounce

BARRIER_COUNT = 4
BARRIER_BLOCK_ROWS = 3
BARRIER_BLOCK_COLS = 7
BARRIER_BLOCK_SIZE = 10
BARRIER_TOP_Y = -120

SCORE_PER_ALIEN = 10

# --------------- Screen ---------------
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.title("Space Invaders - Python Turtle")
screen.bgcolor("black")
screen.tracer(0)  # Manual updates for smoother animation

# --------------- HUD / Writer ---------------
hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("white")
hud.goto(0, SCREEN_HEIGHT // 2 - 40)

# --------------- Player ---------------
player = turtle.Turtle()
player.shape("triangle")
player.color("#39FF14")  # neon green
player.shapesize(stretch_wid=1.2, stretch_len=1.2)
player.penup()
player.setheading(90)  # point up
player.goto(0, -SCREEN_HEIGHT // 2 + 60)

# --------------- Bullet ---------------
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("white")
bullet.shapesize(stretch_wid=0.2, stretch_len=0.6)
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"  # "ready" or "fire"

# --------------- Aliens ---------------
aliens = []
alien_dx = ALIEN_INIT_DX
swarm_alive = True

def create_aliens():
    global aliens
    aliens = []
    start_x = - (ALIEN_COLS - 1) * ALIEN_SPACING_X // 2
    for r in range(ALIEN_ROWS):
        for c in range(ALIEN_COLS):
            a = turtle.Turtle()
            a.shape("circle")
            a.color("#00FFFF")  # cyan
            a.shapesize(stretch_wid=1.0, stretch_len=1.4)
            a.penup()
            x = start_x + c * ALIEN_SPACING_X
            y = ALIEN_START_Y - r * ALIEN_SPACING_Y
            a.goto(x, y)
            aliens.append(a)

# --------------- Barriers ---------------
barrier_blocks = []

def create_barrier(center_x, base_y):
    # make a blocky barrier as a small grid of squares
    for row in range(BARRIER_BLOCK_ROWS):
        for col in range(BARRIER_BLOCK_COLS):
            # shape the barrier: leave corners empty to resemble classic style
            if row == 0 and (col == 0 or col == BARRIER_BLOCK_COLS - 1):
                continue
            b = turtle.Turtle()
            b.shape("square")
            b.color("#7CFC00")  # lawn green
            b.shapesize(stretch_wid=BARRIER_BLOCK_SIZE / 20.0,
                        stretch_len=BARRIER_BLOCK_SIZE / 20.0)
            b.penup()
            x = center_x + (col - (BARRIER_BLOCK_COLS // 2)) * (BARRIER_BLOCK_SIZE + 2)
            y = base_y + row * (BARRIER_BLOCK_SIZE + 2)
            b.goto(x, y)
            barrier_blocks.append(b)

def create_barriers():
    barrier_spacing = SCREEN_WIDTH // (BARRIER_COUNT + 1)
    start_x = -SCREEN_WIDTH // 2 + barrier_spacing
    for i in range(BARRIER_COUNT):
        cx = start_x + i * barrier_spacing
        create_barrier(cx, BARRIER_TOP_Y)

# --------------- Utility ---------------
def clamp_player():
    x = player.xcor()
    half_w = SCREEN_WIDTH // 2 - 30
    if x < -half_w:
        x = -half_w
    if x > half_w:
        x = half_w
    player.setx(x)

def distance(t1, t2):
    return math.hypot(t1.xcor() - t2.xcor(), t1.ycor() - t2.ycor())

# --------------- Controls ---------------
def move_left():
    if game_state["running"]:
        player.setx(player.xcor() - PLAYER_MOVE_STEP)
        clamp_player()

def move_right():
    if game_state["running"]:
        player.setx(player.xcor() + PLAYER_MOVE_STEP)
        clamp_player()

def fire_bullet():
    global bullet_state
    if game_state["running"] and bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

def quit_game():
    try:
        turtle.bye()
    except:
        pass

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")
screen.onkeypress(quit_game, "q")

# How to run:

# Copy the code below into a file named space_invaders.py.
# Run with:
# python space_invaders.py

# Controls:

# Left / Right Arrow: Move the ship
# Space: Fire
# Q: Quit