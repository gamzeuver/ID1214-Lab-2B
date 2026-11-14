import heapq
from problem_model import ORDER, SLOTS, COST, INITIAL, is_goal, is_valid

INF = float("inf")

def h(state):
    """Sum of the cheapest still-allowed slot for each unscheduled exam.
    Only conflicts with already-scheduled exams count, so is_valid(state, ...)
    is exactly what we need."""
    total = 0
    for i in range(len(state), len(ORDER)):
        exam = ORDER[i]
        options = [COST[exam][s] for s in SLOTS if is_valid(state, exam, s)]
        if not options:
            return INF              #dead end: this exam has no legal slot
        total += min(options)
    return total

def successors(state):
    """Assign the next unscheduled exam to every valid slot."""
    exam = ORDER[len(state)]
    for s in SLOTS:
        if is_valid(state, exam, s):
            new_state = state + (s,)
            if h(new_state) < INF:  #discard states that can't lead to a schedule
                yield new_state, COST[exam][s]

def astar():
    counter = 0                     #tie-breaker for the heap
    open_set = [(h(INITIAL), counter, 0, INITIAL)]  #(f, counter, g, state)
    best_g = {INITIAL: 0}
    parent = {INITIAL: None}
    expanded = 0

    while open_set:
        f, _, g_cur, state = heapq.heappop(open_set)

        if g_cur > best_g[state]:   #outdated entry, a cheaper path was found
            continue

        if is_goal(state):
            return state, g_cur, expanded, parent

        expanded += 1
        for new_state, step_cost in successors(state):
            new_g = g_cur + step_cost
            if new_g < best_g.get(new_state, INF):
                best_g[new_state] = new_g
                parent[new_state] = state
                counter += 1
                heapq.heappush(open_set, (new_g + h(new_state), counter, new_g, new_state))

    return None, None, expanded, parent

def reconstruct(goal, parent):
    path = []
    while goal is not None:
        path.append(goal)
        goal = parent[goal]
    return path[::-1]

if __name__ == "__main__":
    goal, total_cost, expanded, parent = astar()
    if goal is None:
        print("No valid schedule found")
    else:
        print("Schedule:")
        for exam, slot in zip(ORDER, goal):
            print(f"  {exam} -> slot {slot}")
        print("Total cost:", total_cost)
        print("States expanded:", expanded)
        print("Path:", reconstruct(goal, parent))