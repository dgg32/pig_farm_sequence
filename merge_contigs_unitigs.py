import screed
import sys
import os

unitigs_file = sys.argv[1]
contigs_file = sys.argv[2]

new_unitigs_file = unitigs_file + "_new_unitigs.fasta"

with screed.open(unitigs_file) as seqfile:
    with open(new_unitigs_file, mode="a") as outfile:
        for read in seqfile:
            #print(read.name, read.sequence)
            outfile.write(f">uni{read.name}\n{read.sequence}\n")



output_file = contigs_file + "_contigs_unitigs.fasta"
os.system(f"cat {contigs_file} {new_unitigs_file} > {output_file}")