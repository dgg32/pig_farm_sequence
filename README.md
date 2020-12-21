# pig_farm_sequence
DSMZ pig farm sequencing project


To calculate the read coverage of contigs:

 1. canu assembly of the PacBio sequences
 2. run BWA to map the illumina reads on the pacbio contigs, and merge the bam file into one, name it as something like all.bam and generate the bai file.
 3. generate a list of contigs of interest, one contig per line. Name it contig_list.txt and run bam_sample_stats.py as follows:
`python bam_sample_stats.py all.bam contig_list.txt`

For the canu assembly please refer to:
 https://github.com/dgg32/canu_slurm


Using pb-metagenome-binning:

`conda activate pb-binning`

`cd binning_folder`

`snakemake  --snakefile '/home/sih13/tool/pb-metagenomics-tools/Genome-Binning-Pipeline/Snakefile-genomebinning' --configfile '/home/sih13/tmp/martinique_metagenome_pacbio/661/call-export_fastq/execution/pb_binning_unitig_contig/config.yaml'   -j 48 --use-conda`


For selective contigs, a further analysis can be done.

1. checkm
`sbatch -p mid  -c 8 --mem=64G --wrap="checkm  lineage_wf -t 8 -x fasta '/home/sih13/tmp/martinique_metagenome_pacbio/co_ass_9_2/bigger_than_1m' '/home/sih13/tmp/martinique_metagenome_pacbio/co_ass_9_2/bigger_than_1m_checkm'"`
