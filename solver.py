import copy
import time


class Type:
    END = "E"
    LINE = "L"
    CORNER = "C"


class Vec3:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"


def add(a: Vec3, b: Vec3) -> Vec3:
    return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)


def cmp(a: Vec3, b: Vec3) -> bool:
    return a.x == b.x and a.y == b.y and a.z == b.z


class Bounds:
    def __init__(self, init: Vec3, max_width: int):
        self.max_width = max_width
        self.min_x = init.x
        self.max_x = init.x
        self.min_y = init.y
        self.max_y = init.y
        self.min_z = init.z
        self.max_z = init.z

    def allows(self, pos: Vec3) -> bool:
        max_diff = self.max_width - 1
        x_limit_reached = self.max_x - self.min_x == max_diff
        y_limit_reached = self.max_y - self.min_y == max_diff
        z_limit_reached = self.max_z - self.min_z == max_diff

        if x_limit_reached and (pos.x > self.max_x or pos.x < self.min_x):
            return False
        if y_limit_reached and (pos.y > self.max_y or pos.y < self.min_y):
            return False
        if z_limit_reached and (pos.z > self.max_z or pos.z < self.min_z):
            return False
        return True

    def update(self, pos: Vec3):
        if pos.x > self.max_x:
            self.max_x = pos.x
        elif pos.x < self.min_x:
            self.min_x = pos.x

        if pos.y > self.max_y:
            self.max_y = pos.y
        elif pos.y < self.min_y:
            self.min_y = pos.y

        if pos.z > self.max_z:
            self.max_z = pos.z
        elif pos.z < self.min_z:
            self.min_z = pos.z


class Component:
    def __init__(self, type: Type, pos: Vec3, dir: Vec3):
        self.type = type
        self.pos = pos
        self.dir = dir

    def reachable(self) -> list[tuple[Vec3, Vec3]]:
        """Returns list of (position, direction) tuples reachable from `src`."""
        if self.type in [Type.END, Type.LINE]:
            return [(add(self.pos, self.dir), self.dir)]

        if self.dir.x != 0:
            directions = [
                Vec3(0, 1, 0),
                Vec3(0, -1, 0),
                Vec3(0, 0, 1),
                Vec3(0, 0, -1),
            ]
            return [(add(self.pos, d), d) for d in directions]

        if self.dir.y != 0:
            directions = [
                Vec3(1, 0, 0),
                Vec3(-1, 0, 0),
                Vec3(0, 0, 1),
                Vec3(0, 0, -1),
            ]
            return [(add(self.pos, d), d) for d in directions]

        if self.dir.z != 0:
            directions = [
                Vec3(1, 0, 0),
                Vec3(-1, 0, 0),
                Vec3(0, 1, 0),
                Vec3(0, -1, 0),
            ]
            return [(add(self.pos, d), d) for d in directions]

        assert False


class Configuration:
    def __init__(self, start: Component, width: int):
        self.route = [start]
        self.bounds = Bounds(start.pos, width)

    def add(self, component: Component):
        self.route.append(component)
        self.bounds.update(component.pos)

    def head(self) -> Component:
        return self.route[-1]

    def allows(self, pos: Vec3) -> bool:
        if not self.bounds.allows(pos):
            return False
        for c in self.route:
            if cmp(c.pos, pos):
                return False
        return True


def search(input: list[Type], width: int):
    max_len = 1
    last_time = time.time()
    start_pos = Vec3(0, 0, 0)
    start_dir = Vec3(1, 0, 0)
    start_component = Component(Type.END, start_pos, start_dir)

    # Prime the search queue.
    search_queue: list[Configuration] = []
    search_queue.append(Configuration(start_component, width))

    while search_queue:
        config = search_queue.pop(0)
        route_len = len(config.route)
        if route_len > max_len:
            max_len = route_len
            delta = time.time() - last_time
            last_time = time.time()
            print(
                f"Max route length: {max_len} ({delta:.4f}s) | queue size = {len(search_queue)}"
            )

        # Used up all input components.
        if route_len == len(input):
            return config

        # Search from last point in route.
        c = config.head()

        for pos, dir in c.reachable():
            if config.allows(pos):
                next_component = Component(input[route_len], pos, dir)
                next_config = copy.deepcopy(config)
                next_config.add(next_component)
                search_queue.append(next_config)
