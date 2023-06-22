from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import pyplot as plt
import errors.errors as e
import numpy as np
from scipy.spatial import ConvexHull
from math import sqrt
import random


class List:
    def __init__(self, values: list = []):
        self.values = values

    def __str__(self):
        return f'List[{", ".join([str(value) for value in self.values])}]'

    def add(self, value):
        self.values.append(value)

    def remove(self, index=None):
        if index is None:
            self.values.pop()
        self.values.pop(index)

    def get(self, index: int):
        return self.values[index]

    def length(self):
        return len(self.values)


class Point:
    def __init__(self, x: float, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'Point({self.x}, {self.y}, {self.z})'

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def set_x(self, new_x):
        if type(new_x) == float or type(new_x) == int:
            self.x = new_x
        else:
            raise e.TypeMismatchError(type(new_x))

    def set_y(self, new_y):
        if type(new_y) == float or type(new_y) == int:
            self.y = new_y
        else:
            raise e.TypeMismatchError(type(new_y))

    def set_z(self, new_z):
        if type(new_z) == float or type(new_z) == int:
            self.z = new_z
        else:
            raise e.TypeMismatchError(type(new_z))


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f'Line({self.start}, {self.end})'

    def get_start(self) -> Point:
        return self.start

    def get_end(self) -> Point:
        return self.end

    def set_start(self, new_start):
        if type(new_start) != Point:
            raise e.TypeMismatchError(type(new_start))
        self.start = new_start

    def set_end(self, new_end):
        if type(new_end) != Point:
            raise e.TypeMismatchError(type(new_end))
        self.end = new_end

    def length(self) -> float:
        return round(sqrt((self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2 +
                     (self.start.z - self.end.z) ** 2), 5)


class Polyhedron:
    def __init__(self, lines: list[Line]):
        self.lines_list = lines

    def __str__(self):
        return f'Polyhedron[{", ".join([str(line) for line in self.lines_list])}]'

    def lines(self) -> list[Line]:

        return self.lines_list

    def points(self) -> list[Point]:
        points = []
        for line in self.lines_list:
            for point in [line.get_start(), line.get_end()]:
                if not points:
                    points.append(point)
                else:
                    occurence = False
                    for p in points:
                        if (p.x == point.x and p.y == point.y and p.z == point.z):
                            occurence = True
                    if not occurence:
                        points.append(point)
        return points


class Collection:
    def __init__(self, polyhedrons: list[Polyhedron] = []):
        self.polyhedrons = polyhedrons

    def __str__(self):
        return f'Collection[{", ".join([str(polyhedron) for polyhedron in self.polyhedrons])}]'

    def add(self, polyhedron: Polyhedron):
        self.polyhedrons.append(polyhedron)

    def remove(self, polyhedron: Polyhedron):
        self.polyhedrons.remove(polyhedron)

    def empty(self):
        self.polyhedrons = []

    def display(self):
        fig = plt.figure("Collection")
        ax = fig.add_subplot(111, projection='3d')
        for polyhedron in self.polyhedrons:
            r, g, b = random.random(), random.random(), random.random()
            color = (r, g, b)
            display_points = []
            for point in polyhedron.points():
                display_points.append([point.get_x(), point.get_y(), point.get_z()])
            points = np.array(display_points)
            hull = ConvexHull(points)
            for s in hull.simplices:
                tri = Poly3DCollection([points[s]])
                tri.set_color(color)
                tri.set_alpha(0.9)
                ax.add_collection3d(tri)
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=color, s=0.25)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
