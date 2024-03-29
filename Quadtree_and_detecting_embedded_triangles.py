import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (
            point.x >= self.x - self.w and
            point.x < self.x + self.w and
            point.y >= self.y - self.h and
            point.y < self.y + self.h
        )

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

        return (
            self.northeast.insert(point) or
            self.northwest.insert(point) or
            self.southeast.insert(point) or
            self.southwest.insert(point)
        )

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

    def is_inside_quadtree(self, quadtree):
        rect = Rectangle(self.vertices[0][0], self.vertices[0][1], self.vertices[2][0] - self.vertices[0][0], self.vertices[2][1] - self.vertices[0][1])
        return self._is_inside_quadtree_recursive(quadtree, rect)

    def _is_inside_quadtree_recursive(self, quadtree, rect):
        if not quadtree.boundary.contains(Point(rect.x, rect.y)) and not quadtree.boundary.contains(Point(rect.x + rect.w, rect.y + rect.h)):
            return False

        for point in quadtree.points:
            if rect.contains(point):
                return True

        if quadtree.divided:
            return (
                self._is_inside_quadtree_recursive(quadtree.northeast, rect) or
                self._is_inside_quadtree_recursive(quadtree.northwest, rect) or
                self._is_inside_quadtree_recursive(quadtree.southeast, rect) or
                self._is_inside_quadtree_recursive(quadtree.southwest, rect)
            )

        return False

def generate_random_triangles_and_points(num_triangles, num_points):
    points = [Point(random.random(), random.random()) for _ in range(num_points)]
    triangles = []

    for _ in range(num_triangles):
        # Randomly select three points to form a triangle
        triangle_points = random.sample(points, 3)
        # Extract the coordinates of the selected points to form the triangle
        triangle_vertices = [(p.x, p.y) for p in triangle_points]

        triangles.append(Triangle(triangle_vertices))

    return triangles, points

def on_key(event):
    if event.key == 'q':
        plt.close()

def main():
    num_triangles = 10
    num_points = 100
    triangles, points = generate_random_triangles_and_points(num_triangles, num_points)

    # Create Quadtree
    quadtree_boundary = Rectangle(0, 0, 1, 1)
    quadtree = Quadtree(quadtree_boundary, 4)

    for point in points:
        quadtree.insert(point)

    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for triangle in triangles:
        color = 'yellow' if any(triangle.is_inside_quadtree(quadtree) for p in points) else 'red'
        ax.add_patch(patches.Polygon(triangle.vertices, closed=True, fill=False, color=color))

    ax.scatter([p.x for p in points], [p.y for p in points], color='gray')

    plt.connect('key_press_event', on_key)  # Connect the key event callback

    plt.show()

if __name__ == "__main__":
    main()