## Pipeline for Heatmap
1. The intitial comparison for all fastq files is done with **NoRef_Southern_runner_cp_FILTER.sh**
2. Files are now standardized with **TaxTime.sh**
  TaxTime.sh is quick and dirty bash program to ensure that all taxa have the same number of taxonomic designation fields.
  This is important for the next parsing script which will count on all fields having a standard number. 
3. **Fold_Table_Maker.py** takes table of depths, SRA order and Gene order and outputs a csv.  
   *e.g.* `Fold_Table_Maker.py Phoenix.table SRA_Order_4FoldTable.txt Genes.txt Phoenix` SRA order and Gene orders are lists of one per entry per line.   
4.  **HomeBrew_Heat_Map.py**  takes filtered csv of relative depths, a config file and an output name ending in svg.
     *e.g.*`HomeBrew_Heat_Map.py Poaceae15Feb2017_HeatMapv6.csv Heatmap_Color.config Poaceae15Feb2017_HeatMapv6.svg`
