from collections import Counter
import sys
import csv


def load_data(file_name):
    with open(file_name, "r", encoding="utf-8") as handler:
        lines = list(csv.reader(handler))[1:]
    list_mut = []
    for line in lines:
        if line[14]:
            print(line[14])
            list_mut.append(line[14])

    return list_mut


if __name__ == "__main__":
    data = load_data(sys.argv[1])

    print(Counter(data))
