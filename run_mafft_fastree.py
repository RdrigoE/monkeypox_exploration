# fasttree -gtr -boot 1000 -nt {input} > {output}
# mafft --thread 8 --preservecase {input} > {output}
import sys
import os
from generate_minor_consensus import generate_altered_consensus

if __name__ == "__main__":
    input_consensus = sys.argv[1]
    variants = sys.argv[2]
    output_consensus = sys.argv[3]
    output_aligned = sys.argv[4]
    final_tree = sys.argv[5]
    generate_altered_consensus(input_consensus, variants, output_consensus)
    os.system(
        f"mafft --thread 8 --preservecase {output_consensus} > {output_aligned}")
    os.system(f"fasttree -gtr -boot 1000 -nt {output_aligned} > {final_tree}")
