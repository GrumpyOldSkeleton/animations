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

# create a back surface
back_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))

# and a fader
fader_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
fader_surface.fill([0,0,0]) 
# the alpha governs how fast the previous frame will fade
fader_surface.set_alpha(50)


class Looper():
    
    def __init__(self, seed, colour1, colour2):
        
        self.noise = OpenSimplex(seed)
        self.noise_smoothness   = [200, 50, 30] # this defines how smooth the randomness is
        self.noise_offset_angle = 0
        self.noise_angle_step   = 1 # must cleanly divide 360 for loop to work = 2, 3, 4, 5, 6, 8, 9, 10, 12
        self.colour1 = colour1
        self.colour2 = colour2
        
    def draw(self):
        
        # radius of our drawn circle
        radius = 120
        
        # the multiplier for the random values
        noise_multiplier = 40
        
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
            circle_x += ORIGINX + (nx * noise_multiplier)
            circle_y += ORIGINY + (ny * noise_multiplier)
            
            pygame.draw.rect(screen, self.colour1, [circle_x, circle_y, 1, 1])
            
            # draw a bead
            if a % 40 == 0:
                 pygame.draw.circle(screen, self.colour2, (circle_x, circle_y), 3)
        
        
looper1 = Looper(6, (180, 180, 0), (255, 255, 0) )
looper2 = Looper(3, (200, 0, 0), (220, 0, 170) )
looper3 = Looper(5, (170, 0, 0), (255, 0, 0) )

loopers = []

loopers.append(looper1)
loopers.append(looper2)
loopers.append(looper3)

screen.fill([0,0,0]) 

done = False

while not done:
    
    # blit the previous screen to the background
    back_surface.blit(screen, (0,0))
    # and fade it by blitting the fader over it
    back_surface.blit(fader_surface, (0,0))
    
    screen.fill([0,0,0]) 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                done = True
                
    # blit the previous frame to the screen
    screen.blit(back_surface, (0,0))
    # and draw the new frame
    for looper in loopers:
        looper.draw()
    
    clock.tick(25)
    pygame.display.flip()
    
pygame.quit()
