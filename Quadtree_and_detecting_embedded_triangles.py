import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x < self.x + self.w and
                point.y >= self.y - self.h and
                point.y < self.y + self.h)

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
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        ne = Rectangle(x + w, y - h, w, h)
        self.northeast = Quadtree(ne, self.capacity)
        nw = Rectangle(x - w, y - h, w, h)
        self.northwest = Quadtree(nw, self.capacity)
        se = Rectangle(x + w, y + h, w, h)
        self.southeast = Quadtree(se, self.capacity)
        sw = Rectangle(x - w, y + h, w, h)
        self.southwest = Quadtree(sw, self.capacity)

        self.divided = True

class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices

    def get_vertices(self):
        # Extract and return the x, y coordinates from the vertices list
        return [(self.vertices[i], self.vertices[i + 1]) for i in range(0, len(self.vertices), 2)]

    def contains(self, point):
        # Implement the point-in-triangle check here
        pass


def generate_random_triangles_and_points(num_triangles, num_points):
    triangles = [Triangle([random.random() for _ in range(6)]) for _ in range(num_triangles)]
    points = [[random.random(), random.random()] for _ in range(num_points)]
    return triangles, points

def main():
    num_triangles = 10
    num_points = 100
    triangles, points = generate_random_triangles_and_points(num_triangles, num_points)
    fig, ax = plt.subplots()
    ax.set_facecolor('black')  # Set background color to black
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    for triangle in triangles:
        ax.add_patch(patches.Polygon(triangle.get_vertices(), closed=True, fill=False, color='yellow'))  # Set triangle color to yellow
    ax.scatter(*zip(*points), color='gray')  # Set points color to gray
    plt.show()  # Display the plot

if __name__ == "__main__":
    main()
