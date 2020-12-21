
# pig_farm_sequence
DSMZ pig farm sequencing project

## Assembly
To calculate the read coverage of contigs:

 1. canu assembly of the PacBio sequences
 2. run BWA to map the illumina reads on the pacbio contigs, and merge the bam file into one, name it as something like all.bam and generate the bai file.
 3. generate a list of contigs of interest, one contig per line. Name it contig_list.txt and run bam_sample_stats.py as follows:
`python bam_sample_stats.py all.bam contig_list.txt`

For the canu assembly please refer to:
 https://github.com/dgg32/canu_slurm
 
To assemble the 9er samples, this command is used:

`canu -assemble -p asm -d co_ass_9_2 genomeSize=500000000 -maxInputCoverage=5000 -pacbio-hifi ./input batOptions="-eg 0.0 -sb 0.001 -dg 0 -db 3 -dr 0 -ca 2000 -cp 200"`

## Binning
Using pb-metagenome-binning:

`conda activate pb-binning`

`cd binning_folder`

`snakemake  --snakefile '/home/sih13/tool/pb-metagenomics-tools/Genome-Binning-Pipeline/Snakefile-genomebinning' --configfile '/home/sih13/tmp/martinique_metagenome_pacbio/661/call-export_fastq/execution/pb_binning_unitig_contig/config.yaml'   -j 48 --use-conda`

## Contig analyses
For selective contigs, a further analysis can be done.

1. checkm
`sbatch -p mid  -c 8 --mem=64G --wrap="checkm  lineage_wf -t 8 -x fasta '/home/sih13/tmp/martinique_metagenome_pacbio/co_ass_9_2/bigger_than_1m' '/home/sih13/tmp/martinique_metagenome_pacbio/co_ass_9_2/bigger_than_1m_checkm'"`

2. dfast

dfast --genome input.fasta -o input.fasta_dfast --cpu 8 --use_original_name t
