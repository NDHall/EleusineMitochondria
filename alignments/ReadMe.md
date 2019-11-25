This folder contains alignments used for the analysis in the GBE paper. 


1. `alns_and_key.tar.gz`
  contains inframe exon level alignments in phyllip format aling with SRA to species name key. The key uses '###' as a delimiter, so that
  it can easily be used in ad hoc for do done loops that are common to BASH. This file contains all exon level alignments that passed QC     and as such there is variability in the set of operational taxonomic units present in each. 
  
  ```
atp1.phy      cox1.phy                   nad2_et1.phy  nad5_e3.phy   nad9.phy          rps2.phy
atp4.phy      cox2_e1.phy                nad2_et2.phy  nad5_et1.phy  Pseudo_rpl10.phy  rps3_e1.phy
atp6.phy      cox2_e2.phy                nad2_et3.phy  nad5_et2.phy  rpl16.phy         rps3_e2.phy
atp8.phy      cox3_441570_442367_ZM.phy  nad2_et4.phy  nad5_et4.phy  rpl2.phy          rps4.phy
atp9.phy      matR.phy                   nad2_et5.phy  nad5_et5.phy  rpl5.phy          rps7.phy
ccmB.phy      mttB.phy                   nad3.phy      nad6.phy      rps11.phy         strict_tax_key.list
ccmC.phy      nad1_et1.phy               nad4_e1.phy   nad7_e1.phy   rps12.phy
ccmFC_e1.phy  nad1_et2.phy               nad4_e2.phy   nad7_e2.phy   rps13.phy
ccmFC_e2.phy  nad1_et3.phy               nad4_e3.phy   nad7_e3.phy   rps14.phy
ccmFN.phy     nad1_et4.phy               nad4_e4.phy   nad7_e4.phy   rps19.phy
cob.phy       nad1_et5.phy               nad4L.phy     nad7_e5.phy   rps1.phy
  ```


2. `atp_paml.tar.gz` contains phylip and newick tree used in codeml analysis, see GBE paper for details. 

```
atp1.phy  atp1.tre  atp4.phy  atp4.tre  
atp6.phy  atp6.tre  atp8.phy  atp8.tre  
atp9.phy  atp9.tre
```

3.`raxml.tar.gz` contains the output from FASconCAT, PartitionFinder V2.0, and RAxML, run with both exon level partitions and no paritions. The tree topology for both trees remains inaccurate, though it does cluster species together rather well.

```
FcC_info.xls                 FcC_supermatrix_partition.txt
FcC_supermatrix.cfg          figtree_RAxML_bipartitionsBranchLabels.full_matrix_v2_no_partition
FcC_supermatrix.fasta        figtree_RAxML_bipartitionsBranchLabels.full_matrix_v2_partition
FcC_supermatrix.phy          rax_partition.txt
FcC_supermatrix.phy.reduced
```



