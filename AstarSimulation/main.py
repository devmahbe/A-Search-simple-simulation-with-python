from pyamaze import maze, agent, textLabel
from queue import PriorityQueue
import tkinter as tk  
import time  

#calculate Manhattan distance as the heuristic for A* search
def heuristic(cell1, cell2):
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

#implementation of A* algorithm for pathfinding in the maze
def a_star_search(maze_instance):
    start = (maze_instance.rows, maze_instance.cols)  
    goal = (1, 1)  #goal at top-left corner

    #initialize cost maps for g-score(distance from start) and f-score(estimated total cost)
    g_score = {cell: float('inf') for cell in maze_instance.grid}
    f_score = {cell: float('inf') for cell in maze_instance.grid}
    g_score[start] = 0
    f_score[start] = heuristic(start, goal)

    #priority queue to manage exploration of nodes
    open_set = PriorityQueue()
    open_set.put((f_score[start], start))

    #dictionary to keep track of the path
    came_from = {}

    while not open_set.empty():
        current = open_set.get()[1]

        #if we reach the goal we exit the loop
        if current == goal:
            break

        #explore neighbors(east, south, north, west)
        for direction in 'ESNW':
            if maze_instance.maze_map[current][direction]:
                if direction == 'E':
                    neighbor = (current[0], current[1] + 1)
                elif direction == 'W':
                    neighbor = (current[0], current[1] - 1)
                elif direction == 'N':
                    neighbor = (current[0] - 1, current[1])
                elif direction == 'S':
                    neighbor = (current[0] + 1, current[1])

                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))
                    came_from[neighbor] = current

    #reconstruct the path from goal to start
    path = {}
    step = goal
    while step != start:
        path[came_from[step]] = step
        step = came_from[step]
    return path

def run_maze(rows, cols):
    maze_instance = maze(rows, cols)
    maze_instance.CreateMaze()

    path = a_star_search(maze_instance)
    agent_instance = agent(maze_instance, footprints=True, filled=True, shape='arrow')

    #im adding delay for a smooth visual representation of the agent's path you can skip it if you want to....
    for cell in path:
        maze_instance.tracePath({agent_instance: [cell]}, delay=500)
        time.sleep(0.1)

    textLabel(maze_instance, 'A* Path Length', len(path) + 1)

    maze_instance._win.focus_force()

    maze_instance.run()
rows = int(input("Enter the number of rows for the maze: "))
cols = int(input("Enter the number of columns for the maze: "))

run_maze(rows, cols)
