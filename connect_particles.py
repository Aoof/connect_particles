from custom import Colors
import pygame
import random
pygame.init()

colors = Colors()


id = 0
class Particle:
    connected = False
    connections = []
    def __init__(self, x, y, xPush, yPush, color):
        global id
        self.x, self.y, self.xPush, self.yPush = x, y, xPush, yPush
        self.color = color
        id += 1
        self.id = id

    def draw(self, surf):
        if self.connected:
            for connection in self.connections:
                pygame.draw.line(surf, self.color, (round(self.x), round(self.y)), (round(connection.x), round(connection.y)))

    def mouseMove(self, width, height, particle_array, connectionRange):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.x = mouse_x
        self.y = mouse_y

        if not self.connected:
            for particle in particle_array:
                if abs(particle.x - self.x) < connectionRange and abs(particle.y - self.y) < connectionRange:
                    self.connected = True
                    self.connections.append(particle)
        else:
            for particle in particle_array:
                if abs(particle.x - self.x) < connectionRange and abs(particle.y - self.y) < connectionRange:
                    self.connected = True
                    self.connections.append(particle)
            for connection in self.connections:
                if abs(connection.x - self.x) >= connectionRange and abs(connection.y - self.y) >= connectionRange:
                    self.connections.remove(connection)
            if len(self.connections):
                self.connected = True
            else:
                self.connected = False

    def move(self, width, height, particle_array, connectionRange):
        if self.x <= 0 or self.x >= width:
            self.xPush = -self.xPush

        if self.y <= 0 or self.y >= height:
            self.yPush = -self.yPush

        self.x += self.xPush
        self.y += self.yPush

        if not self.connected:
            for particle in particle_array:
                if abs(particle.x - self.x) < connectionRange and abs(particle.y - self.y) < connectionRange:
                    self.connected = True
                    self.connections.append(particle)
        else:
            for particle in particle_array:
                if abs(particle.x - self.x) < connectionRange and abs(particle.y - self.y) < connectionRange:
                    self.connected = True
                    self.connections.append(particle)
            for connection in self.connections:
                if abs(connection.x - self.x) >= connectionRange and abs(connection.y - self.y) >= connectionRange:
                    self.connections.remove(connection)
            if len(self.connections):
                self.connected = True
            else:
                self.connected = False
mainParticle = Particle(0, 0, 0, 0, colors.random())

def start():
    width, height = (1200, 800)
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    max_speed = 3
    min_speed = 1
    n_particles = 50
    connectionRange = 40

    particles = [Particle(random.randint(0, width), random.randint(0, height), random.randrange(min_speed, max_speed), random.randrange(min_speed, max_speed), colors.random()) for _ in range(n_particles)]

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()

        win.fill((255, 255, 255))

        mainParticle.mouseMove(width, height, particles, connectionRange)
        mainParticle.draw(win)

        for particle in particles:
            particle.move(width, height, particles, connectionRange)
            particle.draw(win)

        pygame.display.update()

start()
