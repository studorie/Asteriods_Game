import pygame
from circleshape import CircleShape
from constants import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)


    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        random_angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(random_angle) * 1.2
        velocity2 = self.velocity.rotate(-random_angle) * 1.2

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        new_asteroid1.velocity = velocity1
        new_asteroid2.velocity = velocity2

        for group in self.groups():
            group.add(new_asteroid1, new_asteroid2)


    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, width=2)


    def update(self, dt):
        self.position += self.velocity * dt
