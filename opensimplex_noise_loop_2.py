import pygame
import math
from opensimplex import OpenSimplex
  
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
ORIGINX = SCREEN_WIDTH / 2
ORIGINY = SCREEN_HEIGHT / 2
pygame.init()
pygame.display.set_caption("OpenSimplex Loop")
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
clock = pygame.time.Clock()


class Looper():
    
    def __init__(self):
        
        self.noise = OpenSimplex(1)
        self.noise_smoothness   = [300, 250, 100, 30] # this defines how smooth the randomness is
        self.noise_offset_angle = 0
        self.noise_angle_step   = 2 # must cleanly divide 360 for loop to work = 2, 3, 4, 5, 6, 8, 9, 10, 12
        
    def draw(self):
        
        # radius of our drawn circle
        radius = 90
        
        # the multiplier for the random values
        random_effect = 40
        
        # this is the big circle that walks a circular path through the random noise field
        # stepping through 1 frame at a time. 
        self.noise_offset_angle += self.noise_angle_step
        if self.noise_offset_angle == 360 - self.noise_angle_step:
            self.noise_offset_angle = 0
            print('looppoint')
        
        # the offsets are cos and sin. This moves us through the noise field
        # in a circular path so that by the time the noise_offset_angle reaches 360
        # we will be back at our starting position and the loop will work
        pathx = math.cos(math.radians(self.noise_offset_angle)) 
        pathy = math.sin(math.radians(self.noise_offset_angle))
        
        # this bit now draws the whole circle for this frame, 
        # adding in noise values to each point
        
        numpoints = 360
    
        for a in range(0, numpoints):
            
            circle_x = math.cos(math.radians(a)) * radius
            circle_y = math.sin(math.radians(a)) * radius
            
            # each point of the circle gets a new random noise value from a circle centered at pathx, pathy
            nx = 0
            ny = 0
            
            for smooth_val in self.noise_smoothness:
                nx += (self.noise.noise2d(pathx + circle_x / smooth_val, pathx + circle_y / smooth_val))
                ny += (self.noise.noise2d(pathy + circle_x / smooth_val, pathy + circle_y / smooth_val))
            
            # add the noise values to the polar point
            circle_x += ORIGINX + (nx * random_effect)
            circle_y += ORIGINY + (ny * random_effect)
            
            pygame.draw.rect(screen, (255, 255, 0), [circle_x, circle_y, 1, 1])
            
            # draw a bead
            if a % 40 == 0:
                 pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 3)
        
        
looper = Looper()

done = False

while not done:
    
    screen.fill([0,0,0]) 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                done = True
                
    mousex, mousey = pygame.mouse.get_pos()
    looper.draw()
    clock.tick(25)
    pygame.display.flip()
    
pygame.quit()
