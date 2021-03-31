import pygame
import math  
from vector import Vector2
  
done = False
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
ORIGINX = SCREEN_WIDTH / 2
ORIGINY = SCREEN_HEIGHT / 2
pygame.init()
pygame.display.set_caption("Animated Points")
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
clock = pygame.time.Clock()


#==============================================================
#==============================================================
#==============================================================
#
#
# set RENDER_GIF to true if you want to render the frames
#
# leave set to false if you just want to view the animation
#
RENDER_GIF = False
NUM_FRAMES_TO_RENDER = 180
#
#
#
#==============================================================
#==============================================================
#==============================================================

class CircleWithRotator():
    
    def __init__(self, x, y, radius, start_angle, angle_speed):
    
        self.originx     = x
        self.originy     = y
        self.radius      = radius
        self.angle       = start_angle
        self.angle_speed = angle_speed 
        self.rotator_pos = Vector2(0, 0)
        
    def update(self):
        
        self.angle += self.angle_speed
        if self.angle > (360 - self.angle_speed):
            self.angle = 0
        
        self.rotator_pos.x = self.originx + (self.radius * math.cos(math.radians(self.angle)))
        self.rotator_pos.y = self.originy + (self.radius * math.sin(math.radians(self.angle)))

    def draw(self):
        
        self.update()
        
        # draw the circle
        pygame.draw.circle(screen, (100,0,75), (self.originx, self.originy), self.radius, 1)
        
        # draw the rotator
        pygame.draw.circle(screen, (0,255,255), (self.rotator_pos.x, self.rotator_pos.y), 4)
        
   
class Square():
    
    def __init__(self):
        
        # corners are pointers to the circle rotator vector objects
        self.corners = []
    
    def setCornerPoints(self, corner_points):
        
        self.corners = corner_points

    def getPointsBetween(self, v1, v2, num_points):
        
        # returns a list of equally spaced points between Vector1 and Vector2
        # ie, points along a line between 2 of our corners.
        # each point is stored in the list as an xy tuple
        
        points = []
        
        # get a copy of V2 that is safe to mess with
        dist = v2.getCopy()
        
        # subtract the other top corner
        dist.sub(v1)
        
        # now I can work out the distance between the points
        distance_between_points = dist.mag()
        step = distance_between_points / (num_points+1)
        dist.normalise()
     
        # this calculates all the steps along the line
        for i in range(num_points):
            
            dist.mult(step * (i+1))
            x = v1.x + dist.x
            y = v1.y + dist.y
            points.append((x,y))
            dist.normalise()
        
        return points

        
    def draw(self):
        
        num_points    = 8
        top_points    = self.getPointsBetween(self.corners[0], self.corners[1], num_points)
        bottom_points = self.getPointsBetween(self.corners[3], self.corners[2], num_points)
            
        # draw points and lines joining the points
        for tp, bp in zip(top_points, bottom_points):
            
            pygame.draw.circle(screen, (255,255,255), tp, 3)
            pygame.draw.circle(screen, (255,255,255), bp, 3)
            pygame.draw.line(screen, (255,0,255), tp, bp)

        # draw the lines that make up our square
        for i in range(0, len(self.corners)-1):
             
            p1 = self.corners[i]   
            p2 = self.corners[i+1]
            pygame.draw.line(screen, (255,255,0), (p1.x, p1.y), (p2.x, p2.y))
            
            # join last corner position to 1st
            if i == len(self.corners)-2:
                p1 = self.corners[-1]
                p2 = self.corners[0]
                
                pygame.draw.line(screen, (255,255,0), (p1.x, p1.y), (p2.x, p2.y))
        
        
        
        
class Animation():
    
    def __init__(self):
        
        # gif stuff
        self.rendering        = RENDER_GIF
        self.render_done      = False
        self.frame_number     = 0
        self.frames_to_render = NUM_FRAMES_TO_RENDER
        
        # these values set up where the circles will be placed
        # their posx, posy, radius, start angle, and anglespeed
        #
        #                      px    py   r     a  s   
        self.circle_params = [(200,  60,  50,   0, 4),
                              (200, 150,  82,  90, 2),
                              (60,   60,  50, 180, 2),
                              (80,  200,  75, 270, 1)]
        self.circles = []
        self.square = Square()

        # make dem circles!
        for x, y, radius, startangle, angleinc in self.circle_params:
            c = CircleWithRotator(x, y, radius, startangle, angleinc)
            self.circles.append(c)
            
        # gather all the circle rotor vectors
        positions = []
        for c in self.circles:
            pos = (c.rotator_pos)
            positions.append(pos)
            
        # and pass them in to the spinny square
        self.square.setCornerPoints(positions)
        
    def renderFrame(self):
        
        filename = '{}.png'.format(self.frame_number)
        pygame.image.save(screen, filename)       
        print('Rendered file ' + filename)
        
    def draw(self):
        
        if self.rendering and self.frame_number == self.frames_to_render:
            self.rendering = False
            print('Render completed.')
        else:
            self.frame_number += 1
            
        for c in self.circles:
            c.draw()
            
        self.square.draw()
        
        if self.rendering:
            self.renderFrame()
            


animation = Animation()

while not done:
    
    screen.fill([0,0,0]) 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE):
                done = True
                
    mousex, mousey = pygame.mouse.get_pos()

    animation.draw()
    clock.tick(50)
    pygame.display.flip()
    

pygame.quit()
