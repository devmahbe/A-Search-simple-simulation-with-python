from pyamaze import maze, agent, textLabel  
from queue import PriorityQueue  

# Function to calculate heuristic (Manhattan distance) between two cells
def heuristic(cell1, cell2):
    x1, y1 = cell1  # Coordinates of the first cell
    x2, y2 = cell2  # Coordinates of the second cell
    return abs(x1 - x2) + abs(y1 - y2)  # Return the sum of the absolute differences of the coordinates

# A* algorithm to find the shortest path in the maze
def a_star_search(maze_obj):
    # Start cell is the bottom-right corner of the maze
    start = (maze_obj.rows, maze_obj.cols)
    
    # Initialize g-scores (cost from start to the current cell)
    g_scores = {cell: float('inf') for cell in maze_obj.grid}
    g_scores[start] = 0  # Start cell has a g-score of 0
    
    # Initialize f-scores (estimated total cost from start to goal)
    f_scores = {cell: float('inf') for cell in maze_obj.grid}
    f_scores[start] = heuristic(start, (1, 1))  # Calculate f-score for the start cell
    
    # Create a priority queue for open list and add the start cell
    open_list = PriorityQueue()
    open_list.put((f_scores[start], start))
    
    # Dictionary to store the path
    path_taken = {}

    # Continue searching until the open list is empty
    while not open_list.empty():
        current = open_list.get()[1]  # Get the cell with the lowest f-score from the open list
        
        # If the current cell is the goal cell, stop searching
        if current == (1, 1):  # Goal is at the top-left corner (1,1)
            break

        # Check each possible direction (East, South, North, West) from the current cell
        for direction in 'ESNW':
            if maze_obj.maze_map[current][direction] == True:  # Check if the path in this direction is open
                # Determine the next cell based on the direction
                if direction == 'E':
                    next_cell = (current[0], current[1] + 1)
                elif direction == 'W':
                    next_cell = (current[0], current[1] - 1)
                elif direction == 'N':
                    next_cell = (current[0] - 1, current[1])
                elif direction == 'S':
                    next_cell = (current[0] + 1, current[1])
                
                # Calculate temporary g-score for the next cell
                temp_g = g_scores[current] + 1
                
                # Calculate temporary f-score for the next cell
                temp_f = temp_g + heuristic(next_cell, (1, 1))

                # If the calculated f-score is better than the current f-score for the next cell
                if temp_f < f_scores[next_cell]:
                    g_scores[next_cell] = temp_g  # Update g-score
                    f_scores[next_cell] = temp_f  # Update f-score
                    open_list.put((temp_f, next_cell))  # Add next cell to the open list
                    path_taken[next_cell] = current  # Record the path

    # Reconstruct the path by backtracking from the goal cell to the start
    final_path = {}
    cell = (1, 1)  # Start at the goal cell
    while cell != start:
        final_path[path_taken[cell]] = cell # Add cell and its parent to the path
        cell = path_taken[cell]# Move to the parent cell
    
    return final_path# Return the reconstructed path

m = maze(6, 9)
m.CreateMaze()
path = a_star_search(m)
agent_obj = agent(m, footprints=True, filled=True)
m.tracePath({agent_obj: path})
label = textLabel(m, 'A* Path Length', len(path) + 1)
m.run()