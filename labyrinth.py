import networkx as nx
import numpy as np
from tqdm import tqdm  # Progress bar
import random
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("qtagg")  # Or whatever backed is convenient


class Room:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

        # Randomize exits
        n = random.choice([1, 2, 3, 4])
        valid_exit_directions = [(self.x+1, self.y), (self.x-1, self.y),
                                 (self.x, self.y+1), (self.x, self.y-1)]
        random.shuffle(valid_exit_directions)
        self.exits = [valid_exit_directions.pop() for _ in range(n)]

    def __eq__(self, other):
        # Same location --> same room
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Room at ({self.x},{self.y}) with exits to {self.exits}"

    def __str__(self):
        # This is called when drawing node labels on networkx graphs
        return f"{self.x},{self.y}"


# User-defined parameters
plot_final: bool = True
reruns: int = 250
max_iter: int = 100

history = []
for _ in tqdm(range(reruns)):
    origin = Room(0, 0)
    G = nx.DiGraph()
    G.add_node(origin)

    unvisited = [origin]
    unvisited_per_it = [len(unvisited)]
    it = 0
    while unvisited and it < max_iter:
        todolist = []  # Do not modify unvisited during iteration
        for room in unvisited:
            neighbors = [Room(*ex) for ex in room.exits]  # Peek through the exits
            # Only add neighbors if they didn't already exist
            new_neighbors = [nb for nb in neighbors if nb not in G.nodes]
            todolist.extend(new_neighbors)
            G.add_nodes_from(new_neighbors)
            # Exits can point to existing rooms
            G.add_edges_from([(room, n) for n in neighbors])
        unvisited = todolist
        unvisited_per_it.append(len(unvisited))
        it += 1
    history.append(unvisited_per_it)

mean_per_it = np.zeros(max_iter)
for h in history:
    # If a run ends early, pad zeros out to max_iter
    h_padded = np.zeros(max_iter)
    length = min(len(h), max_iter)
    h_padded[:length] = h[:length]
    mean_per_it += h_padded
mean_per_it /= reruns

xs = range(len(mean_per_it))
# Get best fit (linear)
fit = np.polyfit(xs, mean_per_it, 1)
fit_line = np.poly1d(fit)
fit_line_ys = fit_line(xs)

# All the rest is plotting
plt.plot(xs, mean_per_it, "b:", label=f"Average of {reruns} runs")
plt.plot(xs, fit_line_ys, "r--", label=f"# = {fit[0]:.2f}×IT + {fit[1]:.2f}")
plt.xlabel("Iteration")
plt.ylabel("Average # of Unvisited Rooms")
plt.xlim(0, max_iter)
plt.xticks(plt.xticks()[0], [f"{int(tick)}" for tick in plt.xticks()[0]])
plt.tight_layout()
plt.legend()
plt.show()
