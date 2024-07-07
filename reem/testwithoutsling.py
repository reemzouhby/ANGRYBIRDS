import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Angry Birds ")

# Load images
redbird = pygame.image.load("red-bird3.png").convert_alpha()
background = pygame.image.load("background.png").convert_alpha()
bird_rect = redbird.get_rect()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Constants
g = 9.8  # Acceleration due to gravity (m/s^2)
k = 0.1  # Drag coefficient (kg/s)
m = 1.0  # Mass of the projectile (kg)
dt = 0.1  # Time step (s)
scale = 1  # Scale to make the simulation visible on screen

# Initial conditions
bird_pos = np.array([100, 100], dtype=float)  # Start position of the bird
launching = False  # Flag to check if bird is being launched
trajectory = []  # List to store the trajectory points

# Function to calculate derivatives
def derivatives(vx, vy):
    dvx_dt = -k / m * vx
    dvy_dt = -g - k / m * vy
    return dvx_dt, dvy_dt

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))  # Draw the background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not launching:
                start_pos = pygame.mouse.get_pos()
                bird_pos = np.array(start_pos, dtype=float)
                trajectory = []

        elif event.type == pygame.MOUSEMOTION:
            if not launching and pygame.mouse.get_pressed()[0]:
                end_pos = pygame.mouse.get_pos()
                pygame.draw.line(screen, green, start_pos, end_pos, 2)
                bird_pos = np.array(end_pos, dtype=float)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if not launching:
                end_pos = pygame.mouse.get_pos()
                dx = start_pos[0] - end_pos[0]
                dy = start_pos[1] - end_pos[1]
                v0 = np.sqrt(dx**2 + dy**2) * scale  # Adjust the scaling factor as needed
                theta = np.arctan2(dy, dx)
                v0x = v0 * np.cos(theta)
                v0y = -v0 * np.sin(theta)
                launching = True

    if launching:
        dvx_dt, dvy_dt = derivatives(v0x, v0y)
        v0x += dvx_dt * dt
        v0y += dvy_dt * dt
        bird_pos[0] += v0x * dt * scale
        bird_pos[1] -= v0y * dt * scale  # Subtract because the screen's y-coordinates increase downward
        trajectory.append((bird_pos[0], bird_pos[1]))

        if bird_pos[1] > height:  # Reset if bird hits the ground
            launching = False
            bird_pos = np.array([100,  100], dtype=float)
    line_top_y = 100  # Line height is 50 pixels from the ground
    pygame.draw.line(screen, white, (100, 100), (100, 100), 2)
    # Draw the bird
    bird_rect.center = (int(bird_pos[0]), int(bird_pos[1]))
    screen.blit(redbird, bird_rect)

    # Draw the trajectory
    for point in trajectory:
        pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 3)

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit() 


