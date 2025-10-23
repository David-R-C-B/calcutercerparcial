import numpy as np

class GameOfLife:
    def __init__(self, rows, cols, initial_state=None, toroidal=True):
        self.rows = rows
        self.cols = cols
        self.toroidal = toroidal

        if initial_state is not None:
            if initial_state.shape != (rows, cols):
                raise ValueError(f"Initial state shape ({initial_state.shape}) must match Game of Life grid shape ({(rows, cols)}).")
            self.grid = np.array(initial_state, dtype=int)
        else:
            self.grid = np.random.randint(0, 2, (rows, cols), dtype=int)

    def _count_neighbors(self, r, c):
        live_neighbors = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                if self.toroidal:
                    nr %= self.rows
                    nc %= self.cols
                    live_neighbors += self.grid[nr, nc]
                else:
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        live_neighbors += self.grid[nr, nc]
        return live_neighbors

    def next_generation(self):
        new_grid = np.zeros((self.rows, self.cols), dtype=int)
        for r in range(self.rows):
            for c in range(self.cols):
                live_neighbors = self._count_neighbors(r, c)
                current_state = self.grid[r, c]

                # Game of Life rules (B3/S23)
                if current_state == 1:  # Cell is alive
                    if live_neighbors == 2 or live_neighbors == 3:
                        new_grid[r, c] = 1  # Survives
                else:  # Cell is dead
                    if live_neighbors == 3:
                        new_grid[r, c] = 1  # Becomes alive (birth)
        self.grid = new_grid

    def get_grid(self):
        return self.grid
