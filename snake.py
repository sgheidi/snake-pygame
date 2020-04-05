import pygame as pg
import random as rand
import sys
import os
import timea

RES = 500
UNIT = RES//20
HEAD_X = RES//2
HEAD_Y = RES//2
HEAD_ROW = (HEAD_X//25)+1
HEAD_COL = (HEAD_Y//25)+1

OFFSET = RES//10
SNAKE_SIDE_LEN = UNIT
FOOD_LEN = UNIT//4
VEL = UNIT
INITIAL_SNAKE_SIZE = 10

keypress = "D"
Pause = False
level=1

class Snake(object):
  """Main class for data & methods relating
  to moving Snake
  """
  def __init__(self):
    self.x = [HEAD_X]
    self.y = [HEAD_Y]
    self.col = [HEAD_COL]
    self.row = [HEAD_ROW]
    self.dir = ["D"]
    self.size = INITIAL_SNAKE_SIZE
    if self.size > 1:
      for i in range(1,self.size):
        self.dir.append("D")
        self.col.append(HEAD_COL)
        self.row.append(HEAD_ROW-i)
        self.x.append(HEAD_X)
        self.y.append(HEAD_Y-(UNIT*i))
    self.pivcol = []
    self.pivrow = []
    self.pivdir = []

  def turn(self):
    """This function handles snake's turning direction.
        Logic: When turning, save the pivot direction & position.
        Then, for each piece in the snake, check if the position matches
        any saved pivot position. If it does, set the piece direction to the
        pivot's direction.
        If a pivot position reaches the tail position, remove that pivot.
    """
    for i in range(1, self.size):
      # check whether any piece's position matches a pivot's position
      for k in range(0, len(self.pivcol)):
        if self.col[i] == self.pivcol[k] and self.row[i] == self.pivrow[k]:
          self.dir[i] = self.pivdir[k]
    # remove pivot if it equals tail position
    newcol = []
    newrow = []
    newdir = []
    for i in range(0, len(self.pivcol)):
      if self.pivcol[i] != self.col[Snake.size-1] or self.pivrow[i] != self.row[Snake.size-1]:
        newcol.append(self.pivcol[i])
        newrow.append(self.pivrow[i])
        newdir.append(self.pivdir[i])
    self.pivcol = newcol
    self.pivrow = newrow
    self.pivdir= newdir

  def CheckDeath(self, level):
    for i in range(1,self.size):
      if self.col[0] == self.col[i] and self.row[0] == self.row[i]:
        losesound.play()
        time.sleep(1.5)
        print("You reached level %d!"%level)
        sys.exit()
    if self.col[0] < 1 or self.col[0] > RES//25 or self.row[0] < 1 \
    or self.row[0] >RES//25:
      losesound.play()
      time.sleep(1.5)
      print("You reached level %d!"%level)
      sys.exit()

  def print_pos(self):
    for i in range(self.size):
      print("Piece %d: Row %d Col %d" % (i, self.row[i], self.col[i]))

  def print_dir(self):
    for i in range(self.size):
      print("Piece %d: %s" % (i, self.dir[i]))

  def piv_pos(self):
    if Snake.size > 1:
      for i in range(len(self.pivdir)):
        print("Pivot %d: Row %d Col %d\n" % (i, self.pivrow[i], self.pivcol[i]))

  def piv_dir(self):
    if Snake.size > 1:
      for i in range(len(self.pivdir)):
        print("Pivot %d: %s\n" % (i,self.pivdir[i]))

class Map(object):
  """Class for defining map and boundaries"""
  def draw_grid(self):
    grid_color = (100, 100, 100)
    # horizontal
    for i in range(0, RES, UNIT):
      pg.draw.line(win, grid_color, (0, i), (RES,i))
    pg.draw.line(win, grid_color, (0, RES-1), (RES,RES-1))
    # vertical
    for i in range(0, RES, UNIT):
      pg.draw.line(win, grid_color, (i, 0), (i, RES))
    pg.draw.line(win, grid_color, (RES-1, 0), (RES-1,RES))
    pg.display.flip()

  def draw_borders(self):
    pass

def event_loop():
  """Game enters from here"""
  iter = 1
  delay = 100
  keypress = "D"
  food_row = rand.randrange(0, RES/25)+1
  food_col = rand.randrange(0, RES/25)+1
  Pause = False
  eaten=0
  level=1

  while True:
    Map.draw_grid()
    iter += 1
    for event in pg.event.get():
      if event.type == pg.QUIT:
        sys.exit()
      elif event.type == pg.KEYDOWN:
        if (event.key == pg.K_w or event.key == pg.K_UP) and keypress !="D" and keypress !="U":
          keypress = "U"
          if Snake.size > 1:
            Snake.pivcol.append(Snake.col[0])
            Snake.pivrow.append(Snake.row[0])
            Snake.pivdir.append("U")
        elif (event.key == pg.K_s or event.key == pg.K_DOWN) and keypress !="U" and keypress !="D":
          keypress = "D"
          if Snake.size > 1:
            Snake.pivcol.append(Snake.col[0])
            Snake.pivrow.append(Snake.row[0])
            Snake.pivdir.append("D")
        elif (event.key == pg.K_d or event.key == pg.K_RIGHT) and keypress !="L" and keypress !="R":
          keypress = "R"
          if Snake.size > 1:
            Snake.pivcol.append(Snake.col[0])
            Snake.pivrow.append(Snake.row[0])
            Snake.pivdir.append("R")
        elif (event.key == pg.K_a or event.key == pg.K_LEFT) and keypress !="R" and keypress !="L":
          keypress = "L"
          if Snake.size > 1:
            Snake.pivcol.append(Snake.col[0])
            Snake.pivrow.append(Snake.row[0])
            Snake.pivdir.append("L")
        elif event.key == pg.K_q or event.key == pg.K_ESCAPE:
          sys.exit()
        elif event.key == pg.K_p:
          pausesound.play()
          if Pause == False:
            Pause = True
          elif Pause == True:
            Pause=False
        elif event.key == pg.K_r:
          Snake.__init__()
          keypress = "D"
          food_row = rand.randrange(0, RES/25)+1
          food_col = rand.randrange(0, RES/25)+1
          Pause = False

    if iter % delay == 0 and Pause == False:
      Snake.CheckDeath(level)
      if keypress == "R":
        Snake.x[0] += VEL
        Snake.col[0] += 1
        Snake.dir[0] = "R"
      elif keypress == "L":
        Snake.x[0] -= VEL
        Snake.col[0] -= 1
        Snake.dir[0] = "L"
      elif keypress == "U":
        Snake.y[0] -= VEL
        Snake.row[0] -= 1
        Snake.dir[0] = "U"
      elif keypress == "D":
        Snake.y[0] += VEL
        Snake.row[0] += 1
        Snake.dir[0] = "D"
      Snake.turn()

      # update snake piece positions based on its string values
      for i in range(1, Snake.size):
        if Snake.dir[i] == "U":
          Snake.y[i] -= VEL
          Snake.row[i] -= 1
        elif Snake.dir[i] == "D":
          Snake.y[i] += VEL
          Snake.row[i] += 1
        elif Snake.dir[i] == "L":
          Snake.x[i] -= VEL
          Snake.col[i] -= 1
        elif Snake.dir[i] == "R":
          Snake.x[i] += VEL
          Snake.col[i] += 1

    # check if Snake has eaten food
    if Snake.row[0] == food_row and Snake.col[0] == food_col and \
    iter % delay == 0 and Pause == False:
      eaten+=1
      if eaten%4==0:
        levelsound.play()
        level +=1
        delay -= 10
      foodsound.play()
      food_row = rand.randrange(0, RES//25)+1
      food_col = rand.randrange(0, RES//25)+1
      # set the direction & position of the new piece to be added
      # this is set based off tail's direction & position
      if Snake.dir[Snake.size-1] == "D":
        Snake.dir.append("D")
        Snake.x.append(Snake.x[Snake.size-1])
        Snake.y.append(Snake.y[Snake.size-1] - UNIT)
        Snake.col.append(Snake.col[Snake.size-1])
        Snake.row.append(Snake.row[Snake.size-1]-1)
      elif Snake.dir[Snake.size-1] == "U":
        Snake.dir.append("U")
        Snake.x.append(Snake.x[Snake.size-1])
        Snake.y.append(Snake.y[Snake.size-1] + UNIT)
        Snake.col.append(Snake.col[Snake.size-1])
        Snake.row.append(Snake.row[Snake.size-1]+1)
      elif Snake.dir[Snake.size-1] == "L":
        Snake.dir.append("L")
        Snake.x.append(Snake.x[Snake.size-1] + UNIT)
        Snake.y.append(Snake.y[Snake.size-1])
        Snake.col.append(Snake.col[Snake.size-1]+1)
        Snake.row.append(Snake.row[Snake.size-1])
      elif Snake.dir[Snake.size-1] == "R":
        Snake.dir.append("R")
        Snake.x.append(Snake.x[Snake.size-1] - UNIT)
        Snake.y.append(Snake.y[Snake.size-1])
        Snake.col.append(Snake.col[Snake.size-1]-1)
        Snake.row.append(Snake.row[Snake.size-1])
      Snake.size += 1
    win.fill((0,0,0))
    for i in range(Snake.size):
      """New food should not spawn on snake itself. Keep
      generating random numbers until it is not on snake itself.
      """
      if food_row==Snake.row[i] and food_col==Snake.col[i]:
        i=0
        food_row = rand.randrange(0, RES//25)+1
        food_col = rand.randrange(0, RES//25)+1
    pg.draw.circle(win, (200,50,0), ((food_col*25)-12, (food_row*25)-12), FOOD_LEN)
    for i in range(Snake.size):
      pg.draw.rect(win, (0,150,0), (Snake.x[i], Snake.y[i], SNAKE_SIDE_LEN, SNAKE_SIDE_LEN))


if __name__ == '__main__':
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (RES, RES/6)
  win = pg.display.set_mode((RES,RES+OFFSET))
  pg.display.set_caption("Snake")
  pg.mixer.init(22050, -16, 9, 251)
  foodsound= pg.mixer.Sound("sounds/food.wav")
  pausesound= pg.mixer.Sound("sounds/pause.wav")
  losesound= pg.mixer.Sound("sounds/lose.wav")
  levelsound= pg.mixer.Sound("sounds/level.wav")
  pg.mixer.music.load('sounds/song.mp3')
  pg.mixer.music.play(-1)
  pg.init()
  Snake = Snake()
  Map = Map()
  event_loop()
