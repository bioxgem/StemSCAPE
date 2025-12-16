# StemSCAPE
We developed StemSCAPE, a visible machine learning framework that integrates transcriptomic and CRISPR datasets to map stemness–associated genes, pathways, and samples with mechanistic interpretability. StemSCAPE delineates conserved and context-specific stemness programs across malignancies, resolves gene–pathway–sample relationships, and links stemness activity to immune and metabolic axes associated with patient outcomes. This landscape reveals core regulatory modules shared across cancers and subtype-specific vulnerabilities.

![](Figure1.png)
**Development and validation of StemSCAPE framework.**


This repository hosts the source code used for the data processing within our study, alongside all relevant raw data/files. For comprehensive details regarding the methodology, please refer to
> Visible Machine Learning Maps Cancer Stemness Landscape
>
> Jung-Yu Lee, Chih-Yuan Chou, Yen-Lin Chen, Yao-Feng Li, Yun-Ti Chen, Chun-Yu Lin, Chia-Hwa Lee, Jinn-Moon Yang

## Description
![](StemSCAPE.png)
**Overview of StemSCAPE framework.**

To characterize pan-cancer stemness, we developed the **StemSCAPE** model. This white-box machine learning framework is designed to **identify stemness-associated samples** and **map their underlying genes and pathways**.

The model comprises two major, distinct steps:

### Step 1: StemSCAPE-Gene Index (GI) Calculation by Anchor Gene Community-Regulated Stemness-Related Pathways (AnGReP)

* **Process:** We analyzed the transcriptomic data of 8,215 tumor and 726 normal samples across 24 cancer types from The Cancer Genome Atlas Program (TCGA) to calculate the AnGReP. Subsequently, we computed a **StemSCAPE-GI** for each gene.
* **Resources:** The **AnGReP score** (mapping genes to each pathway), the final **StemSCAPE-GI**, and the **stemness-related gene labels** are provided within the `StemSCAPE-GI` folder.

### Step 2: StemSCAPE-Sample Index (SI) Calculation

* **Process:** A refined set of 1,463 stemness-related genes (selected based on high StemSCAPE-GI values) was used to calculate the **StemSCAPE-SI** for each individual sample.
* **Resources:** This step includes the **`StemSCAPE-SI.py` Python program**, required **input files**, and the corresponding **output files**, all located in the `StemSCAPE-SI` folder.

## Data sources

The cancer stemness-associated genes ([n=87 literature-reported](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/87_literature-reported_CSC_genes.txt)) were curated from the following four references:

- [30 cancer-stemness genes](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/30_CSC_genes_from_2020_Signal_Transduct_Tar.txt) were downloaded from [Yang et al., _Signal Transduct Tar_, 2020](https://doi.org/10.1038/s41392-020-0110-5)
- [42 cancer-stemness genes](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/42_CSC_genes_from_2020_Front_Immunol.txt) were downloaded from [Walcher et al., _Front Immunol_, 2020](https://doi.org/10.3389/fimmu.2020.01280)
- [43 cancer-stemness genes](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/43_CSC_genes_from_2019_Radiation_Oncology.txt) were downloaded from [Nagle et al., _Radiation Oncology_, 2019](https://doi.org/10.1007/978-3-319-52619-5_104-1)
- [42 cancer-stemness genes](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/42_CSC_genes_from_2017_Cancer_Transl_Med.txt) were downloaded from [Zhao et al, _Cancer Transl Med_, 2017](https://doi.org/10.4103/ctm.ctm_69_16)

The testing datasets were curated from the following two references:

- [100 cancer-stemness genes and 131 normal-stemness genes](http://www.bio-bigdata.center/CellMarkerSearch.jsp?quickSearchInfo=stem%20cell&index_key=2#framekuang) were downloaded from CellMarker 2.0 by [Hu et al., _Nucleic Acids Res_, 2023](https://doi.org/10.1093/nar/gkac947)
- [69 high confidience cancer-stemness genes (confidience score > 0.5)](https://bicresources.jcbose.ac.in/ssaha4/bcscdb/downloads/CSC_Biomarker_2022_All.csv) were downloaded from BCSCdb by [Firdous et al., _Database-Oxford_, 2022](https://doi.org/10.1093/database/baac082)


The external evaluation sets were compiled from publicly available resources, specifically providing the following components:

* [26 stemness gene sets](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/26_stemness_gene_sets.txt) (see [Supplementary Table 1](https://github.com/bioxgem/StemSCAPE/blob/main/StemSCAPE-GI/Supplementary_Table_1.txt))
* [10 cancer hallmark gene sets](https://figshare.com/ndownloader/files/7881838)

## Installation and setup
### Project dependencies
This project uses `Python` version 3.10.14.

The following `Python` packages are used in this repository:
- `numpy` (v1.26.4)
- `pandas` (v2.2.1)
- `scikit-learn` (v1.3.0)
- `shap` (v0.45.1)


### Project initialization
```bash
git clone https://github.com/bioxgem/StemSCAPE.git

cd StemSCAPE
```
## Usage instructions
```bash
python StemSCAPE-SI.py \
    -i ./StemSCAPE-SI_Input/TCGA_and_GSE30652_1344genes_for_training.txt \
    -e ./StemSCAPE-SI_Input/TCGA_others-1_1344genes_for_testing.txt \   
    -l Label \   
    -s Sample \ 
    -o ./StemSCAPE-SI_Output/TCGA_SHAP    
```

## Contact Information

All technical questions pertaining to the StemSCAPE datasets and associated scripts should be directed to [BioXGEM](https://bioxgem.life.nctu.edu.tw/bioxgem/).

We appreciate your interest in our published work.
