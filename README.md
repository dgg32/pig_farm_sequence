# pig_farm_sequence
DSMZ pig farm sequencing project


#1 canu assembly of the PacBio sequences

https://github.com/dgg32/canu_slurm

But with custom coverage settings:

> corOutCoverage=10000 corMhapSensitivity=high corMinCoverage=0
> redMemory=32 oeaMemory=32 batMemory=200 genomeSize=500m useGrid=false


#2 run BWA to map the illumina reads on the pacbio contigs, and merge the bam file into one, name it as something like all.bam and generate the bai file.

#3 generate a list of contigs of interest, one contig per line. Name it contig_list.txt and run bam_sample_stats.py as follows:

>  python bam_sample_stats.py all.bam contig_list.txt


