import pygame
import sys
import random
import math
import time


WIDTH = 750
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Percolation Visualization")

clock = pygame.time.Clock()

in_game = True

my_font = pygame.font.SysFont('Comic Sans MS', 40)

grid_size = int(input("What size should the grid be: "))

site_list = []
lines = []

percolates = False

class Site:
  def __init__(self, x, y, size, color, open, flowing, row, col):
    self.x = x
    self.y = y
    self.size = size
    self.color = color
    self.open = open
    self.flowing = flowing
    self.row = row
    self.col = col

  def draw(self):
    pygame.draw.rect(screen, self.color, [self.x, self.y, self.size, self.size])

  def return_rect(self):
    return pygame.Rect(self.x, self.y, self.size, self.size)

  def update(self):
    if self.open:
      self.color = (255, 255, 255)
      self.check_neighbors()
    if self.row == 0 and self.open:
      self.flowing = True
    if self.flowing:
      self.color = (0, 157, 186)
      
  def check_neighbors(self):
    places_to_check = [[self.row + 1, self.col], [self.row, self.col + 1], [self.row - 1, self.col], [self.row, self.col - 1]]
    for place in places_to_check:
      if place[0] < grid_size and place[0] > -1 and place[1] < grid_size and place[1] > -1:
        for site in site_list:
          if site.row == place[0] and site.col == place[1]:
            if site.flowing:
              self.flowing = True

def create_grid():
  site_list.clear()
  x = 100
  y = 0
  site_size = round((HEIGHT - 50) / grid_size)
  for i in range(grid_size):
    for j in range(grid_size):
      site_list.append(Site(x, y, site_size, (0, 0, 0), False, False, math.floor(y / site_size), math.floor((x - 100) / site_size)))
      x += site_size
    x = 100
    y += site_size

def create_lines():
  startx, starty = 100, 0
  endx, endy = 100, HEIGHT - 50
  site_size = round((HEIGHT - 50) / grid_size)
  for i in range(grid_size + 1):
    lines.append([startx, starty, endx, endy])
    startx += site_size
    endx += site_size
  startx, starty = 100, 0
  endx, endy = WIDTH - 100, 0
  site_size = round((HEIGHT - 50) / grid_size)
  for i in range(grid_size + 1):
    lines.append([startx, starty, endx, endy])
    starty += site_size
    endy += site_size

def display_text(text, x, y, color):
  text = my_font.render(text, False, color)
  screen.blit(text, (x, y))

def check_percolation():
  global site_list, percolates
  for site in site_list:
    if site.row == grid_size - 1:
      if site.flowing == True:
        percolates = True
  
choices = []
def set_choices():
  choices.clear()
  for i in range(grid_size):
    for j in range(grid_size):
      choices.append([i, j])

def randomed():
  for i in range(math.floor((3/5) * grid_size * grid_size)):
    choice = random.choice(choices)
    for site in site_list:
      if site.row == choice[0] and site.col == choice[1]:
        site.open = True
        choices.remove(choice)

create_grid()   
create_lines()

while in_game:
  screen.fill((130, 201, 217))
  check_percolation()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      in_game = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        grid_size = int(input("What size should the grid be: "))
        create_grid()
        lines.clear()
        create_lines()
        percolates = False
      if event.key == pygame.K_c:
        create_grid()
        lines.clear()
        create_lines()
        percolates = False
      if event.key == pygame.K_s:
        create_grid()
        lines.clear()
        create_lines()
        percolates = False
        set_choices()
        randomed()


    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      if mouse_pos[0] <= WIDTH - 100 and mouse_pos[0] >= 100 and mouse_pos[1] >= 0 and mouse_pos[1] <= HEIGHT - 50:
        chosen_site = [site for site in site_list if site.return_rect().collidepoint(mouse_pos)]
        chosen_site[0].open = True

  for site in site_list:
    site.draw()
    site.update()
  for line in lines:
    pygame.draw.line(screen, (255, 255, 255), (line[0], line[1]), (line[2], line[3]))

  if percolates == True:
    text = "Percolates"
  elif percolates == False:
    text = "It does not percolate"
  display_text(text, 250, 560, (0, 0, 0))

  pygame.display.update()

  clock.tick(60)

pygame.quit()
quit()