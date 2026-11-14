ORDER = ["A", "B", "C", "D"]
SLOTS = [1, 2, 3]

COST = {
    "A": {1: 1, 2: 3, 3: 4},
    "B": {1: 2, 2: 4, 3: 3},
    "C": {1: 3, 2: 1, 3: 2},
    "D": {1: 2, 2: 1, 3: 4},
}

CONFLICTS = {("A", "B"), ("A", "C"), ("B", "D")}

def conflicts(x, y):
    return (x, y) in CONFLICTS or (y,x ) in CONFLICTS

INITIAL = ()

def is_goal(state):
    return len(state) == len(ORDER)

def is_valid(state, exam, slot):
    for i, s in enumerate(state):
        if s == slot and conflicts(ORDER[i], exam):
            return False
    return True

def g(state):
    return sum(COST[ORDER[i]][s] for i, s in enumerate(state))