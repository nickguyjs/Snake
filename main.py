import pygame
import random
import time

# create the snake and apple classes
# the object parameter means it is inheriting the object class.
class Snake(object):
  def __init__(self):
    self.headX = random.randint(0,16)*30
    self.headY = random.randint(0,16)*30
    self.length = 1
    self.pos = []
    self.pos.append([self.headX, self.headY])
    d = random.randint(0,3)
    self.direction = "NORTH" if d == 0 else "EAST" if d == 1 else "SOUTH" if d == 2 else "WEST"


  def drawMe(self):
    #self.pos.append([self.headX, self.headY])
    temp = list(self.pos)
    i = 0
    for i in range(len(temp)):
      for j in range(len(temp)):
        if i != j and temp[i] == temp[j]:
          pygame.quit()
    while(len(temp) > 0):
      e = temp.pop()
      pygame.draw.rect(screen, GREEN, (e[0],e[1],30,30))
      pygame.draw.rect(screen, BLACK, (e[0],e[1],30,30),2)
  
  def update(self, add):
    #print("SNAKE: " + str(self.headX))
    if(self.direction == "NORTH"):
      self.headY -= 30
    elif(self.direction == "SOUTH"):
      self.headY += 30
    elif(self.direction == "EAST"):
      self.headX += 30
    else:
      self.headX -= 30
    #temp = self.pos.pop(0)
    #print("POP! " + str(temp[0]) + ", " + str(temp[1]))
    if not add:
      self.pos.pop(0)
    if add:
      self.length += 1
    self.pos.append([self.headX, self.headY])
    self.checkEdge()
    self.drawMe()

  def checkEdge(self):
    if self.headX < 0 or self.headX >= WIDTH or self.headY < 0 or self.headY >= WIDTH:
      pygame.quit()

  def setDirection(self, dir):
    if(self.length > 1 and dir == "SOUTH" and self.direction == "NORTH" or dir == "NORTH" and self.direction == "SOUTH" or dir == "WEST" and self.direction == "EAST" or dir == "EAST" and self.direction == "WEST"):
      pass
    else:
      self.direction = dir

  def getX(self):
    return self.headX
  
  def getY(self):
    return self.headY

  def getPos(self):
    return self.pos
  
  def getLength(self):
    return self.length

class Apple(object):
  def __init__(self):
    self.appleX = 0
    self.appleY = 0
    
  
  def drawMe(self):
    pygame.draw.rect(screen, RED, (self.appleX,self.appleY,30,30))
    pygame.draw.rect(screen, BLACK, (self.appleX,self.appleY,30,30),2)

  def eatApple(self, pos):
    self.appleX = random.randint(0,16)*30
    self.appleY = random.randint(0,16)*30
    while [self.appleX, self.appleY] in pos:
      self.appleX = random.randint(0,16)*30
      self.appleY = random.randint(0,16)*30    
    #print("APPLE: " + str(self.appleX))
    self.drawMe()
  
  def getX(self):
    return self.appleX
  
  def getY(self):
    return self.appleY

# set dimensions
WIDTH = 30*17

# set speed
SPEED = 250

# create the pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, WIDTH+60))
pygame.display.set_caption('Snake')
run = False

# declare colors
BLACK = (0,0,0)
WHITE = (255,255,255)
CORNFLOWER = (100,149,237)
NAVY = (0,0,128)
GREEN = (0,255,0)
RED = (255,0,0)

s = Snake()
a = Apple()
a.eatApple(s.getPos())
time.sleep(1)
lastMove = 0
clock = pygame.time.Clock()
cooldown = 0
start = False
        
# while loop for the program to run inside of
while run == False:
  screen.fill(WHITE)
  myfont = pygame.font.SysFont("monospace", 64)
  scoretext = myfont.render("Score = " + str(s.getLength()), 1, BLACK)
  screen.blit(scoretext, (5, 510))
  if start == False:
    # draw the board left to right, top to bottom
    x = 0
    y = 0
    flip = True
    for row in range(17):
      for column in range(17):
        pygame.draw.rect(screen, NAVY if flip else CORNFLOWER, (x,y,30,30))
        x += 30
        flip = not flip
      y += 30
      x = 0
    s.drawMe()
    a.drawMe()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = True
        
    keys = pygame.key.get_pressed()
    if cooldown == 0 and keys[pygame.K_LEFT] or keys[pygame.K_a]:
      cooldown = 500
      s.setDirection("WEST")
      start = True
    elif cooldown == 0 and keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      cooldown = 500
      s.setDirection("EAST")
      start = True
    elif cooldown == 0 and keys[pygame.K_UP] or keys[pygame.K_w]:
      cooldown = 500
      s.setDirection("NORTH")
      start = True
    elif cooldown == 0 and keys[pygame.K_DOWN] or keys[pygame.K_s]:
      cooldown = 500
      s.setDirection("SOUTH")
      start = True
  
  if start:
    addRing = False
    if s.getX() == a.getX() and s.getY() == a.getY():
      a.eatApple(s.getPos())
      addRing = True
      if(SPEED > 100):
        SPEED -= 5
      keys = pygame.key.get_pressed()
      if cooldown == 0 and keys[pygame.K_LEFT] or keys[pygame.K_a]:
        cooldown = 500
        s.setDirection("WEST")
      elif cooldown == 0 and keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        cooldown = 500
        s.setDirection("EAST")
      elif cooldown == 0 and keys[pygame.K_UP] or keys[pygame.K_w]:
        cooldown = 500
        s.setDirection("NORTH")
      elif cooldown == 0 and keys[pygame.K_DOWN] or keys[pygame.K_s]:
        cooldown = 500
        s.setDirection("SOUTH")
      lastMove = 250

    # draw the board left to right, top to bottom
    x = 0
    y = 0
    flip = True
    for row in range(17):
      for column in range(17):
        pygame.draw.rect(screen, NAVY if flip else CORNFLOWER, (x,y,30,30))
        x += 30
        flip = not flip
      y += 30
      x = 0
    
    # update time since last move, draw the snake
    dt = clock.tick() 
    lastMove += dt
    if lastMove > SPEED:
      s.update(addRing)
      cooldown = 0
      lastMove = 0
    else:
      s.drawMe()

    # draw apple
    a.drawMe()

  pygame.display.flip()

pygame.quit()