#!/usr/local/bin/python3
import pandas as pd
import re
import gzip
import argparse

my_parser = argparse.ArgumentParser(description='get arguments')
my_parser.add_argument('-tumour_sample_platekey',
                       type=str,
                       help='sample')
my_parser.add_argument('-v1_tumour_sv_vcf',
                       type=str,
                       help='v1_tumour_sv_vcf')
my_parser.add_argument('-v2_somatic_cnv_vcf',
                       type=str,
                       help='v2_somatic_cnv_vcf')
my_parser.add_argument('-v2_somatic_sv_vcf',
                       type=str,
                       help='v2_somatic_sv_vcf')
my_parser.add_argument('-cancer_analysis_table',
                       type=str,
                       help='cancer_analysis_table')
args = my_parser.parse_args()

sample = args.tumour_sample_platekey
v1_tumour_sv_vcf = args.v1_tumour_sv_vcf
v2_somatic_cnv_vcf = args.v2_somatic_cnv_vcf
v2_somatic_sv_vcf = args.v2_somatic_sv_vcf
cancer_analysis_table = args.cancer_analysis_table


##read in the vcf files and pull out tp
tp = {}

file_list = [v1_tumour_sv_vcf, v2_somatic_cnv_vcf,v2_somatic_sv_vcf]
file_list_names = ['v1_tumour_sv_vcf', 'v2_somatic_cnv_vcf', 'v2_somatic_sv_vcf']

for file in range(len(file_list)):
  f = gzip.open(file_list[file])
  lines= f.readlines()
  f.close()
  lines = [i.decode('utf-8') for i in lines]
  matching = [s for s in lines if any(xs in s for xs in ['TumourPurity'])]
  if len(matching) >0:
    tp[file_list_names[file]] = float(re.findall("\d+\.\d+", matching[0])[0])
  else:
    tp[file_list_names[file]] = 'tp_not_found'

df = pd.DataFrame.from_dict(tp, orient='index',columns=[sample])
df = df.T
df.to_csv(sample+ '_tp_comp.csv', index=False)

