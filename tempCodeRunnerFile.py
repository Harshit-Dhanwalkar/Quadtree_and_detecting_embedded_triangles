def update(frame, animated_points, quadtree, ax, scatter, triangle_patches):
    ax.clear()
    ax.set_facecolor('black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    for animated_point in animated_points:
        animated_point.update_coordinates()
        animated_point.scatter.set_offsets((animated_point.point.x, animated_point.point.y))

    scatter = ax.scatter([p.point.x for p in animated_points], [p.point.y for p in animated_points], color='gray')

    for triangle_patch in triangle_patches:
        triangle_patch.remove()  # Remove previous triangle patches

    new_triangle_patches = []  # Create a new list for updated triangle patches

    for triangle in triangles:
        color = 'yellow' if triangle.is_inside_quadtree(quadtree) else 'red'
        triangle_patch = patches.Polygon(triangle.vertices, closed=True, fill=False, color=color)
        ax.add_patch(triangle_patch)
        new_triangle_patches.append(triangle_patch)

    return new_triangle_patches