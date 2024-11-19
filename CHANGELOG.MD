# Changelog: Asteroids Game Updates

## Player
### Explosion Effect
- Added an explosion animation for the player using `destroyed` sprites.
- Explosion location remains static during the animation for accuracy.
- The player resets to the center of the screen after the explosion.
- Added invincibility for 3 seconds post-explosion to prevent immediate collisions.

### Sound Effects
- Integrated an explosion sound (`p-explosion.mp3`) for when the player is destroyed.
- Added a laser shooting sound (`laser.mp3`) when the player fires a bullet.

### Shooting Mechanics
- Implemented bullet sprites (`bullet.png`) that rotate according to the player's orientation.
- Fixed a rotation bug to ensure bullets align correctly with the ship's direction.

### Ship Enhancements
- Increased the ship's size for improved visibility and gameplay experience.
- Improved rendering logic to prevent the ship from rendering during the explosion animation.
- Added a flickering effect to indicate invincibility after an explosion.

### Lives System
- Designed a life system using heart sprites (`0.png`, `1.png`, `2.png`, `3.png`).
- The game ends when the player's lives reach zero.
- Lives decrease upon collision with asteroids.

---

## Asteroids
### Explosion Effect
- Added an explosion animation for asteroids using `destroyed` sprites.
- Large and medium asteroids play `medium-destroy.mp3` on destruction.
- Small asteroids play `small-destroy.mp3` on destruction.

### Splitting Mechanism
- Large and medium asteroids split into smaller ones upon destruction.
- Splitting logic includes randomized velocities and directions for more dynamic gameplay.

---

## Shots
### Bullet Mechanics
- Implemented smooth bullet movement and collision detection with asteroids.
- Bullets destroy asteroids upon collision, rewarding the player with points.

---

## Score System
### Score Display
- Added a score system displayed at the top-left of the screen.
- The score increments by 5 points for every asteroid destroyed.

---

## Health and Respawn
### Health Bar
- Lives are displayed as a row of heart icons.
- The health bar updates dynamically when lives are lost.

### Respawn Logic
- After an explosion, the player respawns at the center of the screen.
- Invincibility is applied for 3 seconds post-respawn to avoid immediate collisions.

---

## Background and Visuals
### Background Image
- Added a space-themed background (`1.png`), scaled to fit the screen resolution.

### UI Enhancements
- Improved alignment of the score and health bar for a clean, organized interface.

---

## General Fixes and Improvements
### Game Over Logic
- Implemented a "Game Over" condition to end the game loop when lives reach zero.

### Collision Fixes
- Shots now ignore exploding asteroids during their destruction animation.
- Explosion animations no longer interfere with gameplay mechanics.

### Optimized Update and Draw Calls
- Centralized update and draw calls for improved game performance.

### Sound Volume Control
- Balanced audio with volume adjustments:
  - Explosion sounds: `0.5`
  - Laser sound: `1.0`.

### Asteroid Randomization
- Randomized spawn positions and velocities for asteroids to enhance gameplay variability.

---

## Next Steps
- [ ] Implement and refine power-up mechanics.
- [ ] Add more visual and sound feedback for critical moments (e.g., low health).
- [ ] Continue performance optimizations and code refactoring.