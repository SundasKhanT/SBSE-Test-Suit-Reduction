"""
experiment.py
-------------
Runs both algorithms over 30 independent seeds.
Saves results to the results/ folder.
Prints a summary table to the terminal.
"""

import os
import csv
import statistics
import sys
sys.path.insert(0, ".")

from src.parser     import load_all
from src.model      import fitness, solution_info
from src.algorithms import pure_random_sampling, elitist_random_search


# ── Settings ──────────────────────────────────────────────────
N_SEEDS = 30        # number of independent runs per algorithm
BUDGET  = 10000     # fitness evaluations per run
OUT_DIR = "results" # folder to save output files


def run_all_seeds(data):
    """Run both algorithms for N_SEEDS seeds each. Return all logs."""

    prs_finals = []   # final best fitness for each seed (PRS)
    ers_finals = []   # final best fitness for each seed (ERS)
    prs_logs   = []   # full convergence log for each seed (PRS)
    ers_logs   = []   # full convergence log for each seed (ERS)

    print(f"Starting experiment: {N_SEEDS} seeds × {BUDGET} evaluations × 2 algorithms")
    print("=" * 60)

    for seed in range(N_SEEDS):

        # ── Pure Random Sampling ───────────────────────────────
        bx_prs, bf_prs, log_prs = pure_random_sampling(
            data, budget=BUDGET, seed=seed
        )
        prs_finals.append(bf_prs)
        prs_logs.append(log_prs)

        # ── Elitist Random Search ──────────────────────────────
        bx_ers, bf_ers, log_ers = elitist_random_search(
            data, budget=BUDGET, seed=seed
        )
        ers_finals.append(bf_ers)
        ers_logs.append(log_ers)

        # Progress update every 5 seeds
        if (seed + 1) % 5 == 0:
            print(f"  Completed {seed + 1}/{N_SEEDS} seeds  |  "
                  f"PRS best so far: {min(prs_finals):.4f}  |  "
                  f"ERS best so far: {min(ers_finals):.4f}")

    print()
    return prs_finals, ers_finals, prs_logs, ers_logs


def print_summary(prs_finals, ers_finals):
    """Print a statistics table to the terminal."""

    def stats(vals):
        s = sorted(vals)
        n = len(s)
        return {
            "min"   : s[0],
            "q1"    : s[n // 4],
            "median": statistics.median(s),
            "q3"    : s[3 * n // 4],
            "max"   : s[-1],
            "mean"  : statistics.mean(s),
            "stdev" : statistics.stdev(s),
        }

    ps = stats(prs_finals)
    es = stats(ers_finals)

    print("=" * 60)
    print("FINAL FITNESS DISTRIBUTION  (lower = better)")
    print("=" * 60)
    print(f"{'Metric':<10} {'PRS':>12} {'ERS':>12}")
    print("-" * 36)
    for key in ["min", "q1", "median", "q3", "max", "mean", "stdev"]:
        print(f"{key:<10} {ps[key]:>12.6f} {es[key]:>12.6f}")
    print()

    winner = "ERS" if es["median"] < ps["median"] else "PRS"
    print(f"→ {winner} achieves lower median fitness (better result)")
    print()


def save_results(prs_finals, ers_finals, prs_logs, ers_logs):
    """Save CSV files to the results/ folder."""
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── File 1: final fitness per seed ────────────────────────
    path1 = os.path.join(OUT_DIR, "final_fitness.csv")
    with open(path1, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "PRS_final_fitness", "ERS_final_fitness"])
        for s in range(N_SEEDS):
            w.writerow([s, round(prs_logs[s][-1], 6), round(ers_logs[s][-1], 6)])
    print(f"Saved: {path1}")

    # ── File 2: convergence curves (median every 100 evals) ───
    path2 = os.path.join(OUT_DIR, "convergence.csv")
    with open(path2, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["evaluation", "PRS_median", "ERS_median"])
        for i in range(BUDGET):
            if i % 100 == 0 or i == BUDGET - 1:
                prs_at_i = [prs_logs[s][i] for s in range(N_SEEDS)]
                ers_at_i = [ers_logs[s][i] for s in range(N_SEEDS)]
                w.writerow([
                    i + 1,
                    round(statistics.median(prs_at_i), 6),
                    round(statistics.median(ers_at_i), 6),
                ])
    print(f"Saved: {path2}")


def show_best_solution(data):
    """Show the best solution found by each algorithm on seed=0."""
    print("=" * 60)
    print("BEST SOLUTION DETAILS  (seed=0)")
    print("=" * 60)

    for name, fn in [("PRS", pure_random_sampling),
                     ("ERS", elitist_random_search)]:
        bx, bf, _ = fn(data, budget=BUDGET, seed=0)
        print(f"\n{name}:")
        solution_info(bx, data)


# ── Main entry point ──────────────────────────────────────────
if __name__ == "__main__":
    # Load data
    data = load_all()

    # Run experiment
    prs_finals, ers_finals, prs_logs, ers_logs = run_all_seeds(data)

    # Print summary table
    print_summary(prs_finals, ers_finals)

    # Save CSV files
    save_results(prs_finals, ers_finals, prs_logs, ers_logs)

    # Show best solutions
    show_best_solution(data)

    print("\nAll done! Check the results/ folder for output files.")