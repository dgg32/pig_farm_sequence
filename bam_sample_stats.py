#bam_venn

import sys
import pysam
import os
from multiprocessing import Pool, Lock
import multiprocessing

import functools

input_bam_file = sys.argv[1]
contig_list_file = sys.argv[2]

contig_list = set()

lock = multiprocessing.Lock()

with open(contig_list_file, 'r') as infile:
    for line in infile:
        contig_list.add(line.strip())

print (f"contig\treads")

def worker(contig):

    samfile_temp = pysam.AlignmentFile(input_bam_file, "rb")

    reads = samfile_temp.count(contig = contig, read_callback = "all")

    with lock:
        print (f"{contig}\t{reads}")

    #return (shared, samfile_temp.get_reference_length(contig))

samfile = pysam.AlignmentFile(input_bam_file, "rb")

contigs = [x for x in samfile.references if x in contig_list]

#contigs = ["tig00000642"]

num_of_cpu = multiprocessing.cpu_count()

with Pool(num_of_cpu) as P:

    #P.map(worker, contigs)
    #pass
    P.map(worker, contigs)

    P.close()
    P.join()
    #print (f"shared: {results[0]}, reference_len: {results[1]}")

#print ("\n".join(str(x) for x in samfile.get_index_statistics()))

#print ("tig00000642" in contigs)