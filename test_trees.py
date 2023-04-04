import csv
import sys
from Bio import Phylo
import numpy as np
from Bio.Phylo.TreeConstruction import DistanceMatrix, DistanceTreeConstructor


def load_data(file_name):
    with open(file_name, "r", encoding="utf-8") as handler:
        lines = list(csv.reader(handler))[1:]
    sample_dict: dict[str, set] = {}
    for line in lines:
        if line[0] not in sample_dict:
            sample_dict[line[0]] = set()
        sample_dict[line[0]].add(line[2] + line[5])

    return sample_dict


def custom_distance(seq1: set, seq2: set):
    return len(seq1.intersection(seq2))


if __name__ == "__main__":
    input_file = sys.argv[1]
    dict_data = load_data(input_file)
    keys = list(dict_data.keys())
    data = list(dict_data.values())
    n = len(data)
    result = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1, n):
            dist = custom_distance(data[i], data[j])
            result[i][j] = dist
            result[j][i] = dist
    # max_value = 0
    # for i in result:
    #     m = max(i)
    #     if m > max_value:
    #         max_value = m
    for i, row in enumerate(result):
        for j, _ in enumerate(row):
            result[i][j] = 196956 - result[i][j]
    for idx, row in enumerate(result):
        result[idx] = np.array(row)

    lower_triangle = [[result[i][j] for j in range(i+1)] for i in range(n)]
    dm = DistanceMatrix(names=keys, matrix=lower_triangle)

    constructor = DistanceTreeConstructor()
    # tree = constructor.upgma(dm)
    tree = constructor.nj(dm)
    Phylo.draw_ascii(tree)
    Phylo.write(tree, 'tree.nwk', 'newick')
