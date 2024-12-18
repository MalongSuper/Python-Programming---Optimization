# Project Management Problem
# Given a set of tasks
# Each task needs time/number of days to complete (duration)
# and a subset of tasks that need to be completed first (preceding tasks)
# Can execute several tasks in parallel
# Find the earliest start for each task
from ortools.linear_solver import pywraplp


# D: The table of project
def solve_project_management(d):
    s = pywraplp.Solver('Project Management Problem',
                        pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    n = len(d)  # Number of tasks/days
    # Maximum finishing time
    # Consider the tasks are scheduled sequentially, one after another
    days_max = sum(d[i][1] for i in range(n))
    # Decision variables
    t = [s.NumVar(0, days_max, 't[%i]' % i) for i in range(n)]
    total = s.NumVar(0, days_max, 'Total')
    # Constraints
    for i in range(n):
        s.Add(t[i] + d[i][1] <= total)
        for j in d[i][2]:  # The precedence job in subsets {...}
            s.Add(t[j] + d[j][1] <= t[i])
    s.Minimize(total)
    status = s.Solve()
    obj_val = s.Objective().Value()
    sol_val = [t[i].solution_value() for i in range(n)]
    return status, obj_val, sol_val


def calculate_earliest_start(d):  # Calculate the earliest start for each task
    # Initialize the earliest start time for each task as 0
    earliest_start = {i: 0 for i in range(len(d))}
    # Process tasks in topological order
    for task in range(len(d)):
        duration, predecessors = d[task][1], d[task][2]
        earliest_finish_time = earliest_start[task] + duration
        # Update the earliest start time for all tasks dependent on this task
        for successor in range(len(d)):
            if task in d[successor][2]:  # If the task is a predecessor of successor
                # Ex: Task 4 is performed after Task 1, Task 2, Task 3
                # By the time you finish these tasks, you will reach day 9
                # As Task 1 takes until day 9 to complete after Task 0
                # Therefore, Task 4 starts from day 9
                earliest_start[successor] = max(earliest_start[successor], earliest_finish_time)
    return earliest_start


def main():
    print("Project Management Problem (Earliest Time)")
    # D[i] = [task i, duration, {preceding tasks of task i}]
    D = [[0, 3, {}],
         [1, 6, {0}],
         [2, 3, {}],
         [3, 2, {2}],
         [4, 2, {1, 2, 3}],
         [5, 7, {}],
         [6, 7, {0, 1}],
         [7, 5, {6}],
         [8, 2, {1, 3, 7}],
         [9, 7, {1, 7}],
         [10, 4, {7}],
         [11, 5, {0}]]
    status, value, t = solve_project_management(D)
    print("Value of objective function (total time): {:0.2f}".format(value))
    print("Schedule:")
    print("Task\t", end=" ")
    n = len(t)
    # Find the earliest start
    earliest_start = calculate_earliest_start(D)
    for i in range(n):
        print('{:d}\t'.format(i), end=' ')
    print('\nStart\t', end=' ')
    for i in range(n):
        print('{:.0f}\t'.format(earliest_start[i]), end=' ')
    print('\nEnd \t', end=' ')
    for i in range(n):
        print('{:.0f}\t'.format(earliest_start[i] + D[i][1]), end=' ')


main()
