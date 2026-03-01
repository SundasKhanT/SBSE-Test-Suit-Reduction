
import random
from src.model     import random_solution, repair, fitness
from src.operators import apply_random_operator


def pure_random_sampling(data, budget=10000, seed=42):
    rng    = random.Random(seed)
    best_x = None
    best_f = float("inf")   
    log    = []

    for _ in range(budget):
        # Step 1 & 2: generate and repair
        x = random_solution(data["T"], rng)
        x = repair(x, data, rng)

        # Step 3: evaluate
        f, total_time, uncovered = fitness(x, data)

        # Step 4: update best
        if f < best_f:
            best_f = f
            best_x = x[:]

        # Step 5: log
        log.append(best_f)

    return best_x, best_f, log


def elitist_random_search(data, budget=10000, seed=42):
    rng = random.Random(seed)

    # Step 1 & 2: initialize
    best_x = random_solution(data["T"], rng)
    best_x = repair(best_x, data, rng)
    best_f, _, _ = fitness(best_x, data)
    log = [best_f]

    for _ in range(budget - 1):
        # Step 3a & 3b: mutate and repair
        x_new = apply_random_operator(best_x, data, rng)
        x_new = repair(x_new, data, rng)

        # Step 3c: evaluate
        f_new, _, _ = fitness(x_new, data)

        # Step 3d & 3e: accept only if improved
        if f_new <= best_f:
            best_f = f_new
            best_x = x_new[:]

        log.append(best_f)

    return best_x, best_f, log



if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.parser import load_all
    from src.model  import solution_info

    data = load_all()

    print("Running PRS (seed=0, budget=1000)...")
    bx, bf, log = pure_random_sampling(data, budget=1000, seed=0)
    print(f"Best fitness: {bf:.6f}")
    solution_info(bx, data)

    print("\nRunning ERS (seed=0, budget=1000)...")
    bx2, bf2, log2 = elitist_random_search(data, budget=1000, seed=0)
    print(f"Best fitness: {bf2:.6f}")
    solution_info(bx2, data)