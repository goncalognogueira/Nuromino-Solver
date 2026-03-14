# Nuromino Solver 

A university project developed for an Artificial Intelligence course. This Python-based AI solver tackles Nuruomino (also known as LITS), a logic puzzle involving tetromino placement on a grid. The solver implements multiple AI search strategies using a constraint satisfaction problem (CSP) framework to find valid puzzle solutions.

---

## What is Nuruomino?

Nuruomino (LITS) is a logic puzzle where you must place exactly one tetromino (an L, I, T, or S-shaped piece made of 4 cells) in each outlined region of a grid, subject to the following rules:

- Tetrominoes of the same shape may not touch each other orthogonally.
- All placed tetrominoes must form a single connected group.
- No 2×2 block of shaded cells is allowed anywhere on the grid.

---

## Features

- Solves Nuruomino/LITS puzzles of arbitrary grid size
- Solves puzzles using Depth-First Tree Search
- Constraint propagation to prune the search space efficiently
- Modular design split across three focused Python modules

---

## Project Structure

```
Nuromino-Solver/
├── nuruomino.py   # Puzzle definition, constraints, and CSP model
├── search.py      # Search algorithms (backtracking, A*, heuristic search)
└── utils.py       # Helper functions and shared utilities
```

### Module Overview

| File | Responsibility |
|------|----------------|
| `nuruomino.py` | Defines the puzzle board, regions, tetromino shapes, and constraint checking logic |
| `search.py` | Implements search strategies to explore the solution space |
| `utils.py` | Utility functions used across modules (grid manipulation, display, etc.) |

---

## Getting Started

### Prerequisites

- Python 3.8+

No external libraries are required beyond the Python standard library.

### Running the Solver

```bash
python nuruomino.py
```

---

## How It Works

The solver models the puzzle as a Constraint Satisfaction Problem (CSP):

1. **Variables** — each region of the grid that needs a tetromino placed.
2. **Domain** — the set of valid tetromino placements (shape × position × orientation) for each region.
3. **Constraints** — same-shape adjacency, connectivity, and no 2×2 blocks.

Search algorithms in `search.py` explore the assignment space using Depth-First Tree Search, pruning branches that violate constraints early to efficiently navigate the solution space.

---

## Technologies

- **Language:** Python 3
- **Paradigm:** Constraint Satisfaction / AI Search
- **Algorithms:** Depth-First Tree Search, Constraint Propagation

---

## License

This project is open source. Feel free to use, modify, and distribute.
