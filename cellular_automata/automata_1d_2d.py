import numpy as np

class Automata1D:
    def __init__(self, size, rule_number, initial_state=None):
        if not (0 <= rule_number <= 255):
            raise ValueError("Rule number must be between 0 and 255.")
        self.size = size
        self.rule_number = rule_number
        self.rule_set = self._get_rule_set(rule_number)

        if initial_state is not None:
            if len(initial_state) != size:
                raise ValueError(f"Initial state size ({len(initial_state)}) must match automaton size ({size}).")
            self.current_state = np.array(initial_state, dtype=int)
        else:
            self.current_state = np.random.randint(0, 2, size, dtype=int)
        
        self.history = [self.current_state.copy()]

    def _get_rule_set(self, rule_number):
        # Converts a Wolfram rule number (0-255) into an 8-element binary array
        # representing the output for each of the 8 possible 3-cell patterns.
        # The patterns are ordered from 111 (7) to 000 (0).
        return np.array([(rule_number >> i) & 1 for i in range(8)], dtype=int)

    def next_generation(self):
        new_state = np.zeros(self.size, dtype=int)
        for i in range(self.size):
            left = self.current_state[(i - 1) % self.size]
            center = self.current_state[i]
            right = self.current_state[(i + 1) % self.size]
            
            # Map the 3-cell pattern to an index (0-7)
            # 111 -> 7, 110 -> 6, ..., 000 -> 0
            pattern_index = (left << 2) | (center << 1) | right
            
            # The rule_set is ordered from 000 to 111, so we need to reverse the index
            # or adjust the rule_set creation. Let's adjust the index for clarity.
            # The rule_set is created with index 0 for 000, 1 for 001, ..., 7 for 111.
            # So, pattern_index directly corresponds to the rule_set index.
            new_state[i] = self.rule_set[pattern_index]
        
        self.current_state = new_state
        self.history.append(self.current_state.copy())

    def get_current_state(self):
        return self.current_state

    def get_history(self):
        return self.history

class Automata2D:
    def __init__(self, rows, cols, birth_rules, survival_rules, initial_state=None, toroidal=True):
        self.rows = rows
        self.cols = cols
        self.birth_rules = set(birth_rules)
        self.survival_rules = set(survival_rules)
        self.toroidal = toroidal

        if initial_state is not None:
            if initial_state.shape != (rows, cols):
                raise ValueError(f"Initial state shape ({initial_state.shape}) must match automaton shape ({(rows, cols)}).")
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

                if current_state == 1:  # Cell is alive
                    if live_neighbors in self.survival_rules:
                        new_grid[r, c] = 1
                else:  # Cell is dead
                    if live_neighbors in self.birth_rules:
                        new_grid[r, c] = 1
        self.grid = new_grid

    def get_grid(self):
        return self.grid
