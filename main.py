import time

from solver import search
from visualizer import render_configuration

WIDTH = 3
INPUT = [
    "E",
    "L",
    "C",
    "L",
    "C",
    "L",
    "C",
    "L",
    "C",
    "C",
    "C",
    "C",
    "L",
    "C",
    "L",
    "C",
    "C",
    "C",
    "L",
    "C",
    "C",
    "L",
    "C",
    "C",
    "C",
    "L",
    "E",
]

start = time.time()
solution = search(INPUT, WIDTH)
duration = time.time() - start

if solution is None:
    print(f"no solution found after {duration}s")
    exit(1)

print(f"found solution after {duration}s")
if solution:
    for c in solution.route:
        print(f"{c.type} {c.pos} pointed {c.dir}")

render_configuration(solution)
