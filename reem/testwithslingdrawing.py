import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Angry Birds Projectile Motion")

# Load images
redbird = pygame.image.load("red-bird3.png").convert_alpha()
background = pygame.image.load("background.png").convert_alpha()
bird_rect = redbird.get_rect()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Constants
g = 9.8
k = 0.1
m = 1.0  # Mass of the projectile (kg)
dt = 0.1  # Time step (s)
scale = 1

# Initial conditions
bird_pos = np.array([100, 400], dtype=float)  # Start position of the bird
launching = False  # Flag to check if bird is being launched
trajectory = []  # List to store the trajectory points

# Function to calculate derivatives
def derivatives(vx, vy):
    dvx_dt = -k / m * vx
    dvy_dt = -g - k / m * vy
    return dvx_dt, dvy_dt

# RK4 method implementation
def rk4_step(func, t, y, dt):
    k1 = np.array(func(*y))
    k2 = np.array(func(*(y + dt / 2 * k1)))
    k3 = np.array(func(*(y + dt / 2 * k2)))
    k4 = np.array(func(*(y + dt * k3)))
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

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
                state = [v0x, v0y]

    if launching:
        state = rk4_step(derivatives, 0, state, dt)
        bird_pos[0] += state[0] * dt
        bird_pos[1] -= state[1] * dt  # Subtract because the screen's y-coordinates increase downward
        trajectory.append((bird_pos[0], bird_pos[1]))

        if bird_pos[1] > height:  # Reset if bird hits the ground
            launching = False
            bird_pos = np.array([100, height - 100], dtype=float)

    # Draw a static vertical line at x = 100, from ground to 50 pixels up
    pygame.draw.line(screen, white, (100, 600), (100, 400), 2)
    
    # Draw a cup shape
    cup_x = 90  # Adjust as needed
    cup_y = 400 # Adjust as needed
    cup_width = 20  # Adjust as needed
    cup_height = 30  # Adjust as needed
    pygame.draw.rect(screen, white, (cup_x, cup_y, cup_width, cup_height))
    pygame.draw.line(screen, white, (cup_x, cup_y), (cup_x + cup_width, cup_y + cup_height), 2)
    pygame.draw.line(screen, white, (cup_x + cup_width, cup_y), (cup_x, cup_y + cup_height), 2)



    # Draw the bird
    bird_rect.center = (int(bird_pos[0]), int(bird_pos[1]))
    screen.blit(redbird, bird_rect)

    # Draw the bird
    bird_rect.center = (int(bird_pos[0]), int(bird_pos[1]))
    screen.blit(redbird, bird_rect)

    # Draw the trajectory
    for point in trajectory:
        pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 3)

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
