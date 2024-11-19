import pygame
from circleshape import CircleShape
from constants import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, CircleShape.PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.invincible = False  # Player starts non-invincible
        self.invincible_timer = 0  # Timer for invincibility
        
        # Explosion-related attributes
        self.exploding = False
        self.explosion_frames = self.load_explosion_frames()
        self.explosion_frame = 0
        self.explosion_speed = 30  # Frames per second for faster explosion
        self.explosion_time_since_last_frame = 0
        self.explosion_position = None  # Track explosion position separately

        # Load the ship sprite and scale it
        self.sprite = pygame.image.load("sprites/player/ship.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (65, 65))  # Adjust size as needed

        # Load the explosion sound
        self.explosion_sound = pygame.mixer.Sound("sprites/player/p-explosion.mp3")
        self.laser_sound = pygame.mixer.Sound("sprites/player/laser.mp3")
        self.laser_sound.set_volume(1)
        self.explosion_sound.set_volume(0.5)

    def make_invincible(self, duration):
        """Activate invincibility for a given duration (in seconds)."""
        self.invincible = True
        self.invincible_timer = duration

    @staticmethod
    def load_life_sprites():
        """Loads, resizes, and returns a dictionary of life sprites."""
        heart_size = (75, 25)  # Desired size (width, height) in pixels
        return {
            0: pygame.transform.scale(pygame.image.load("sprites/player/0.png").convert_alpha(), heart_size),
            1: pygame.transform.scale(pygame.image.load("sprites/player/1.png").convert_alpha(), heart_size),
            2: pygame.transform.scale(pygame.image.load("sprites/player/2.png").convert_alpha(), heart_size),
            3: pygame.transform.scale(pygame.image.load("sprites/player/3.png").convert_alpha(), heart_size),
        }

    @staticmethod
    def load_explosion_frames():
        """Loads explosion animation frames for the player."""
        frames = []
        for i in range(64):  # Assuming 64 explosion frames
            path = f"sprites/player/destroyed/tile{i:03}.png"
            try:
                frame = pygame.image.load(path).convert_alpha()
                frames.append(frame)
            except FileNotFoundError:
                continue
        return frames

    def explode(self):
        """Trigger the player's explosion."""
        self.exploding = True
        self.explosion_frame = 0
        self.explosion_position = self.position.copy()  # Freeze explosion position
        self.invincible = False  # Turn off invincibility during explosion

        # Play the explosion sound
        self.explosion_sound.play()

    def reset(self, x, y):
        """Reset the player after explosion."""
        self.position = pygame.Vector2(x, y)
        self.exploding = False
        self.invincible = False
        self.invincible_timer = 0

    def shoot(self):
        if self.laser_sound:
            self.laser_sound.play()  # Play the laser sound effect
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = direction * PLAYER_SHOOT_SPEED
        return Shot(self.position.x, self.position.y, velocity, self.rotation)

    def handle_input(self, event, shots_group):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not self.exploding and self.shoot_timer <= 0:  # Can't shoot while exploding
                shot = self.shoot()
                shots_group.add(shot)
                self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def draw(self, screen):
        """Draw the player's ship sprite or explosion."""
        if self.exploding:
            if self.explosion_frame < len(self.explosion_frames):
                frame = self.explosion_frames[self.explosion_frame]
                frame_rect = frame.get_rect(center=(self.explosion_position.x, self.explosion_position.y))
                screen.blit(frame, frame_rect)
            return  # Skip drawing the ship during explosion

        if self.invincible:
            # Flicker effect: Draw only in alternate frames
            if pygame.time.get_ticks() % 500 < 250:
                return  # Skip drawing for flickering effect

        # Rotate the sprite based on the player's rotation
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.rotation + 180)  # Adjust by 180 degrees
        sprite_rect = rotated_sprite.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_sprite, sprite_rect)

    def rotate(self, dt, direction):
        self.rotation += direction * PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def update(self, dt):
        if self.exploding:
            # Handle explosion animation
            self.explosion_time_since_last_frame += dt
            if self.explosion_time_since_last_frame > 1 / self.explosion_speed:
                self.explosion_frame += 1
                self.explosion_time_since_last_frame = 0
                if self.explosion_frame >= len(self.explosion_frames):
                    # After explosion finishes, reset player and apply invincibility
                    self.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    self.make_invincible(3)  # Apply invincibility after explosion
            return

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False  # Turn off invincibility after the timer ends

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
    bullet_image = None  # Class variable to hold the bullet sprite

    def __init__(self, x, y, velocity, rotation, bullet_width=50, bullet_height=100):
        """
        Initializes the Shot class.

        :param x: X-coordinate of the bullet.
        :param y: Y-coordinate of the bullet.
        :param velocity: Velocity of the bullet.
        :param rotation: Rotation angle of the bullet (in degrees).
        :param bullet_width: Desired width of the bullet sprite.
        :param bullet_height: Desired height of the bullet sprite.
        """
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = velocity
        self.rotation = rotation  # Store rotation angle

        # Load and scale the bullet sprite
        if Shot.bullet_image is None:
            Shot.bullet_image = pygame.image.load("sprites/player/bullet.png").convert_alpha()
            Shot.bullet_image = pygame.transform.scale(Shot.bullet_image, (bullet_width, bullet_height))

        # Rotate the bullet sprite to match the rotation angle
        self.bullet_sprite = pygame.transform.rotate(Shot.bullet_image, -self.rotation)

    def draw(self, screen):
        """Draws the rotated bullet sprite."""
        if self.bullet_sprite:
            bullet_rect = self.bullet_sprite.get_rect(center=(self.position.x, self.position.y))
            screen.blit(self.bullet_sprite, bullet_rect)
        else:
            # Fallback to a circle if the sprite fails to load
            pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius)

    def update(self, dt):
        """Updates the bullet's position."""
        self.position += self.velocity * dt
