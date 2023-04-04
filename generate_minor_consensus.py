from Bio import SeqIO, Seq
import sys
from typing_extensions import NamedTuple
import csv


class Mutation(NamedTuple):
    position: int
    reference: str
    alteration: str


def load_variants(file_name) -> dict[str, list[Mutation]]:
    with open(file_name, "r", encoding="utf-8") as handler:
        lines = list(csv.reader(handler))[1:]
    sample_dict: dict[str, list[Mutation]] = {}
    for line in lines:
        if line[0] not in sample_dict:
            sample_dict[line[0]] = list()
        sample_dict[line[0]].append(Mutation(int(line[2])-1, line[4], line[5]))

    return sample_dict


def load_sequences(file_path):
    with open(file_path) as handler:
        return list(SeqIO.parse(handler, "fasta"))


def generate_altered_consensus(input_consensus, variants, output_consensus):
    sequences = load_sequences(input_consensus)
    minor_variants = load_variants(variants)
    counter = 0
    counter_all = 0
    new_sequences = []
    for record in sequences:
        sequence = Seq.MutableSeq(record.seq)
        for mutation in minor_variants.get(record.id[:-11], []):
            count = 0
            counter_all += 1

            # print(sequence[mutation.position: mutation.position +
            #       len(mutation.alteration)], mutation.reference, mutation.alteration)
            if ''.join(sequence[mutation.position: mutation.position +
                                len(mutation.alteration)]) == mutation.reference:

                counter += 1
            for idx in range(mutation.position, mutation.position + len(mutation.alteration)):
                sequence[idx] = mutation.alteration[count]
                count += 1
        record.seq = sequence
        record.id = str(record.id)
        new_sequences.append(record)
    print(counter, counter_all)
    with open(output_consensus, "w") as handler:
        SeqIO.write(new_sequences, handler, "fasta")


if __name__ == "__main__":
    input_consensus = sys.argv[1]
    variants = sys.argv[2]
    output_consensus = sys.argv[3]
    generate_altered_consensus(input_consensus, variants, output_consensus)
