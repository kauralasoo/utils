#!/bin/bash

#The job should run on the testing partition
#SBATCH -p main

#The name of the job is test_job
#SBATCH -J replace_coords

#The job requires 1 compute node
#SBATCH -N 1

#The job requires 1 task per node
#SBATCH --ntasks-per-node=1

#The maximum walltime of the job is a half hour
#SBATCH -t 24:00:00

#SBATCH --mem 24000

#These commands are run on one of the nodes allocated to the job (batch node)
module load R/3.5.1
Rscript liftover_scripts/replace_coordinates_bed.R -s Alzheimers_disease_Lambert_2013_NatGen_GWAS_meta_stage1.sorted.txt.gz -c new_coords/Alzheimers_disease_Lambert_2013_NatGen_GWAS_meta_stage1.new_coords.bed -o GRCh38/Alzheimers_disease_Lambert_2013_NatGen_GWAS_meta_stage1.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s CAD_C4D_cardiogram_Nikpay_2015_additive.sorted.txt.gz -c new_coords/CAD_C4D_cardiogram_Nikpay_2015_additive.new_coords.bed -o GRCh38/CAD_C4D_cardiogram_Nikpay_2015_additive.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Celiac_disease_Dubois_2010_NatGen_GWAS.sorted.txt.gz -c new_coords/Celiac_disease_Dubois_2010_NatGen_GWAS.new_coords.bed -o GRCh38/Celiac_disease_Dubois_2010_NatGen_GWAS.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Celiac_disease_Trynka_2011_NatGen_Immunochip.sorted.txt.gz -c new_coords/Celiac_disease_Trynka_2011_NatGen_Immunochip.new_coords.bed -o GRCh38/Celiac_disease_Trynka_2011_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Creatinine.unified.sorted.txt.gz -c new_coords/Creatinine.unified.new_coords.bed -o GRCh38/Creatinine.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Crohns_disease_Jostins_2012_Nature_GWAS.sorted.txt.gz -c new_coords/Crohns_disease_Jostins_2012_Nature_GWAS.new_coords.bed -o GRCh38/Crohns_disease_Jostins_2012_Nature_GWAS.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s CRP.unified.sorted.txt.gz -c new_coords/CRP.unified.new_coords.bed -o GRCh38/CRP.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Glucose.unified.sorted.txt.gz -c new_coords/Glucose.unified.new_coords.bed -o GRCh38/Glucose.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s HDL.unified.sorted.txt.gz -c new_coords/HDL.unified.new_coords.bed -o GRCh38/HDL.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s HGB.unified.sorted.txt.gz -c new_coords/HGB.unified.new_coords.bed -o GRCh38/HGB.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s HOMA_b.unified.sorted.txt.gz -c new_coords/HOMA_b.unified.new_coords.bed -o GRCh38/HOMA_b.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s HOMA_ir.unified.sorted.txt.gz -c new_coords/HOMA_ir.unified.new_coords.bed -o GRCh38/HOMA_ir.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s IL6.unified.sorted.txt.gz -c new_coords/IL6.unified.new_coords.bed -o GRCh38/IL6.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Inflammatory_bowel_disease_CD_Liu_2015_NatGen_Immunochip.sorted.txt.gz -c new_coords/Inflammatory_bowel_disease_CD_Liu_2015_NatGen_Immunochip.new_coords.bed -o GRCh38/Inflammatory_bowel_disease_CD_Liu_2015_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Inflammatory_bowel_disease_Liu_2015_NatGen_Immunochip.sorted.txt.gz -c new_coords/Inflammatory_bowel_disease_Liu_2015_NatGen_Immunochip.new_coords.bed -o GRCh38/Inflammatory_bowel_disease_Liu_2015_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Inflammatory_bowel_disease_UC_Liu_2015_NatGen_Immunochip.sorted.txt.gz -c new_coords/Inflammatory_bowel_disease_UC_Liu_2015_NatGen_Immunochip.new_coords.bed -o GRCh38/Inflammatory_bowel_disease_UC_Liu_2015_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Insulin.unified.sorted.txt.gz -c new_coords/Insulin.unified.new_coords.bed -o GRCh38/Insulin.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s LDL.unified.sorted.txt.gz -c new_coords/LDL.unified.new_coords.bed -o GRCh38/LDL.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s MCHC.unified.sorted.txt.gz -c new_coords/MCHC.unified.new_coords.bed -o GRCh38/MCHC.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s MCH.unified.sorted.txt.gz -c new_coords/MCH.unified.new_coords.bed -o GRCh38/MCH.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s MCV.unified.sorted.txt.gz -c new_coords/MCV.unified.new_coords.bed -o GRCh38/MCV.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s MI_C4D_cardiogram_Nikpay_2015_additive.sorted.txt.gz -c new_coords/MI_C4D_cardiogram_Nikpay_2015_additive.new_coords.bed -o GRCh38/MI_C4D_cardiogram_Nikpay_2015_additive.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Multiple_sclerosis_IMSGC-Beecham_2013_NatGen_Immunochip.sorted.txt.gz -c new_coords/Multiple_sclerosis_IMSGC-Beecham_2013_NatGen_Immunochip.new_coords.bed -o GRCh38/Multiple_sclerosis_IMSGC-Beecham_2013_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Narcolepsy_Faraco_2013_PLoSGen_Immunochip.sorted.txt.gz -c new_coords/Narcolepsy_Faraco_2013_PLoSGen_Immunochip.new_coords.bed -o GRCh38/Narcolepsy_Faraco_2013_PLoSGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s PCV.unified.sorted.txt.gz -c new_coords/PCV.unified.new_coords.bed -o GRCh38/PCV.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s PLT.unified.sorted.txt.gz -c new_coords/PLT.unified.new_coords.bed -o GRCh38/PLT.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Primary_biliary_cirrhosis_Cordell_2015_NatCommun_GWAS_meta.sorted.txt.gz -c new_coords/Primary_biliary_cirrhosis_Cordell_2015_NatCommun_GWAS_meta.new_coords.bed -o GRCh38/Primary_biliary_cirrhosis_Cordell_2015_NatCommun_GWAS_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Psoriasis_Tsoi_2012_NatGen_meta_NCBI_dbGAP_GAIN.sorted.txt.gz -c new_coords/Psoriasis_Tsoi_2012_NatGen_meta_NCBI_dbGAP_GAIN.new_coords.bed -o GRCh38/Psoriasis_Tsoi_2012_NatGen_meta_NCBI_dbGAP_GAIN.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s RBC.unified.sorted.txt.gz -c new_coords/RBC.unified.new_coords.bed -o GRCh38/RBC.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Rheumatoid_Arthritis_Eyre_2012_NatGen_Immunochip.sorted.txt.gz -c new_coords/Rheumatoid_Arthritis_Eyre_2012_NatGen_Immunochip.new_coords.bed -o GRCh38/Rheumatoid_Arthritis_Eyre_2012_NatGen_Immunochip.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Rheumatoid_Arthritis_Okada_2014_Nature_GWAS_meta.sorted.txt.gz -c new_coords/Rheumatoid_Arthritis_Okada_2014_Nature_GWAS_meta.new_coords.bed -o GRCh38/Rheumatoid_Arthritis_Okada_2014_Nature_GWAS_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Schizophrenia_Ripke_2014_Nature_GWAS.sorted.txt.gz -c new_coords/Schizophrenia_Ripke_2014_Nature_GWAS.new_coords.bed -o GRCh38/Schizophrenia_Ripke_2014_Nature_GWAS.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Systemic_lupus_erythematosus_Bentham_2015_NatGen_GWAS.sorted.txt.gz -c new_coords/Systemic_lupus_erythematosus_Bentham_2015_NatGen_GWAS.new_coords.bed -o GRCh38/Systemic_lupus_erythematosus_Bentham_2015_NatGen_GWAS.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s TC.unified.sorted.txt.gz -c new_coords/TC.unified.new_coords.bed -o GRCh38/TC.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s TG.unified.sorted.txt.gz -c new_coords/TG.unified.new_coords.bed -o GRCh38/TG.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_Case_control.sorted.txt.gz -c new_coords/Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_Case_control.new_coords.bed -o GRCh38/Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_Case_control.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_meta.sorted.txt.gz -c new_coords/Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_meta.new_coords.bed -o GRCh38/Type_1_diabetes_Onengut-Gumuscu_2015_NatGen_Immunochip_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Type_2_diabetes_Morris_2012_NatGen_Metabochip_meta.sorted.txt.gz -c new_coords/Type_2_diabetes_Morris_2012_NatGen_Metabochip_meta.new_coords.bed -o GRCh38/Type_2_diabetes_Morris_2012_NatGen_Metabochip_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Type_2_diabetes_Morris_2012_NatGen_meta.sorted.txt.gz -c new_coords/Type_2_diabetes_Morris_2012_NatGen_meta.new_coords.bed -o GRCh38/Type_2_diabetes_Morris_2012_NatGen_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s ukbb.1000g.exome.hard.meta.filter.unified.sorted.txt.gz -c new_coords/ukbb.1000g.exome.hard.meta.filter.unified.new_coords.bed -o GRCh38/ukbb.1000g.exome.hard.meta.filter.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Ulcerative_cholitis_Jostins_2012_Nature_GWAS.sorted.txt.gz -c new_coords/Ulcerative_cholitis_Jostins_2012_Nature_GWAS.new_coords.bed -o GRCh38/Ulcerative_cholitis_Jostins_2012_Nature_GWAS.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s Ulcerative_cholitis_Julia_2014_HumMolGenet_GWAS_meta.sorted.txt.gz -c new_coords/Ulcerative_cholitis_Julia_2014_HumMolGenet_GWAS_meta.new_coords.bed -o GRCh38/Ulcerative_cholitis_Julia_2014_HumMolGenet_GWAS_meta.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s UricAcid.unified.sorted.txt.gz -c new_coords/UricAcid.unified.new_coords.bed -o GRCh38/UricAcid.unified.sorted.GRCh38.txt.gz
Rscript liftover_scripts/replace_coordinates_bed.R -s WBC.unified.sorted.txt.gz -c new_coords/WBC.unified.new_coords.bed -o GRCh38/WBC.unified.sorted.GRCh38.txt.gz

