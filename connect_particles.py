import pygame
import random
import argparse
pygame.init()

class Colors:
    Navy = (0, 31, 63)
    Blue = (0, 116, 217)
    Aqua = (127, 219, 255)
    Teal = (57, 204, 204)
    Olive = (61, 153, 112)
    Green = (46, 204, 64)
    Lime = (1, 255, 112)
    Yellow = (255, 220, 0)
    Orange = (255, 133, 27)
    Red = (255, 65, 54)
    Maroon = (133, 20, 75)
    Fushcia = (240, 18, 190)
    Purple = (177, 13, 201)
    Black = (17, 17, 17)
    Gray = (170, 170, 170)
    Silver = (221, 221, 221)
    White = (245, 245, 245)
    all = [Navy, Blue, Aqua, Teal, Olive, Green, Lime, Yellow, Orange, Red, Maroon, Fushcia, Purple, Black, Gray, Silver, White]

    def inverse(self, color):
        return (abs(color[0]-255), abs(color[1]-255), abs(color[2]-255))

    def random(self, *args):
        all = []
        for arg in args:
            if arg in self.all:
                for color in self.all:
                    if color != arg:
                        all.append(color)
        if len(all) <= 1:
            all = self.all

        return random.choice(all)

colors = Colors()

id = 0
class Particle:
    def __init__(self, x, y, xPush, yPush, color):
        global id
        self.x, self.y, self.xPush, self.yPush = x, y, xPush, yPush
        self.connections = []
        self.color = color
        id += 1
        self.id = id

    def draw(self, surf):
        for connection in self.connections:
            pygame.draw.line(surf, self.color, (round(self.x), round(self.y)), (round(connection.x), round(connection.y)))

    def mouseMove(self, particle_array, connectionRange):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.x = mouse_x
        self.y = mouse_y

        self.connectionLogic(particle_array, connectionRange)

    def move(self, width, height, particle_array, connectionRange):
        if self.x <= 0 or self.x >= width:
            self.xPush = -self.xPush

        if self.y <= 0 or self.y >= height:
            self.yPush = -self.yPush

        self.x += self.xPush
        self.y += self.yPush

        self.connectionLogic(particle_array, connectionRange)

    def connectionLogic(self, particle_array, connectionRange):
        for particle in particle_array:
            if abs(round(particle.x) - round(self.x)) <= connectionRange and abs(round(particle.y) - round(self.y)) <= connectionRange:
                self.connections.append(particle)
            else:
                if particle in self.connections:
                    self.connections.remove(particle)
            if self in particle.connections and particle in self.connections:
                self.connections.remove(particle)

mainParticle = Particle(0, 0, 0, 0, colors.random(colors.Gray))

def start():
    clock = pygame.time.Clock()

    parser = argparse.ArgumentParser()

    parser.add_argument("--width", default=1200, type=int, help="Window width.", dest="width")
    parser.add_argument("--height", default=800, type=int, help="Window height.", dest="height")
    parser.add_argument("--maxspeed", default=3, type=int, help="The maximum speed of the particles.", dest="max_speed")
    parser.add_argument("--minspeed", default=1, type=int, help="The minimum speed of the particles.", dest="min_speed")
    parser.add_argument("--particles", default=50, type=int, help="The amount of particles summoned.", dest="n_particles")
    parser.add_argument("--connectat", default=150, type=int, help="When a particle reaches this much to another particle connect them.", dest="connectionRange")
    parser.add_argument("--unifiedcolors", action="store_true", dest="unicolor", help="Unify the colors of the particles.")

    args = parser.parse_args()

    width, height = (args.width, args.height)
    win = pygame.display.set_mode((width, height))
    max_speed = args.max_speed
    min_speed = args.min_speed
    n_particles = args.n_particles
    connectionRange = args.connectionRange
    unifiedColors = args.unicolor

    particles = [Particle(random.randint(0, width), random.randint(0, height), random.randrange(min_speed, max_speed), random.randrange(min_speed, max_speed), colors.random(colors.Gray)) for _ in range(n_particles)]

    if unifiedColors:
        color = colors.Black # Each color we add here is not included in the randomizer
        for particle in particles:
            particle.color = color
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()

        win.fill(colors.Gray)

        mainParticle.mouseMove(particles, connectionRange)
        mainParticle.draw(win)

        for particle in particles:
            particle.move(width, height, particles, connectionRange)
            particle.draw(win)

        pygame.display.update()

start()
