##Intitial Comparison
1. The intitial comparison for all fastq files is done with **NoRef_Southern_runner_cp_FILTER.sh**
2. Files are now standardized with **TaxTime.sh**
  TaxTime.sh is quick and dirty bash program to ensure that all taxa have the same number of taxonomic designation fields.
  This is important for the next parsing script which will count on all fields having a standard number. 
3. **Fold_Table_Maker.py** takes table of depths, SRA order and Gene order and outputs a csv.  
   e.g. Fold_Table_Maker.py Phoenix.table ../SRA_Order_4FoldTable.txt Genes.txt Phoenix 
4.
