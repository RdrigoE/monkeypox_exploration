import csv
import sys
from typing import NamedTuple
from Bio import SeqIO


class Mutation(NamedTuple):
    position: int
    reference: str
    alteration: str


def load_data(file_name) -> dict[str, list[Mutation]]:
    with open(file_name, "r", encoding="utf-8") as handler:
        lines = list(csv.reader(handler))[1:]
    sample_dict: dict[str, list[Mutation]] = {}
    for line in lines:
        if line[0] not in sample_dict:
            sample_dict[line[0]] = list()
        sample_dict[line[0]].append(
            Mutation(int(line[2]) - 1, line[4], line[5]))

    return sample_dict


def load_fasta(file_path):
    with open(file_path) as handler:
        return list(SeqIO.parse(handler, "fasta"))[0].seq


def main():
    input_file = sys.argv[1]
    ref_file = sys.argv[2]
    data = load_data(input_file)
    fasta_seq = load_fasta(ref_file)
    # GA to AA or TC to TT
    apobec = {
        "TC": 0,
        "GA": 0
    }
    for sample_id, mutation_list in data.items():
        for mutation in mutation_list:
            if mutation.reference == "C" and mutation.alteration == "T":
                if fasta_seq[mutation.position - 1] == "T" and fasta_seq[mutation.position] == "C":
                    apobec["TC"] += 1
            if mutation.reference == "G" and mutation.alteration == "A":
                if fasta_seq[mutation.position] == "G" and fasta_seq[mutation.position + 1] == "A":
                    apobec["GA"] += 1

    print(apobec)


if __name__ == "__main__":
    main()
