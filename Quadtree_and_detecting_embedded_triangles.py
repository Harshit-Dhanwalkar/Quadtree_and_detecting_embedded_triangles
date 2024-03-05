import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Triangle:
    def __init__(self, vertices):
        self.vertices = np.array(vertices)

    def contains(self, point):
        v0 = self.vertices[:2]
        v1 = self.vertices[2:4]
        v2 = self.vertices[4:]

        v0v1 = v1 - v0
        v0v2 = v2 - v0
        vp = np.array(point) - v0

        dot00 = np.dot(v0v1, v0v1)
        dot01 = np.dot(v0v1, v0v2)
        dot02 = np.dot(v0v1, vp)
        dot11 = np.dot(v0v2, v0v2)
        dot12 = np.dot(v0v2, vp)

        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        return (u >= 0) and (v >= 0) and (u + v < 1)

def generate_random_triangles_and_points(num_triangles, num_points):
    triangles = [Triangle([random.random() for _ in range(6)]) for _ in range(num_triangles)]
    points = np.random.rand(num_points, 2)
    return triangles, points

def main():
    num_triangles = 10
    num_points = 100
    triangles, points = generate_random_triangles_and_points(num_triangles, num_points)

    fig, ax = plt.subplots()
    ax.set_facecolor('black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for triangle in triangles:
        color = 'yellow' if any(triangle.contains(p) for p in points) else 'red'
        ax.add_patch(patches.Polygon(triangle.vertices.reshape(3, 2), closed=True, fill=False, color=color))

    ax.scatter(points[:, 0], points[:, 1], color='gray')
    plt.show()

if __name__ == "__main__":
    main()
