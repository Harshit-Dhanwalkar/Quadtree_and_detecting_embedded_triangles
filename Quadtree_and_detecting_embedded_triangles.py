import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        if not self.divided:
            self.subdivide()
        return (self.northeast.insert(point) or
                self.northwest.insert(point) or
                self.southeast.insert(point) or
                self.southwest.insert(point))

    def subdivide(self):
        # Implement the subdivision logic here
        pass

class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

    def contains(self, point):
        # Implement the point-in-triangle check here
        pass

def generate_random_triangles_and_points(num_triangles, num_points):
    triangles = [Triangle([random.random() for _ in range(6)]) for _ in range(num_triangles)]
    points = [[random.random(), random.random()] for _ in range(num_points)]
    return triangles, points