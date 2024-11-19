import pygame
from circleshape import CircleShape
from constants import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, frames=None):
        super().__init__(x, y, radius)
        self.velocity = pygame.Vector2(0, 0)
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 10  # Frames per second
        self.time_since_last_frame = 0
        self.explosion_frames = None
        self.exploding = False  # To track explosion state
        self.explosion_frame = 0
        self.explosion_speed = 15  # Frames per second for explosion
        self.explosion_time_since_last_frame = 0
        self.active = True  # Active state for collisions

        # Load sound for large and medium asteroids
        if radius > ASTEROID_MIN_RADIUS:
            self.explosion_sound = pygame.mixer.Sound("sprites/asteroids/medium-destroy.mp3")
        else:
            self.explosion_sound = pygame.mixer.Sound("sprites/asteroids/small-destroy.mp3")
        self.explosion_sound.set_volume(0.25)


    def start_explosion(self):
        """Trigger the explosion animation and deactivate collisions."""
        self.exploding = True
        self.explosion_frames = Asteroid.load_explosion_frames()
        self.explosion_frame = 0
        self.active = False  # Deactivate asteroid for collision purposes

        # Play the explosion sound for large and medium asteroids
        if self.explosion_sound:
            self.explosion_sound.play()

    def split(self):
        """Splits the asteroid into smaller ones if possible."""
        self.start_explosion()  # Trigger explosion animation

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        random_angle = random.uniform(20, 50)

        velocity1 = self.velocity.rotate(random_angle) * 1.2
        velocity2 = self.velocity.rotate(-random_angle) * 1.2

        size = None
        if new_radius == ASTEROID_MAX_RADIUS:
            size = "large"
        elif new_radius == ASTEROID_MIN_RADIUS * 2:
            size = "medium"
        elif new_radius == ASTEROID_MIN_RADIUS:
            size = "small"

        frames = Asteroid.load_asteroid_frames(size) if size else None

        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius, frames)
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius, frames)

        new_asteroid1.velocity = velocity1
        new_asteroid2.velocity = velocity2

        for group in self.groups():
            group.add(new_asteroid1, new_asteroid2)

    def collision(self, other):
        """Override collision to ignore inactive (exploding) asteroids."""
        if not self.active:
            return False
        return super().collision(other)

    def update(self, dt):
        """Updates the asteroid's position and animation frame."""
        if self.exploding:
            self.explosion_time_since_last_frame += dt
            if self.explosion_time_since_last_frame > 1 / self.explosion_speed:
                self.explosion_frame += 1
                self.explosion_time_since_last_frame = 0
                if self.explosion_frame >= len(self.explosion_frames):
                    self.kill()  # Remove asteroid completely after explosion finishes
            return

        # Normal asteroid behavior
        self.position += self.velocity * dt
        if self.frames:
            self.time_since_last_frame += dt
            if self.time_since_last_frame > 1 / self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.time_since_last_frame = 0

    def draw(self, screen):
        """Renders the asteroid or explosion on the screen."""
        if self.exploding:
            if self.explosion_frame < len(self.explosion_frames):
                frame = self.explosion_frames[self.explosion_frame]
                frame_rect = frame.get_rect(center=(self.position.x, self.position.y))
                screen.blit(frame, frame_rect)
        elif self.frames:
            frame = self.frames[self.current_frame]
            scaled_frame = pygame.transform.scale(frame, (self.radius * 2, self.radius * 2))
            frame_rect = scaled_frame.get_rect(center=(self.position.x, self.position.y))
            screen.blit(scaled_frame, frame_rect)
        else:
            pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, width=2)

    @staticmethod
    def load_asteroid_frames(size):
        """Loads animation frames for asteroids based on their size."""
        if not size:
            return None

        frames = []
        for i in range(48):  # Adjust the range if the number of frames differs
            path = f"sprites/asteroids/{size}/tile{i:03}.png"
            try:
                frame = pygame.image.load(path).convert_alpha()
                frames.append(frame)
            except FileNotFoundError:
                continue

        return frames

    @staticmethod
    def load_explosion_frames():
        """Loads explosion animation frames."""
        frames = []
        for i in range(17):  # Explosion frames
            path = f"sprites/asteroids/destroyed/tile{i:03}.png"
            try:
                frame = pygame.image.load(path).convert_alpha()
                frames.append(frame)
            except FileNotFoundError:
                continue

        return frames
