# pig_farm_sequence
DSMZ pig farm sequencing project


To calculate the read coverage of contigs:

 1. canu assembly of the PacBio sequences
 2. run BWA to map the illumina reads on the pacbio contigs, and merge the bam file into one, name it as something like all.bam and generate the bai file.
 3. generate a list of contigs of interest, one contig per line. Name it contig_list.txt and run bam_sample_stats.py as follows:
`python bam_sample_stats.py all.bam contig_list.txt`

For the canu assembly please refer to:
 https://github.com/dgg32/canu_slurm





