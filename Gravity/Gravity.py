import pygame,sys,random,math

pygame.init()

#screen variables
screenSize = width,height = 900,600
backgroundColor = (255,255,255)

#gravity variables
gravityx = math.pi
gravityy = 0.0005
elasticity = 0.75
massOfAir = 0.02




def randomColor():
    #get a number between 0 and 255
    randColor = random.randint(0,255)
    return randColor

def addVectors(angle,speed, gravityx,gravityy):
    x = math.sin(angle)*speed + math.sin(gravityx)*gravityy #create one side of triangele
    y = math.cos(angle)*speed + math.cos(gravityx)*gravityy # create second side of triangle from vectors
    length = math.hypot(x,y) #find new length by taking hypotenuse
    angleNew = 0.5*math.pi - math.atan2(y,x)
    return(angleNew,length)

#lets use know we found a particle
def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

#collide particles
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
	    
        p1.speed *= elasticity
	    
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap

#make a particle now
class Particle:
    def __init__(self,x,y,size,mass = 1):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.color = (randomColor(),randomColor(),randomColor())
        self.thickness = 0
        self.speed = 0.01
        self.angle = math.pi/2
        self.drag = (self.mass/(self.mass + massOfAir)) ** self.size

    def display(self):
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.size,self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        #need to subtract the y because positive y is down
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag
        (self.angle,self.speed) = (addVectors(self.angle,self.speed,gravityx,gravityy))

    def bounce(self):
        #boundaries at x = 0, x= width, y = 0, y = height
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x #calcualte how much we exceeded boundary by
            self.angle = - self.angle
            #need to create drag so we dont bounce forever
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
           #need to create drag so we dont bounce forever 
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            #again here
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            #all all the boundary conditions
            self.speed *= elasticity

   



screen = pygame.display.set_mode(screenSize)
screen.fill(backgroundColor)
pygame.display.set_caption("Gravity")

numberParticles = 10
particleArray = []

for n in range(numberParticles):
    size = random.randint(20,50)
    #randomly decide location. wnat to make sure it's in the window
    x = random.randint(size,width-size)
    y = random.randint(size,height-size)
    #calculate random density for mass
    density = random.randint(10,20)
    p = Particle(x,y,size,density*size*2)
    #returns the next random floating point number between 0.0 and 1.0
    p.speed = random.random()
    p.angle = random.uniform(0,math.pi*2)
    particleArray.append(p)


selected_particle = None

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(particleArray, mouseX, mouseY)
            
        elif event.type == pygame.MOUSEBUTTONUP:
                selected_particle = None

        if selected_particle:
            #selected_particle.color = (255,0,0)
            #want to be able to throw the particles around
            (mouseX, mouseY) = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.angle = math.atan2(dy, dx) + 0.5*math.pi
            selected_particle.speed = math.hypot(dx, dy) * 0.005
            

        
            
            
    screen.fill(backgroundColor)
    #for loop to draw all the circles
    for i,particle in enumerate(particleArray):
        if particle != selected_particle:
            particle.move()
            particle.bounce()
        for particle2 in particleArray[i+1:]:
            collide(particle,particle2)

        particle.display()

    pygame.display.flip()

pygame.quit()
sys.exit()


