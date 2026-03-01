import csv
import os


def load_tests(filepath="data/tests.csv"):
    test_ids = []
    times = []

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            test_ids.append(row["test_id"])
            times.append(float(row["time"]))
    return test_ids, times


def load_coverage(filepath="data/coverage.csv"):
    elements = []
    cov_matrix = []

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter="\t")  
        elements = [col.strip() for col in reader.fieldnames if col.strip() != "test_id"]
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            row_coverage = [int(row[e]) for e in elements]
            cov_matrix.append(row_coverage)

    return elements, cov_matrix


def load_all(tests_path="data/tests.csv", coverage_path="data/coverage.csv"):
    test_ids, times = load_tests(tests_path)
    elements, cov_matrix = load_coverage(coverage_path)

    T = len(test_ids)  
    E = len(elements)   
    T_max = sum(times)  

    data = {
        "test_ids"   : test_ids,    # ['t1', 't2', ..., 't30']
        "times"      : times,       # [3.2, 1.5, ..., 1.4]
        "elements"   : elements,    # ['e1', 'e2', ..., 'e20']
        "cov_matrix" : cov_matrix,  # 30 x 20 matrix of 0s and 1s
        "T"          : T,           # 30
        "E"          : E,           # 20
        "T_max"      : T_max        # 79.7
    }

    return data



if __name__ == "__main__":
    data = load_all()
    print(f"Tests loaded  : {data['T']}")
    print(f"Elements      : {data['E']}")
    print(f"T_max         : {data['T_max']}")
    print(f"First test    : {data['test_ids'][0]}, time={data['times'][0]}")
    print(f"Coverage row 0: {data['cov_matrix'][0]}")