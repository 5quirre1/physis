"""
Made by the gayest squirrel alive; Squirrel Gay Acorns

3/22/2025 uhh 1:44 PM
"""

import math
import pygame
import random

class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalized(self):
        length = self.length()
        if length == 0:
            return Vec2(0, 0)
        return Vec2(self.x / length, self.y / length)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def __str__(self):
        return f"Vec2({self.x}, {self.y})"


class PhysicsObject:
    def __init__(self, position, mass=1.0):
        self.position = position
        self.velocity = Vec2(0, 0)
        self.acceleration = Vec2(0, 0)
        self.force = Vec2(0, 0)
        self.mass = mass
        self.restitution = 0.8

    def apply_force(self, force):
        self.force = self.force + force

    def update(self, dt):
        self.acceleration = self.force * (1.0 / self.mass)
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.force = Vec2(0, 0)


class Circle(PhysicsObject):
    def __init__(self, position, radius, mass=None):
        self.radius = radius
        if mass is None:
            mass = math.pi * radius**2
        super().__init__(position, mass)
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            self.color, 
            (int(self.position.x), int(self.position.y)), 
            self.radius
        )


class PhysicsEngine:
    def __init__(self, width, height):
        self.objects = []
        self.gravity = Vec2(0, 9.8 * 30)
        self.width = width
        self.height = height
        self.collision_iterations = 1

    def add_object(self, obj):
        self.objects.append(obj)

    def check_circle_collision(self, c1, c2):
        delta = c2.position - c1.position
        distance = delta.length()
        min_distance = c1.radius + c2.radius
        
        if distance < min_distance:
            penetration = min_distance - distance
            
            if distance == 0:
                normal = Vec2(1, 0)
            else:
                normal = delta.normalized()
            

            rel_velocity = c2.velocity - c1.velocity
            
            vel_along_normal = rel_velocity.dot(normal)
            if vel_along_normal > 0:
                return
            

            restitution = min(c1.restitution, c2.restitution)
            
            j = -(1 + restitution) * vel_along_normal
            j /= (1 / c1.mass) + (1 / c2.mass)
            
            impulse = normal * j
            c1.velocity = c1.velocity - impulse * (1 / c1.mass)
            c2.velocity = c2.velocity + impulse * (1 / c2.mass)
            

            correction = normal * (penetration * 0.5)
            c1.position = c1.position - correction
            c2.position = c2.position + correction

    def handle_boundary_collision(self, obj):
        if isinstance(obj, Circle):
            if obj.position.x - obj.radius < 0:
                obj.position.x = obj.radius
                obj.velocity.x = -obj.velocity.x * obj.restitution
            
            if obj.position.x + obj.radius > self.width:
                obj.position.x = self.width - obj.radius
                obj.velocity.x = -obj.velocity.x * obj.restitution
            
            if obj.position.y - obj.radius < 0:
                obj.position.y = obj.radius
                obj.velocity.y = -obj.velocity.y * obj.restitution
                
            if obj.position.y + obj.radius > self.height:
                obj.position.y = self.height - obj.radius
                obj.velocity.y = -obj.velocity.y * obj.restitution

    def update(self, dt):
        for obj in self.objects:
            obj.apply_force(self.gravity * obj.mass)
            obj.update(dt)
            
            self.handle_boundary_collision(obj)
        

        for _ in range(self.collision_iterations):
            for i in range(len(self.objects)):
                for j in range(i + 1, len(self.objects)):
                    obj1 = self.objects[i]
                    obj2 = self.objects[j]
                    
                    if isinstance(obj1, Circle) and isinstance(obj2, Circle):
                        self.check_circle_collision(obj1, obj2)

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("help")
    clock = pygame.time.Clock()
    

    engine = PhysicsEngine(width, height)
    

    for _ in range(10):
        radius = random.randint(10, 30)
        x = random.randint(radius, width - radius)
        y = random.randint(radius, height - radius)
        circle = Circle(Vec2(x, y), radius)
        circle.velocity = Vec2(random.uniform(-100, 100), random.uniform(-100, 100))
        engine.add_object(circle)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                radius = random.randint(10, 30)
                circle = Circle(Vec2(pos[0], pos[1]), radius)
                engine.add_object(circle)
        
        dt = 1/60
        engine.update(dt)
        
        screen.fill((0, 0, 0))
        for obj in engine.objects:
            obj.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
