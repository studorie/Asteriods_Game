import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Load the background image
    background = pygame.image.load("sprites/maps/1.png").convert()
    # If scaling is required to fit the screen resolution
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load life sprites through Player class
    life_sprites = Player.load_life_sprites()  # Use the function from player.py
    lives = 3  # Initialize lives

    # Initialize sprite groups
    shots = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable,)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    updatable.add(player)
    drawable.add(player)

    asteroid_field = AsteroidField()
    updatable.add(asteroid_field)

    score = 0  # Initialize score

    # Initialize font
    pygame.font.init()
    pygame.mixer.init()
    font = pygame.font.Font(None, 36)  # Default font, size 36

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event, shots)

        # Update all sprites
        for sprite in updatable:
            sprite.update(dt)

        # Check player-asteroid collisions
        for asteroid in asteroids:
            if asteroid.exploding:
                continue  # Skip exploding asteroids
            if not player.exploding and not player.invincible and player.collision(asteroid):
                player.explode()
                lives -= 1
                if lives > 0:
                    # Let the explosion animation finish before respawning
                    print(f"Lives remaining: {lives}")
                else:
                    print("Game Over!")
                    running = False
                break  # Stop checking further collisions for this frame


        # Handle shots hitting asteroids
        for shot in shots:
            for asteroid in asteroids:
                if not asteroid.exploding and shot.collision(asteroid):  # Ignore exploding asteroids
                    score += 5  # Increment score only for active asteroids
                    shot.kill()
                    asteroid.split()
                    break

        # Draw the background image
        screen.blit(background, (0, 0))  # Draw background before other elements

        # Draw all drawable sprites
        for sprite in drawable:
            sprite.draw(screen)

        # Render and display the score
        score_text = font.render(f"Score: {score}", True, "white")
        screen.blit(score_text, (10, 10))  # Position score at (10, 10)

        # Display the life sprite based on the current number of lives
        if lives >= 0:
            screen.blit(life_sprites[lives], (10, 50))  # Position below the score

        # Update the display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
