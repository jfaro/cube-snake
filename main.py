import time

from solver import Type, search
from visualizer import render_configuration

WIDTH = 3

INPUT = [
    Type.END,
    Type.LINE,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.CORNER,
    Type.CORNER,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.CORNER,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.CORNER,
    Type.LINE,
    Type.CORNER,
    Type.CORNER,
    Type.CORNER,
    Type.LINE,
    Type.END,
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