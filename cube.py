import requests
import time
import threading
import pygame
import numpy as np

# Replace with the URL you want to scrape
url = 'http://192.168.130.145/'  # Change this to the actual URL

# Global variable to store sensor values
sensor_values = [0, 0, 0, 0]

def get_html_content():
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text  # Return the entire HTML content
    except Exception as e:
        print(f"Error fetching HTML content: {e}")
        return None

def update_sensor_values():
    global sensor_values
    while True:
        html_content = get_html_content()
        if html_content is not None:
            try:
                # Assuming the HTML content is a comma-separated string of integers
                sensor_values = list(map(int, html_content.split(',')))
                print(f"Updated sensor values: {sensor_values}")  # Log the sensor values
            except ValueError:
                print("Error parsing sensor values.")
        else:
            print("Failed to retrieve HTML content.")
        
        # time.sleep(5)   Wait for 5 seconds before the next request

def draw_cube(screen, angle_x, angle_y):
    # Define the cube vertices
    vertices = np.array([
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ])

    # Define the edges that connect the vertices
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    # Define the faces of the cube
    faces = [
        (0, 1, 2, 3),  # Back face
        (4, 5, 6, 7),  # Front face
        (0, 1, 5, 4),  # Bottom face
        (2, 3, 7, 6),  # Top face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5)   # Right face
    ]

    # Define a list of colors for each face
    face_colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 165, 0),  # Orange
        (128, 0, 128)   # Purple
    ]

    # Rotation matrices
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    # Apply rotations
    rotated_vertices = vertices @ rotation_x.T @ rotation_y.T

    # Scale and translate the cube
    scale = 100
    offset = np.array([400, 300])  # Center of the screen (2D offset)
    projected_vertices = (rotated_vertices[:, :2] * scale) + offset  # Only take x and y

    # Draw the faces with assigned colors
    for i, face in enumerate(faces):
        pygame.draw.polygon(screen, face_colors[i], projected_vertices[list(face)], 0)  # Draw filled polygon

    # Draw the edges
    for edge in edges:
        pygame.draw.line(screen, (255, 255, 255), projected_vertices[edge[0]], projected_vertices[edge[1]], 2)

def map_sensor_value_to_speed(sensor_value):
    # Map the sensor value to a rotation speed
    # A value of 0 corresponds to a maximum negative rotation speed
    # A value of 2048 corresponds to zero rotation speed
    # A value of 4095 corresponds to a maximum positive rotation speed
    max_speed = 0.1  # Adjust this value to control the maximum rotation speed
    if(sensor_value >1800 and sensor_value<2200):
        speed = 0
    else:
        speed = (sensor_value - 2048) / 2048 * max_speed
    return speed

def main():
    # Start the sensor value update thread
    threading.Thread(target=update_sensor_values, daemon=True).start()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rotating Cube")

    # Initialize the font module
    pygame.font.init()

    # Create a font object
    font = pygame.font.SysFont('Arial', 24)

    clock = pygame.time.Clock()

    angle_x, angle_y = 0, 0  # Initial rotation angles

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Get the rotation speed from the sensor values
        try:
            speed_x = map_sensor_value_to_speed(sensor_values[0])
            speed_y = map_sensor_value_to_speed(sensor_values[1])
        except IndexError:
            print("Sensor values not available yet.")
            speed_x, speed_y = 0, 0  # Default to no rotation if values are not available

        # Update the rotation angles based on the calculated speed
        angle_x += speed_x
        angle_y += speed_y

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the rotating cube
        draw_cube(screen, angle_x, angle_y)

        # Render the sensor data as text
        sensor_text = font.render(f"Sensor Values: {sensor_values}", True, (255, 255, 255))
        screen.blit(sensor_text, (10, 10))  # Draw the text at the top-left corner

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main()