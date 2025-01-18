import pygame
import random
import math

width, height = 800, 600

num_of_boids = 100
max_speed = 4
max_force = 0.1
neighbour_radius = 50
separation_radius = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Boids Flocking Simulation')


class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = max_speed
        self.max_force = max_force

    def edges(self):

        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width
        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def velocity_matching(self, boids):
        # Velocity matching: steer towards the average velocity of nearby boids.
        avg_velocity = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < neighbour_radius:
                avg_velocity += boid.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * self.max_speed
            steering = avg_velocity - self.velocity
            return self.limit(steering, self.max_force)
        return pygame.Vector2(0, 0)

    def flock_centering(self, boids):
        # Flock centering: steer towards the average position of nearby boids.
        avg_position = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < neighbour_radius:
                avg_position += boid.position
                total += 1
        if total > 0:
            avg_position /= total
            desired = avg_position - self.position
            desired = desired.normalize() * self.max_speed
            steering = desired - self.velocity
            return self.limit(steering, self.max_force)
        return pygame.Vector2(0, 0)

    def collision_avoidance(self, boids):
        # Collision avoidance: steer to avoid crowding local flockmates.
        desired_separation = 25
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < desired_separation:
                diff = self.position - boid.position
                diff /= distance  # Weight by distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            # Only normalize and limit if steer vector has non-zero length
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed
                steering = steer - self.velocity
                return self.limit(steering, self.max_force)
        return pygame.Vector2(0, 0)

    def group_separation(self, boids):
        steer = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < separation_radius:
                diff = self.position - boid.position
                diff /= distance
                steer += diff
                total += 1
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed
                steering = steer - self.velocity
                return self.limit(steering, self.max_force)
        return pygame.Vector2(0, 0)

    def limit(self, vector, max_value):
        # Limit the magnitude of a vector.
        if vector.length() > max_value:
            vector.scale_to_length(max_value)
        return vector

    def update(self, boids):
        # Update boid position and velocity based on rules
        # Combining the three rules
        align_force = self.velocity_matching(boids)
        cohesion_force = self.flock_centering(boids)
        separation_force = self.collision_avoidance(boids)
        group_separation_force = self.group_separation(boids)

        self.acceleration = align_force + cohesion_force + separation_force + group_separation_force

        self.velocity += self.acceleration
        self.velocity = self.limit(self.velocity, self.max_speed)
        self.position += self.velocity
        self.edges()

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        size = 5  # Size of the boid

        # Calculate the vertices of the triangle based on the angle of motion
        front = self.position + pygame.Vector2(size, 0).rotate(angle * 180 / math.pi)
        left = self.position + pygame.Vector2(-size / 2, -size / 2).rotate(angle * 180 / math.pi)
        right = self.position + pygame.Vector2(-size / 2, size / 2).rotate(angle * 180 / math.pi)

        pygame.draw.polygon(screen, WHITE, [front, left, right])

def main():
    boids = [Boid(random.uniform(0, width), random.uniform(0, height)) for _ in range(num_of_boids)]

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for boid in boids:
            boid.update(boids)
            boid.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
