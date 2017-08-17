## Mito_Compare.sh

Mito_Compare.sh is bash script that extracts annontated regions from a genbank file, 
creates a blast database with the extracted sequences
and uses the blastn and the database to annontate a set of contigs. This works pretty well for plant mitochondria where the 
the conserved sequence similiarity is high. 

At present the color dictionary and blast_to_svg_Customv2.py are hard coded for gene names and fonts are optimized for smaller contigs. It does not scale well to full genomes because it is designed for on the fly visualization of contigs during assembly.

Usage:
```
      Mito_Compare.sh <genbank_ref> <fasta_to_annontate>
```

