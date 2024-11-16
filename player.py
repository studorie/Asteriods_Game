import pygame
from circleshape import CircleShape
from constants import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, CircleShape.PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0


    def shoot(self):
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = direction * PLAYER_SHOOT_SPEED

        return Shot(self.position.x, self.position.y, velocity)


    def handle_input(self, event, shots_group):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.shoot_timer <= 0:
                shot = self.shoot()
                shots_group.add(shot)
                self.shoot_timer = PLAYER_SHOOT_COOLDOWN


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]


    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), width=2)


    def rotate(self, dt, direction):
        self.rotation += direction * PLAYER_TURN_SPEED * dt


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def update(self, dt):
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
            self.rotate(dt, 1)


        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)



class Shot(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity


    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius)


    def update(self, dt):
        self.position += self.velocity * dt
