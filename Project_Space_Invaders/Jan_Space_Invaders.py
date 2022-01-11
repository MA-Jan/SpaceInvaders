# Mohammad Jan
# Nov 28 2020
# Space_Invaders V.1

##### INITIALIZATIONS

import random
import pygame

pygame.init() # initializes pygame after importing. Must be done for pygame to work when running

screen_width = 500
screen_height = 500

Screen = pygame.display.set_mode((screen_width,screen_height)) # creates pygame window with size ((x,y))
pygame.display.set_caption('Space Invaders') # title for window above

background = pygame.image.load('SI_background.png')
ship_image = pygame.image.load('SI_ship.png')
invader_image = pygame.image.load('SI_invader.png')
block_image = pygame.image.load('SI_block.png')
cannon_image = pygame.image.load('SI_cannon.png')

fps = pygame.time.Clock()

flag =  True

##### CLASSES

class Ship(object):
    def __init__(self):
        self.x = 250
        self.y = 400
        self.width = 35
        self.height = 35
        self.speed = 2
        self.life = 3

    def move(self, ship, block):
        keys = pygame.key.get_pressed() # sets up list that will allow to check what keys are being pressed
        
        # COLISSION DETECTION + MOVEMENT
        
        if keys[pygame.K_UP] and ship.y > 0:
            if ship.x not in range((block.x - ship.width), (block.x + block.width)):
                    ship.y-= ship.speed      
            elif ship.x in range((block.x - ship.width), (block.x + block.width)):
                if ship.y > (block.y+block.height) or (ship.y+ship.height) <= block.y:  
                    ship.y -= ship.speed

        if keys[pygame.K_DOWN] and ship.y < (500-36):
            if ship.x not in range((block.x - ship.width), (block.x + block.width)):
                ship.y+= ship.speed
            elif ship.x in range((block.x - ship.width), (block.x + block.width)):
                if (ship.y+ship.height) < (block.y-1) or ship.y >= (block.y+block.height):
                    ship.y += ship.speed   
            
        if keys[pygame.K_LEFT] and ship.x > 0:
            if ship.y not in range((block.y-ship.height), (block.y+block.height)):
                ship.x-= ship.speed
            elif ship.y in range((block.y-ship.height), (block.y+block.height)):
                if ship.x > (block.x+block.width+2) or (ship.x+ship.width) < block.x:
                    ship.x -= ship.speed
            
        if keys[pygame.K_RIGHT] and ship.x < (500-33):
            if ship.y not in range((block.y-ship.height), (block.y+block.height)):
                ship.x+=ship.speed
            elif ship.y in range((block.y-ship.height), (block.y+block.height)):
                if (ship.x+ship.width) < (block.x-1) or ship.x > (block.x+block.width-1):
                    ship.x += ship.speed
                    
    def draw(self):
        Screen.blit(ship_image, (self.x,self.y)) # blit is used to draw an exteral image into the pygame window
        
class Block(object):
    def __init__(self):
        self.x = (250-56)
        self.y = 350
        self.width = 142
        self.height = 20
        
    def draw(self): 
        Screen.blit(block_image, (self.x, self.y))

class Invader(object):
    def __init__(self):
        self.x = random.randint(0,450)
        self.y = 0
        self.width = 30
        self.height = 30
        self.speed = 2
        self.respawn = False
        
    def strafe(self, invader, ship):
        invader.respawn = False
        invader.y += invader.speed
        
        if (invader.y + invader.height) in range((ship.y - 2), (ship.y + ship.height + invader.height)):
            if invader.x < (ship.x + ship.width) and (invader.x + invader.width) > ship.x:
                invader.respawn = True
                ship.life -= 1
                
        if (invader.y) > 500:
            ship.life -= 1
            invader.respawn = True
                    
        
    def draw(self):
        Screen.blit(invader_image, (self.x,self.y))
        
class Cannon(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.height = 18
        self.width = 8
        self.speed = 3
        
        self.shot = False
        
    def shoot(self, cannon):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            if cannon.shot == False:
                cannon.shot = True
                cannon.x = int(ship.x + 17)
                cannon.y = ship.y - cannon.height
            
    def draw(self, invader, cannon, block):
        Screen.blit(cannon_image, (cannon.x, cannon.y))
        cannon.y -= cannon.speed
        
        if cannon.y <= (invader.y+invader.height): # if statements determining if cannon shot has hit an enemy
            if (cannon.x + cannon.width) > invader.x and cannon.x < (invader.x + invader.width):
                cannon.shot = False
                invader.respawn = True
            
        if cannon.y <= (block.y + block.height) and cannon.y >= block.y: # if statements determining if cannon shot has hit the block
            if (cannon.x + cannon.width) >= block.x and cannon.x < (block.x + block.width):
                cannon.shot = False
                
        if cannon.y <= 0:
            cannon.shot = False

##### INSTANCES

ship = Ship() # creates instance of ship and block class
block = Block()
invader = Invader()
cannon = Cannon()

##### GAME LOOP

while flag:
    
    fps.tick(60) # fps
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
            
    ship.move(ship, block)
    invader.strafe(invader, ship)
    cannon.shoot(cannon)
    
    Screen.blit(background, (0,0)) # CREATES NEW SCREEN TO BLANK OUT OLD IMAGES
    
    ship.draw() # draws objects onto screen
    block.draw()
    invader.draw()
    
    if cannon.shot == True: # uses booleans to check whether to draw certain objects, such as 'cannon.shot' to see if the cannon needs to be drawn
        cannon.draw(invader, cannon, block) # will draw the cannon when space is pressed (done through 'cannon.shoot(cannon)' and will draw it for as long a it doesn't touch anything 
    
    if invader.respawn == True: # if the cannon hits the invader the invader will respawn with these new coordinates
        invader.y = 0
        invader.x = random.randint(0,450)
    
    if ship.life == 0:
        flag = False
    
    pygame.display.update()
    
pygame.quit()
