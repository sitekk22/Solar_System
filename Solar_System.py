import pygame
import math
pygame.init()


# Pygame initialization
WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

# Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (51, 153, 255)
DARKY_ORANGE = (204, 102, 0)
GREY = (160, 160, 160)
BRONZE_ORANGE = (255, 181, 89)

FONT = pygame.font.SysFont("cantrellregular", 30)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 300 / AU
    TIMESTEP = 3600*24 # 1 day
    RADIUS_SCALE = 3
    
    def __init__(self, x, y, radius, color, mass): 
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass # In KG
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        
        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit)>2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2 
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000/149.6e6 ,4)}AU", 1, WHITE)
            win.blit(distance_text, (x- 50, y- 10))
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2) # distance = sqrt(a**2 + b**2) 
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


# Main function

def main():
    run = True
    clock = pygame.time.Clock()
    
    # (x, y, radius, color, mass)
    
    sun = Planet(0, 0, 69 , YELLOW, 1.98892 * 10**30) # 1/3 of radius
    sun.sun = True
    
    mercury = Planet(0.39 * Planet.AU, 0, 2.44 * Planet.RADIUS_SCALE, GREY, 3.30 * 10**23)
    mercury.y_vel = 47.4 * 1000
    
    venus = Planet(0.72 * Planet.AU, 0, 6.05 * Planet.RADIUS_SCALE, BRONZE_ORANGE, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000
    
    earth = Planet(1 * Planet.AU, 0 , 6.37 * Planet.RADIUS_SCALE, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    
    mars = Planet(1.52 * Planet.AU, 0, 3.39 * Planet.RADIUS_SCALE, DARKY_ORANGE , 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    
    
    
    
    planets = [sun, mercury, venus, earth, mars]
    
    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        

        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()       
    
    pygame.quit()


main()
                