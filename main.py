import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

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

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_input(event, shots)

        for sprite in updatable:
            sprite.update(dt)

        for asteroid in asteroids:
            if player.collision(asteroid):
                print("Game over!")
                running = False
                break

        for shot in shots:
            for asteroid in asteroids:
                if shot.collision(asteroid):
                    shot.kill()
                    asteroid.split()
                    break
        screen.fill("black")

        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
