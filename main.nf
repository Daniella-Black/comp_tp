#! /usr/bin/env nextflow
//define channels from input file
Channel 
    .fromPath(params.inputlist)
    .ifEmpty {exit 1, "Cannot find input file : ${params.inputlist}"}
    .splitCsv(skip:1)
    .map{tumour_sample_platekey, v1_tumour_sv_vcf, v2_somatic_cnv_vcf, cancer_analysis_table -> [tumour_sample_platekey, file(v1_tumour_sv_vcf), file(v2_somatic_cnv_vcf),file(cancer_analysis_table)]}
    .set{ ch_input }


//run the script to make MTR input on above file paths
process  CloudOS_MTR_input{
    maxForks 900
    errorStrategy 'ignore'
    maxRetries 3
    container = 'public.ecr.aws/b0q1v7i3/pydocker:latest' 
    tag"$tumour_sample_platekey"
    publishDir "${params.outdir}/$tumour_sample_platekey", mode: 'copy'
    
    input:
    set val(tumour_sample_platekey), file(v1_tumour_sv_vcf), file(v2_somatic_cnv_vcf), file(cancer_analysis_table) from ch_input

    output:
    file "*_tp_comp.csv"
    
    script:
    """
    tp_comp.py -tumour_sample_platekey '$tumour_sample_platekey' -v1_tumour_sv_vcf '$v1_tumour_sv_vcf' -v2_somatic_cnv_vcf '$v2_somatic_cnv_vcf' -cancer_analysis_table '$cancer_analysis_table'
    """ 
}
