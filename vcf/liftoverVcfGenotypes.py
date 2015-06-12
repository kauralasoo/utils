import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "LiftOver SNP coordinates in a VCF file from GRCh37 to GRCh38", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--chrMapFwd", help = "File mapping Ensembl chromosome names to UCSC chromosome names.")
parser.add_argument("--chrMapRev", help = "File mapping UCSC chromosome names to Ensembl chromosome names.")
parser.add_argument("--liftOver", help = "Path to the liftOver file.")
parser.add_argument("--reference", help = "Path to the new reference fasta file.")
parser.add_argument("--vcfSuffix", help = "Suffix of the VCF file.")
parser.add_argument("--indir", help = "Path to the input directory.")
parser.add_argument("--outdir", help = "Path to the output directory.")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	vcf_base_name = line.rstrip()
	input_vcf = os.path.join(args.indir, vcf_base_name + args.vcfSuffix)
	print(input_vcf)

	#Rename chromosomes to UCSC namespace
	hg19_vcf = os.path.join(args.outdir, vcf_base_name + ".hg19" + args.vcfSuffix)
	rename_cmd = " ".join(["bcftools annotate -O z --rename-chrs", args.chrMapFwd, input_vcf, ">", hg19_vcf])
	print(rename_cmd + "\n")

	#Use CrossMap.py to lift over coordinates to hg38
	hg38_vcf = os.path.join(args.outdir, vcf_base_name + ".hg38.vcf")
	hg38_vcf_unmap = os.path.join(args.outdir, vcf_base_name + ".hg38.vcf.unmap")
	crossmap_cmd = " ".join(["CrossMap.py vcf", args.liftOver, hg19_vcf, args.reference, hg38_vcf])
	print(crossmap_cmd + "\n")

	#Postprocess CrossMap output
	posprocess_script = "python /nfs/users/nfs_k/ka8/software/utils/vcf/postprocessCrossmap.py"
	hg38_vcf_gz = os.path.join(args.outdir, vcf_base_name + ".hg38.vcf.gz")
	hg38_vcf_post = os.path.join(args.outdir, vcf_base_name + ".hg38.post.vcf.gz")
	pp_command = " ".join([posprocess_script, "--vcf", hg38_vcf_gz, "| bgzip >", hg38_vcf_post])
	print(pp_command + "\n")

	#Rename chromosomes back to Ensembl namespace
	GRCh38_vcf = os.path.join(args.outdir, vcf_base_name + ".GRCh38.vcf.gz")
	rename_cmd_2 = " ".join(["bcftools annotate -O z --rename-chrs", args.chrMapRev, hg38_vcf_post, ">", GRCh38_vcf])
	print(rename_cmd_2 + "\n")

	#Sort VCF file by position
	sorted_vcf = os.path.join(args.outdir, vcf_base_name + ".GRCh38.sorted.vcf.gz")
	header_cmd = " ".join(["zcat", GRCh38_vcf, "| grep '^#' | bgzip >", sorted_vcf])
	body_cmd = " ".join(["zcat", GRCh38_vcf, "| grep -v '^#' | LC_ALL=C sort -k1,1 -k2,2n | bgzip >>", sorted_vcf])
	sort_command = " ".join([header_cmd, "&&", body_cmd])
	print(sort_command + "\n")

	#Execute all of the commands
	if (args.execute == "True"):
		#Rename chromosomes
		print(rename_cmd + "\n")
		#subprocess.call(['bash','-c',rename_cmd])
		os.system(rename_cmd)

		#Run Crossmap and compress output
		print(crossmap_cmd + "\n")
		#subprocess.call(['bash','-c',crossmap_cmd])
		os.system(crossmap_cmd)
		os.system('bgzip ' + hg38_vcf)
		os.system('bgzip ' + hg38_vcf_unmap)
		#subprocess.call(['bash','-c','gzip ' + hg38_vcf])
		#subprocess.call(['bash','-c','gzip ' + hg38_vcf_unmap])

		#Postprocess Crossmap output
		print(pp_command + "\n")
		#subprocess.call(['bash','-c',pp_command])
		os.system(pp_command)

		#Rename chromosomes back
		print(rename_cmd_2 + "\n")
		os.system(rename_cmd_2)
		#subprocess.call(['bash','-c',rename_cmd_2])

		#Rename chromosomes back
		print(sort_command + "\n")
		#subprocess.call(['bash','-c',sort_command])
		os.system(sort_command)








