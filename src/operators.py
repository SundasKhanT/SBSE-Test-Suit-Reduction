
import random


def bit_flip_mutation(x, data, rng):
    x   = x[:]             
    T   = data["T"]
    idx = rng.randint(0, T - 1)   
    x[idx] = 1 - x[idx]          
    return x


def swap_mutation(x, data, rng):
    x = x[:]
    T = data["T"]

    included = [i for i in range(T) if x[i] == 1]
    excluded = [i for i in range(T) if x[i] == 0]

    # Fallback if swap is impossible
    if not included or not excluded:
        return bit_flip_mutation(x, data, rng)

    remove = rng.choice(included)   
    add    = rng.choice(excluded)   

    x[remove] = 0
    x[add]    = 1

    return x


def apply_random_operator(x, data, rng):
    if rng.random() < 0.5:
        return bit_flip_mutation(x, data, rng)
    else:
        return swap_mutation(x, data, rng)



if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.parser import load_all

    data = load_all()
    rng  = __import__("random").Random(42)

    x = [1, 0, 0, 1, 0, 1, 0, 0, 1, 0,
         0, 1, 0, 1, 0, 0, 1, 0, 0, 1,
         0, 0, 1, 0, 1, 0, 0, 1, 0, 0]

    print("Original:", x)

    x1 = bit_flip_mutation(x, data, rng)
    print("After bit-flip:", x1)

    x2 = swap_mutation(x, data, rng)
    print("After swap:    ", x2)