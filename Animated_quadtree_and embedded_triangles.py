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
        triangle_points = random.sample(points, 3)
        triangle_vertices = [(p.x, p.y) for p in triangle_points]
        triangles.append(Triangle(triangle_vertices))

    return triangles, points

animated_points = []

class AnimatedPoint:
    def __init__(self, x, y):
        self.point = Point(x, y)
        self.scatter = None

    def update_coordinates(self):
        self.point.x = random.random()
        self.point.y = random.random()

def update(frame, animated_points, quadtree, ax, scatter):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for animated_point in animated_points:
        animated_point.update_coordinates()
        animated_point.scatter.set_offsets((animated_point.point.x, animated_point.point.y))

    scatter = ax.scatter([p.point.x for p in animated_points], [p.point.y for p in animated_points], color='gray')

    for triangle in triangles:
        color = 'yellow' if triangle.is_inside_quadtree(quadtree) else 'red'
        triangle_patch = patches.Polygon(triangle.vertices, closed=True, fill=False, color=color)
        ax.add_patch(triangle_patch)

def main():
    global animated_points, triangles, quadtree

    num_triangles = 10
    num_points = 100
    triangles, points = generate_random_triangles_and_points(num_triangles, num_points)

    quadtree_boundary = Rectangle(0, 0, 1, 1)
    quadtree = Quadtree(quadtree_boundary, 4)

    for point in points:
        quadtree.insert(point)

    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    animated_points = [AnimatedPoint(random.random(), random.random()) for _ in range(num_points)]
    scatter = ax.scatter([p.point.x for p in animated_points], [p.point.y for p in animated_points], color='gray')

    for animated_point in animated_points:
        animated_point.scatter = scatter

    ani = animation.FuncAnimation(fig, update, frames=100, interval=100, fargs=(animated_points, quadtree, ax, scatter), repeat=True)

    plt.show()

if __name__ == "__main__":
    main()
