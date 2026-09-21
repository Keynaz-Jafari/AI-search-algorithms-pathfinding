# Rescue Robot Pathfinding with Search Algorithms

A Python implementation and comparison of five classical artificial intelligence search algorithms in a grid-based rescue robot scenario.

The project models a rescue robot navigating through a damaged building to reach a trapped person while avoiding blocked cells. The same grid, movement rules, and evaluation criteria are used for all algorithms to make the comparison fair. :chatgpt-content-reference{index="0"}

## Overview

The environment is represented as a 2D grid loaded from `map.txt`.

The robot:

- starts at the cell marked `S`
- must reach the goal cell marked `G`
- may move only up, down, left, or right
- cannot move through obstacle cells marked `X`
- uses unit cost for every valid move

The project implements and compares:

- Breadth First Search (BFS)
- Depth First Search (DFS)
- Iterative Deepening Search (IDS)
- Greedy Best First Search
- A* Search :chatgpt-content-reference{index="1"}

## Problem Formulation

Each valid grid position is treated as a state:

```text
(row, column)
