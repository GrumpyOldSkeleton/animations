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


#==============================================================
#==============================================================
#==============================================================
#
#
# set RENDER_GIF to true if you want to render the frames
#
# leave set to false if you just want to view the animation
#
RENDER_GIF = True
START_RENDER_AT_FRAME = 180
NUM_FRAMES_TO_RENDER  = 179
END_RENDER_AT_FRAME   = START_RENDER_AT_FRAME + NUM_FRAMES_TO_RENDER
#
#
# command to convert pngs to gif:
#
# ffmpeg -i %d.png output.gif
#
#==============================================================
#==============================================================
#==============================================================


class Looper():
    
    def __init__(self, seed, colour1, colour2, draw_radius, randomiser_strength):
        
        self.noise = OpenSimplex(seed)
        self.noise_smoothness   = [80, 30] # this defines how smooth the randomness is
        self.noise_offset_angle = 0
        self.noise_angle_step   = 2 # must cleanly divide 360 for loop to work = 2, 3, 4, 5, 6, 8, 9, 10, 12
        self.line_colour = colour1
        self.bead_colour = colour2
        self.draw_radius = draw_radius # radius of our drawn circle
        self.randomiser_strength = randomiser_strength # the multiplier for the random values
        
    def draw(self):
        

        # this is the big circle that walks a circular path through the random noise field
        # stepping through 1 frame at a time. 
        self.noise_offset_angle += self.noise_angle_step
        if self.noise_offset_angle == 360 - self.noise_angle_step:
            self.noise_offset_angle = 0
        
        # the offsets are cos and sin. This moves us through the noise field
        # in a circular path so that by the time the noise_offset_angle reaches 360
        # we will be back at our starting position and the loop will work
        pathx = math.cos(math.radians(self.noise_offset_angle)) 
        pathy = math.sin(math.radians(self.noise_offset_angle))
        
        # this bit now draws the whole circle for this frame, 
        # adding in noise values to each point
        
        numpoints = 360
    
        for a in range(0, numpoints):
            
            circle_x = math.cos(math.radians(a)) * self.draw_radius
            circle_y = math.sin(math.radians(a)) * self.draw_radius
            
            # each point of the circle gets a new random noise value from a circle centered at pathx, pathy
            nx = 0
            ny = 0
            
            for smooth_val in self.noise_smoothness:
                nx += (self.noise.noise2d(pathx + circle_x / smooth_val, pathx + circle_y / smooth_val))
                ny += (self.noise.noise2d(pathy + circle_x / smooth_val, pathy + circle_y / smooth_val))
            
            # add the noise values to the polar point
            circle_x += ORIGINX + (nx * self.randomiser_strength)
            circle_y += ORIGINY + (ny * self.randomiser_strength)
            
            pygame.draw.rect(screen, self.line_colour, [circle_x, circle_y, 1, 1])
            
            # draw a bead
            if a % 40 == 0:
                 pygame.draw.circle(screen, self.bead_colour, (circle_x, circle_y), 3)
        
        



class Animation():
    
    def __init__(self):
        
        # gif stuff
        self.render          = RENDER_GIF
        self.rendering        = False
        self.render_done      = False
        self.frame_number     = 0

        self.loopers = []
                       # seed, colour1,        colour2,        draw_radius, randomiser_strength):
        looper1 = Looper(6,    (98, 170, 221), (221, 248, 208), 120,         40)
        looper2 = Looper(3, (127, 227, 220), (221, 248, 208), 120, 40 )
        looper3 = Looper(5, (160, 245, 198), (221, 248, 208), 120, 40 )
        looper4 = Looper(8, (84, 41, 194), (84, 99, 217), 200, 60 )
        self.loopers.append(looper1)
        self.loopers.append(looper2)
        self.loopers.append(looper3)
        self.loopers.append(looper4)
        
    def renderFrame(self):
        
        frame_number = self.frame_number - START_RENDER_AT_FRAME
        
        filename = '{}.png'.format(frame_number)
        pygame.image.save(screen, filename)       
        print('Rendered file ' + filename)
        
    def draw(self):
        
        if self.render:
            self.rendering = (self.frame_number >= START_RENDER_AT_FRAME and self.frame_number <= END_RENDER_AT_FRAME)
        
        for looper in self.loopers:
            looper.draw()
        
        if self.rendering:
            self.renderFrame()
            
        self.frame_number += 1            


animation = Animation()

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
    animation.draw()
    
    clock.tick(55)
    pygame.display.flip()
    
pygame.quit()
