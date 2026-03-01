import random


W_TIME    = 0.3   
W_PENALTY = 0.7   


def random_solution(T, rng):
    return [rng.randint(0, 1) for _ in range(T)]


def repair(x, data, rng):
    
    x = x[:]  
    T          = data["T"]
    E          = data["E"]
    cov_matrix = data["cov_matrix"]

    for j in range(E):
       
        is_covered = any(x[i] == 1 and cov_matrix[i][j] == 1 for i in range(T))

        if not is_covered:
            candidates = [i for i in range(T) if cov_matrix[i][j] == 1]
            chosen = rng.choice(candidates)
            x[chosen] = 1

    return x


def fitness(x, data):
    times      = data["times"]
    cov_matrix = data["cov_matrix"]
    T_max      = data["T_max"]
    T          = data["T"]
    E          = data["E"]

    total_time = sum(times[i] for i in range(T) if x[i] == 1)

 
    covered = [0] * E
    for i in range(T):
        if x[i] == 1:
            for j in range(E):
                if cov_matrix[i][j] == 1:
                    covered[j] = 1

    uncovered = E - sum(covered)  

 
    time_score    = total_time / T_max   # normalized to [0, 1]
    penalty_score = uncovered  / E       # normalized to [0, 1]

    f = W_TIME * time_score + W_PENALTY * penalty_score

    return f, total_time, uncovered


def solution_info(x, data):
    test_ids = data["test_ids"]
    T        = data["T"]
    f, total_time, uncovered = fitness(x, data)

    selected = [test_ids[i] for i in range(T) if x[i] == 1]
    covered  = data["E"] - uncovered

    print(f"  Selected tests ({len(selected)}): {selected}")
    print(f"  Total time    : {total_time:.2f}s")
    print(f"  Coverage      : {covered}/{data['E']} elements")
    print(f"  Fitness F(x)  : {f:.6f}")



if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.parser import load_all

    data = load_all()
    rng  = random.Random(42)

    x = random_solution(data["T"], rng)
    x = repair(x, data, rng)

    print("Example repaired solution:")
    solution_info(x, data)