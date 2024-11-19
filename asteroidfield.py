import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        """Initialize the asteroid field and its spawn timer."""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        """
        Spawns an asteroid with a given radius, position, and velocity.

        :param radius: The radius of the asteroid.
        :param position: The initial position of the asteroid as a vector.
        :param velocity: The velocity of the asteroid as a vector.
        """
        size = None
        if radius == ASTEROID_MAX_RADIUS:
            size = "large"
        elif radius == ASTEROID_MIN_RADIUS * 2:
            size = "medium"
        elif radius == ASTEROID_MIN_RADIUS:
            size = "small"

        # Load animation frames based on asteroid size
        frames = Asteroid.load_asteroid_frames(size) if size else None

        asteroid = Asteroid(position.x, position.y, radius, frames)
        asteroid.velocity = velocity

        # Add asteroid to all relevant sprite groups
        for group in self.groups():
            group.add(asteroid)

    def update(self, dt):
        """
        Updates the asteroid field by checking if new asteroids need to be spawned.

        :param dt: The delta time since the last frame.
        """
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            radius = ASTEROID_MIN_RADIUS * kind

            # Spawn a new asteroid
            self.spawn(radius, position, velocity)
