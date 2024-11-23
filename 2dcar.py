
import math
import sys

import neat
import pygame
import time

resolution = [1920, 1080] # Resolution of the size
carDimensions= 15    
boundary = (255, 255, 255, 255) #rgb white
iteration = 0 

choice = "austin"

if choice == "silverstone":
    start_area_x = 1165
    start_area_y = 900
    angle = 135
    obsticleCord = 1278, 253
    obstacleSpeedX = 1
    obstacleSpeedY = 0.74

    obsticle2Cord =330, 620
    obstacle2SpeedX = 1
    obstacle2SpeedY = 1


    circuit = "silverstone.png"
elif choice == "austin":
    start_area_x = 120
    start_area_y = 650
    angle = -15
    obsticleCord = 825, 233
    obstacleSpeedX = 7
    obstacleSpeedY = -1

    obsticle2Cord =300, 795
    obstacle2SpeedX = 1
    obstacle2SpeedY = -0.76


    circuit = "austin.png"
area_width = 30
area_height = 30

def is_within_start_area(car_x, car_y):
    return (start_area_x <= car_x <= start_area_x + area_width) and \
        (start_area_y <= car_y <= start_area_y + area_height)

class Car:
    def __init__(self):
        # Importing car image
        self.sprite = pygame.image.load('f1car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (carDimensions, carDimensions))
        self.rotatesprite = self.sprite 

        # Adjusting starting position, angle, speed and position
        self.position = [start_area_x, start_area_y] 
        self.angle = angle
        self.speed = 3
        self.center = [self.position[0] + carDimensions / 2, self.position[1] + carDimensions / 2] 

        # Sensor list and alive check
        self.sensors = []
        self.alive = True
        
        # Distance and time elapsed
        self.distance = 0 
        self.time = 0 

        self.start_time_recorded = False
        self.lap = 0
        self.lap_times = []
        self.lap_start_time = time.time()  # Start the timer
        self.min_lap_interval = 1.0  # Minimum time interval in seconds between laps


    def drawCar(self, screen):
        # Draws car
        screen.blit(self.rotatesprite, self.position) 
        # Draws car sensors
        for sensor in self.sensors:
            position = sensor[0]
            pygame.draw.circle(screen, (200, 10, 255), position, 2)
            pygame.draw.line(screen, (200, 10, 255), self.center, position, 1)

    def collisionCheck(self, map):
        self.alive = True
        for point in self.corners:
            if map.get_at((int(point[0]), int(point[1]))) == boundary:
                self.alive = False
                break

    def sensorCheck(self, degree, map, obstacle, obstacle2):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        DetectionPoint = None
        while not map.get_at((x, y)) == boundary:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
           
            # Check if sensor hits the obstacle
            if obstacle.collidepoint(x, y):
                # If it does, set the hit point and break
                DetectionPoint = (x, y)
                break
            if obstacle2.collidepoint(x, y):
                # If it does, set the hit point and break
                DetectionPoint = (x, y)
                break

        if DetectionPoint is None:
            DetectionPoint = (x, y)


        # Calculating the distance between car and the hit point
        dist = int(math.sqrt(math.pow(DetectionPoint[0] - self.center[0], 2) + math.pow(DetectionPoint[1] - self.center[1], 2)))
        # Adding it to the sensor list
        self.sensors.append([DetectionPoint, dist])
    


    def update(self, map,obstacle, obstacle2):
        # Rotates car
        self.rotatesprite = self.rotateCenter(self.sprite, self.angle)
        # Adjusts the x and y coordinates of the car's position.
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        # Increase time and speed
        self.distance += self.speed
        self.time += 1

        # New Center
        self.center = [int(self.position[0]) + carDimensions / 2, int(self.position[1]) + carDimensions / 2]


        # Define angle offsets for each corner relative to the car's current angle
        angle_offsets = [30, 150, 210, 330]

        # Initialize an empty list to store corner positions
        self.corners = []

        # Loop through each angle offset and calculate the corner positions
        for offset in angle_offsets:
            x = self.center[0] + math.cos(math.radians(360 - (self.angle + offset))) * (0.1 * carDimensions)
            y = self.center[1] + math.sin(math.radians(360 - (self.angle + offset))) * (0.1 * carDimensions)
            self.corners.append([x, y])


        # Check collision
        self.collisionCheck(map)
        # Check collisions with the moving obstacles
        self.checkObstacleCollision(obstacle, obstacle2)

        self.sensors.clear()

        # Define all angles for sensor checks
        angles = [-90, -45, 0, 45, 90, -15, 15, -7, 7]

        # Check sensor for each angle
        for angle in angles:
            self.sensorCheck(angle, map, obstacle, obstacle2)

        current_time = time.time()
        if is_within_start_area(self.position[0], self.position[1]):
            if (current_time - self.lap_start_time) > self.min_lap_interval:
                lap_time = current_time - self.lap_start_time  # Calculate the elapsed time
                self.lap_times.append(lap_time)  # Save the lap time
                print(f"Lap {self.lap + 1}: {lap_time:.2f} seconds")  # Print the lap time
                self.lap_start_time = current_time  # Reset the timer for the next lap
                self.lap += 1
            #self.start_time_recorded = True

    def checkObstacleCollision(self, obstacle,obstacle2):
        # Convert corners to Pygame Rect for collision detection
        car_rect = pygame.Rect(self.position[0], self.position[1], carDimensions, carDimensions)
        # Check if the car collides with the obstacle
        if car_rect.colliderect(obstacle):
            self.alive = False
        if car_rect.colliderect(obstacle2):
            self.alive = False


    def getData(self):
        # Get Distances
        sensors = self.sensors
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i, sensor in enumerate(sensors):
            values[i] = int(sensor[1] / 30)

        return values

    def isAlive(self):
        return self.alive

    def getReward(self):
        return self.distance / (carDimensions / 2)

    def rotateCenter(self, image, angle):
        # Obtain the original image rectangle and rotate the image
        original = image.get_rect()
        rotatedImage = pygame.transform.rotate(image, angle)
        # Adjust the rectangle to match the new image's center
        rotatedRect = original.copy()
        rotatedRect.center = rotatedImage.get_rect().center
        # Crop the image to the adjusted rectangle
        rotatedImage = rotatedImage.subsurface(rotatedRect).copy()
        return rotatedImage

def runSimulation(genomes, config):
    
    nets = []
    cars = []

    pygame.init()
    screen = pygame.display.set_mode((resolution[0], resolution[1]))

    for i, g in genomes:
        net = neat.nn.RecurrentNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    map = pygame.image.load(circuit).convert()

    global iteration
    iteration += 1

    counter = 0
    obstacle = pygame.Rect(obsticleCord[0], obsticleCord[1], 10, 10)
    obstacle2 = pygame.Rect(obsticle2Cord[0], obsticle2Cord[1], 10, 10)
    obstacle_speed = 1
    obstacle_speed2 = 2
    
    while True:
        # Iterate over each car and corresponding neural network
        for index, car in enumerate(cars):
            # Get the neural network outputs for the current car's sensor data
            outputs = nets[index].activate(car.getData())
            # Determine the action with the highest output value
            action = outputs.index(max(outputs))

            # Decide the car's movement based on the neural network's decision
            if action == 0:  # Option 0: Turn Right
                car.angle += 10
            elif action == 1:  # Option 1: Turn Left
                car.angle -= 10
            elif action == 2:  # Option 2: Slow Down, with a minimum speed limit
                if car.speed > 12:
                    car.speed -= 2
            else:  # Any other output: Speed Up
                car.speed += 2

        # Track the number of cars still active (alive)
        activeCars = 0
        for index, car in enumerate(cars):
            # Update each car's state and check if it's still active
            if car.isAlive():
                activeCars += 1
                car.update(map, obstacle, obstacle2)
                # Increment the car's fitness based on its performance
                genomes[index][1].fitness += car.getReward()

        # If no cars are active, end the simulation
        if activeCars == 0:
            break
        counter += 1
        # Stop After 1 minute
        if counter == 60 * 60: 
            break

        # Clear screen
        screen.fill((0, 0, 0))  # Fill the screen with black or background color

        # Blit the map onto the screen
        screen.blit(map, (0, 0))

        # Update obstacle's position
        obstacle.x += obstacle_speed * obstacleSpeedX
        obstacle.y += obstacle_speed * obstacleSpeedY
        obstacle2.x += obstacle_speed2 * obstacle2SpeedX
        obstacle2.y -= obstacle_speed2 * obstacle2SpeedY

        if choice == "silverstone":
            print(obstacle2.right)
            if obstacle.right > resolution[0] - 400 or obstacle.left < 1278:
                obstacle_speed = -obstacle_speed
            if obstacle2.right < 329:
                obstacle_speed2 = 2
            if obstacle2.right > 475:
                obstacle_speed2 = -2
        else:
            if obstacle.right > resolution[0] - 700 or obstacle.left < 825:
                obstacle_speed = -obstacle_speed
            if obstacle2.right < 300:
                obstacle_speed2 = 2
            if obstacle2.right > 455:
                obstacle_speed2 = -2

        # Draw the moving obstacle on the screen after the map has been blitted
        pygame.draw.rect(screen, (255, 255, 255, 255), obstacle)
        pygame.draw.rect(screen, (255, 255, 255, 255), obstacle2)
        
        
        # Update and draw each car if it is still "alive"
        for car in cars:
            if car.isAlive():
                car.update(map, obstacle, obstacle2)  # Update car state with obstacles
                car.drawCar(screen)  # Draw the car on the screen

        # Create a new clock instance for timing
        clock = pygame.time.Clock()

        # Render and display iteration information
        topText = pygame.font.SysFont("Calibri", 50).render(f"Iteration: {iteration}", True, (0, 0, 0))
        topTextRect = topText.get_rect(center=(1700, 75))
        screen.blit(topText, topTextRect)

        # Render and display the count of active cars
        bottomText = pygame.font.SysFont("Calibri", 40).render(f"Alive: {activeCars}", True, (0, 250, 0))
        bottomTextRect = bottomText.get_rect(center=(1700, 125))
        screen.blit(bottomText, bottomTextRect)

        # Update the display and maintain a 60 FPS frame rate
        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 frames per second


# Path to the NEAT configuration file
config_path = "./config.txt"

# Load the configuration
config = neat.Config(neat.DefaultGenome,
                     neat.DefaultReproduction,
                     neat.DefaultSpeciesSet,
                     neat.DefaultStagnation,
                     config_path)

# Create a NEAT population based on the loaded configuration
population = neat.Population(config)

# Add a standard output reporter to display progress in the terminal
population.add_reporter(neat.StdOutReporter(True))

# Create a statistics reporter to gather and report statistics of the population
stats_reporter = neat.StatisticsReporter()
population.add_reporter(stats_reporter)

# Run the simulation for a specified number of generations
generation_count = 1000
population.run(runSimulation, generation_count)
